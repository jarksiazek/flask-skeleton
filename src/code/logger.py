import json
import logging
from collections import OrderedDict


def create_logger(name: str) -> logging.Logger:
    logger: logging.Logger = logging.Logger(name)
    logger.setLevel("INFO")
    logger.handlers = []
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        json.dumps(
            (
                OrderedDict(
                    [
                        ("@timestamp", "%(asctime)s"),
                        ("logger_name", "flask-skeleton"),
                        ("module_name", "%(module)s"),
                        ("function", "%(funcName)s"),
                        ("pid", "%(processName)s"),
                        ("pname", "%(levelname)s"),
                        ("message", "%(message)s"),
                    ]
                )
            )
        ),
        "%Y-%m-%dT%H:%M:%S%z"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
