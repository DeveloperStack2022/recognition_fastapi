from abc import ABC,abstractclassmethod
from typing import Generic,TypeVar

HttpResponse = TypeVar('HttpResponse')

class HttpInterface(ABC,Generic[HttpResponse]):
    @abstractclassmethod
    def get(self,url:str,params:None,**kwargs) -> HttpResponse:
        """Execute an Http get request"""
    
    def post(self,url:str,params:None,**kwargs) -> HttpResponse:
        """Execute an Http Post Request"""