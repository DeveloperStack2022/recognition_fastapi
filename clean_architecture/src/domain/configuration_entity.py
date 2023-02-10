
class ConfigurationEntity:
    def __init__(self,users_source:str,db_url:str,env:str):
        self.users_source = users_source
        self.env = env
        self.db_url = db_url