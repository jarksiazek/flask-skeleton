import json
import logging
from collections import OrderedDict
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
apscheduler: APScheduler = APScheduler()


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        json.dumps(
            OrderedDict(
                [
                    ("@timestamp", "%(asctime)s"),
                    ("logger_name", "slack-bot-app"),
                    ("module_name", "%(module)s"),
                    ("function", "%(funcName)s"),
                    ("pid", "%(process)d"),
                    ("pname", "%(processName)s"),
                    ("level", "%(levelname)s"),
                    ("message", "%(message)s"),
                ]
            )
        ),
        "%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def create_app(config_object) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    return app
