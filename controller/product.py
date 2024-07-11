from models.product import ProductModel
from users.validation import ProductInputSchema
from utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_201_CREATED, HTTP_404_NOT_FOUND
from utils.common import generate_response
from server import db


def create_product(request, input_data):
    """
    It add a new product

    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
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