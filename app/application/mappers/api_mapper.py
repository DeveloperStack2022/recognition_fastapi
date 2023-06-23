from abc import ABC,abstractmethod
from typing import Generic,TypeVar

Entity = TypeVar('Entity')
Presenter = TypeVar('Presenter')
Payload = TypeVar('Payload')


class ApiMapper(ABC,Generic[Entity,Presenter,Payload]):

    @abstractmethod
    def to_api(self,entity:Entity) -> Presenter:
        """""" 
    @abstractmethod
    def to_entity(self,payload:Payload) -> Entity:
        """"""