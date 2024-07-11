from flask import Response, request, make_response
from flask_restful import Resource
from controller.product import get_product, create_product, get_all_product

PRODUCT_NOT_FOUND = "Product not found."

class Product(Resource):
    @staticmethod
    def get() -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = get_product(request, input_data)
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


class ProductList(Resource):
    @staticmethod
    def get() -> Response :
        response, status = get_all_product(request)
        return make_response(response, status)