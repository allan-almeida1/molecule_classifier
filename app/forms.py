from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ExampleForm(FlaskForm):
    """Example form."""
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
