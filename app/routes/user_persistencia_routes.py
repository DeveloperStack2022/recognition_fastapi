import base64
import os 
from fastapi import APIRouter,File,UploadFile,Form
from fastapi.responses  import StreamingResponse
from ..models import (UserPersistencia)
from ..services import UserPersistenciaService
from fastapi.responses import (JSONResponse,FileResponse)
from ..utils import (build_response, gen_frames)
from werkzeug.utils import secure_filename
import cv2
import numpy as np 
import face_recognition
from ..utils import (verify_cedula,validarSiExisteUnArchivo,validarSiExisteUnaCarpeta)
from starlette.status import (HTTP_400_BAD_REQUEST)
from xml.etree.ElementTree import Element,SubElement,tostring
import xml.etree.ElementTree as ET

router = APIRouter()



@router.post('/addImage')
async def addUserPersistencia(num_cedula:str = Form(...),nombres: str = Form(...),apellidos:str = Form(...),image: UploadFile = File(...)):
    
    respuesta = verify_cedula(num_cedula)
    if not respuesta:
        return await build_response(HTTP_400_BAD_REQUEST,msg="Numero de cedula no es correcto")
    services = UserPersistenciaService()
    
    # print(image.file.read())
    # file_dir = validarSiExisteUnArchivo('data_image.xml') # Verificacamos si el archivo "data_image.xml" existe / si no existe lo crea la funcion y retorna la ruta
    # validarSiExisteUnaCarpeta("Uploads") # Verificacamos si la carpeta "Uploads" existe / si no existe lo crea la funcion.
    # print(file_dir['path_dir'])
    
    # if file_dir['existe'] == 'si':
    #     tree = ET.parse(file_dir['path_dir'])
    #     root = tree.getroot()
    #     data_element = Element('Data')
    #     numero_cedula = SubElement(data_element,"numero_cedula")
    #     nombres_element = SubElement(data_element,'nombres')
    #     apellidos_element = SubElement(data_element,'apellidos')
    #     image_element = SubElement(data_element,"image")
    #     numero_cedula.text = f'{num_cedula}'    
    #     nombres_element.text = f'{nombres}'    
    #     apellidos_element.text = f'{apellidos}' 
    #     image_encode = base64.standard_b64encode(image.file.read())
    #     image_element.text = f'{image_encode}'
    #     root.append(data_element)
    #     tree.write(file_dir['path_dir'])
    # else:
    #     top_element = Element('Element')
    #     data_element = SubElement(top_element,'Data')
    #     num_element = SubElement(data_element,'numero_cedula')
    #     nombres_element = SubElement(data_element,'nombres')
    #     apellidos_element = SubElement(data_element,'apellidos')
    #     image_element = SubElement(data_element,"image")

    #     num_element.text = f'{num_cedula}'    
    #     nombres_element.text = f'{nombres}'    
    #     apellidos_element.text = f'{apellidos}'    

    #     image_encode = base64.standard_b64encode(image.file.read())
    #     image_element.text = f'{image_encode}'

    #     xml_file = open(file_dir['path_dir'],'w')
    #     xml_file.write(tostring(top_element).decode('utf-8'))
    #     xml_file.close()


    # root_dir = os.getcwd()
    # path_dir = root_dir + "/Uploads"
    # _,file_extension = os.path.splitext(image.filename)
    # image.filename = str(num_cedula) + file_extension
    
    # with open(os.path.join(path_dir,image.filename),'wb') as myfile:
    #     content = await image.read() 
    #     myfile.write(content)
    #     myfile.close()
    
    # images:list[str] = []
    # print(image.file.read())
    # images.append(str('http://localhost:8000/api/v0.1/userpersistencia/image/' + image.filename))
    user:UserPersistencia = UserPersistencia(numero_cedula=num_cedula,nombres=nombres,apellidos=apellidos,images_id=[''])
    return await services.create_user_image_file(user,image)

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


@router.get("/get_user_image")
async def get_image_user_gridfs(numero_cedula:str):
    services = UserPersistenciaService()
    # for ser in response_bd:
    #     # print(ser)
    # return {"ok":"success"}
    # response_bd = await services.get_image_user_gridfs(numero_cedula)
    return await services.get_image_user_gridfs(numero_cedula)
