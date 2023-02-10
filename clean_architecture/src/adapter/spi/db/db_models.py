from http.client import HTTPException
from telnetlib import STATUS
from pydantic import Field,BaseModel,validator
from .db_connection import DbConnection


class UserFact(BaseModel):
    nombres:str = Field(...)
    numero_cedula:str = Field(...)
   
