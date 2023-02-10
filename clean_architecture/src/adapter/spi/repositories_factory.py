from src.adapter.spi.db.db_connection import DbConnection
from src.adapter.spi.http.http_connection import HttpConnection
from src.domain.configuration_entity import ConfigurationEntity
from src.adapter.spi.db.user_fact_repository import UserFactRepository

class RepositoriesFactory:
    def __init__(self,config:ConfigurationEntity,db_connection:DbConnection,http_connection:HttpConnection) -> None:
        # self.__repositories:dict = {
        #     "user_fact_repository":UserFactRepository(db_connection)
        # }
        self._repositories = UserFactRepository(db_connection)

    def get_repository(self):
        users = self._repositories.get_all_user_facts()
        for user in users:
            print(user)
        return users
        # if repository_name in self.__repositories:
        #     return self.__repositories[repository_name]
        # else:
        #     raise Exception("Repository does not exist")
            
