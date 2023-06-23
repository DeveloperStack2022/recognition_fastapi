import typing
from app.adapter.spi.db.db_connection import DbConnection
from app.adapter.spi.db.mappers import DatosGeneralesMapper
from app.application.repositories.datos_generales_repository_abstract import DatosGeneralesRepositoryAbstract
from app.domain.api_exception import ApiException
from app.domain.datos_generales_entity import DatosGeneralesEntity

class DatosGeneralesRepositoryFactory(DatosGeneralesRepositoryAbstract):
    def __init__(self,db_connection:DbConnection) -> None:
        self.mapper = DatosGeneralesMapper()
        self.db_connection = db_connection

    def get_datos_generales(self) -> typing.List[DatosGeneralesEntity]:
        res = self.db_connection.get_client()['new_project']
        
        res = res['user_persistencia_collection']

        data = res.find()
        if not data:
            raise ApiException("couldn't retrieve Users fact from user_persistencia_collection")

        return self.mapper.to_entity(data)

    def create_datos_generales(self,datos:DatosGeneralesEntity) -> typing.Dict[DatosGeneralesEntity,any]:
        res = res['user_persistencia_collection']

        data = res.insert_one(datos).inserted_id
        data = res.find_one({'_id':data})
        if  not data:
            raise ApiException("Couldn't retrieve Users fact from user_persistencia_collection")
        
        return self.mapper.to_entity(data)
        