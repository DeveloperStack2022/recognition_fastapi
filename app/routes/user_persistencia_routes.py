import os 
from fastapi import APIRouter,File,UploadFile,Form
from ..models import (UserPersistencia)
from ..services import UserPersistenciaService
from fastapi.responses import JSONResponse
from ..utils import allowed_file,createDir
from werkzeug.utils import secure_filename


router = APIRouter()


@router.post('/addImage')
async def addUserPersistencia(num_cedula:str = Form(...),nombres: str = Form(...),apellidos:str = Form(...),image: UploadFile = File(...)):
    services = UserPersistenciaService()
   
    if not os.path.exists(os.getcwd() + "/Uploads"):
        os.mkdir("Uploads")
    path_dir = os.getcwd() + "/Uploads"
    file_name,file_extension = os.path.splitext(image.filename)
    image.filename = str(num_cedula) + file_extension

    with open(os.path.join(path_dir,image.filename),'wb') as myfile:
        content = await image.read() 
        myfile.write(content)
        myfile.close()
    
    images:list[str] = []
    images.append(str(image.filename))
    user:UserPersistencia = UserPersistencia(numero_cedula=num_cedula,nombres=nombres,apellidos=apellidos,images_id=images)
    return await services.create_new_user_persistencia(user)
 
@router.get('/get_users')
async def getUsersPersistencia():
    services = UserPersistenciaService()
    return await services.get_users_persistencia()