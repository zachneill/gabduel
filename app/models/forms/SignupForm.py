from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class SignupForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Sign Up')