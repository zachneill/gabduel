"""This file resets the database."""
from app import create_app

from database import db

app = create_app()
with app.app_context():
    db.drop_all()
