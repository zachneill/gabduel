"""This file contains the AdminForm object in the /admin route"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField


class AdminForm(FlaskForm):
    """Admin Form for admin.html page"""
    requestAdmin = SubmitField('Request Admin')
