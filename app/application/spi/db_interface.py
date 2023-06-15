from abc import ABC,abstractmethod
from app.domain.configuration_entity import ConfigurationEntity

class DbInterface(ABC):
    @abstractmethod
    def connection(self,config:ConfigurationEntity) -> None:
        """Execute a database connection"""
    @abstractmethod
    def close_connection(self) -> None:
        """Exceute a close connection"""