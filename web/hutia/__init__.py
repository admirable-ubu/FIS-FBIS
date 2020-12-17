from flask import Flask
import variables as v
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask_login
from flask_cors import CORS


def create_app(config_name):
    """
    Creación de la aplicación.

    Arguments:
        config_name {string} -- configuración
    Returns:
        Flask -- aplicación flask
    """
    v.start()
    v.basedir = os.path.abspath(os.path.dirname(__file__))
    v.appdir = os.path.join(v.basedir, "..")

    app = Flask(__name__, static_folder='static')
    v.app = app

    app.config.from_pyfile('../config.py')                               

    v.db = SQLAlchemy(app)

    app.config['CORS_HEADERS'] = 'Content-Type'
    v.cors = CORS(app, resources={r"/givemethepower": {"origins": "*"}})

    v.login_manager = LoginManager()

    v.login_manager.init_app(app)
    v.login_manager.login_view = "users.login"
    from hutia.core.views import login_required
    flask_login.login_required = login_required

    from hutia.core.views import core
    from hutia.user.views import user

    app.register_blueprint(core)
    app.register_blueprint(user)

    def format_date(number):
        number = str(number)
        year = number[0:4]
        month = number[4:6]
        day = number[6:8]
        return day+"-"+month+"-"+year

    app.jinja_env.filters["date"] = format_date


    return app
