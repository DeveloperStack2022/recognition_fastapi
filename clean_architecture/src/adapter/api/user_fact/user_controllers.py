import typing
from fastapi import APIRouter
from fastapi_injector import Injected

# Layer Adapters
from src.adapter.api.user_fact.user_facts_mappers import UserFactPresenterMapper
from src.adapter.api.user_fact.user_fact_presenter import UserFactPresenter
from src.adapter.api.shared.api_error_handling import ApiErrorHandling
from src.adapter.spi.repositories_factory import RepositoriesFactory

#Layer Application
from src.application.repositories.user_fact_reposity_abstract import UserFactsRepositoryAbstract
from src.application.usecases.get_all_users_facts_usecase import GetAllFactsUseCase
from src.application.usecases.get_one_random_user_fact_usecase import GetOneRandomUserFactUseCase

#Routes
router = APIRouter()

@router.get("/")
async def get_all_users_fact(factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        user_fact_repository:UserFactsRepositoryAbstract = factory.get_repository("user_fact_repository")
        user_fact_presenter_mapper:UserFactPresenterMapper = UserFactPresenterMapper()
        get_all_user_facts_usecases = GetAllFactsUseCase(repository=user_fact_repository)
        user_facts = get_all_user_facts_usecases.execute()
        facts: typing.List[UserFactPresenter] = []
        for data in user_facts:
            facts.append(user_fact_presenter_mapper.to_api(data))
        return facts
    except Exception as e:
        raise ApiErrorHandling.http_errr("Unexpected error getting all user facts",e)

@router.get("/random")
async def get_one_random_cat_fact(factory:RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        user_fact_repository:UserFactsRepositoryAbstract = factory.get_repository("user_fact_repository")
        user_fact_presenter_mappers:UserFactPresenterMapper = UserFactPresenterMapper()
        get_random_user_fact_usecase:GetOneRandomUserFactUseCase = GetOneRandomUserFactUseCase(user_fact_repository)
        user_fact = get_random_user_fact_usecase.execute()
        
        return user_fact_presenter_mappers.to_api(user_fact)
    except Exception as e:
        raise ApiErrorHandling.http_errr("Unexpected error getting a random user fact",e)