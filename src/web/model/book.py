from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.web.const import create_logger
from src.web.const import db

logger = create_logger(__name__)


class Books(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    author_id = Column(String(64), nullable=False)
