"""This file resets the database."""
import os

from flask import url_for

from app import create_app

from database import db

app = create_app()


with app.app_context(), app.test_request_context():
    avatarFolder = url_for('static', filename='images/avatars')
    if os.path.exists(avatarFolder):
        for file in os.listdir(avatarFolder):
            os.remove(os.path.join(avatarFolder, file))
    else:
        os.makedirs(avatarFolder)
    db.drop_all()
    db.create_all()