from abc import ABC,abstractmethod
from src.domain.configuration_entity import ConfigurationEntity

from pymongo import MongoClient


class DBInterface(ABC):
    @abstractmethod
    def connection(self,config:ConfigurationEntity) -> MongoClient:
        """Execute a database connection"""
    @abstractmethod
    def close_db_connection(self,config:ConfigurationEntity):
       """Execute a database close"""
            