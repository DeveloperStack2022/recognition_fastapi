from typing import Callable,Optional
from starlette.requests import Request
from fastapi.routing import APIRoute


def get_route_name() -> Optional[str]:                                                                                                                                                       
    return _route_name_ctx_var.get() 

class VerifyTokenRoute(APIRoute):
    def get_route_handle(self) -> Callable:
        original_route_handler = super().get_route_handler()                                                                                                                                 
        route_name = self.name                      

        async def verify_token_middleware(request:Request):
            token = request.headers['Authorization'].split(" ")[1]
            print("Token")
            print(token)
        return verify_token_middleware   