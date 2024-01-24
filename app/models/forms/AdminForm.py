from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField


class AdminForm(FlaskForm):
    requestAdmin = SubmitField('Request Admin')
