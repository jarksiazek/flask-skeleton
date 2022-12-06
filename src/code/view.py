from flask import Blueprint

from src.code.logger import create_logger

logger = create_logger(__name__)

blueprint: Blueprint = Blueprint("flask-skeleton", __name__)


@blueprint.route("/")
def home():
    return "works"
