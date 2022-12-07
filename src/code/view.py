from flask import Blueprint
from flask import render_template
from src.code.logger import create_logger

logger = create_logger(__name__)

blueprint: Blueprint = Blueprint("flask-skeleton", __name__)


@blueprint.route("/")
def home():
    return render_template("base_page.html")
