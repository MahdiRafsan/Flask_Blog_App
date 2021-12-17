import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config=Config):
    """
    create an instance of the application
    :param config: Configuration class to configure the app settings
    :return: an instance of app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # initializing the flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    
    # import blueprints
    from .auth import auth
    from .main import main
    from .post import post
    from .user import user
    from .error import error

    # register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(post)
    app.register_blueprint(user)
    app.register_blueprint(error)
    
    create_database(app)
    
    return app

def create_database(app):
    """
    used to create database if database does not exists
    :param app: application
    :return: None    
    """
    if not os.path.exists("app/" + Config().DB_NAME):
        db.create_all(app=app)
