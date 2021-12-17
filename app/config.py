import os

class Config(object):
    """
    create configuration for the app
    """
    DB_NAME = "database.db"

    # app configurations
    SECRET_KEY = os.environ.get("SECRET_KEY") or "flaskblogapp"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or f"sqlite:///{DB_NAME}"

    # mail configurations
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False # use MAIL_PORT = 465 if MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("FlaskBlog", "flaskblog@flaskblog.com")