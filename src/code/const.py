from typing import Union
from flask import Flask


def create_app(config_object: Union[object, str]) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_object)
    return app
