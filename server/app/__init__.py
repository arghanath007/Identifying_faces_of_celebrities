from os import path
from flask_restx import Api
from flask import Blueprint

from app.main.config import authorizations, version

blueprint=Blueprint('api', __name__)

api=Api(blueprint, title='Image Classification Project', version='1.0', description='Detecting or identifying the faces of celebrities such as Virat Kohli, Lionel Messi, Maria Sahapora, Serena Williams, Roger Federer', authorizations=authorizations)

from app.main.controller.image_classification_controller import api as image_clf_ns

api.add_namespace(image_clf_ns,path='/face')