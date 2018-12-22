from ..models import Site
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SiteForm(FlaskForm):
    site_name = StringField("Name of Site", validators=[DataRequired()])
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State", validators=[Length(0, 2)])
    zipcode = StringField("Zipcode")
    submit = SubmitField("Submit")