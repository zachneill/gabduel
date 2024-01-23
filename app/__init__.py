import os

from app.logic.accounts import getUserById
from database import db
from app.controllers.main import main
from app.controllers.auth import auth
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets
from os import path
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    CSRFProtect(app)
    basedir = path.abspath(os.path.dirname(__file__))
    app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return getUserById(user_id)

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
