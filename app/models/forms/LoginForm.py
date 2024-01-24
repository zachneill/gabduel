"""This file contains the LoginForm object in the /login route"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login Form for login.html page"""
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    rememberMe = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')
