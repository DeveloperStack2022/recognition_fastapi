from pydantic import (
    BaseModel,
    Field
)

class BaseUserDetect(BaseModel):
    numero_cedula:str = Field(...)

class AddUserDetect(BaseModel):
    numero_cedula:str

class OutUserDetect(BaseModel):
    numero_cedula:str = Field(...)
