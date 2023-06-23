import os 
from injector import Injector,SingletonScope
from fastapi_injector import attach_injector
from fastapi import FastAPI

#Controllers  
from app.adapter.api.datos_generales_fact import datos_generales_fact_controller as datosGeneralesController

# 
from app.domain.configuration_entity import ConfigurationEntity
from .configuration_mapper import ConfigurationMapper
from app.adapter.spi.db.db_connection import DbConnection
from app.adapter.spi.http.http_connection import HttpConnection
from app.adapter.spi.respositroy_factory import RepositoryFactory

config: ConfigurationEntity = ConfigurationMapper(os.getenv('.env')).get_config()
db_connection: DbConnection = DbConnection(config=config)
http_connection:HttpConnection = HttpConnection()

repository_factory =  RepositoryFactory(config=config,db_connection=db_connection,http_connection=http_connection)

def create_app(injector:Injector) -> FastAPI:
    app:FastAPI = FastAPI()

    app.include_router(datosGeneralesController.router,prefix='/api/v2/datosGenerales',tags=['DatosGenerales'])

    injector.binder.bind(RepositoryFactory,to=repository_factory,scope=SingletonScope)

    attach_injector(app,injector)
    return app