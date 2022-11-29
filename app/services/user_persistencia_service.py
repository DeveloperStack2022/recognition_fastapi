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
        print(user)
        user_persistencia_dict:dict = user.dict()

        _ = await self._db.create_user_persistencia(user_persistencia_dict)
        
        return await build_response(HTTP_201_CREATED,msg="New User Created")
    
    async def get_users_persistencia(self):
        user = await self._db.get_user_persistencia()
        if user:
           return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success': True,
                'payload': OutUserPersistencia(**user).dict()
            },
        )
