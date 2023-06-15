import logging 
from pymongo import MongoClient
from app.configs import MONGO_URL,MONGO_TIMEOUT
from app.application.spi.db_interface import DbInterface
from app.domain.configuration_entity import ConfigurationEntity
from app.domain.api_exception import ApiException
class DbConnection(DbInterface):
    def __init__(self,config:ConfigurationEntity) -> None:
        try:
            self.connection(config)
            if config.env != 'test':
                self.close_connection()
        except Exception as error:
            raise ApiException('error initialize connection to DB: {}'.format(str(error))) from error
        
    def connection(self, config: ConfigurationEntity) -> None:
        self.database = MongoClient(MONGO_URL, serverSelectionTimeoutMS=MONGO_TIMEOUT)
        