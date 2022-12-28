import os
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK
from .db import open_db_connection, close_db_connection
from .configs import PATH_FILENAME
import cv2
import pathlib
import numpy as np
import face_recognition


async def build_response(status_code=HTTP_200_OK, **kwargs):
    payload = kwargs.get('data', None)
    detail = kwargs.get('msg', None)
    detect = kwargs.get('detect',None)

    if bool(payload):
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'payload': payload
            }
        )
    elif bool(detail):
       return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'detail': detail
            }
        )
    elif bool(detect):
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'detect': detect
            }
        )

def startup_handler():
    open_db_connection()

def shutdown_handler():
    close_db_connection()

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg','png'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createDir(nameDir:str) -> str:
    path = os.getcwd()
    FOLDER = os.path(path,str(nameDir))
    print(FOLDER)
    if not os.path.isdir(FOLDER):
        os.makedirs(str(nameDir))
    return FOLDER

def verify_cedula(num:str) -> bool:
    indice = 0
    validation = True
    resultado:list = []
    ultimoValor = num[9]
    total = 0
    while indice < len(num) - 1:
        numero:int = int(num[indice])
        # print(f'{numero} \n')
        if validation:
            res = numero * 2
            if res > 9:
                res = res - 9 
            resultado.append(res)
            validation = False
        else:
            res = numero * 1
            resultado.append(res)
            validation = True
        indice += 1
    
    for numero in resultado:
        total = total + numero

    valorString = str(total)[0]
    decena = ( int(valorString) + 1 ) * 10 
    digito_validador = decena - total

    if digito_validador == int(ultimoValor):
        return True
    else:
        return False

def validarSiExisteUnArchivo(nombre_archivo:str) -> str:

    dir_folder = os.path.join(os.getcwd(),"app/files")
    path_dir = os.path.join(os.getcwd(),f"app/files/{nombre_archivo}")

    if not os.path.exists(path_dir):
        os.makedirs(dir_folder)
        with open(path_dir,'w')  as file:
            pass   
        return { "path_dir":str(path_dir),"existe":'no'} 
    return {
        "path_dir":str(path_dir),
        "existe":'si'
    }

def validarSiExisteUnaCarpeta(nombre_carpeta:str) -> str:
    root_path = os.getcwd()
    dir_path = os.path.join(root_path,f"{nombre_carpeta}")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return "The folder has been created"
    return "The folder already existed"



know_face_encodings = []
know_faces_name = []

def face_r():
    path = os.getcwd()
    pathAbsolute = os.path.join(path,"Uploads")
    # print(pathAbsolute)
    for file_name in os.listdir(pathAbsolute):
        # image = cv2.imread(pathAbsolute+"/"+file_name)
        # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = face_recognition.load_image_file(pathAbsolute+"/"+file_name)
        f_encoding = face_recognition.face_encodings(image)[0]

        know_face_encodings.append(f_encoding)
        know_faces_name.append(file_name.split('.')[0])


def gen_frames():
    face_detector  = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
    clasificacion_face = cv2.CascadeClassifier(str(face_detector))
    camera = cv2.VideoCapture(0)
    face_r()
    while True:
        success, frame = camera.read()
        rgb_frame = frame[:, :, ::-1]
        if not success: # false => true | true => false
            break
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

       
        flag, encodedImage = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
