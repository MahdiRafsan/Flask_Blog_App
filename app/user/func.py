from flask import render_template, url_for
from flask_mail import Message

from app import mail

def send_email(user):
    """
    send email to the user with a token from
    :param user: user to recieve the password
    :return: None 
    """
    token = user.get_token()
    msg = Message(subject="Reset Password", sender=("FlaskBlog Team", "flaskblog@flaskblog.com"), recipients=[user.email])
    password_reset_url = url_for("user.reset_password", token=token, _external=True)
    msg.html = render_template("password_reset_email.html", url=password_reset_url)
    mail.send(msg)
