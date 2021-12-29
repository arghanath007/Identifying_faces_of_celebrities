from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage

class ImageClassificationDto:
    api=Namespace('Face Detection', description='Upload Image')
    image_upload=api.parser()
    image_upload.add_argument('image', type=FileStorage, location='files')