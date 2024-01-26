"""This file contains the LoginForm object in the /login route"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login Form for login.html page"""
    login = StringField('Email or Username', validators=[DataRequired(), Length(min=2, max=80)],
                        render_kw={'autofocus': True, 'placeholder': 'Email or Username'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)],
                             render_kw={'placeholder': 'Password'})
    rememberMe = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login', render_kw={'class': 'btn btn-success'})
