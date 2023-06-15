class ConfigurationEntity:
    def __init__(self,registros_collection:str,env:str) -> None:
        self.registros_collection = registros_collection
        self.env = env