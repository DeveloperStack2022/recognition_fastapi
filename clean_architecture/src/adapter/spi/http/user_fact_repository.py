import typing
from src.adapter.spi.http.http_connection import HttpConnection
# from src.adapter.spi.http.
from src.application.repositories.user_fact_reposity_abstract import UserFactsRepositoryAbstract
from src.domain.api_exceptions import ApiException
from src.domain.user_fact_entiry import UserEntityFact
from src.adapter.spi.http.mappers import UserFactHttpMapper

class UserFactRepository(UserFactsRepositoryAbstract):
    def __init__(self,http_connection:HttpConnection,source:str) -> None:
        self.mapper = UserFactHttpMapper()
        self.source = source
        self.http_connection = http_connection
    
    def get_random_user_fact(self) -> UserEntityFact:
        res = self.http_connection.get("{}/fact".format(self.source))
        if not res.ok:
            raise ApiException("couldn't retrieve random user fact")
        
        res_json = res.json()
        if not res_json:
            raise ApiException("couldn't process json response")
        
        return self.mapper.to_entity(res_json)

    def get_all_user_facts(self) -> typing.List[UserEntityFact]:
        res = self.http_connection.get("{}/facts".format(self.source))
        if not res.ok:
            raise ApiException("couldn't retrive ")
        
        res_json = res.json()
        if not res_json:
            raise ApiException("couldn't process json response")
        
        facts:typing.List[UserEntityFact] = []
        for data in res_json['data']:
            facts.append(self.mapper.to_entity(data))
        return facts
         