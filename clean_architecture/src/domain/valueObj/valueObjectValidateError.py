from src.domain.DomainError import DomainError

class ValueObjectValidationError(DomainError):
    ERROR_ID = '2266749d-def0-4614-bde7-66e8fcc3b46f'

    def __init__(self,msg:str = None):
        if msg is None:
            msg = 'Atribute validation error'
        
        self.msg = msg
    
    def to_primitives(self) -> dict | list:
        return {
            'message':self.msg,
            'id':self.get_id()
        }

    def get_id(self) -> str:
        return ValueObjectValidationError.ERROR_ID
