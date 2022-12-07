from typing import Union
from flask import Flask
from flask_restx import Api
from flask import Blueprint

swagger: Blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api: Api = Api(
    swagger,
    version="0.1",
    title="api",
    doc="/swagger/"
)


def create_app(config_object: Union[object, str]) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_object)
    app.static_folder = "src/code/templates"
    app.template_folder = "src/code/templates"
    return app
