from app import blueprint
from app.main import create_app

app=create_app('dev')
app.register_blueprint(blueprint)

app.app_context().push()
