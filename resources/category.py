from flask import Response, request, make_response
from flask_restful import Resource

from models.category import CategoryModel
from controller.category import *


CATEGORY_NOT_FOUND = "Category not found."
CATEGORY_ALREADY_EXISTS = "Category '{}' Already exists."

class Category(Resource):   
    @staticmethod    
    def get(id) -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        response, status = get_category(request,id)
        return make_response(response, status)
    
    @staticmethod
    def post() -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_category(request,input_data)
        return make_response(response, status)

    def put(self,id=None):
        response, status = edit_category(request,id)

        return make_response(response, status)
    def delete(self,id):
        response, status = delete_category(request,id)
        return make_response(response, status)


class CategoryList(Resource):
    @staticmethod
    def get() -> Response :
        response, status = get_all_category(request)
        return make_response(response, status)
