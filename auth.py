import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity
)
from models import User, TokenBlocklist

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=data.get("username"), email=data.get("email"))

    new_user.set_password(password=data.get("password"))

    new_user.save()

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user and (user.check_password(password=data.get("password"))):
        access_token = create_access_token(identity=user.username, fresh=datetime.timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=user.username)

        return (
            jsonify(
                {
                    "message": "User logged in successfully",
                    "username": user.username,
                    "tokens": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid username or password"}), 400


@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_detail": {
                "username": current_user.username,
                "email": current_user.email,
            },
        }
    )


@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity, fresh=False)
    
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']
    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify(
        {
            "new_access_token": new_access_token,
            "msg" : f"{token_type.capitalize()} has been revoked"
        })


@auth_bp.get('/logout')
@jwt_required() 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify(
        {
            "message": "User logged out Successfully",
            "token": token_type.capitalize()
        }
        ) , 200

# Only allow fresh JWTs to access this route with the `fresh=True` arguement.
@auth_bp.get("/protected")
@jwt_required(fresh=True)
def protected():
    return jsonify(
        {
            "message": "Protected Content"
        }
    )