from models.category import CategoryModel
from validation import CategoryInputSchema
from utils.http_code import *
from utils.common import generate_response
from server import db, jwt

from flask_jwt_extended import (
    jwt_required,
    get_jwt,
)

def create_category(request, input_data):
    """
    It add a new category

    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    create_validation_schema = CategoryInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_category_exists = CategoryModel.find_by_category_name(category_name=input_data.get("category_name"))
    if check_category_exists:
        return generate_response(
            message="Category already exists", status=HTTP_400_BAD_REQUEST
        )
    
    new_category = CategoryModel(**input_data)
    db.session.add(new_category)  # Adds new User record to database
    db.session.commit()  # Comment
    return generate_response(
        data=input_data, message="Category added Successfully", status=HTTP_201_CREATED
    )

def get_category(request,id):
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response

    :param : None
    :return: A dictionary with the keys: data, message, status
    """
    category = CategoryModel.find_by_id(id)
    if category:
        return generate_response(
        data=category.json(), message="Category", status=HTTP_200_OK
        )
    return generate_response(
        message="Category not availabe", status=HTTP_200_OK
        )

@jwt_required(verify_type=False)
def edit_category(request,id=None):
    """
    It takes in a request and input data, validates the input data, checks if the category exists, 
    and updates the category details if the category is found.
    
    :param id: category ID
    :return: A dictionary with the keys: data, message, status
    """
    if not id:
        return generate_response(
            data=None, message="Category ID must be provided", status=HTTP_400_BAD_REQUEST
        )

    category = CategoryModel.query.get(id)
    if not category:
        return generate_response(
            data=None, message="Category not found", status=HTTP_404_NOT_FOUND
        )

    # Get input data from request
    data = request.get_json()
    if not data:
        return generate_response(
            data=None, message="No input data provided", status=HTTP_400_BAD_REQUEST
        )

    # Update category details
    try:
        category.category_name = data.get('category_name', category.category_name)

        # Save updated category to database
        db.session.commit()

        return generate_response(
            data=category.json(), message="Category updated successfully", status=HTTP_200_OK
        )
    except Exception as e:
        db.session.rollback()
        return generate_response(
            data=None, message=str(e), status=HTTP_500_INTERNAL_SERVER_ERROR
        )

def get_all_category(request):
        
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=3, type=int)
    categories = CategoryModel.query.paginate(page=page, per_page=per_page)
    result = CategoryInputSchema().dump(categories, many=True)
    return generate_response(
    data=result, message="List of category", status=HTTP_200_OK
    )


@jwt_required()
def delete_category(request,id):
    claims = get_jwt()
    if claims.get("is_staff") != True:
        return generate_response(
            message="You are not authorized to delete this category",
            status=HTTP_400_BAD_REQUEST
        )
    
    category = CategoryModel.find_by_id(id)
    if not category:
        return generate_response(
            message="Category Not found",
            status=HTTP_400_BAD_REQUEST
        )

    try:
        category.delete_from_db()
        return generate_response(
            message="Category Deleted Successfully",
            status=HTTP_200_OK
        )
    except Exception as e:
        return generate_response(
            message="Can't Delete Category at the moment",
            status=HTTP_400_BAD_REQUEST
        )