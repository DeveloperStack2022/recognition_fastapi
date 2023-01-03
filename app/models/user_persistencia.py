
from fastapi import HTTPException
from typing import List,Optional
from pydantic.class_validators import validator   
from pydantic import (BaseModel,Field)
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from bson.objectid import ObjectId

class BaseUserPersistencia(BaseModel):
    numero_cedula:str = Field(...)
    nombres:str = Field(...)
    apellidos:str = Field(...)
    images_id:List[str] = Field(...)
    disabled:bool = Field(default=False)


class UserPersistencia(BaseUserPersistencia):

    @validator('numero_cedula')
    def validate_numero_cedula(cls,v):
        if v is '':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Numero de cedula es requerido"
            )
        return v

    @validator('nombres')
    def validate_nombres(cls,v):
        if v is '':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nombres es requerido"
            )
        return v
    
    @validator("apellidos")
    def validate_apellidos(cls,v):
        if v is '':
             raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Apellido es requerido"
            )
        return v

class AddUserPersistencia(BaseModel):
    numero_cedula:str
    nombres:str
    apellidos:str
    images_id:List[str]

class UpdateUserPersistencia(BaseModel):
    numero_cedula: Optional[str] = None
    nombres:Optional[str] = None
    apellidos:Optional[str] = None
    images_id: Optional[list] = None
    disable: Optional[bool] = None

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class OutUserPersistencia(BaseModel):
    file:PydanticObjectId = Field(...)
    numero_cedula:str = Field(...)
    nombres:str = Field(...)
    apellidos:str = Field(...)
    images_id:List[str] = Field(...)
    disabled:bool = Field(...)

class OutUserImageGridfs(BaseModel):
    numero_cedula:str = Field(...)
    image_base64:str = Field(...)
    sizeX:int = Field(...)
    sizeY:int = Field(...)