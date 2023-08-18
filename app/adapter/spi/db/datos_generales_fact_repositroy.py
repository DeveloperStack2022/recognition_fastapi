import typing
from app.adapter.spi.db.db_connection import DbConnection
from app.adapter.spi.db.mappers import DatosGeneralesMapper
from app.application.repositories.datos_generales_repository_abstract import DatosGeneralesRepositoryAbstract
from app.domain.api_exception import ApiException
from app.domain.datos_generales_entity import DatosGeneralesEntity
from app.domain.configuration_entity import ConfigurationEntity


class DatosGeneralesRepositoryFactory(DatosGeneralesRepositoryAbstract):

    def __init__(self,db_connection:DbConnection,config:ConfigurationEntity) -> None:
        self.mapper = DatosGeneralesMapper()
        self.db_connection = db_connection
        self.config = config

    def get_datos_generales(self) -> typing.List[DatosGeneralesEntity]:
        try:
            self.db_connection.connection(self.config)
            db = self.db_connection.get_client()
            res = db['new_project']
            res = res['user_persistencia_collection']

            data = res.find()

            if not data:
                raise ApiException("couldn't retrieve Users fact from user_persistencia_collection")
            
            facts: typing.List[DatosGeneralesEntity] = []
            for data_ in list(data): 
                facts.append(self.mapper.to_entity(data_))
            return facts
        
        except Exception as exception: 
            print(exception)
            raise ApiException('Error')

    def create_datos_generales(self,datos:DatosGeneralesEntity) -> typing.Dict[DatosGeneralesEntity,any]:
        try:
            self.db_connection.connection(self.config)
            db = self.db_connection.get_client()
            res = db['new_project']
            res = res['datos_generales']
            data = res.insert_one(datos.__dict__).inserted_id

            data_entity = res.find_one({'_id':data})
            print(data_entity)
            if  not data_entity:
                raise ApiException("Couldn't retrieve Users fact from user_persistencia_collection")
            
            return self.mapper.to_entity(model=dir(data_entity))
        except Exception as exception:
            raise ApiException('Error',)