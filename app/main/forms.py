from ..models import Facility
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Optional, Length
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.fields.html5 import DateField


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
    constructed_date = DateField(
        "Date Constructed", validators=[Optional()], filters=[lambda x: x or None]
    )
    unit_type = SelectField(
        "Type", choices=[("impoundment", "Impoundment"), ("landfill", "Landfill")]
    )
    submit = SubmitField("Submit")


class WellForm(FlaskForm):
    well_id = StringField("Well ID", validators=[DataRequired()])
    well_type = SelectField(
        "Type",
        choices=[
            ("piezometer", "Piezometer"),
            ("monitoring", "Monitoring"),
            ("supply", "Supply"),
        ],
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
    installation_date = DateField(
        "Date of Installation", validators=[Optional()], filters=[lambda x: x or None]
    )
    abandoned_date = DateField(
        "Date Closed/Sealed", validators=[Optional()], filters=[lambda x: x or None]
    )
    top_riser = FloatField(
        "Top of Riser", validators=[Optional()], filters=[lambda x: x or None]
    )
    top_bent_seal = FloatField(
        "Top of Bentonite Seal", validators=[Optional()], filters=[lambda x: x or None]
    )
    top_gravel_pack = FloatField(
        "Top of Gravel Pack", validators=[Optional()], filters=[lambda x: x or None]
    )
    top_screen = FloatField(
        "Top of Screen", validators=[Optional()], filters=[lambda x: x or None]
    )
    bottom_screen = FloatField(
        "Bottom of Screen", validators=[Optional()], filters=[lambda x: x or None]
    )
    bottom_well = FloatField(
        "Bottom of Well", validators=[Optional()], filters=[lambda x: x or None]
    )
    bottom_gravel_pack = FloatField(
        "Bottom of Gravel Pack", validators=[Optional()], filters=[lambda x: x or None]
    )
    bottom_boring = FloatField(
        "Bottom of Boring", validators=[Optional()], filters=[lambda x: x or None]
    )
    grout_seal_desc = StringField(
        "Description of Grout Seal",
        validators=[Optional()],
        filters=[lambda x: x or None],
    )
    bent_seal_desc = StringField(
        "Description of Bentonite Seal",
        validators=[Optional()],
        filters=[lambda x: x or None],
    )
    screen_type = StringField(
        "Screen Type", validators=[Optional()], filters=[lambda x: x or None]
    )
    gravel_pack_desc = StringField(
        "Description of Gravel Pack",
        validators=[Optional()],
        filters=[lambda x: x or None],
    )
    riser_pipe_desc = StringField(
        "Description of Riser Pipe",
        validators=[Optional()],
        filters=[lambda x: x or None],
    )
    spacer_depths = StringField(
        "List of Spacer Depths", validators=[Optional()], filters=[lambda x: x or None]
    )
    notes = StringField("Notes", validators=[Optional()], filters=[lambda x: x or None])
    submit = SubmitField("Submit")
