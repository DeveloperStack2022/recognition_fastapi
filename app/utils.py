import os
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK
from .db import open_db_connection, close_db_connection
from .configs import PATH_FILENAME

async def build_response(status_code=HTTP_200_OK, **kwargs):
    payload = kwargs.get('data', None)
    detail = kwargs.get('msg', None)

    if bool(payload):
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'payload': payload
            }
        )
    elif bool(detail):
       return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'detail': detail
            }
        ) 

def startup_handler():
    open_db_connection()

def shutdown_handler():
    close_db_connection()

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg','png'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createDir(nameDir:str) -> str:
    path = os.getcwd()
    FOLDER = os.path(path,str(nameDir))
    print(FOLDER)
    if not os.path.isdir(FOLDER):
        os.makedirs(str(nameDir))
    return FOLDER
