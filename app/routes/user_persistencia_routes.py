import os 
from fastapi import APIRouter,File,UploadFile,Form
from fastapi.responses  import StreamingResponse
from ..models import (UserPersistencia)
from ..services import UserPersistenciaService
from fastapi.responses import (JSONResponse,FileResponse)
from ..utils import (gen_frames)
from werkzeug.utils import secure_filename
import cv2
import numpy as np 
import face_recognition

router = APIRouter()


@router.post('/addImage')
async def addUserPersistencia(num_cedula:str = Form(...),nombres: str = Form(...),apellidos:str = Form(...),image: UploadFile = File(...)):
    services = UserPersistenciaService()
   
    if not os.path.exists(os.getcwd() + "/Uploads"):
        os.mkdir("Uploads")
    path_dir = os.getcwd() + "/Uploads"
    _,file_extension = os.path.splitext(image.filename)
    image.filename = str(num_cedula) + file_extension
    
    with open(os.path.join(path_dir,image.filename),'wb') as myfile:
        content = await image.read() 
        myfile.write(content)
        myfile.close()
        
    images:list[str] = []
    images.append(str('http://localhost:8000/api/v0.1/userpersistencia/image/' + image.filename))
    user:UserPersistencia = UserPersistencia(numero_cedula=num_cedula,nombres=nombres,apellidos=apellidos,images_id=images)
    return await services.create_new_user_persistencia(user)

@router.get('/get_users')
async def getUsersPersistencia():
    services = UserPersistenciaService()
    return await services.get_users_persistencia()

@router.get("/getImages")
async def getOneUserByNumCedula(numero_cedula:str):
    services = UserPersistenciaService()
    return await services.get_images_users(numero_cedula)

@router.delete('/delete_user')
async def deleteUserPersistencia(numero_cedula:str):
    services = UserPersistenciaService()
    return await services.delete_user_persistencia(numero_cedula)

@router.get('/image/{name_file}')
async def file(name_file:str):
    path = os.getcwd() + "/uploads/" + name_file
    return FileResponse(path)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades +
     "haarcascade_frontalface_default.xml")

know_faces_name = []
know_face_encodings = []

def face_r():
    path = os.getcwd()
    pathAbsolute = os.path.join(path,"Uploads")
    # print(pathAbsolute)
    for file_name in os.listdir(pathAbsolute):
        # image = cv2.imread(pathAbsolute+"/"+file_name)
        # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(pathAbsolute+"/"+file_name)
        image = face_recognition.load_image_file(pathAbsolute+"/"+file_name)
        f_encoding = face_recognition.face_encodings(image)[0]

        know_face_encodings.append(f_encoding)
        know_faces_name.append(file_name.split('.')[0])

def generate():
    while True:
        success, frame = cap.read()
        if not success:
            break

        if success:
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame,face_locations)
            
            for (top,right,bottom,left), face_encodings in zip(face_locations,face_encodings):
                matches = face_recognition.compare_faces(know_face_encodings,face_encodings)
                name = "know"
                face_distances = face_recognition.face_distance(know_face_encodings,face_encodings)
                bets_match_index = np.argmin(face_distances)

                if matches[bets_match_index]:
                    name = know_faces_name[bets_match_index]
                
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')

@router.get('/detectFaceRecognetion')
async def detectFaceRecognetion():
    face_r()
    return StreamingResponse(generate(),media_type="multipart/x-mixed-replace;boundary=frame")