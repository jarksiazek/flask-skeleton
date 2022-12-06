from src.code.db import db
from src.code.model.product import Product


class TestIntegrationProduct:
    def test_get_all(self, db_setup):
        Product().get_all_products()
