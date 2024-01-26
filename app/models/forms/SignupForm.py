"""This file contains the SignupForm object in the /signup route"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length


class SignupForm(FlaskForm):
    """Signup Form for signup.html page"""
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)],
                            render_kw={'autofocus': True, 'placeholder': 'First Name'})
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)],
                           render_kw={'placeholder': 'Last Name'})
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)],
                           render_kw={'placeholder': 'Username'})
    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=80)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)],
                             render_kw={'placeholder': 'Password'})
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                    Length(min=2, max=50)],
                                    render_kw={'placeholder': 'Confirm Password'})
    rememberMe = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sign Up', render_kw={'class': 'btn btn-success'})
