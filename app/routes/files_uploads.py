# TODO: Fast APi - Server 
from fastapi import APIRouter,UploadFile,File
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR
import pandas as pd
# TODO: Types - Python 
from typing import List
# TODO: System Operative 
import os 
# TODO: Service - 
from ..services.files_upload_services import FileUploadFilesService
# TODO: Models - 
from ..models.file_upload_models import FileUploadModelLista,BaseDataInputFieldUploadList

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

@router.get('/creatUsersToFolder')
async def createUserToFolder():
    service = FileUploadFilesService()
    path_root = os.getcwd()
    path_dir = os.path.join(path_root,'FilesUpload')
   
    path_dir_list_files = os.listdir(path_dir)
    filename_csv:str = ''
    for file in path_dir_list_files:
        if file.split('.').pop() == 'csv':
            filename_csv = file
    
    path_file_csv = os.path.join(path_dir,filename_csv)
   
    # TODO: Read Pandas
    df = pd.read_csv(path_file_csv,sep=';')
    
    list_data: List = []

    for iterador in range(len(df)):
        # print(df.iloc[iterador]['nombres'])
        # df.iloc[iterador]['nombres'] -> nombres 
        # df.iloc[iterador]['apellidos'] -> apellidos 
        # df.iloc[iterador]['numero cedula'] -> numero cedula
        list_data.append({'numero_cedula':f'''{df.iloc[iterador]['numero cedula']}''','nombres':df.iloc[iterador]['apellidos'] + df.iloc[iterador]['nombres']  })
        
    lista = FileUploadModelLista(users=list_data)
    service.create_user_for_csv(user=lista)

    return JSONResponse(
        status_code=HTTP_200_OK,
        content={
            'success':True,
            'message':'Archivos guardados correctamente.' 
        }
    )
    
@router.get('/createUsersToFolderFields')
async def createUsersToFolderFields():
    service = FileUploadFilesService()
    # TODO: OS - {1. Obtener la ruta principal - 2. Ruta directorio exacto 3.listamos todos los archivos del directorio }
    path_root = os.getcwd()
    path_dir = os.path.join(path_root,'FilesUpload')
    path_dir_list_files = os.listdir(path_dir)

    # FileName del archivo CSV
    filename_csv:str = ''
    for file in path_dir_list_files:
        if file.split('.').pop() == 'csv':
            filename_csv = file
    path_file_csv = os.path.join(path_dir,filename_csv)
    # TODO: Read .csv -> 
    df = pd.read_csv(path_file_csv,encoding='ISO-8859-1',sep=';')
    df = df.drop_duplicates(subset='numero_cedula')

    list_data = []

    for iterador in range(len(df)):
        # print(df.iloc[iterador]['fecha_nacimiento'])
        list_data.append({
            'numero_cedula':df.iloc[iterador]['numero_cedula'],
            'nombres':f'''{df.iloc[iterador]['apellido_1 ']} {df.iloc[iterador]['apellido_2']} {df.iloc[iterador]['nombre_1']} {df.iloc[iterador]['nombre_2']}''',
            'nacionalidad':f'''{df.iloc[iterador]['nacionalidad']}''',
            'lugar_nacimiento':f'''{df.iloc[iterador]['lugar_nacimiento']}''',
            'fecha_nacimiento':f'''{df.iloc[iterador]['fecha_nacimiento']}'''})

    lista = BaseDataInputFieldUploadList(users=list_data)
    
    await service.create_user_for_csv_fields(user=lista)
    
    for f in os.listdir(path_dir):
        os.remove(os.path.join(path_dir,f))

    return JSONResponse(
        status_code=HTTP_200_OK,
        content={
            'success':True,
            'message':'Archivos guardados correctamente.' 
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