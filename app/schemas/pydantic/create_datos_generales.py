from pydantic import (
    BaseModel,
    Field
)

class DatosGeneralesPostRequest(BaseModel):
    c_identificacion:str = Field(...)
    nombres:str = Field(...)
    lugar_nacimiento:str = Field(...)
    sexo:str = Field(...)
    domicilio:str = Field(...)
    calles:str = Field(...)
    instruccion:str = Field(...)
    condicion_c:str = Field(...)
    nacionalidad:str = Field(...)
    e_civil:str = Field(...)
    n_casa:str = Field(...)
    pofofesion:str = Field(...)



