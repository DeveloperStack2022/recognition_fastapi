import typing

from app.application.repositories.datos_generales_repository_abstract import DatosGeneralesRepositoryAbstract
from app.application.usecases.interfaces import UseCaseMultipleEntities
from app.application.utils.error_handling_utils import ErrorHandlingUtils

from app.domain.datos_generales_entity import DatosGeneralesEntity

class GetAllDatosGeneralesUseCase(UseCaseMultipleEntities):
    def __init__(self,repository:DatosGeneralesRepositoryAbstract) -> None:
        self.repository = repository

    def execute(self) -> typing.Iterable[DatosGeneralesEntity]:
        try:
            return self.repository.get_datos_generales()
        except Exception as exception:
            raise ErrorHandlingUtils.application_error('Cannot get all datos generales de R2g3str4 C3v3l')

    