from flask import Response, request, make_response
from flask_restful import Resource

from models.category import CategoryModel
from controller.category import create_category,get_category, get_all_category


CATEGORY_NOT_FOUND = "Category not found."
CATEGORY_ALREADY_EXISTS = "Category '{}' Already exists."

class Category(Resource):
    @staticmethod    
    def get() -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = get_category(request,input_data)
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


    def delete(self, id):
        category_date = CategoryModel.find_by_id(id)
        if category_date:
            category_date.delete_from_db()
            return {'message': "Category Deleted successfully"}, 200
        return {'message': CATEGORY_NOT_FOUND}, 404


class CategoryList(Resource):
    @staticmethod
    def get() -> Response :
        response, status = get_all_category(request)
        return make_response(response, status)
