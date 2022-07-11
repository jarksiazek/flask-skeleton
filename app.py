#!/usr/bin/env python3
import os

from src.web.const import create_app
from src.web.const import create_logger
from src.web.const import db

logger = create_logger(__name__)

app = create_app("src.web.config.Config")
db.init_app(app)

# importing at the end to avoid circular imports issue
from src.web.view import blueprint as view  # noqa

app.register_blueprint(view)  # noqa

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
