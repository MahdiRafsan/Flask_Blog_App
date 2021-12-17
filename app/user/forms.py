from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
from flask_login import current_user

# from app.models import User
from ..models import User

class EditProfileForm(FlaskForm):
    """
    create a form to edit the profile
    """
    username = StringField("Username", validators = [DataRequired(), Length(min=4, max=20, 
                                       message="Username must be between %(min)d and %(max)d characters.")])
    email = StringField("Email", validators = [DataRequired(), Email()])
    bio = TextAreaField("Add a bio", widget=TextArea(), validators=[Length(max=200, message="Bio must be than %(max)d characters.")])
    new_password = PasswordField("New Password")
    confirm = PasswordField("Confirm New Password", validators=[
                        EqualTo("new_password", message="Password must match with the newly entered password.")])
    image = FileField("Change Profile Picture", validators = [FileAllowed(["jpeg", "jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """
        validate that the username is unique
        :param username: updated username to be used
        :raise ValidationError: if username already exists in the database 
        :return: None
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username is already in use. Please choose a different username!")

    def validate_email(self, email):
        """
        validate that the email is unique
        :param username: updated email to be used
        :raise ValidationError: if email already exists in the database 
        :return: None
        """
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("The email is already in use. Choose a different email!")

class ResetRequestForm(FlaskForm):
    """
    create a form for user to request the password reset token
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Get Password Reset Token")

    def validate_email(self, email):
        """
        validate the user already has an account
        :param email: email address to be checked
        :raise ValidationError: if email is not registered
        :return: None
        """
        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError("That email does not exist. Please create an account first.")

class PasswordResetForm(FlaskForm):
    """
    create a form to allow user to reset password 
    """
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Reset Password")
    