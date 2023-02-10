# import typing
# # PyMongo
# from pymongo import MongoClient


# from src.adapter.spi.db.db_connection import DbConnection
# from src.application.repositories.user_fact_reposity_abstract import UserFactsRepositoryAbstract
# from src.domain.api_exceptions import ApiException
# from src.domain.user_fact_entiry import UserEntityFact
# from src.adapter.spi.db.mapper import UserFactMapper
# from src.adapter.spi.db.db_models import UserFact

# from src.domain.user_entity import UserEntity
# import gridfs
# from src.adapter.spi.db.db_connection import DbConnection

# class UserFactRepository(UserFactsRepositoryAbstract): # Para que funcione 'database' tiene que pasar por parametro la conexion mongodb
#     def __init__(self,database:DbConnection) -> None:
#         # self._collection = 
#     def get_user_fact_by_id(self,email:str) -> UserEntityFact:
#         user = self._collection.find({'email':email})
#         if not user:
#             return False
#         return user
    
#     def get_all_user_facts(self) -> typing.List[UserEntity]:
#         ...

#     def get_random_user_fact() -> UserEntity:
#         ...

from abc import abstractmethod
from typing import Any,Generic,TypeVar

from pymongo import MongoClient

T = TypeVar('T')

class PyMongoRepository(Generic[T]):

    def __init__(self,client:MongoClient):
        self._client = client
        self._database = self._client.get_database(self.get_database_name())
        self._collection = self._database.get_collection(self.get_colection_name())

    @abstractmethod
    def get_database_name(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_colection_name(self):
        raise NotImplementedError()

    def _get_collection(self):
        return self._collection
    
    async def _find_one(self,raw_query:dict[str,Any]) -> Any:
        return self._collection.find_one(raw_query)
    
    async def _find_many(self,raw_query:dict[str,Any]) -> Any:
        cursor =  self._collection.find(raw_query)
        data = list(cursor)
        return data
    
    async def _find_by_numero_cedula(self,numero_cedula)