import logging
import typing 
from fastapi import APIRouter
from fastapi_injector import Injected

# 
from app.adapter.spi.respositroy_factory import RepositoryFactory
from app.adapter.api.datos_generales_fact.datos_generales_fact_mapper import DatosGeneralesFactPresenterMapper
from app.application.usecases.get_all_datosGenerales_usecase import GetAllDatosGeneralesUseCase
from app.application.usecases.create_datosGenerales_usecase import CreateDatosGeneralesUseCase
from app.adapter.api.datos_generales_fact.datos_generales_fact_presenters import DatosGeneralesFactPresenters
from app.adapter.api.shared.api_erro_handling import ApiErrorHandling
from app.schemas.pydantic.create_datos_generales import DatosGeneralesPostRequest

router = APIRouter()

@router.get('/')
async def get_all_datosGenerales(factory:RepositoryFactory = Injected(RepositoryFactory)):
    try:
        datosGenerales_fact_repository: RepositoryFactory = factory.get_repository("users_collection")
        datosGenerales_fact_mapper:DatosGeneralesFactPresenterMapper = DatosGeneralesFactPresenterMapper()
        get_all_datosGenerales_fact_usecase:GetAllDatosGeneralesUseCase = GetAllDatosGeneralesUseCase(datosGenerales_fact_repository)
        datos_generales_facts = get_all_datosGenerales_fact_usecase.execute()
        
        facts:typing.List[DatosGeneralesFactPresenterMapper] = [] 
        for data in datos_generales_facts:
            facts.append(datosGenerales_fact_mapper.to_api(data))

        return facts        
    except  Exception as exception:
        raise ApiErrorHandling.http_error("Unexpected error getting all DatosGenerales fact",exception)  

@router.post('/create')
async def create_datosGenerales(datos:DatosGeneralesPostRequest,factory:RepositoryFactory = Injected(RepositoryFactory)):
    try:
        
        datosGenerales_fact_repository:RepositoryFactory = factory.get_repository('create_datos_generales')
        # datosGenerales_fact_mapper: DatosGeneralesFactPresenterMapper = DatosGeneralesFactPresenterMapper()
        print('Estas aqui 1')
        create_datosGeerales_fact_usecase: CreateDatosGeneralesUseCase = CreateDatosGeneralesUseCase(datos=datos,repository=datosGenerales_fact_repository)
        print('Estas aqui 2')
        datos_generales_facts = create_datosGeerales_fact_usecase.execute()
        print('Estas aqui 3')
        
        
    except Exception as exception:
        raise ApiErrorHandling.http_error("Unexpected error getting all DatosGenerales fact",exception)