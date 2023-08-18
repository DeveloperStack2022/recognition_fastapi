from abc import abstractmethod,ABC
import typing
from app.domain.datos_generales_entity import DatosGeneralesEntity

class DatosGeneralesRepositoryAbstract(ABC):
    @abstractmethod
    def get_datos_generales(self) -> typing.List[DatosGeneralesEntity]:
        """Get data de R2g3tr4 C3v3l"""
    
    @abstractmethod
    def create_datos_generales(self,datos:DatosGeneralesEntity) -> typing.Dict[DatosGeneralesEntity,any]:
        '''Create a datos generales'''