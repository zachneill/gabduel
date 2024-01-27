"""This file resets the database."""
import os

from flask import url_for

from app import create_app

from database import db

app = create_app()

os.rmdir(url_for('static', filename='images/avatars'))
os.mkdir(url_for('static', filename='images/avatars'))

with app.app_context():
    db.drop_all()
