from ..models import Facility
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Optional, Length
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField


def facility_query():
    return Facility.query


class FacilityForm(FlaskForm):
    name = StringField("Name of Facility", validators=[DataRequired()])
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
    longitude = FloatField(
        "Longitude", validators=[Optional()], filters=[lambda x: x or None]
    )
    latitude = FloatField(
        "Latitude", validators=[Optional()], filters=[lambda x: x or None]
    )
    submit = SubmitField("Submit")


class StorageTankForm(FlaskForm):
    tank_registration_id = StringField(
        "Tank Registration ID",
        validators=[Optional(), Length(max=12)],
        filters=[lambda x: x or None],
    )
    capacity = IntegerField(
        "Capacity", validators=[Optional()], filters=[lambda x: x or None]
    )
    stored_substance = StringField(
        "Stored Substance", validators=[Optional(), Length(max=64)]
    )
    status = SelectField(
        "Type",
        choices=[("active", "Active"), ("inactive", "Inactive"), ("closed", "Closed")],
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
    tank_type = SelectField("Type", choices=[("ust", "UST"), ("ast", "AST")])
    submit = SubmitField("Submit")


class WasteUnitForm(FlaskForm):
    name = StringField("Unit Name", validators=[Length(max=64)])
    submit = SubmitField("Submit")
