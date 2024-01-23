from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Login')
