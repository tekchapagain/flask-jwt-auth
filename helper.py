import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.common import TokenGenerator  # Assuming TokenGenerator is defined elsewhere

def send_forgot_password_email(request, user):
    """
    Sends an email to the user with a link to reset their password
    
    :param request: The request object
    :param user: The user object of the user who requested the password reset
    """
    current_site = os.environ.get("API_URL")
    mail_subject = "Niceclickllc - Password Reset"
    token = TokenGenerator.encode_token(user.email)
    reset_password_link = f"{current_site}/api/auth/reset-password/{token}"
    
    sender_email = "info@niceclickllc.com"
    receiver_email = user.email
    password = os.environ.get("EMAIL_HOST_PASSWORD") # Replace with your email password
    
    message = MIMEMultipart("alternative")
    message["Subject"] = mail_subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the HTML version of your message
    html = f"""
    <html>
      <body>
        <p>Please click on the link below to reset your password:</p>
        <p><a href="{reset_password_link}">{reset_password_link}</a></p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)
    login_email = os.environ.get("EMAIL_HOST_USER")
    # Try to send the email
    try:
        # Connect to the SMTP server
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(login_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        return None

    return token
