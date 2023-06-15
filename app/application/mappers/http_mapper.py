from abc import ABC,abstractclassmethod
from typing import Generic,TypeVar

Entity = TypeVar('Entity')
HttpObject = TypeVar('HttpObject')


class HttpMapper(ABC,Generic[Entity,HttpObject]):

    @abstractclassmethod
    def to_http(self,entity:Entity) -> HttpObject:
        """Map an Entity to an HttpObject"""
    
    @abstractclassmethod
    def to_entity(self,http_object:HttpObject) -> Entity:
        """Map an HttpObject to an Entity"""