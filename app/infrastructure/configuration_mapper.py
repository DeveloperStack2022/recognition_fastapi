from typing import Dict,Optional
from dotenv import dotenv_values

from app.domain.configuration_entity import ConfigurationEntity

class ConfigurationMapper:
    def __init__(self,env:str) -> None:

        env = env.lower()

        __config_raw:Dict[str,Optional[str]] = dotenv_values('.env')
        
        uri_database = __config_raw.get('MONGODB_URI')
        user_collection = __config_raw.get('USER_COLLECTION')

        if uri_database is None or user_collection is None:
            raise Exception()
        
        self.config = ConfigurationEntity(uri_database,user_collection,env)
    
    def get_config(self) -> ConfigurationEntity:
        return self.config