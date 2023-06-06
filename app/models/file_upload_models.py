from fastapi import HTTPException
from pydantic.class_validators import validator
from pydantic import (BaseModel,Field)
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import List,Optional
from bson.objectid import ObjectId as BsonObjectId
from datetime import datetime,date
# from ..utils import verify_cedula


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        print(v)
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class BaseFileUploadModel(BaseModel):
    numero_cedula:str = Field(...)
    nombres:str = Field(...)

class FileUploadModel(BaseFileUploadModel):
    @validator('numero_cedula')
    def validate_numero_cedula(cls,v):
        if v == '':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Numero de cedula es requerido"
            )
        # validate_response = verify_cedula(v)
        # if validate_response == False:
        #     raise HTTPException(
        #         status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        #         detail="Numero de cedula es incorrecto"
        #     )
        return v

class FileUploadModelLista(BaseModel):
    users:List[BaseFileUploadModel]

class BaseDataInputFileUpload(BaseModel):
    numero_cedula:str = Field(...)
    nombres:str = Field(...)
    nacionalidad:str = Field(...)
    lugar_nacimiento:str = Field(...)
    
class BaseDataInputFieldUploadList(BaseModel):
    users:List[BaseDataInputFileUpload]