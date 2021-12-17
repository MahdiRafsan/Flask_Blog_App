from flask_login import UserMixin
from datetime import datetime
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    """
    return the user object given the id
    :param id: user_id
    :return: user with associated id
    """
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    """
    create a database table for users
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="blog.jpg")
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    about = db.Column(db.String(200), nullable=True) 
    post = db.relationship("Post", backref="author", cascade="all, delete", passive_deletes=True, lazy=True)
    comments = db.relationship("Comment", backref="author", cascade="all, delete", passive_deletes=True, lazy=True)
    likes = db.relationship("Like", backref="author", cascade="all, delete", passive_deletes=True, lazy=True)

    def get_token(self):
        """
        create a token to reset password
        :return: token 
        """
        serializer = Serializer(current_app.config["SECRET_KEY"])
        return serializer.dumps({"user_id": self.id}, salt="confirm-password")

    @staticmethod
    def verify_token(token):
        """
        verify the token to update the password
        :param token: password reset token
        :raise Exception: if token doesn't match the original token
        :return: user_id with the token  
        """
        serializer = Serializer(current_app.config["SECRET_KEY"]) 
        try:
            user_id = serializer.loads(token, salt="confirm-password", max_age=1800)["user_id"]
        except:
            return None
        return User.query.filter_by(id=user_id).first()

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.date})"

class Post(db.Model):
    """
    create a database table for posts
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    post_author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comment", backref="post", cascade="all, delete", passive_deletes=True, lazy=True)
    likes = db.relationship("Like", backref="post", cascade="all, delete", passive_deletes=True, lazy=True)

    def __repr__(self): 
        return f"Post({self.title}, {self.date})"

class Comment(db.Model):
    """
    create a database table for comments
    """
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

class Like(db.Model):
    """
    create a database table to store likes
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
