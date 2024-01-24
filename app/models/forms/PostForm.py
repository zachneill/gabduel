"""This file contains the PostForm object in the /create route"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """Post Form for create.html page"""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = StringField('Content', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Post')
