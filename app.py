#!/usr/bin/env python3
import os
from src.code.logger import create_logger
from src.code.const import create_app
from src.code.db import db
from src.code.const import swagger

logger = create_logger(__name__)

app = create_app("src.code.config.Config")
# db.init_app(app)

# importing at the end to avoid circular imports issue
from src.code.view import blueprint as view  # noqa

app.register_blueprint(view)  # noqa

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
