from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from ..models import User

class SignUpForm(FlaskForm):
    """
    create a signup form and handle validations
    """
    username = StringField("Username", validators = [DataRequired(), Length(min = 4, max = 20, 
                                       message="Username must be between %(min)d and %(max)d characters.")])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password", message="Passwords must match.")])
    signup = SubmitField("Sign-Up")
 
    def validate_username(self, username):
        """
        check if the user has an unique username
        :param username: username to be queried
        :raise ValidationError: if the username is already in database        
        :return: None
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is already in use. Please choose a different username!")

    def validate_email(self, email):
        """
        check if the user has an unique email
        :param email: email to be queried
        :raise ValidationError: if the email is already in database        
        :return: None
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("The email is already in use. Choose a different email!")

class LoginForm(FlaskForm):
    """
    create a login form and handle validations
    """
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Stay logged in")
    login = SubmitField("Login")


