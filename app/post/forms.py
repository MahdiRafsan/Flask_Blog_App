from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    """
    display a form to create and update a post
    """
    title = StringField("Title", validators=[DataRequired(), Length(max=150, message="Title cannot be more than %(max)d characters.")])
    content = TextAreaField("Content", validators=[DataRequired()])
    post = SubmitField("Post")

class CommentForm(FlaskForm):
    """
    display a form to create a comment
    """
    comment = StringField(validators=[DataRequired()])
    submit = SubmitField("Comment")
    