from typing import Any
from app.adapter.api.datos_generales_fact.datos_generales_fact_presenters import DatosGeneralesFactPresenters
from app.application.mappers.api_mapper import ApiMapper
from app.domain.datos_generales_entity import DatosGeneralesEntity

class DatosGeneralesFactPresenterMapper(ApiMapper):

    def to_api(self, entity: DatosGeneralesEntity) -> DatosGeneralesFactPresenters:
        return DatosGeneralesFactPresenters(
            numero_cedula=entity.numero_cedula,
            nacionalidad=entity.nacionalidad,
            nombres=entity.nombres,
            condicion_cedulado=entity.condicion_cedulado,
            disabled=entity.disabled,
            lugar_ins_nacimiento=entity.lugar_ins_nacimiento
            )
    
    def to_entity(self, payload: Any) -> DatosGeneralesEntity:
        raise Exception('Not Implemented')