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
    cors = CORS(app)
    # app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config.from_prefixed_env()

    # This is the configuration for the email server.
    app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
    app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
    app.config["MAIL_USE_TLS"] = True
    app.config['MAIL_DEBUG'] = True

    mail = Mail(app)

    app.config.from_object("config.Config")

    api = Api(app=app)

    from users.routes import create_authentication_routes

    create_authentication_routes(api=api)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    return app
