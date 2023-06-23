import typing 

from app.application.repositories.datos_generales_repository_abstract import DatosGeneralesRepositoryAbstract
from app.application.usecases.interfaces import UseCaseOneEntity
from app.application.utils.error_handling_utils import ErrorHandlingUtils
from app.domain.datos_generales_entity import DatosGeneralesEntity


class CreateDatosGeneralesUseCase(UseCaseOneEntity):

    def __init__(self,datos:DatosGeneralesEntity, repository:DatosGeneralesRepositoryAbstract) -> None:
        self.repository = repository
        self.datos = datos
    
    def execute(self) -> typing.Dict[DatosGeneralesEntity,any]:
        try:
            return self.repository.create_datos_generales(datos=self.datos)
        except Exception as exception: 
            raise ErrorHandlingUtils.application_error('Can not create datos generalos')