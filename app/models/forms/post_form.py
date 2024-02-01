"""This file contains the PostForm object in the /create route"""
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerRangeField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """Post Form for create.html page"""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)],
                        render_kw={'autofocus': True, 'placeholder': 'Title'})
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=1000)],
                            render_kw={'placeholder': 'Content'})
    otherAuthor = SelectField('Other Author', validators=[DataRequired(), Length(min=1, max=100)],
                              render_kw={'placeholder': 'Authors'})
    intensity = IntegerRangeField('Intensity', validators=[DataRequired()],
                                  render_kw={'placeholder': 'Intensity'}, default=1)
    type = SelectField('Type', validators=[DataRequired()], render_kw={'placeholder':
                            'Authors'},
                       choices=[('duel', 'Duel'), ('gab', 'Gab')])
    submit = SubmitField('Post', render_kw={'class': 'btn btn-success'})
