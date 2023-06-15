from abc import abstractclassmethod,ABC
import typing
from app.domain.datos_generales_entity import DatosGeneralesEntity

class DatosGeneralesRepositoryAbstract(ABC):
    @abstractclassmethod
    def get_datos_generales(self) -> DatosGeneralesEntity:
        """Get data de R2g3tr4 C3v3l"""
    