from src.domain.user_entity import UserEntity

class UserEntityFact(UserEntity):
    def __init__(self,fact_text:str,fact_length:int) -> None:
        super().__init__()
        self.fact_text = fact_text
        self.fact_length = fact_length