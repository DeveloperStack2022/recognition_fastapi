from abc import ABC,abstractmethod
from typing import Generic,Iterable,TypeVar

# Domain 
from src.domain.user_entity import UserEntity

Entity = TypeVar("Entity")

class GenericUseCases(ABC,Generic[Entity]):
    @abstractmethod
    def execute(self) -> Entity:
        """ Execute a usecase & return an generic type """

class UseCaseOneEntity(GenericUseCases):
    @abstractmethod
    def execute(self) -> UserEntity:
        """Execute a use case & return an entity object"""

class UseCaseMultipleEntities(GenericUseCases):
    @abstractmethod
    def execute(self) -> Iterable[UserEntity]:
        """Execute a use case & return multiple entity objects"""