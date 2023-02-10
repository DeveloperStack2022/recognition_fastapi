# Domain Fact
from src.domain.user_fact_entiry import UserEntityFact
# Error Handling Utils 
from src.application.utils.error_handling_utils import ErrorHandlingUtils
# UseCases Interface 
from src.application.usecases.interfaces import UseCaseOneEntity
# User Repository 
from src.application.repositories.user_fact_reposity_abstract import UserFactsRepositoryAbstract


class GetOneRandomUserFactUseCase(UseCaseOneEntity):
    def __init__(self,repository:UserFactsRepositoryAbstract) -> None:
        self.repository = repository
    
    def execute(self) -> UserEntityFact:
        try:
            return self.repository.get_random_user_fact()
        except Exception as e:
            raise ErrorHandlingUtils.application_error("can't get random user fact",e)