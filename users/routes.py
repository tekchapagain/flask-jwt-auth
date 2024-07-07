from flask_restful import Api
from users.views import *


def create_authentication_routes(api: Api):
    """Adds resources to the api.
    :param api: Flask-RESTful Api Object
    """
    api.add_resource(SignUpApi, "/api/auth/register")
    api.add_resource(LoginApi, "/api/auth/login")
    api.add_resource(WhoAmI, "/api/auth/whoami")
    api.add_resource(RefreshApi, "/api/auth/refresh")
    api.add_resource(LogoutApi, "/api/auth/logout")
    api.add_resource(ForgotPassword, "/api/auth/forgot")
    api.add_resource(ResetPassword, "/api/auth/reset-password/<token>")
    api.add_resource(ResetEmail, "/api/auth/emailreset")
