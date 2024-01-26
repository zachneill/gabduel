"""This file contains the search bar form in the home and search pages"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    """Form for the search bar in the navbar"""
    search = StringField('Search', validators=[DataRequired(), Length(min=2, max=80)],
                         render_kw={'placeholder': 'Search', 'class': 'w-50 m-auto'})
    submit = SubmitField('Go', render_kw={'class': 'btn btn-success d-flex'})
