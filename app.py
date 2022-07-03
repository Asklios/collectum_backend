import json

from flask import Flask, Blueprint

from backend.settings import *
from backend.api import api
from backend.public_endpoints import namespace as public_namespace
from backend.private_endpoints import namespace as private_namespace

app = Flask(__name__)

app.config['SERVER_NAME'] = SERVER_NAME
app.config['SWAGGER_UI_DOC_EXPANSION'] = RESTPLUS_SWAGGER_EXPANSION
app.config['RESTPLUS_VALIDATE'] = RESTPLUS_VAL
app.config['RESTPLUS_MASK_SWAGGER'] = RESTPLUS_MASK_SWAGGER

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api.init_app(blueprint)
api.add_namespace(public_namespace)
api.add_namespace(private_namespace)
app.register_blueprint(blueprint)


if __name__ == '__main__':
    if EXPORT_SWAGGER_FILE:
        with app.app_context():
            print(json.dumps(api.__schema__))
            exit()
    app.run()

application = app
