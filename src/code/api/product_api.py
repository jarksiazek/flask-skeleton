from flask_restx import Namespace
from flask_restx import Resource

from src.code.model.product import Product
ns = Namespace("product", description="Product api")

product = ns.model(
    "Product", {  }
)

@ns.route("/")
class Products(Resource):
    @ns.doc(description="Get products")
    @ns.marshal_with(product, as_list=True)
    @ns.response(code=200, description="List of products")
    @ns.response(code=500, description="Internal server error")
    def get(self):
        return Product().get_all_products()
    