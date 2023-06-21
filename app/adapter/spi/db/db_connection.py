import logging 
from pymongo import MongoClient
from app.configs import MONGO_TIMEOUT
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
        logging.info('Establish database connection')
        try:
            self.database = MongoClient(config.uri_database, serverSelectionTimeoutMS=MONGO_TIMEOUT)
            self.database.server_info()
            logging.info('Connected to database succesfully')
        except:
            logging.error('Connecting to databse failed')
    
    def close_connection(self) -> None:
        logging.info('Closing Database Connection')
        try:
            self.database.close()
            logging.info('Database disconnected successfully')
        except:
            logging.error('Database disconnected failed')
    
    def get_client(self) -> MongoClient:
        return self.database