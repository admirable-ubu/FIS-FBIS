import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv("SECRET_KEY", "dev")
SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "password_salt")
TESTING = os.getenv("TESTING", "0") == "1"
LOGIN_DISABLED = False


# sqlalchemy configuration
SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, "hutia/data.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_HEADERS = 'Content-Type'
