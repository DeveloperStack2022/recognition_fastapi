from typing import Dict,Optional
from dotenv import dotenv_values

from src.domain.configuration_entity import ConfigurationEntity

class ConfigurationMapper:
    def __init__(self,env:str):
        env = env.lower()

        __confi_raw:Dict[str,Optional[str]] = dotenv_values(".env.{}".format(env))
        
        user_source = __confi_raw.get("USER_SOURCE")
        db_url = __confi_raw.get("MONGO_URL")

        if user_source is None or db_url is None:
            raise Exception()
        
        self.config = ConfigurationEntity(user_source,db_url,env)

    def get_config(self) -> ConfigurationEntity:
        return self.config