from flask import Response, request, make_response
from flask_restful import Resource
from controller.product import *

PRODUCT_NOT_FOUND = "Product not found."

class Product(Resource):
    @staticmethod
    def get(id=None) -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        response, status = get_product(request, id)
        return make_response(response, status)
    
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_product(request, input_data)
        return make_response(response, status)
    
    def delete(self,id):
        response, status = delete_product(request,id)
        return make_response(response, status)

class ProductList(Resource):
    @staticmethod
    def get() -> Response :
        response, status = get_all_product(request)
        return make_response(response, status)
    
class ProductSearch(Resource):
    @staticmethod
    def get() -> Response:
        """
        GET response method for creating user.

        :return: JSON object
        """
        response, status = search_products(request)
        return make_response(response, status)