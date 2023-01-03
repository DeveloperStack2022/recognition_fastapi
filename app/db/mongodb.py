import base64
import logging
from fastapi import File,UploadFile
from fastapi.exceptions import HTTPException
from PIL import Image
from starlette.status import (
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from bson import ObjectId
from pymongo.errors import PyMongoError
from pymongo import (
    MongoClient,
    ReturnDocument

)
from ..configs import (
    MONGO_DB_NAME,
    MONGO_USERS_COLLECTION,
    MONGO_USER_PERSISTENCIA_COLLECTION,
    MONGO_USER_DETECT_COLLECTION

)
import gridfs


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
 
        users = self._coll_pers.find({'numero_cedula':user['numero_cedula']})
        for u in users:
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
    async def get_user_persistencia(self):
        try:
            users = self._coll_pers.find({"disabled":False})
            # users = self._coll_pers.find({"disabled":False}).populate([{
            #     'path':'file',
            #     'populate':{
            #         'path':'file_id',
            #         'model':'fs.files'
            #     }
            # }])
            if not users:
                return False
            return list(users)
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB retrive error"
            )

    async def delete_user_persistencia(self,numero_cedula:str):
        try:
            user = self._coll_pers.find_one_and_update({'numero_cedula':numero_cedula},{'$set':{
                'disabled':True
            }})
            return user
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB delete error"
            )
    
    async def get_user_by_numero_cedula(self,numero_cedula:str):
        try:
            user = self._coll_pers.find_one({"numero_cedula":numero_cedula})
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
        users = self._coll_pers.find({'numero_cedula':user['numero_cedula']})
        for u  in users:
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