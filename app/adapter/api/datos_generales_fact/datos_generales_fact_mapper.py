from typing import Any
from app.adapter.api.datos_generales_fact.datos_generales_fact_presenters import DatosGeneralesFactPresenters
from app.application.mappers.api_mapper import ApiMapper
from app.domain.datos_generales_entity import DatosGeneralesEntity

class DatosGeneralesFactPresenterMapper(ApiMapper):

    def to_api(self, entity: DatosGeneralesEntity) -> DatosGeneralesFactPresenters:
        return DatosGeneralesFactPresenters(numero_cedula=entity.identificacion)
    
    def to_entity(self, payload: Any) -> DatosGeneralesEntity:
        raise Exception('Not Implemented')