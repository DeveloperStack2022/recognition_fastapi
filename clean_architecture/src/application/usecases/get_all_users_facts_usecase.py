import typing
#Repository
from src.application.repositories.user_fact_reposity_abstract import UserFactsRepositoryAbstract
# Interfaces 
from src.application.usecases.interfaces import UseCaseMultipleEntities
# Domain
from src.domain.user_fact_entiry import UserEntityFact
# ErrorHandlingUtils 
from src.application.utils.error_handling_utils import ErrorHandlingUtils


class GetAllFactsUseCase(UseCaseMultipleEntities):
    def __init__(self,repository:UserFactsRepositoryAbstract) -> None:
        self.repository = repository
    
    def execute(self) -> typing.Iterable[UserEntityFact]:
        try:
            return self.repository.get_all_user_facts()
        except Exception as e:
            raise ErrorHandlingUtils.application_error("Can't get all users facts",e)
