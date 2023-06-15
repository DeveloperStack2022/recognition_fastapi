# Domain Layer 
from app.domain.datos_generales_entity import DatosGeneralesEntity
# Adapter Layer 
from app.application.mappers.db_mapper import DbMapper,DbModel

from typing import Any

class DatosGeneralesMapper(DbMapper):

    def to_db(self, entity: DatosGeneralesEntity) -> DbModel:
        raise Exception('Not implemented')
    
    def to_entity(self, model: Any) -> DatosGeneralesEntity:
        return DatosGeneralesEntity(model)