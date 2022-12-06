import pytest

import src.tests.test_env # noqa
from src.code.const import create_app
from src.code.db import db


@pytest.fixture()
def db_setup():
    app = create_app("src.tests.config.Config")
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()