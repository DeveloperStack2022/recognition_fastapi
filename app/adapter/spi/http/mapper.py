from  typing  import Any
# Application
from app.application.mappers.http_mapper import HttpMapper
# Entity
from app.domain.datos_generales_entity import DatosGeneralesEntity
class DatosGeneralesHttpMapper(HttpMapper):

    def to_http(self,entity:DatosGeneralesEntity) -> Any:
        raise Exception('Not implement')
    
    def to_entity(self,http_obj:Any) -> DatosGeneralesEntity:
        return DatosGeneralesEntity(http_obj[''],http_obj[''])