from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import JSON

from src.code.logger import create_logger
from src.code.db import db

logger = create_logger(__name__)


class Product(db.Model):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    additional_info = Column(JSON)

    def get_all_products(self) -> "Product":
        return db.session.query(Product).all()
