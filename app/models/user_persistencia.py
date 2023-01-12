
from fastapi import HTTPException
from typing import List,Optional
from pydantic.class_validators import validator   
from pydantic import (BaseModel,Field)
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from bson.objectid import ObjectId
from datetime import date,datetime

class BaseUserPersistencia(BaseModel):
    numero_cedula:str = Field(...)
    nombres:str = Field(...)
    condicion_cedulado:str = Field(...)
    fecha_nacimiento:datetime 
    lugar_ins_nacimiento:str = Field(...)
    anio_ins_nacimiento:str = Field(...)
    nacionalidad:str = Field(...)
    codigo_dactilar:str = Field(...)
    estado_civil:str = Field(...)
    conyuge:str = Field(...)
    instruccion:str = Field(...)
    profession:str = Field(...)
    nombre_padre:str = Field(...)
    nacionalidad_padre:str = Field(...)
    nombre_madre:str = Field(...)
    nacionalidad_madre:str = Field(...)
    domicilio:str = Field(...)
    calles_domicilio:str = Field(...)
    doble_nacionalidad:str = Field(...)
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

class AddUserPersistencia(BaseModel):
    numero_cedula:str
    nombres:str
    condicion_cedulado:str
    fecha_nacimiento:datetime
    lugar_ins_nacimiento:str
    anio_ins_nacimiento:str
    nacionalidad:str
    codigo_dactilar:str
    estado_civil:str
    conyuge:str
    instruccion:str
    profession:str
    nombre_padre:str
    nacionalidad_padre:str
    nombre_madre:str
    nacionalidad_madre:str
    domicilio:str
    calles_domicilio:str
    doble_nacionalidad:str
    images_id:List[str]

class UpdateUserPersistencia(BaseModel):
    numero_cedula: Optional[str] = None
    nombres:Optional[str] = None
    apellidos:Optional[str] = None
    # images_id: Optional[list] = None
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

class File_Type(BaseModel):
    image_base64:str = Field(...)
    sizeX:int = Field(...)
    sizeY:int = Field(...)
    file_id:PydanticObjectId = Field(...)

class OutUserPersistencia(BaseModel):
    numero_cedula:str = Field(...)
    nombres:str = Field(...)
    apellidos:str = Field(default="")
    disabled:bool = Field(...)
    file:list[PydanticObjectId] = Field(...)
    # file:list[File_Type] = Field(...)

class OutUserImageGridfs(BaseModel):
    numero_cedula:str = Field(...)
    image_base64:str = Field(...)
    sizeX:int = Field(...)
    sizeY:int = Field(...)

class OutUserImageBase64(BaseModel):
    image_base64:str = Field(...)