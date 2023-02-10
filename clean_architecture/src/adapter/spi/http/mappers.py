from typing import Any
from src.application.mappers.http_mapper import HttpMapper
from src.domain.user_fact_entiry import UserEntityFact

class UserFactHttpMapper(HttpMapper):
    def to_http(self, entity: UserEntityFact) -> Any:
        raise Exception("not implemented")
    
    def to_entity(self, http_obj: Any) -> UserEntityFact:
        return UserEntityFact(http_obj['fact'],http_obj['length'])