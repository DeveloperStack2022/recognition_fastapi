import os 
from fastapi import FastAPI
from injector import Injector,SingletonScope
from fastapi_injector import attach_injector

from src.domain.configuration_entity import ConfigurationEntity

from src.infrastructure.config_mapper import ConfigurationMapper

from src.adapter.api.user_fact import user_controllers as user_facts_controller
from src.adapter.spi.db.db_connection import DbConnection
from src.adapter.spi.http.http_connection import HttpConnection
from src.adapter.spi.repositories_factory import RepositoriesFactory


config: ConfigurationEntity = ConfigurationMapper(os.getenv("ENV","dev")).get_config()
db_connection: DbConnection = DbConnection(config)
http_connection: HttpConnection = HttpConnection()
repositories_factory = RepositoriesFactory(config,db_connection,http_connection)

def create_app(injector:Injector) -> FastAPI:
    app:FastAPI = FastAPI()

    app.include_router(user_facts_controller.router,prefix="/api/v1/users",tags=["users"])

    injector.binder.bind(RepositoriesFactory,to=repositories_factory,scope=SingletonScope)
    attach_injector(app,injector)
    return app
