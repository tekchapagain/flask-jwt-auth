from models.product import ProductModel
from validation import ProductInputSchema
from utils.http_code import *
from utils.common import generate_response
from server import db
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
)

@jwt_required(verify_type=False)
def create_product(request, input_data):
    """
    It add a new product

    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    claims = get_jwt()
    if claims.get("is_staff") != True:
        return generate_response(
            message="Authorization needed",
            status=HTTP_400_BAD_REQUEST
        )
    create_validation_schema = ProductInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    # check_email_exist = User.get_user_by_email(email=input_data.get("email"))
    # if check_product_exists:
    #     return generate_response(
    #         message="Product already exi", status=HTTP_400_BAD_REQUEST
    #     )
    
    new_product = ProductModel(**input_data)
    db.session.add(new_product)  # Adds new User record to database
    db.session.commit()  # Comment
    return generate_response(
        data=input_data, message="Product added Successfully", status=HTTP_201_CREATED
    )

@jwt_required(verify_type=False)
def edit_product(request,id=None):
    """
    It takes in a request and input data, validates the input data, checks if the product exists, 
    and updates the product details if the product is found.
    
    :param id: Product ID
    :return: A dictionary with the keys: data, message, status
    """
    if not id:
        return generate_response(
            data=None, message="Product ID must be provided", status=HTTP_400_BAD_REQUEST
        )

    product = ProductModel.query.get(id)
    if not product:
        return generate_response(
            data=None, message="Product not found", status=HTTP_404_NOT_FOUND
        )

    # Get input data from request
    data = request.get_json()
    if not data:
        return generate_response(
            data=None, message="No input data provided", status=HTTP_400_BAD_REQUEST
        )

    # Update product details
    try:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.category_id = data.get('category_id', product.category_id)

        # Save updated product to database
        db.session.commit()

        return generate_response(
            data=product.json(), message="Product updated successfully", status=HTTP_200_OK
        )
    except Exception as e:
        db.session.rollback()
        return generate_response(
            data=None, message=str(e), status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    

def get_product(request, id=None):
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response

    :param : None
    :return: A dictionary with the keys: data, message, status
    """
    if id:
        product = ProductModel.query.get(id)
    else:
        return generate_response(
            data=None, message="Product ID must be provided", status=HTTP_400_BAD_REQUEST
        )

    if product:
        return generate_response(
            data=product.json(), message="Product found", status=HTTP_200_OK
        )
    else:
        return generate_response(
            data=None, message="Product not found", status=HTTP_404_NOT_FOUND
        )



def get_all_product(request):
        
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=3, type=int)
    products = ProductModel.query.paginate(page=page, per_page=per_page)
    result = ProductInputSchema().dump(products, many=True)
    return generate_response(
    result, status=HTTP_200_OK
    )

def search_products(request):
    """
    Search for products based on query parameters such as name and category.

    Query Parameters:
    - name (str): The name or part of the name of the product to search for.
    - category (str): The category or part of the category of the product to search for.

    Returns:
    - A JSON response with the search results and HTTP status code 200.
    """
    # Get search parameters
    search_name = request.args.get("term", type=str)
    
    # Build the base query
    query = ProductModel.query
    
    # Apply search filters
    if search_name:
        query = query.filter(ProductModel.name.ilike(f"%{search_name}%"))

    # Execute the query
    products = query.all()

    # Serialize the results
    result = ProductInputSchema(many=True).dump(products)

    # Generate the response
    return generate_response(result, status=HTTP_200_OK)

@jwt_required(verify_type=False)
def delete_product(request, id):
    claims = get_jwt()
    if claims.get("is_staff") != True:
        return generate_response(
            message="You are not authorized to delete this product",
            status=HTTP_400_BAD_REQUEST
        )

    product = ProductModel.find_by_id(id)
    if not product:
        return generate_response(
            message="Product Not found",
            status=HTTP_400_BAD_REQUEST
        )

    try:
        product.delete_from_db()
        return generate_response(
            message="Product Deleted Successfully",
            status=HTTP_200_OK
        )
    except Exception as e:
        return generate_response(
            message=e.message,
            status=HTTP_404_NOT_FOUND
        )