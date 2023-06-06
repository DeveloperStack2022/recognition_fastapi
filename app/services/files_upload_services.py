# TODO: Imports files customs - 
from ..db import (MongoDB,get_client)
from ..models.file_upload_models import BaseFileUploadModel,FileUploadModelLista,BaseDataInputFileUpload,BaseDataInputFieldUploadList

# TODO: Fast APi - 
from fastapi import File,UploadFile

# TODO: Response Json
from starlette.responses import JSONResponse
from starlette.status import (HTTP_200_OK)
from ..utils import verify_cedula

# TODO: Types - List - 
from typing import List

class FileUploadFilesService: 
    def __init__(self):
        super().__init__()
        self._db = MongoDB(get_client())

    def create_user_for_csv(self,user:FileUploadModelLista):
        
        #print(user.dict().get('users')) # TODO: Aqui tenemos todo el listado del array de objetos que esta pasando. 
        # data_user_dict:List[BaseFileUploadModel] = user.dict().get('users')
        self._db.create_user_with_file_CSV(user=user)
        return True
        # data_user_dic:dict = dict(user)
        # print(data_user_dic)
    
    async def create_user_for_csv_fields(self,user:BaseDataInputFieldUploadList):
        return await self._db.create_user_with_file_csv_fields(data=user)
        