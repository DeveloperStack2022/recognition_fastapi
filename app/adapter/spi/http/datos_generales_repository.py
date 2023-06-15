import typing
from  app.adapter.spi.http.http_connection import HttpConnection
# Application
from app.application.repositories.datos_generales_repository_abstract import DatosGeneralesRepositoryAbstract
from app.application.mappers.http_mapper import HttpMapper
# Entity 
from  app.domain.datos_generales_entity import DatosGeneralesEntity
from app.domain.api_exception import ApiException


class DatosGeneralesRepository(DatosGeneralesRepositoryAbstract):
    def __init__(self,http_connection:HttpConnection,source:str) -> None:
        self.mapper = HttpMapper
        self.source = source
        self.http_connection = http_connection
    
    def get_datos_generales(self) -> DatosGeneralesEntity:
        res = self.http_connection.get('{}/url_r2g3str4_c3v3l')
        if not res.ok:
            raise ApiException('no se encontro informacion')
        res_json = res.json()
        if not res_json:
            raise ApiException('no se encontro data en format json')
        
        return self.mapper.to_entity(res_json)
    
    

