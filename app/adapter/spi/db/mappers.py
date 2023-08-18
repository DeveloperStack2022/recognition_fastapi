# Domain Layer 
from app.domain.datos_generales_entity import DatosGeneralesEntity
# Adapter Layer 
from app.application.mappers.db_mapper import DbMapper,DbModel

from typing import Any,List

class DatosGeneralesMapper(DbMapper):

    def to_db(self, entity: DatosGeneralesEntity) -> DbModel:
        raise Exception('Not implemented')
    
    def to_entity(self, model:DatosGeneralesEntity ) -> DatosGeneralesEntity:
        return DatosGeneralesEntity(numero_cedula=model['numero_cedula'],condicion_cedulado=model['condicion_cedulado'],disabled=model['disabled'],lugar_ins_nacimiento=model['lugar_ins_nacimiento'],nacionalidad=model['nacionalidad'],nombres=model['nombres'])