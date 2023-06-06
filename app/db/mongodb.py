# TODO: Configs 
from ..configs import (
    MONGO_DB_NAME,
    MONGO_USERS_COLLECTION,
    MONGO_USER_PERSISTENCIA_COLLECTION,
    MONGO_USER_DETECT_COLLECTION,
    PAGE_LIMIT
)

# TODO: Generics - 
import math
import base64
import logging
from bson import ObjectId
from typing import List

# TODO: Fast API - 
from fastapi import File,UploadFile
from fastapi.exceptions import HTTPException

from PIL import Image
# TODO: Status Http - 
from starlette.status import (
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR
)
# TODO: Mongod DB - 
from pymongo.errors import PyMongoError,BulkWriteError
from pymongo import (
    MongoClient,
    ReturnDocument,
)
# TODO: GridFs 
import gridfs

# TODO: Upload File Model - 
from ..models.file_upload_models import BaseFileUploadModel,FileUploadModelLista,BaseDataInputFileUpload,BaseDataInputFieldUploadList
from bson.objectid import ObjectId as BsonObjectId

# TODO: import module sistema operativo - (os)
import os 

#TODO: Utils 
from app import utils

# FIXME: Start class MongoDB:
class MongoDB:
    def __init__(self, client: MongoClient):
        self._client: MongoClient = client
        self._db = None
        self._coll = None
        self._gridfs = None
        try:
            self._client.server_info()
            self._db = self._client[MONGO_DB_NAME]
            self._gridfs = gridfs.GridFS(self._db)

            # Collections Mongodb
            self._coll = self._db[MONGO_USERS_COLLECTION]
            self._coll_pers = self._db[MONGO_USER_PERSISTENCIA_COLLECTION]
            self._coll_detect = self._db[MONGO_USER_DETECT_COLLECTION]

            # 
            self._coll_pers.create_index('numero_cedula',unique=True)

        except PyMongoError as e:
           logging.error(f'Database Connection Error ::: {e}')

    def db_health_check(self):
        try:
            self._client.server_info()
            return True
        except PyMongoError as e:
            return False

    async def insert_user(self, user: dict):
        users = self._coll.find({'email': user['email']})

        for u in users:
            if user['email'] in u.values():
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="This email is already in use"
                )
        try:
            id = self._coll.insert_one(user).inserted_id
            return str(id)
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB insert error"
            )

    async def get_user(self, email: str):
        try:
            users = self._coll.find({'email': email})

            if not users:
                return False

            for u in users:
                if email in u.values():
                    return u

            return False
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB retrive error"
            )

    async def get_user_by_id(self, id: str):
        try:
            users = self._coll.find({'_id': ObjectId(id)})

            if not users:
                return False

            for u in users:
                if ObjectId(id) in u.values():
                    return u

            return False
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB retrive error"
            )

    async def update_user(self, user: dict, email: str):
        try:
            user = self._coll.find_one_and_update(
                {'email': email}, {'$set': user}, return_document=ReturnDocument.AFTER)
            return user
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB update error"
            )

    async def delete_user(self, email: str):
        try:
            user = self._coll.find_one_and_delete({'email': email})
            return user
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB delete error"
            )
    
    
    async def create_user_persistencia(self,user:dict):
 
        users = self._coll_pers.find({'numero_cedula':user['numero_cedula'],"disabled":False})
        for u in users:
            print(u)
            if user['numero_cedula'] in u.values():
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="Este usuario ya esta registrado"
                )
        try:
            id = self._coll_pers.insert_one(user).inserted_id
            return str(id)
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB error"
            )

    def get_user_persistencia_nPage(self):
        try:
            n_documents_:int = self._coll_pers.count_documents({})
            return n_documents_
        except Exception as e: 
            raise(e)


    async def get_user_persistencia(self,numero_page:int):
        try:
            """ 
                Example:
                Data --------- 
                    {'name': 'Audi', '_id': ObjectId('5b41eb21b9c5d915989d48a8')}
                    {'name': 'Mercedes', '_id': ObjectId('5b41eb21b9c5d915989d48a9')}
                    {'name': 'Skoda', '_id': ObjectId('5b41eb21b9c5d915989d48aa')}
                    {'name': 'Volvo', '_id': ObjectId('5b41eb21b9c5d915989d48ab')}
                    {'name': 'Bentley', '_id': ObjectId('5b41eb21b9c5d915989d48ac')}
                    {'name': 'Citroen', '_id': ObjectId('5b41eb21b9c5d915989d48ad')}
                    {'name': 'Hummer', '_id': ObjectId('5b41eb21b9c5d915989d48ae')}
                    {'name': 'Volkswagen', '_id': ObjectId('5b41eb21b9c5d915989d48af')}
                End Data --------
                    .skip() -> De donde va iniciar. 
                    .limit() -> Donde va terminar.
                    db.collection.find().skip(2).limit(3)

                    Output: 
                        Element 1: {'name': 'Skoda', '_id': ObjectId('5b41eb21b9c5d915989d48aa')}
                        Element 2: {'name': 'Volvo', '_id': ObjectId('5b41eb21b9c5d915989d48ab')}
                        Element 3: {'name': 'Bentley', '_id': ObjectId('5b41eb21b9c5d915989d48ac')}
                
                Nota:
                    - Una page tiene 10 registro (n*10)
                        - por ejemplo si vamos a pagina 1(uno) seria el calculo asi .skip(10 * (1 - 1)).limit(10) | .skip(10 * 0).limit(10) 
                            -Empieza en el registro 0 y termina en el registro 10
                    - Pagina numero 2 seria de la 10 - 20 registro 
                        - por ejemplo si vamos a la pagina 2(dos) seria calculado asi .skip(10 * (2-1)).limit(10) | .skip(10 * 1 ).limit(10) | .skip(10).limit(10)
                    - Pagina numero 2 seria de la 20 - 30 registro 
                        - por ejemplo si vamos a la pagina 3(dos) seria calculado asi .skip(10 * (3-1)).limit(10) | .skip(10 * 2 ).limit(10) | .skip(20).limit(10)

                .skip(page_limit_ * (page - 1)).limit(page_limit_)
                .skip(10 * (8 - 1)).limit(10)
                .skip(10 * 9).limit(10)
                .skip(90).limit(10)
            """
            page_limit_:int = PAGE_LIMIT
            n_documents_:int = self._coll_pers.count_documents({})
            total_pages = math.ceil(n_documents_ / page_limit_ )
           
            # print(total_pages)
            # 10 *  - 1 
            if numero_page == 0: numero_page = 1
            users = self._coll_pers.find({"disabled":False}).skip(page_limit_ * (numero_page - 1)).limit(page_limit_)
        
            # if int(n_documents_) >  page_limit_ * (numero_page - 1): # 10 * (2 - 1) => 10 * 1 = 10  | si n_documents_ > 10 ?  True : false
            #     users = self._coll_pers.find({"disabled":False}).skip(page_limit_ * (numero_page - 1)).limit(page_limit_)
            #     current_pages = math.ceil( n_documents_ % numero_page ) # page 0 | 1 | 2 | 3 | 4
            # else:
            #     numero_page_ = 1
            #     users = self._coll_pers.find({"disabled":False}).skip(page_limit_ * (numero_page_ - 1)).limit(page_limit_)
                
            # users = self._coll_pers.find({"disabled":False}).skip(0).limit(10)
            if not users:
                return False
            return {
                'users':list(users),
                'total_pages':total_pages,
                'current_pages':2,
                'n_documents_':n_documents_
            }
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB retrive error"
            )

    async def delete_user_persistencia(self,numero_cedula:str):
        try:
            # print(numero_cedula)
            user = self._coll_pers.find_one_and_update({'numero_cedula':numero_cedula,"disabled":False},{'$set':{
                'disabled':True
            }})
            if not user:
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="Este usuario no existe"
                )
            return user
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB delete error"
            )
    
    def get_user_by_numero_cedula(self,numero_cedula:str):
        try:
            user =  self._coll_pers.find_one({"numero_cedula":numero_cedula,"disabled":False})
            if not user: 
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="El usuario con este numero de identificacion no existe"
                )
            return user
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB Error al buscar el usuario"
            )
    #
    def get_user_by_numero_cedula_all_data(self,numero_cedula:str):
        try:
            user = self._coll_pers.find_one({'numero_cedula':numero_cedula})
            if not user: 
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="El usuario con este numero de identificacion no existe"
                )
            return user
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB Error al buscar el usuario"
            )
    
    async def create_user_detect(self,numero_cedula:str):
        try:
            user = self._coll_detect.insert_one({'numero_cedula': numero_cedula}).inserted_id
            return str(user)
        except:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB Error"
            )
        

    async def delete_user_detect(self,numero_cedula:str):
        try:
            self._coll_detect.delete_many({})
            return True
        except:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB Error"
            )

    async def create_user_with_file(self,user:dict,file:UploadFile = File(...)):
        users = await self._coll_pers.find({'numero_cedula':user['numero_cedula'],"disabled":False})
        for u in users:
            if user['numero_cedula'] in u.values():
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail="Este usuario ya esta registrado"
                )
        fs = self._gridfs
        #convert to base64
        encoded_base64 = base64.standard_b64encode(file.file.read())
        numero_cedula = user['numero_cedula']
        img = Image.open(file.file)
        width, height = img.size
        file_fs = fs.put(encoded_base64,file_name=str(numero_cedula),sizeX=width,sizeY=height)
        # array = [list(i) for i in user.items()]
        user['file'] = [file_fs]
        try:
            id = self._coll_pers.insert_one(user).inserted_id
            return str(id)
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Mongo Db Error"
            )

    def create_user_with_file_CSV(self,user: FileUploadModelLista): #,file: UploadFile = File(...)
        """
            user = [{'numero_cedula':'2300143571','nombres':'Juanito David','apellidos':'Zambrano Piero'},{...},{...},{...}]
            
            - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            1. Read "path_dir" del Archivo
            2. 
            fs.put()
        """ 
        data_user_dict:List[BaseFileUploadModel] = user.dict().get('users')

        fs = self._gridfs
        list_filter = []

        # TODO: Path Dir files Images 
        path_root = os.getcwd() + '/FilesUpload'

        
        for lista in data_user_dict:
            # print(lista['nombres']) # HACK: Funciona = True
            validation = self._coll_pers.find_one({'numero_cedula':lista['numero_cedula']})
           
            if validation is not None:
                string_var = path_root + "/"+lista['numero_cedula']+".png"
                with open( string_var ,'rb') as file_:
                    encode_base64_ = base64.standard_b64encode(file_.read())
                    image_ = Image.open(f'''{path_root}/{lista['numero_cedula']}.png''')
                    width_,height_ = image_.size
                    id_fs_ = fs.put(encode_base64_,file_name=str(lista['numero_cedula']),sizeX=width_,sizeY=height_)
                    list_filter.append({'numero_cedula':lista['numero_cedula'],'nombres':lista['nombres'],'file':[id_fs_]})
        
        if len(list_filter) > 0 : 
            self._coll_pers.insert_many(list_filter).inserted_ids

    async def create_user_with_file_csv_fields(self,data:BaseDataInputFieldUploadList):
        # print(dict(data.users))
        data_users: List[BaseDataInputFileUpload] = data.dict().get('users')
        path_root = os.getcwd() + '/FilesUpload'
        fs = self._gridfs
        lista_filter = []
        for i in data_users:
            verify = utils.verify_cedula(num=i['numero_cedula'])
            if verify:
                validation = self._coll_pers.find_one({'numero_cedula':i['numero_cedula']})
                # validation = self._coll_pers.find_one_and_update({'numero_cedula':i['numero_cedula']},{
                #     '$set':{
                    # 'disabled':False,
                    # 'condicion_cedulado':'',
                    # 'anio_ins_nacimiento':'',
                    # 'nacionalidad':'',
                    # 'codigo_dactilar':'',
                    # 'estado_civil':'',
                    # 'conyuge':'',
                    # 'instruccion':'',
                    # 'profession':'',
                    # 'nombre_padre':'',
                    # 'nacionalidad_padre':'',
                    # 'nombre_madre':'',
                    # 'nacionalidad_madre':'',
                    # 'domicilio':'',
                    # 'calles_domicilio':'',
                    # 'doble_nacionalidad':''
                #     }}) # TODO: Return Veradero - falso

        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
                if validation is None: # False -> True | True -> False
                    string_var = path_root + "/" + i['numero_cedula']+".jpg"
                    if os.path.exists(string_var):
                        with open(string_var,'rb') as write_file:
                            encode_base64_ = base64.standard_b64encode(write_file.read())
                            image_ = Image.open(f'''{path_root}/{i['numero_cedula']}.jpg''')
                            width_,height_ = image_.size
                            id_fs_ = fs.put(encode_base64_,file_name=str(i['numero_cedula']),sizeX=width_,sizeY=height_)

                            lista_filter.append({
                                'numero_cedula':i['numero_cedula'],
                                'nombres':i['nombres'],
                                'nacionalidad':i['nacionalidad'],
                                'lugar_ins_nacimiento':i['lugar_nacimiento'],
                                'file':[id_fs_],
                                'disabled':False,
                                'condicion_cedulado':'',
                                'anio_ins_nacimiento':'',
                                'nacionalidad':'',
                                'codigo_dactilar':'',
                                'estado_civil':'',
                                'conyuge':'',
                                'instruccion':'',
                                'profession':'',
                                'nombre_padre':'',
                                'nacionalidad_padre':'',
                                'nombre_madre':'',
                                'nacionalidad_madre':'',
                                'domicilio':'',
                                'calles_domicilio':'',
                                'doble_nacionalidad':''
                                })

        try:

            if len(lista_filter) > 0:
                self._coll_pers.insert_many(lista_filter).inserted_ids
        except BulkWriteError  as Error:
            print(Error)
        
    def get_images_user(self,numero_cedula:str):
        # print(numero_cedula)
        fs = self._gridfs 
        user_images = fs.find({"file_name":numero_cedula})
        # file = user_image.read()
        imagelist = []
        for image in user_images:
            read_base64 = image.read()
            imagelist.append({'image_base64':read_base64,"sizeX":image.sizeX,"sizeY":image.sizeY})
        return imagelist
    
    def all_images_user(self):
        fs = self._gridfs
        user_images = fs.find()
        image_lists = [] 
        for image in user_images:
            read_base64 = image.read()
            image_lists.append({'image_base64':read_base64,"file_name":image.file_name})
        return image_lists
    
    def convert_image_to_numpy_array(self,numero_cedula:str,image_array_list:any):
        # TODO:  
        self._coll_pers.find_one_and_update({'numero_cedula':numero_cedula},{
            '$push':{
                'image_array':image_array_list
            }
        }) 
        # self._coll_pers.find_one_and_update({'numero_cedula':numero_cedula},{
        #     '$pop':{
        #         'image_array':1
        #     }
        # })
        return True

    def get_data_imgArrays(self,img_array):
        # values_ = self._coll_pers.find({'image_array':{"$elemMatch":img_array}})
        # print(values_)
        # for data in values_:
        #     print(data) 
        return True

    def get_user_paginate(self,skip:int,limit:int):
        return self._coll_pers.find({"disabled":False}).skip(limit * (skip - 1)).limit(limit)
    

    