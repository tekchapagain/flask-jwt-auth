import os
from flask_mail import Message
from utils.common import TokenGenerator
from server import mail


def send_forgot_password_email(request, user):
    """
    It sends an email to the user with a link to reset their password

    :param request: The request object
    :param user: The user object of the user who requested the password reset
    """
    current_site = request.url_root
    mail_subject = "Niceclickllc - Password Reset"
    token = TokenGenerator.encode_token(user.email)
    msg = Message(
        mail_subject, sender="info@niceclickllc.com", recipients=[user.email]
    )
    msg.html = f"Please click on the link to reset your password, {current_site}api/auth/reset-password/{token}"
    # print(msg.html)
    # mail.send(msg)
    return token
    
