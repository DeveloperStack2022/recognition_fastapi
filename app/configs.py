from starlette.config import Config

config = Config('.env')

API_VERSION = config('API_VERSION', cast=str, default='v0.1')
API_PREFIX = f'/api/{API_VERSION}'

MONGO_HOST = config('MONGO_HOST', cast=str, default='127.0.0.1')
MONGO_PORT = config('MONGO_PORT', cast=str, default='27017')
MONGO_DB_NAME = config("MONGO_DB_NAME", cast=str, default='new_project')

MONGO_USERS_COLLECTION = config("MONGO_USERS_COLLECTION", cast=str, default='users_collection')
MONGO_USER_PERSISTENCIA_COLLECTION = config('MONGO_USER_PERSISTENCIA_COLLECTION',cast=str,default="user_persistencia_collection")
MONGO_USER_DETECT_COLLECTION = config('MONGO_USER_DETECT_COLLECTION',cast=str,default="user_detect")

MONGO_URL = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'
MONGO_TIMEOUT = 1000

SECRET_KEY = config('SECRET_KEY', cast=str, default='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
ALGORITHM = config('ALGORITHM', cast=str, default='HS256')
ACCESS_TOKEN_EXP = config('ACCESS_TOKEN_EXP', cast=int, default=15*1)
REFRESH_TOKEN_EXP = config('REFRESH_TOKEN_EXP', cast=int, default=15*1)

PATH_FILENAME = config('PATH_FILENAME',cast=str,default="Uploads")

CLOUDINARY_CLOUD_NAME = config('CLOUD_NAME',cast=str)
CLOUDINARY_CLOUD_API_KEY = config('CLOUD_API_KEY',cast=str)
CLOUDINARY_API_SECRET = config('CLOUD_API_SECRET',cast=str) 