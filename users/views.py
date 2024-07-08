from flask import Response
from flask_restful import Resource
from flask.views import MethodView
from flask import request, make_response
from users.service import *


class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for login user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)
    
class WhoAmI(Resource):
    @staticmethod
    def get() -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        response, status = whoami()
        return make_response(response, status)

class RefreshApi(Resource):
    @staticmethod
    def get() -> Response:
        """
        Get response method for knowing user identity.

        :return: JSON object
        """
        response, status = refresh_access()
        return make_response(response, status)

class LogoutApi(Resource):
    @staticmethod
    def delete() -> Response:
        """
        Logout the user and revoke the tokens.

        :return: JSON object
        """
        response, status = logout_user()
        return make_response(response, status)

class ForgotPassword(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for forgot password email send user.

        :return: JSON object
        """
        # input_data = ""
        input_data = request.get_json()
        response, status = reset_password_email_send(request, input_data)
        return make_response(response, status)


class ResetPassword(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for save new password.

        :return: JSON object
        """
        # Access request headers
        token = request.headers["Token"]
        input_data = request.get_json()
        response, status = reset_password(request, input_data, token)
        return make_response(response, status)

class ResetEmail(MethodView):
    @staticmethod
    def post() -> Response:
        """
        POST response method for save new password.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = reset_email(request, input_data)
        return make_response(response, status)
    
class UserListApi(MethodView):
    @staticmethod
    def get() -> Response:
        """
        POST response method for save new password.

        :return: JSON object
        """
        response, status = get_all_users(request)
        return make_response(response, status)