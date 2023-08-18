from app.domain.configuration_entity import ConfigurationEntity
from app.adapter.spi.db.db_connection import DbConnection
from app.adapter.spi.http.http_connection import HttpConnection
from app.adapter.spi.db.datos_generales_fact_repositroy import DatosGeneralesRepositoryFactory
from app.domain.api_exception import ApiException

class RepositoryFactory:
    
    def __init__(self,config:ConfigurationEntity,db_connection:DbConnection,http_connection:HttpConnection) -> None:
        self.__repositories:dict = {
            'users_collection': DatosGeneralesRepositoryFactory(db_connection=db_connection,config=config),
            'create_datos_generales':DatosGeneralesRepositoryFactory(db_connection=db_connection,config=config)
        }

    def get_repository(self,repository_name:str):
        
        if repository_name in self.__repositories:
            return self.__repositories[repository_name]
        else:
            raise ApiException('Repository does not exist')
    
