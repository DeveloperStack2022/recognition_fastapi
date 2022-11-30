
from fastapi import HTTPException
from typing import List,Optional
from pydantic.class_validators import validator   
from pydantic import (BaseModel,Field)
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

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
                detail="Campo apellido es requerido"
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

class OutUserPersistencia(BaseModel):
    numero_cedula:str = Field(...)
    nombres:str = Field(...)
    apellidos:str = Field(...)
    images_id:List[str] = Field(...)
    disabled:bool = Field(...)