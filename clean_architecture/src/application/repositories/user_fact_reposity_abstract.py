from abc import ABC,abstractmethod
import typing

# 
from src.domain.user_fact_entiry import UserEntity

class UserFactsRepositoryAbstract(ABC):
    @abstractmethod
    def get_random_user_fact(self) -> UserEntity:
        """Get random fact"""
    
    @abstractmethod
    def get_all_user_facts(self)-> typing.List[UserEntity]:
        """Get list users"""
        