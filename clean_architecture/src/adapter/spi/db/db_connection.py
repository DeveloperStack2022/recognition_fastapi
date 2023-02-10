# #Configuration Entity
# import logging
# from src.domain.configuration_entity import ConfigurationEntity
# from src.application.spi.interface_db import DBInterface
# #Configuration Domain 
# from src.domain.api_exceptions import ApiException

# # PyMongo
# from pymongo import MongoClient

# class DbConnection(DBInterface):
#     def __init__(self,config:ConfigurationEntity) -> None:
#         try:
#             self.database:MongoClient = None
#             self.connection(config)
#         except Exception as e:
#             raise ApiException("error initialize connection to DB: {}".format(str(e))) from e
        
#     def connection(self,config:ConfigurationEntity) -> MongoClient:
#         try:
#             # print(config.env)
#             self.database = MongoClient(config.db_url)
#             self.database.server_info()
#             logging.info("Connect to database successfully")
#             return self.database
#         except Exception as e:
#             logging.error("Connecting to database failed")
    
#     def close_db_connection(self):
#         try:
#             self.database.close()
#             logging.info("Database disconected successfully")
#         except Exception as e:
#             logging.error("Database disconected failed")

from pymongo import MongoClient
from src.infrastructure.persistencia.mongo.PyMongoConfiguration import PyMongoConfiguration

class PyMongoClientFactory:
    _client:dict[str,MongoClient] = {}

    @staticmethod
    def _get_client(context_name:str):
        return PyMongoClientFactory._client.get(context_name)
    
    @staticmethod
    def _add_client(context_name:str,client:MongoClient):
        PyMongoClientFactory._client[context_name] = client
    
    @staticmethod
    def create_instance(context_name:str,config: PyMongoConfiguration = None):
        client = PyMongoClientFactory._get_client(context_name)
        if client is not None:
            return client
        
        if config is None:
            config = PyMongoConfiguration()
        
        client = config.create_client_from_config()
        PyMongoClientFactory._add_client(context_name,client)
        return client