"""App entry point."""
"""Initialize Flask app."""
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, set_access_cookies

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    cors =CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config.from_prefixed_env()

    # This is the configuration for the email server.
    app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
    app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

    mail = Mail(app)

    app.config.from_object("config.Config")

    api = Api(app=app)

    from users.routes import create_authentication_routes

    create_authentication_routes(api=api)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    # # load user
    # @jwt.user_lookup_loader
    # def user_lookup_callback(_jwt_headers, jwt_data):
    #     identity = jwt_data["sub"]

    #     return User.query.filter_by(username=identity).one_or_none()

    # # additional claims

    # @jwt.additional_claims_loader
    # def make_additional_claims(identity):
    #     if identity == "admin":
    #         return {"is_staff": True}
    #     return {"is_staff": False}

    # # jwt error handlers

    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_data):
    #     return jsonify({"message": "Token has expired.", "error": "token_expired"}), 401

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (
    #         jsonify(
    #             {"message": "Signature verification failed.", "error": "invalid_token"}
    #         ),
    #         401,
    #     )

    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return (
    #         jsonify(
    #             {
    #                 "message": "Request doesnt contain valid token",
    #                 "error": "token_not_valid",
    #             }
    #         ),
    #         401,
    #     )
    
    # @jwt.token_in_blocklist_loader
    # def token_in_blocklist_callback(jwt_header,jwt_data):
    #     jti = jwt_data['jti']

    #     token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

    #     return token is not None
    return app
