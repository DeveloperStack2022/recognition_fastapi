import logging

from fastapi.exceptions import HTTPException
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
    MONGO_USER_PERSISTENCIA_COLLECTION
)


class MongoDB:
    def __init__(self, client: MongoClient):
        self._client: MongoClient = client
        self._db = None
        self._coll = None

        try:
            self._client.server_info()
            self._db = self._client[MONGO_DB_NAME]
            # Collections Mongodb
            self._coll = self._db[MONGO_USERS_COLLECTION]
            self._coll_pers = self._db[MONGO_USER_PERSISTENCIA_COLLECTION]

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
            users = self._coll_pers.find({})
            print(list(users))
            if not users:
                return False

            for u in users:
                return u

            return False
        except PyMongoError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PyMongo DB retrive error"
            )
