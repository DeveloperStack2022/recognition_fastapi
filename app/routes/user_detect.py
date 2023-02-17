""" Modulos """
from io import BytesIO
from fastapi import APIRouter,UploadFile,File
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw
import face_recognition
import  xml.etree.ElementTree as xml 
from ..utils import build_response
from starlette.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
import uuid
from fastapi.responses import (JSONResponse,FileResponse)
from ..services import UserPersistenciaService
import base64
from PIL import Image
from io import BytesIO

router = APIRouter()


@router.post('/compareImage')
async def compareImage(image_original:UploadFile = File(...),image_compare:UploadFile = File(...)):
    imagenes:list = [] 
    
    imagenes.append(image_original)
    imagenes.append(image_compare)

    if not os.path.exists(os.getcwd() + "/Compare"):
        os.makedirs("Compare")
    
    path_dir = os.getcwd() + "/Compare"
    
    try:
        for img in imagenes:
            _,file_extension = os.path.splitext(img.filename)
            img.filename = str(uuid.uuid1()) +  file_extension
            with open(os.path.join(path_dir, img.filename), 'wb') as file:
                content = await img.read()
                file.write(content)
                file.close()

        imgReads: list = []
        path_dir = os.path.join(os.getcwd(),"Compare")
        size = 1920,1080

        for files in os.listdir(path_dir):
            # print(path_dir + "/" + files)
            image = Image.open(path_dir + "/" + files,mode="r")
            # print(f'Image sizes: {image.size}')
            # image.thumbnail(size)
            image_resize = image.resize((1920,1080),Image.NEAREST)
            image_resize.save(path_dir + "/" + files,quality=100)
            # image.save()
            # print(files)


            image_read = cv2.imread(str(path_dir) + "/" + str(files))
            imgReads.append(image_read)
            # print('\n Img Read',image_read)

        if imgReads[0].shape == imgReads[1].shape:
            print("Las imagenes son del mismo tamanio")  
            diferencias = cv2.subtract(imgReads[0],imgReads[1])
            b,g,r = cv2.split(diferencias)
            # print(cv2.countNonZero(b))
            if (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0):
                print("las imagenes son completamente iguales")
            else:
                print("las imagenes no son iguales")
        
        # Verificamos la similtud 
        shift = cv2.xfeatures2d.SIFT_create()
        kp_1,desc_1 = shift.detectAndCompute(imgReads[0],None)
        kp_2,desc_2 = shift.detectAndCompute(imgReads[1], None)

        print("Keypoints 1st image", str(len(kp_1)))
        print("Keypoints 2st image", str(len(kp_2)))

        index_params = dict(algorithm=0,trees=5)
        search_params = dict()

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(desc_1, desc_2, k=2)
        
        buenos_puntos = []

        for m,n in matches:
            if m.distance < 0.6*n.distance:
                buenos_puntos.append(m)
        number_keypoints = 0
        if (len(kp_1) <= len(kp_2)):
            number_keypoints = len(kp_1)
        else:
            number_keypoints = len(kp_2)
        
        print("GOOD matches",len(buenos_puntos))
        print("Que tan bueno es el match", len(buenos_puntos) / number_keypoints * 100, "%")
        result = cv2.drawMatches(imgReads[0], kp_1, imgReads[1], kp_2, buenos_puntos, None)
        if not os.path.exists(os.getcwd() + "/Matching"):
            os.makedirs("Matching")
        path_dir = os.getcwd() + "/Matching"
        cv2.imwrite(os.path.join(path_dir,"img_compare.jpg"), result)

        string = str('http://localhost:8000/api/v0.1/userdetect/imageDetect/img_compare.jpg')
        detect:dict = {
            'url':string,
            'match':len(buenos_puntos) / number_keypoints * 100,
            'keypoints_1':str(len(kp_1)),
            'keypoints_2':str(len(kp_2)),
            'good_pointsKeys':len(buenos_puntos)
        }
        return await build_response(HTTP_200_OK,detect=detect)
        
    except FileNotFoundError:
        return await build_response(HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/compareImageTwo')
async def compareImageTwo(image_original:UploadFile = File(...),image_compare:UploadFile = File(...)):
    imagenes:list = [] 
    
    imagenes.append(image_original)
    imagenes.append(image_compare)

    if not os.path.exists(os.getcwd() + "/Compare"):
        os.makedirs("Compare")
    
@router.get('/imageDetect/{name_file}')
async def ImageDetect(name_file:str):
    path = os.getcwd() + "/Matching/" + name_file
    return FileResponse(path)

@router.delete('/deleteImages')
async def ImageDetect():
    path = os.path.join(os.getcwd(),"Matching")
    for files in os.listdir(path):
        if os.path.isfile(os.path.join(path,files)):
            os.remove(os.path.join(path,files))

    path_two = os.path.join(os.getcwd(),"Compare")
    for files  in os.listdir(path_two):
        if os.path.isfile(os.path.join(path_two,files)):
            os.remove(os.path.join(path_two,files))

    return await build_response(HTTP_200_OK,msg="Delete Success")


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


def generate(path:str):
    cap = cv2.VideoCapture(path)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    
    while True:
        success,frame =   cap.read()

        if not success:
            break
        
        rgb_frame = frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame,face_locations)

        for (top,right,bottom,left),face_encodings in zip(face_locations,face_encodings):
            matches = face_recognition.compare_faces(know_face_encodings,face_encodings)
            name = "know"
            face_distances = face_recognition.face_distance(know_face_encodings,face_encodings)

            bets_match_index = np.argmin(face_distances)

            if matches[bets_match_index]:
                name = know_faces_name[bets_match_index]
            
            cv2.rectangle(frame,(left,top), (right,bottom),(0,255,0),2)
            cv2.rectangle(frame, (left, bottom - 35), (right,bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        flag,encodedImage = cv2.imencode("")

@router.post('/faceRecognetion')
async def faceRecognetion(image_original:UploadFile = File(...)):
    imagenes:list = [] 
    imagenes.append(image_original)

    if not os.path.exists(os.getcwd() + "/Compare"):
        os.makedirs("Compare")
    
    path_dir = os.getcwd() + "/Compare"

    try:
        for img in imagenes:
            
            _,file_extension = os.path.splitext(img.filename)
            img.filename = str(uuid.uuid1()) +  file_extension
            with open(os.path.join(path_dir, img.filename), 'wb') as file:
                content = await img.read()
                file.write(content)
                file.close()

        imgReads: list = []
        path_dir = os.path.join(os.getcwd(),"Compare")

    except FileNotFoundError:
        return await build_response(HTTP_500_INTERNAL_SERVER_ERROR)    


@router.post('/compareImageFaceRecognition')
async def compareImageFaceRecognition(image_original:UploadFile = File(...),image_compare:UploadFile = File(...)):
    # myimages  = MyImages()
    """
        Crate file XML -> bd_images.xml
    """
    # __________________________
    path_dir = os.getcwd()
    dir_file = os.path.join(path_dir,"BdXml/bd_images.xml")

    if not os.path.exists(dir_file):
        os.makedirs(dir_file)
    # __________________________

    
    try:
        

        imgs:list = []
        imgs.append(image_original)
        imgs.append(image_compare)
        if not  os.path.exists(os.path.join(os.getcwd(),"Compare")):
            os.makedirs("Compare")
        path_dir = os.path.join(os.getcwd(),"Compare")

        # for img in imgs:
        #     with open(os.path.join(path_dir, img.filename),mode='rb') as file:
        #         string_image = base64.encode(file.read())

        #     print(string_image)

        # for img in imgs:
        #     im = MyImages.image()
        #     im.src = img
        #     myimages.append(im)

        # with open(str(dir_file),'w') as file:
        #     file.write(myimages.toxml("utf-8")) 

        for img in imgs:
            _,file_extension = os.path.splitext(img.filename)
            img.filename = str(uuid.uuid1()) +  file_extension
            with open(os.path.join(path_dir, img.filename), mode="wb") as file:
                content = await img.read()
                file.write(content)
                file.close()
        
        load_img = []
        know_encodings = []

        dir = os.path.join(os.getcwd(),"Compare")
        for files in os.listdir(dir):
            img = os.path.join(os.getcwd(),"Compare")
            l_img = face_recognition.load_image_file(str(img + "/" + files))
            # print(l_img)
            l_encod = face_recognition.face_encodings(l_img)[0]
            know_encodings.append(l_encod)
            load_img.append(l_img)
        

        # root = xml.Element('Element')
        # image_element = xml.Element('Image')
        # root.append(image_element)
        # root_images = xml.SubElement(image_element,'image')
        # root_images.text()
        # documento = xml.ElementTree(root)

        # with open('output.xml', 'wb') as doc:
        #     documento.write(doc)

        # global elementos 
        # for files in os.listdir(dir):
        #     with open(os.path.join(path_dir, files) , mode="rb") as file: 
        #         # base_string = pybase64.b64encode(file.read())
        #         root = xml.Element("User")
        #         image_element = xml.Element("image")
        #         image_element.text("text")
        #         root.append(image_element)
        #         close_element = xml.ElementTree(root)
        #         elementos = close_element
        
        # with open("output.xml",'wb') as  file_xml:
        #     elementos.write(file_xml)
            
        # Comparacion de distances


        f_distance = face_recognition.face_distance([know_encodings[0]],know_encodings[1])
        f_match_percentage  = (1-f_distance)*100

        f_match = face_recognition.compare_faces([know_encodings[0]],know_encodings[1])
        
        face_landmarks_list = face_recognition.face_landmarks(load_img[0])

        pil_image = Image.fromarray(load_img[0])
        d = ImageDraw.Draw(pil_image)

        
        for lendmarks in face_landmarks_list:
            for facial_feature in lendmarks.keys():
                d.point(lendmarks[facial_feature],fill='white')

        url = str(uuid.uuid1())        
        pil_image.save(os.getcwd() + "/Matching/" + url +".jpg")

        string = str('http://localhost:8000/api/v0.1/userdetect/imageDetect/'+ url + '.jpg')
        detect:dict = {
            'url':string,
            'match':np.round(f_match_percentage,2)[0],
            'keypoints_1':1,
            'keypoints_2':1,
            'good_pointsKeys':1,
            'compare':"Si" if f_match[0] else "No"
        }
        return await build_response(HTTP_200_OK,detect=detect)
    except FileNotFoundError:
        return await build_response(HTTP_500_INTERNAL_SERVER_ERROR)


# @router.post('/compareImageFaceRecognitionTwo')
# async def compareImageFaceRecognitionTwo(image_compare:UploadFile = File(...)):
#     service = UserPersistenciaService()
#     data = service.all_get_images_gridfs()
#     direct = os.path.join(os.getcwd(),'Compare')
#     im = Image.open(image_compare.file)
#     # if im.mode in ("RGBA","p")
#     im.save(str(direct +"/"+ image_compare.filename),quality=50)

#     load_image = face_recognition.load_image_file(str(direct+"/"+image_compare.filename))
#     encoding_image = face_recognition.face_encodings(load_image)[0]

#     load_image_file = []
#     face_encoding_image = []
#     list_users = [] 
    
#     for file_ in data:
#         img_IO = BytesIO(base64.standard_b64decode(file_['image_base64']))
#         img_pil = Image.open(img_IO)
#         img_pil = img_pil.convert('RGB')
#         load_image = np.array(img_pil)
#         # Si en caso de que se use np.array() -> 
#         face_encoding = face_recognition.face_encodings(load_image)[0]
#         load_image_file.append(load_image)
#         face_encoding_image.append(face_encoding)
#         list_users.append(file_['file_name'])
    
#     match = face_recognition.compare_faces(face_encoding_image,encoding_image,tolerance=0.5)
#     user = ''
#     f_distance = face_recognition.face_distance(face_encoding_image,encoding_image)
#     f_match_percentage  = (1-f_distance)*100
#     val = np.round(f_match_percentage,2)
#     for index,match_ in enumerate(match): 
#         if match_: 
#             user = list_users[index]
    
#     service_data = service.get_user_by_numero_cedula(numero_cedula=user,valor_porcentaje=val.max())
#     return service_data

@router.post('/compareImageFaceRecognitionTwo')
async def compareImageFaceRecognitionTwo(image_compare:UploadFile = File(...)):
    pass


@router.get('/ConvertImageToArray')
async def convertToImageToNpArray():
    service = UserPersistenciaService()
    data = service.all_get_images_gridfs()
   
    for file_ in data:
        img_IO = BytesIO(base64.standard_b64decode(file_['image_base64']))
        img_pil = Image.open(img_IO)
        img_pil = img_pil.convert('RGB')
        # print(img_pil)
        load_image = np.array(img_pil)
        string_np_ = np.array2string(load_image)

        # print(string_np_)
        # Save Image to mongodb np.array()
        service.save_image(numero_cedula=file_['file_name'],image_array_list=string_np_)
    return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success':True,
                'payload':{ }
            }
        )

#python3 -m uvicorn app.main:app  --reload
