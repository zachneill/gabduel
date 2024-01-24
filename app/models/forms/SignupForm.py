"""This file contains the SignupForm object in the /signup route"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length


class SignupForm(FlaskForm):
    """Signup Form for signup.html page"""
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    confirmPassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(), Length(min=2, max=50)])
    rememberMe = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sign Up')
