import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_access_cookies,
    get_jwt,
    current_user,
    get_jwt_identity
)
from server import db, jwt
from users.helper import send_forgot_password_email
from users.models import User, TokenBlocklist
from utils.common import generate_response, TokenGenerator
from users.validation import (
    CreateLoginInputSchema,
    CreateResetPasswordEmailSendInputSchema,
    CreateSignupInputSchema, ResetPasswordInputSchema,
)
from utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR


 # load user
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()

# additional claims
@jwt.additional_claims_loader
def make_additional_claims(identity):
    if identity == "admin":
        return {"is_staff": True}
    return {"is_staff": False}

# jwt error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
        return generate_response(
            message="Token is already expired", status=HTTP_401_UNAUTHORIZED
        )

@jwt.invalid_token_loader
def invalid_token_callback(error):
        return generate_response(
            message="Provided token is invalid", status=HTTP_401_UNAUTHORIZED
        )
@jwt.unauthorized_loader
def missing_token_callback(error):
        return generate_response(
            message="Missing Token", status=HTTP_401_UNAUTHORIZED
        )

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header,jwt_data):
    jti = jwt_data['jti']
    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
    return token is not None

def create_user(request, input_data):
    """
    It creates a new user

    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    create_validation_schema = CreateSignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_username_exist = User.get_user_by_username(username=input_data.get("username"))
    check_email_exist = User.get_user_by_email(email=input_data.get("email"))
    if check_username_exist:
        return generate_response(
            message="Username already exist", status=HTTP_400_BAD_REQUEST
        )
    elif check_email_exist:
        return generate_response(
            message="Email already taken", status=HTTP_400_BAD_REQUEST
        )

    new_user = User(**input_data)  # Create an instance of the User class
    new_user.set_password(password=input_data.get("password"))
    db.session.add(new_user)  # Adds new User record to database
    db.session.commit()  # Comment
    del input_data["password"]
    return generate_response(
        data=input_data, message="User Created Successfully", status=HTTP_201_CREATED
    )


def login_user(request, input_data):
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response

    :param request: The request object
    :param input_data: The data that is passed to the function
    :return: A dictionary with the keys: data, message, status
    """
    create_validation_schema = CreateLoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    user = User.query.filter_by(email=input_data.get("email")).first()
    if user is None:
        return generate_response(message="User not found", status=HTTP_400_BAD_REQUEST)
    if user.check_password(input_data.get("password")):
        access_token = create_access_token(identity=user.username, fresh=datetime.timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=user.username)
        input_data["token"] = {"access": access_token, "refresh": refresh_token}
        del input_data["password"]
        # response = jsonify({"msg": "login successful"})
        # set_access_cookies(response, access_token)
        return generate_response(
            data=input_data, message="User logged in successfully", status=HTTP_201_CREATED
        )
    else:
        return generate_response(
            message="Incorrect username or password", status=HTTP_400_BAD_REQUEST
        )

@jwt_required()
def whoami():
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response

    :param : None
    :return: A dictionary with the keys: data, message, status
    """
    input_data = {"username" : current_user.username}
    return generate_response(
        data=input_data, message="User Identity", status=HTTP_201_CREATED
    )

@jwt_required(refresh=True)
def refresh_access():
    """
    It takes in a refresh token and invalidates it,
    and returns new access and refresh token

    :param : None
    :return: A dictionary with the keys: data, message, status
    """
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity, fresh=False)
    new_refresh_token =create_refresh_token(identity=identity)
    
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']
    token_b = TokenBlocklist(jti=jti)

    token_b.save()
    send_data = {
                   "new_access_token": new_access_token,
                   "new_refresh_token": new_refresh_token,
                   "revoked token": f"{token_type.capitalize()}"
                }
    return generate_response(
        data=send_data, message="Provided new access and refresh token", status=HTTP_201_CREATED
    )

@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']

    token_b = TokenBlocklist(jti=jti)

    token_b.save()
    return generate_response(
         message="User logged out successfully", status=HTTP_200_OK
    )

def reset_password_email_send(request, input_data):
    """
    It takes an email address as input, checks if the email address is registered in the database, and
    if it is, sends a password reset email to that address

    :param request: The request object
    :param input_data: The data that is passed to the function
    :return: A response object with a message and status code.
    """
    create_validation_schema = CreateResetPasswordEmailSendInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    user = User.get_user_by_email(email=input_data.get("email"))
    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    
    token = send_forgot_password_email(request, user)
    
    if token is None:
        return generate_response(
        data = input_data, message="Couldnot send email mail server error.", status=HTTP_500_INTERNAL_SERVER_ERROR
    )
    input_data['token'] = token
    return generate_response(
        data = input_data, message="Link sent to the registered email address.", status=HTTP_200_OK
    )


def reset_password(request, input_data, token):
    create_validation_schema = ResetPasswordInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    if not token:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )
    email = TokenGenerator.check_token(token)
    user = User.get_user_by_email(email=email)
    if user is None:
        return generate_response(
            message="The link has already expired",
            status=HTTP_400_BAD_REQUEST,
        )
    print(user)
    user.set_password(input_data.get("password"))
    db.session.commit()
    return generate_response(
        message="Password changed successfully", status=HTTP_200_OK
    )

@jwt_required(fresh=True)
def reset_email(request, input_data):
    username = get_jwt_identity()
    create_validation_schema = CreateResetPasswordEmailSendInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    user= User.get_user_by_username(username=username)

    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    email = input_data.get("email")
    check_email_exist = User.get_user_by_email(email=email)
    if check_email_exist:
        return generate_response(
            message="Email already exists", status=HTTP_400_BAD_REQUEST
        )
    
    user.email = email
    db.session.commit()
    return generate_response(
        data = email ,message="New email updated successfully", status=HTTP_200_OK
    )


@jwt_required()
def get_all_users(request):
    claims = get_jwt()

    if claims.get("is_staff") == True:
        page = request.args.get("page", default=1, type=int)

        per_page = request.args.get("per_page", default=3, type=int)

        users = User.query.paginate(page=page, per_page=per_page)

        result = CreateSignupInputSchema().dump(users, many=True)

        return generate_response(
        result, status=HTTP_200_OK
        )

    return generate_response(
        message="You are not authorized to view this", status=HTTP_401_UNAUTHORIZED
    )