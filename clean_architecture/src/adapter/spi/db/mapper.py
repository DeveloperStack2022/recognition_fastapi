from src.domain.user_fact_entiry import UserEntityFact
from src.application.mappers.db_mapper import DbMapper,DbModel
from src.adapter.spi.db.db_models import UserFact

class UserFactMapper(DbMapper):
    
    def to_db(self, entity: UserEntityFact) -> DbModel:
        return Exception("not implemented")
    
    def to_entity(self,model:UserFact) -> UserEntityFact:
        return UserEntityFact(model.nombres,model.numero_cedula)
