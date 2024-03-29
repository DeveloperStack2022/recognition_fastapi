# import uvicorn

# from dotenv import load_dotenv
# load_dotenv()


# from starlette.middleware.cors import CORSMiddleware
# from fastapi import (
#     FastAPI,
#     HTTPException
# )

# from .exceptions import http_exception_handler
# from .configs import (API_PREFIX,CLOUDINARY_API_SECRET,CLOUDINARY_CLOUD_API_KEY,CLOUDINARY_CLOUD_NAME)
# from .utils import (
#     startup_handler,
#     shutdown_handler
# )

# from .routes import (
#     HealthRoutes,
#     UserRoutes,
#     AuthRoutes,
#     UserPersistencia,
#     UserDetect,
#     FilesUpload
# )



# app = FastAPI()

# origins = ['*']
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.add_event_handler("startup", startup_handler)
# app.add_event_handler("shutdown", shutdown_handler)

# app.include_router(HealthRoutes, prefix=f'{API_PREFIX}/health')
# app.include_router(UserRoutes, prefix=f'{API_PREFIX}/users')
# app.include_router(AuthRoutes, prefix=f'{API_PREFIX}/oauth')
# app.include_router(UserPersistencia,prefix=f'{API_PREFIX}/userpersistencia')
# app.include_router(UserDetect,prefix=f'{API_PREFIX}/userdetect')
# app.include_router(FilesUpload,prefix=f'{API_PREFIX}/folderUpload')

# app.add_exception_handler(HTTPException, http_exception_handler)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from injector import Injector
import uvicorn 

from app.infrastructure.app import create_app
app = create_app(Injector())

if __name__ == "__main__":
    uvicorn.run('main:app')