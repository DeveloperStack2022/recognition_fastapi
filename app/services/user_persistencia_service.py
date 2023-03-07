import face_recognition
import os
from PIL import Image
from fastapi.encoders import jsonable_encoder
from http.client import HTTPException
from ..utils import build_response
from ..db import (MongoDB,get_client)
from ..models.user_persistencia import (UserPersistencia,OutUserPersistencia,UpdateUserPersistencia,OutUserImageGridfs,OutUserImageBase64)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from starlette.responses import JSONResponse
from fastapi import File,UploadFile
import numpy as np


class UserPersistenciaService:
    def __init__(self):
        super().__init__()
        self._db = MongoDB(get_client())

    async def create_new_user_persistencia(self,user:UserPersistencia):
        user_persistencia_dict:dict = user.dict()

        _ = await self._db.create_user_persistencia(user_persistencia_dict)
        
        return await build_response(HTTP_201_CREATED,msg="New User Created")
    
    async def get_n_documents(self):
        documents = await self._db.get_user_persistencia_nPage()
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "n_documents":documents
            }
        )
        
    async def get_users_persistencia(self,n_page:int = 1):
        users = await self._db.get_user_persistencia(numero_page=n_page)
        userList = [OutUserPersistencia(**user) for user in users['users']]
        if users:
           return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success': True,
                'payload': jsonable_encoder(userList),
                'total_pages':users['total_pages'],
                'current_pages':users['current_pages'],
                'n_documents_':users['n_documents_']
            },
        )
        
    async def delete_user_persistencia(self,numero_cedula:str):
        user = await self._db.delete_user_persistencia(numero_cedula)

        if user:
            return await build_response(msg="Usuario eliminado existosamente")
        
        raise HTTPException(
            status_code=HTTP_204_NO_CONTENT,
            detail="Existe un fallo al eliminar el usuario"
        )

    async def get_images_users(self,numero_cedula:str):
        user = await self._db.get_user_by_numero_cedula(numero_cedula)
        path = os.getcwd() + "/Uploads"
        files = os.listdir(path)
        imagenes = []
        for fichero in files:
            for img in user['images_id']:
                if fichero == img:
                    imagenes.append(fichero)
                    
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "success":True,
                'payload':OutUserPersistencia(**user).dict()
            }
        )
    
    async def create_user_image_file(self,user:UserPersistencia,file:UploadFile = File(...)):
        user_persistencia_dict:dict = user.dict()
        
        _ = await self._db.create_user_with_file(user_persistencia_dict,file)

        return await build_response(HTTP_201_CREATED,msg="Usuario creado exitosamente")
       
    async def get_image_user_gridfs(self,numero_cedula:str):
        data = self._db.get_images_user(numero_cedula)
        lista = []
        for res in data:
            lista.append({"image_base64":res['image_base64'],"sizeX":res['sizeX'],"sizeY":res['sizeY'],'numero_cedula':numero_cedula})
        data_list = [OutUserImageGridfs(**user) for user in lista]
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "success":True,
                'payload':jsonable_encoder(data_list)
            }
        )
    
    def all_get_images_gridfs(self):
        data = self._db.all_images_user()
        lista = []
        for file_ in data:
            # print(file_['file_name'])
            lista.append({"image_base64":file_['image_base64'],"file_name":file_['file_name']})
        return lista
    

    def get_user_by_numero_cedula(self,numero_cedula:str,valor_porcentaje:float):
        data =  self._db.get_user_by_numero_cedula(numero_cedula=numero_cedula)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success':True,
                'payload':{
                    'numero_cedula':data['numero_cedula'],
                    'nombres': data['nombres'],
                    'apellidos':"",
                    'valor_match':str(valor_porcentaje)
                }
            }
        )
    def get_user_by_numero_cedula_all_data(self,numero_cedula:str):
        data = self._db.get_user_by_numero_cedula_all_data(numero_cedula=numero_cedula)
        image_data_ =   self._db.get_images_user(numero_cedula=numero_cedula)
        lista = []
        for res in image_data_:
            lista.append({"image_base64":res['image_base64']})

        data_list = [OutUserImageBase64(**user) for user in lista]

        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success':True,
                'payload':{
                    'image_base64':jsonable_encoder(data_list),
                    'numero_cedula':data['numero_cedula'],
                    'nombres':data['nombres'],
                    'condicion_cedulado':data['condicion_cedulado'],
                    # 'fecha_nacimiento':data['fecha_nacimiento'],
                    'lugar_ins_nacimiento':data['lugar_ins_nacimiento'],
                    'anio_ins_nacimiento':data['anio_ins_nacimiento'],
                    'nacionalidad':data['nacionalidad'],
                    'codigo_dactilar':data['codigo_dactilar'],
                    'estado_civil':data['estado_civil'],
                    'conyuge':data['conyuge'],
                    'instruccion':data['instruccion'],
                    'profession':data['profession'],
                    'nombre_padre':data['nombre_padre'],
                    'nacionalidad_padre':data['nacionalidad_padre'],
                    'nombre_madre':data['nombre_madre'],
                    'nacionalidad_madre':data['nacionalidad_madre'],
                    'domicilio':data['domicilio'],
                    'calles_domicilio':data['calles_domicilio'],
                    'doble_nacionalidad':data['doble_nacionalidad']
                }
            }
        )

    def save_image(self,numero_cedula:str,image_array_list):
       return self._db.convert_image_to_numpy_array(numero_cedula,image_array_list)     


    def get_data_solo_imgArrays(self,skip:int,limit:int,encoding_image):
        # return self._db.get_data_imgArrays(img_array)
        users_ =  self._db.get_user_paginate(limit=limit,skip=skip)
        # print(n_documents)
        # print(users_[0]['image_array'][0]) #TODO: Esto si funciona
        face_encoding_images:list = []
        for data_ in users_:
            for key,value in data_.items():
                if key == 'image_array':
                    for value_ in value:
                        valor__ = np.frombuffer(value_,dtype=np.int32).reshape((2,2,3))
                        print(valor__)
                        # vector_str = str(value_)
                        # vector_bytes_encode = vector_str.encode()
                        # vector_bytes_decode = vector_bytes_encode.decode('unicode-escape').encode('ISO-8859-1')[2:-1]
                        # print(valor__)
                        # valor = face_recognition.face_encodings(valor__)[0]
                        # print(valor)
                        # print(face_recognition.face_encodings(value_)[0])
                        # face_encoding_images.append()

                        
        # HACK: Compare images 
        # compare_face = face_recognition.compare_faces(face_encoding_images,encoding_image,tolerance=0.5)
        # print(compare_face)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success':True,
                'payload':{ }
            }
        )