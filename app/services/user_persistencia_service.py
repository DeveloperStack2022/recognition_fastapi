import os
from fastapi.encoders import jsonable_encoder
from http.client import HTTPException
from ..utils import build_response
from ..db import (MongoDB,get_client)
from ..models.user_persistencia import (UserPersistencia,OutUserPersistencia,UpdateUserPersistencia)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from starlette.responses import JSONResponse

class UserPersistenciaService:
    def __init__(self):
        super().__init__()
        self._db = MongoDB(get_client())
    
    async def create_new_user_persistencia(self,user:UserPersistencia):
        user_persistencia_dict:dict = user.dict()

        _ = await self._db.create_user_persistencia(user_persistencia_dict)
        
        return await build_response(HTTP_201_CREATED,msg="New User Created")
    
    async def get_users_persistencia(self):
        users = await self._db.get_user_persistencia()
        # items = jsonable_encoder(users)
        userList = [OutUserPersistencia(**user) for user in users]
        if users:
           return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success': True,
                'payload': jsonable_encoder(userList)
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