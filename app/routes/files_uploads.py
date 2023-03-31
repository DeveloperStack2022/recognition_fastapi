# TODO: Fast APi - Server 
from fastapi import APIRouter,UploadFile,File
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR
# TODO: Types - Python 
from typing import List
# TODO: System Operative 
import os 

#  ----- 
path_save = os.path.join(os.getcwd(),'FilesUpload')

router = APIRouter()



@router.post('/folderUpload')
async def UploadFolder(file: UploadFile = File(...)):
    if os.path.exists(path_save) == False:
        os.makedirs(path_save)

    try:
        file.filename = f'{file.filename}'.split('/').pop()
        with open(f'{path_save}/{file.filename}','wb') as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()
        # for file in files:
        #     print(file.filename)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success':True,
                'message':'Archivos guardados correctamente.' 
            }
        )
    except FileNotFoundError as err: 
        print(err)
        print('Error upload server')
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'success':False,
                'message':'Error interno en el servidor'
            }
        )

@router.post('/folderUploads')
async def UploadFolder(files: List[UploadFile] = File(...)):
    if os.path.exists(path_save) == False:
        os.makedirs(path_save)

    try:
        for file in files:
            file.filename = f'{file.filename}'.split('/').pop()
            with open(f'{path_save}/{file.filename}','wb') as myfile:
                content = await file.read()
                myfile.write(content)
                myfile.close()
        #     print(file.filename)
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                'success':True,
                'message':'Archivos guardados correctamente.' 
            }
        )
    except FileNotFoundError as err: 
        print(err)
        print('Error upload server')
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'success':False,
                'message':'Error interno en el servidor'
            }
        )