"""This file is one of the main files of the application. It creates the app,
    connects the database, and registers the blueprints. It also maintains login functionality.
"""
import os
import secrets
from os import environ

from flask import Flask, redirect, send_file
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, AnonymousUserMixin
from flask_wtf import CSRFProtect

from app.controllers.auth import auth
from app.controllers.views import views
from app.logic.accounts import getUserById
from database import db


def create_app():
    """Creates the app, connects the database, registers the blueprints, and inits login."""
    # Create app reqs
    app = Flask(__name__)
    Bootstrap5(app)
    CSRFProtect(app)

    # Connect to database
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
    app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Maintain login settings
    class Anonymous(AnonymousUserMixin):
        """Used in case of anonymous user image and username NoneType errors."""
        def __init__(self):
            self.image = ''
            self.username = 'Anonymous'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)
    login_manager.anonymous_user = Anonymous

    @login_manager.user_loader
    def load_user(user_id):
        """Used by flask_login to get the user by id, used alongside, e.g., current_user."""
        return getUserById(user_id)

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Custom page error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        print("Errored with: ", e)
        return redirect('/404')

    @app.errorhandler(500)
    def internal_server_error(e):
        print("Errored with: ", e)
        return redirect('/500')

    @app.errorhandler(405)
    def method_not_allowed(e):
        print("Errored with: ", e)
        return redirect('/405')

    # For PWA
    @app.route('/manifest.json')
    def serve_manifest():
        return send_file('static/manifest.json',
                         mimetype='application/manifest+json')

    @app.route('/sw.js')
    def serve_sw():
        return send_file('static/sw.js',
                         mimetype='application/javascript')

    return app
