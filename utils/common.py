from itsdangerous import URLSafeTimedSerializer
from utils.http_code import HTTP_200_OK, HTTP_201_CREATED


def generate_response(data=None, message=None, status=400):
    """
    It takes in a data, message, and status, and returns a dictionary with the data, message, and status

    :param data: The data that you want to send back to the client
    :param message: This is the message that you want to display to the user
    :param status: The HTTP status code, defaults to 400 (optional)
    :return: A dictionary with the keys: data, message, status.
    """
    if status == HTTP_200_OK or status == HTTP_201_CREATED:
        status_bool = True
    else:
        status_bool = False

    return {
        "data": data,
        "message": modify_slz_error(message, status_bool),
        "status": status_bool,
    }, status


def modify_slz_error(message, status):
    """
    It takes a message and a status, and returns a list of errors

    :param message: The error message that you want to display
    :param status: The HTTP status code you want to return
    :return: A list of dictionaries.
    """
    final_error = list()
    if message:
        if type(message) == str:
            if not status:
                final_error.append({"error": message})
            else:
                final_error = message
        elif type(message) == list:
            final_error = message
        else:
            for key, value in message.items():
                final_error.append({"error": str(key) + ": " + str(value[0])})
    else:
        final_error = None
    return final_error


class TokenGenerator:
    @staticmethod
    def encode_token(email):
        """
        The encode_token function takes in a email and returns a token

        :param user: The user email that we want to encode
        :return: A token
        """
        serializer = URLSafeTimedSerializer(secret_key="afkjlkajflkajf")
        return serializer.dumps(email, salt='1234')

    @staticmethod
    def check_token(token,expiration=3600):
        """
        It takes a token, and returns True if the token is valid, and False if it's not

        :param token: The token to be decoded
        :return: A boolean value.
        """
        serializer = URLSafeTimedSerializer(secret_key="afkjlkajflkajf")
        try:
            email = serializer.loads(
            token,
            salt='1234',
            max_age=expiration
        )
        except:
            return False
        return email 

token_generator = TokenGenerator()