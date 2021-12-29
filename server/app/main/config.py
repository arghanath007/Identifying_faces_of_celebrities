import os
from flask_uploads import UploadSet, IMAGES
import cv2

face_cascade= cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

basedir=os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER='./app/main/files'
UPLOADED_PHOTOS_DEST='./app/main/files'
MAX_CONTENT_LENGTH=5*1024*1024

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY', 'VERY_VERY_SECRET_KEY')
    DEBUG=False
    UPLOAD_FOLDER=UPLOAD_FOLDER
    UPLOADED_PHOTOS_DEST=UPLOADED_PHOTOS_DEST
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH

class DevelopmentConfig(Config):
    DEBUG=True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(Config):
    DEBUG = False

image_name_size = 100

configs_by_name=dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key=Config.SECRET_KEY

authorizations={
    'apikey':{
        'type': 'apikey',
        'in': 'header',
        'name': 'Authorization'
    }
}

def version(path,version=1):
    return f"/v{version}/{path}"

photos=UploadSet('photos',IMAGES)   