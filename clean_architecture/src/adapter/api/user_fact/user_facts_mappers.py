from typing import Any
from src.adapter.api.user_fact.user_fact_presenter import UserFactPresenter
from src.domain.user_fact_entiry import UserEntityFact
from src.application.mappers.api_mapper import ApiMapper
class UserFactPresenterMapper(ApiMapper):
    def to_api(self,entity:UserEntityFact) -> UserFactPresenter:
        return UserFactPresenter(entity.fact_text,entity.fact_length)
    
    def to_entity(self, payload: Any) -> UserEntityFact:
        raise Exception("not implimented")