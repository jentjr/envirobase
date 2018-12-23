from ..models import Site
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class SiteForm(FlaskForm):
    name = StringField("Name of Site", validators=[DataRequired()])
    address = StringField(
        "Address",
        validators=[Optional(), Length(max=100)],
        filters=[lambda x: x or None],
    )
    city = StringField(
        "City", validators=[Optional(), Length(max=100)], filters=[lambda x: x or None]
    )
    state = StringField("State", validators=[Optional(), Length(max=2)])
    zipcode = StringField(
        "Zipcode",
        validators=[Optional(), Length(max=10)],
        filters=[lambda x: x or None],
    )
    longitude = StringField(
        "Longitude",
        validators=[Optional(), Length(max=10)],
        filters=[lambda x: x or None],
    )
    latitude = StringField(
        "Latitude",
        validators=[Optional(), Length(max=10)],
        filters=[lambda x: x or None],
    )
    submit = SubmitField("Submit")
