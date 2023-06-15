import requests
from requests import Response
from app.application.spi.http_interface import HttpInterface

class HttpConnection(HttpInterface):
    def __init__(self) -> None:
        pass

    def get(self,url:str,params:None,**kwargs) -> Response:
        return requests.get(url,params,**kwargs)

    def post(self, url: str, params: None, **kwargs) -> Response:
        return requests.post(url, params, **kwargs)