from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


class SiteForm(FlaskForm):
    name = StringField("Name of Site", validators=[DataRequired()])
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State Abbrev.", [Length(min=2, max=2)])
    zipcode = StringField("Zipcode") 
    submit = SubmitField('Submit')
