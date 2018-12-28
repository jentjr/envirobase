import json
from . import db
import pandas as pd
from datetime import datetime
from geoalchemy2 import functions
from geoalchemy2.types import Geometry
from flask import current_app, request, url_for
from .errors import AlreadyExistsError


class BaseExtension(db.MapperExtension):
    """Base extension for all entities."""

    def before_insert(self, mapper, connection, instance):
        instance.created_on = datetime.now()

    def before_update(self, mapper, connection, instance):
        instance.updated_on = datetime.now()


class BaseEntity(object):
    __mapper_args__ = {"extension": BaseExtension()}

    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)


class Facility(db.Model, BaseEntity):
    __tablename__ = "facility"

    facility_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.CHAR(2))
    zipcode = db.Column(db.String)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))

    def __repr__(self):
        return f"Facility('{self.name}', '{self.address}', '{self.city}','{self.state}', '{self.zipcode}', '{self.longitude}', '{self.latitude}')"

    @classmethod
    def add_facility(cls, name, address, city, state, zipcode, longitude, latitude):
        """Add a new facility in the database."""

        geometry = "POINT({} {})".format(longitude, latitude)
        facility = Facility(
            name=name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            longitude=longitude,
            latitude=latitude,
            geometry=geometry,
        )

        db.session.add(facility)
        db.session.commit()

    @classmethod
    def update_geometries(cls):
        """Using each facility's longitude and latitude, add geometry data to db."""

        facilities = Facility.query.all()

        for facility in facilities:
            point = "POINT({} {})".format(facility.longitude, facility.latitude)
            facility.geometry = point

        db.session.commit()

    def to_json(self):
        json_facility = {
            "url": url_for("api.get_facility", facility_id=self.facility_id),
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }
        return json_facility

    @staticmethod
    def from_json(json_facility):
        name = json_facility.get("name")
        address = json_facility.get("address")
        city = json_facility.get("city")
        state = json_facility.get("state")
        zipcode = json_facility.get("zipcode")
        longitude = json_facility.get("longitude")
        latitude = json_facility.get("latitude")
        if name is None or name == "":
            raise ValidationError("Facility must have a name")
        return Facility(
            name=name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            longitude=longitude,
            latitude=latitude,
        )


class Landfill(db.Model, BaseEntity):
    __tablename__ = "landfill"

    landfill_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.ForeignKey("facility.facility_id"))
    name = db.Column(db.Text, nullable=False, unique=True)
    geometry = db.Column(Geometry(geometry_type="POLYGON", srid=4326))

    facility = db.relationship("Facility")

    def __repr__(self):
        return f"Landfill('{self.name}')"

    def to_json(self):
        json_landfill = {
            "url": url_for("api.get_landfill", landfill_id=self.landfill_id),
            "name": self.name,
            # "geometry": json.loads(self.coords),
        }
        return json_landfill


class Impoundment(db.Model, BaseEntity):
    __tablename__ = "impoundment"

    impoundment_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.ForeignKey("facility.facility_id"))
    name = db.Column(db.Text, nullable=False, unique=True)
    constructed_date = db.Column(db.Date)
    geometry = db.Column(Geometry(geometry_type="POLYGON", srid=4326))
    hazard_class = db.Column(db.Text)

    facility = db.relationship("Facility")

    def __repr__(self):
        return "<Impoundment(name='%s')>" % (self.name)

    def to_json(self):
        json_impoundment = {
            "url": url_for("api.get_impoundment", impoundment_id=self.impoundment_id),
            "name": self.name,
            # "geometry": json.loads(self.coords),
        }
        return json_impoundment


class StorageTank(db.Model, BaseEntity):
    __tablename__ = "storage_tank"

    tank_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.facility_id"))
    capacity = db.Column(db.Integer)
    stored_substance = db.Column(db.String(64))
    status = db.Column(db.String(10))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))
    tank_type = db.Column(db.String(24))

    facility = db.relationship("Facility")

    __mapper_args__ = {
        "polymorphic_identity": "storage_tank",
        "polymorphic_on": tank_type,
    }


class UndergroundStorageTank(StorageTank):
    __tablename__ = "underground_storage_tank"

    tank_id = db.Column(
        db.Integer, db.ForeignKey("storage_tank.tank_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "underground_storage_tank"}

    def __repr__(self):
        return f"UndergroundStorageTank('{self.tank_id}', '{self.tank_type}', '{self.stored_substance}', '{self.status}')"

    def to_json(self):
        json_ust = {
            "url": url_for("api.get_ust", tank_id=self.tank_id),
            "capacity": self.capacity,
            "stored_substance": self.stored_substance
            # "geometry": json.loads(self.coords),
        }
        return json_ust


class AbovegroundStorageTank(StorageTank):
    __tablename__ = "aboveground_storage_tank"

    tank_id = db.Column(
        db.Integer, db.ForeignKey("storage_tank.tank_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "aboveground_storage_tank"}

    def __repr__(self):
        return f"AbovegroundStorageTank('{self.tank_id}', '{self.tank_type}', '{self.stored_substance}', '{self.status}')"

    def to_json(self):
        json_ast = {
            "url": url_for("api.get_ast", tank_id=self.tank_id),
            "capacity": self.capacity,
            "stored_substance": self.stored_substance
            # "geometry": json.loads(self.coords),
        }
        return json_ast


class SampleId(db.Model, BaseEntity):
    __tablename__ = "sample_id"
    __table_args__ = (db.UniqueConstraint("sample_id", "facility_id"),)

    sample_id = db.Column(db.String(64), primary_key=True)
    facility_id = db.Column(
        db.ForeignKey("facility.facility_id", ondelete="CASCADE", onupdate="CASCADE")
    )
    sample_type = db.Column(db.String(3), db.ForeignKey("medium_code.medium_cd"))

    facility = db.relationship("Facility")
    medium = db.relationship("MediumCode")

    def __repr__(self):
        return "<SampleId(sample_id='%s', sample_type='%s')>" % (
            self.sample_id,
            self.sample_type,
        )

    def to_json(self):
        json_sample_location = {
            "url": url_for("api.get_sample_id", sample_id_id=self.sample_id),
            "facility": self.facility.name,
            "sample_id": self.sample_id,
            "sample_type": self.sample_type,
        }
        return json_sample_id

    @staticmethod
    def from_json(json_sample_location):
        facility = json_sample_location.get("facility.name")
        sample_id = json_sample_location.get("sample_id")
        sample_type = json_sample_location.get("sample_type")
        if location_id is None or location_id == "":
            raise ValidationError("Sample does not have an ID")
        return SampleLocation(sample_id=sample_id, sample_type=sample_type)


class Boring(db.Model, BaseEntity):
    __tablename__ = "boring"

    boring_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class Well(db.Model, BaseEntity):
    __tablename__ = "well"

    well_id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Text, db.ForeignKey("sample_id.sample_id"), nullable=False)
    boring_id = db.Column(db.Integer, db.ForeignKey("boring.boring_id"), nullable=False)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))
    medium_cd = db.Column(
        db.String(3), db.ForeignKey("sample_id.sample_type"), default="WG"
    )
    installation_date = db.Column(db.Date)
    abandoned_date = db.Column(db.Date)
    top_riser = db.Column(db.Float)
    top_bent_seal = db.Column(db.Float)
    top_gravel_pack = db.Column(db.Float)
    top_screen = db.Column(db.Float)
    bottom_screen = db.Column(db.Float)
    bottom_well = db.Column(db.Float)
    bottom_gravel_pack = db.Column(db.Float)
    bottom_boring = db.Column(db.Float)
    grout_seal_desc = db.Column(db.Text)
    bent_seal_desc = db.Column(db.Text)
    screen_type = db.Column(db.Text)
    gravel_pack_desc = db.Column(db.Text)
    riser_pipe_desc = db.Column(db.Text)
    spacer_depths = db.Column(db.Text)
    notes = db.Column(db.Text)

    boring = db.relationship("Boring")


class Piezometer(db.Model, BaseEntity):
    __tablename__ = "piezometer"

    piezometer_id = db.Column(db.Integer, primary_key=True)
    boring_id = db.Column(db.Integer, db.ForeignKey("boring.boring_id"), nullable=False)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))
    installation_date = db.Column(db.Date)
    abandoned_date = db.Column(db.Date)
    top_riser = db.Column(db.Float)
    top_bent_seal = db.Column(db.Float)
    top_gravel_pack = db.Column(db.Float)
    bottom_pizeometer = db.Column(db.Float)
    bottom_boring = db.Column(db.Float)
    grout_seal_desc = db.Column(db.Text)
    bent_seal_desc = db.Column(db.Text)
    screen_type = db.Column(db.Text)
    gravel_pack_desc = db.Column(db.Text)
    riser_pipe_desc = db.Column(db.Text)
    spacer_depths = db.Column(db.Text)
    notes = db.Column(db.Text)

    boring = db.relationship("Boring")


class MediumCode(db.Model, BaseEntity):
    __tablename__ = "medium_code"

    medium_cd = db.Column(db.String(3), primary_key=True)
    medium_name = db.Column(db.String(64))
    medium_description = db.Column(db.Text)
    legacy_cd = db.Column(db.CHAR(1))

    def __init__(self, **kwargs):
        super(MediumCode, self).__init__(**kwargs)

    def _insert_medium_codes():
        """Inserts USGS Medium Codes. If the codes have already been entered, an error is thrown."""
        if MediumCode.query.first():
            raise AlreadyExistsError("Medium Codes have already been entered.")
        else:
            url = "https://help.waterdata.usgs.gov/medium_cd"
            df = pd.read_html(url, header=0, converters={0: str})[0]
            df.rename(
                index=str,
                columns={
                    "Medium Code": "medium_cd",
                    "Medium Name": "medium_name",
                    "Medium Description": "medium_description",
                    "Medium Legacy Code": "legacy_cd",
                },
                inplace=True,
            )
            df.to_sql("medium_code", con=db.engine, if_exists="append", index=False)


class SampleParameter(db.Model, BaseEntity):
    __tablename__ = "sample_parameter"
    __table_args__ = (
        db.CheckConstraint(
            "param_cd ~ similar_escape('[[:digit:]]{5}'::text, NULL::text)"
        ),
    )

    param_cd = db.Column(db.CHAR(5), primary_key=True)
    group_name = db.Column(db.Text)
    description = db.Column(db.Text)
    epa_equivalence = db.Column(db.Text)
    statistical_basis = db.Column(db.Text)
    time_basis = db.Column(db.Text)
    weight_basis = db.Column(db.Text)
    particle_size_basis = db.Column(db.Text)
    sample_fraction = db.Column(db.Text)
    temperature_basis = db.Column(db.Text)
    casrn = db.Column(db.Text)
    srsname = db.Column(db.Text)
    parameter_unit = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(SampleParameter, self).__init__(**kwargs)

    def _insert_param_codes():
        """Inserts USGS Parameter Codes. If the codes have already been entered, an error is thrown."""
        if SampleParameter.query.first():
            raise AlreadyExistsError("Parameter Codes have already been entered.")
        else:
            url = "https://help.waterdata.usgs.gov/parameter_cd?group_cd=%"
            df = pd.read_html(url, header=0, converters={0: str})[0]
            df.rename(
                index=str,
                columns={
                    "Parameter Code": "param_cd",
                    "Group Name": "group_name",
                    "Parameter Name/Description": "description",
                    "Epa equivalence": "epa_equivalence",
                    "Result Statistical Basis": "statistical_basis",
                    "Result Time Basis": "time_basis",
                    "Result Weight Basis": "weight_basis",
                    "Result Particle Size Basis": "particle_size_basis",
                    "Result Sample Fraction": "sample_fraction",
                    "Result Temperature Basis": "temperature_basis",
                    "CASRN": "casrn",
                    "SRSName": "srsname",
                    "Parameter Unit": "parameter_unit",
                },
                inplace=True,
            )
            df.to_sql(
                "sample_parameter", con=db.engine, if_exists="append", index=False
            )


class SampleResult(db.Model, BaseEntity):
    __tablename__ = "sample_result"
    __table_args__ = (
        db.UniqueConstraint(
            "lab_id", "sample_id", "sample_date", "param_cd", "analysis_result"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.ForeignKey("facility.facility_id"), nullable=False)
    lab_id = db.Column(db.Text)
    sample_id = db.Column(db.ForeignKey("sample_id.sample_id"), nullable=False)
    param_cd = db.Column(db.ForeignKey("sample_parameter.param_cd"), nullable=False)
    sample_date = db.Column(db.Date, nullable=False)
    sample_time = db.Column(db.Time, nullable=True)
    medium_cd = db.Column(db.ForeignKey("medium_code.medium_cd"), default="WG")
    prep_method = db.Column(db.Text)
    analysis_method = db.Column(db.Text, nullable=True)
    analysis_flag = db.Column(db.CHAR(1), nullable=True)
    analysis_result = db.Column(db.Float, nullable=True)
    analysis_unit = db.Column(db.Text, nullable=False)
    detection_limit = db.Column(db.Float)
    reporting_limit = db.Column(db.Float)
    analysis_qualifier = db.Column(db.CHAR(1))
    disclaimer = db.Column(db.Text)
    analysis_date = db.Column(db.DateTime)
    order_comment = db.Column(db.Text)
    analysis_comment = db.Column(db.Text)

    sample = db.relationship("SampleId")
    medium_code = db.relationship("MediumCode")
    sample_parameter = db.relationship("SampleParameter")
    facility = db.relationship("Facility")
