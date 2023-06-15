from app.configs import (
    MONGO_DB_NAME,
    MONGO_USER_PERSISTENCIA_COLLECTION,
)
import logging
from pymongo import (
    MongoClient,
    errors
)
import typing
# Adapter Layer 
from app.adapter.spi.db.mappers import DatosGeneralesMapper
# Application Layer
from app.application.repositories.datos_generales_repository_abstract import DatosGeneralesRepositoryAbstract
# Domain Layer 
from app.domain.datos_generales_entity import DatosGeneralesEntity
from app.domain.api_exception import ApiException

class DatosGeneralesRepository(DatosGeneralesRepositoryAbstract):
    def __init__(self,client:MongoClient)-> None:
        self.client:MongoClient = client
        self.db = None
        self.mapper = DatosGeneralesMapper()

        try:
            self.client.server_info()
            self.db = self.client[MONGO_DB_NAME]


            """Collections Mongodb"""
            self.user_persistencia = self.db[MONGO_USER_PERSISTENCIA_COLLECTION]
        except errors.PyMongoError as error:
            logging.error(f'Database Connection Error ::: {error}')


    def get_datos_generales(self) -> typing.List[DatosGeneralesEntity]:
        res = self.user_persistencia.find()

        if not res:
            raise ApiException("couldn't retrieve Datos Generales")
        
        datos_generales: typing.List[DatosGeneralesEntity] = []

        for data in res:
            datos_generales.append(self.mapper.to_entity(data))
        return datos_generales