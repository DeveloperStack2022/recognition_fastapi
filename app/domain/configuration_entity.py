class ConfigurationEntity:
    def __init__(self,uri_database:str,registros_collection:str,env:str) -> None:
        self.registros_collection = registros_collection
        self.env = env
        self.uri_database = uri_database