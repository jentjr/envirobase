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

    storage_tank = db.relationship("StorageTank", back_populates="facility")
    waste_unit = db.relationship("WasteUnit", back_populates="facility")

    def __repr__(self):
        return f"Facility('{self.facility_id}','{self.name}', '{self.address}', '{self.city}','{self.state}', '{self.zipcode}')"

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
            created_on=datetime.utcnow()
            # geometry = "POINT({} {})".format(longitude, latitude)
        )


class WasteUnit(db.Model, BaseEntity):
    __tablename__ = "waste_unit"
    __table_args__ = (db.UniqueConstraint("name", "facility_id"),)

    unit_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.facility_id"))
    name = db.Column(db.String(64), nullable=False)
    constructed_date = db.Column(db.Date)
    geometry = db.Column(Geometry(geometry_type="POLYGON", srid=4326))
    unit_type = db.Column(db.String(12), nullable=False)

    facility = db.relationship("Facility", back_populates="waste_unit")

    __mapper_args__ = {
        "polymorphic_identity": "waste_unit",
        "polymorphic_on": unit_type,
    }

    def __repr__(self):
        return f"WasteUnit('{self.name}')"

    def to_json(self):
        json_waste_unit = {
            "url": url_for("api.get_waste_unit", unit_id=self.unit_id),
            "name": self.name,
            "constructed_date": self.constructed_date,
            "unit_type": self.unit_type,
        }
        return json_waste_unit


class Landfill(WasteUnit, BaseEntity):
    __tablename__ = "landfill"

    permit_id = db.Column(db.String(24))

    __mapper_args__ = {"polymorphic_identity": "landfill"}

    def __repr__(self):
        return f"Landfill('{self.name}')"

    def to_json(self):
        json_landfill = {
            "url": url_for("api.get_landfill", unit_id=self.unit_id),
            "name": self.name,
        }
        return json_landfill


class Impoundment(WasteUnit, BaseEntity):
    __tablename__ = "impoundment"

    dam_id = db.Column(db.String(24))
    hazard_class = db.Column(db.Text)

    __mapper_args__ = {"polymorphic_identity": "impoundment"}

    def __repr__(self):
        return f"Impoundment('{self.dam_id}', '{self.name}', '{self.hazard_class}')"

    def to_json(self):
        json_impoundment = {
            "url": url_for("api.get_impoundment", unit_id=self.unit_id),
            "name": self.name,
        }
        return json_impoundment


class StorageTank(db.Model, BaseEntity):
    """Base class for UndergroundStorageTank and AbovegroundStorageTank classes using Joined Table Inheritance. When StorageTank is queried only columns in this class are returned."""

    __tablename__ = "storage_tank"
    __table_args__ = (db.UniqueConstraint("tank_registration_id", "facility_id"),)

    tank_id = db.Column(db.Integer, primary_key=True)
    tank_registration_id = db.Column(db.String(12))
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.facility_id"))
    capacity = db.Column(db.Integer)
    stored_substance = db.Column(db.String(64))
    status = db.Column(db.String(10))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))
    tank_type = db.Column(db.String(3), nullable=False)

    facility = db.relationship("Facility", back_populates="storage_tank")

    __mapper_args__ = {
        "polymorphic_identity": "storage_tank",
        "polymorphic_on": tank_type,
    }
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))

    def __repr__(self):
        return f"StorageTank('{self.tank_id}', '{self.tank_type}', '{self.stored_substance}', '{self.status}')"

    def to_json(self):
        json_storage_tank = {
            "url": url_for("api.get_storage_tank", tank_id=self.tank_id),
            "facility": self.facility.name,
            "tank_registration_id": self.tank_registration_id,
            "capacity": self.capacity,
            "stored_substance": self.stored_substance,
            "status": self.status,
            "tank_type": self.tank_type,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }
        return json_storage_tank

    @staticmethod
    def from_json(json_storage_tank):
        facility_id = json_storage_tank.get("facility_id")
        tank_registration_id = json_storage_tank.get("tank_registration_id")
        capacity = json_storage_tank.get("capacity")
        stored_substance = json_storage_tank.get("stored_substance")
        status = json_storage_tank.get("status")
        tank_type = json_storage_tank.get("tank_type")
        longitude = json_storage_tank.get("longitude")
        latitude = json_storage_tank.get("latitude")
        if facility_id is None or facility_id == "":
            raise ValidationError("Tank must be associated with a Facility")
        return StorageTank(
            facility_id=facility_id,
            tank_registration_id=tank_registration_id,
            capacity=capacity,
            stored_substance=stored_substance,
            status=status,
            tank_type=tank_type,
            longitude=longitude,
            latitude=latitude,
            created_on=datetime.utcnow()
            # geometry = "POINT({} {})".format(longitude, latitude)
        )


class UndergroundStorageTank(StorageTank, BaseEntity):
    """Subclass to StorageTank with Joined Table Inheritance. When UndergroundStorageTank is queried all columns from StorageTank are inherited."""

    __tablename__ = "ust"

    __mapper_args__ = {"polymorphic_identity": "ust"}

    def __repr__(self):
        return f"UndergroundStorageTank('{self.tank_id}', '{self.tank_type}', '{self.stored_substance}', '{self.status}')"

    def to_json(self):
        json_ust = {
            "url": url_for("api.get_ust", tank_id=self.tank_id),
            "capacity": self.capacity,
            "stored_substance": self.stored_substance,
        }
        return json_ust


class AbovegroundStorageTank(StorageTank, BaseEntity):
    """Subclass to StorageTank with Joined Table Inheritance. When AbovegroundStorageTank is queried all columns from StorageTank are inherited."""

    __tablename__ = "ast"

    __mapper_args__ = {"polymorphic_identity": "ast"}

    def __repr__(self):
        return f"AbovegroundStorageTank('{self.tank_id}', '{self.tank_type}', '{self.stored_substance}', '{self.status}')"

    def to_json(self):
        json_ast = {
            "url": url_for("api.get_ast", tank_id=self.tank_id),
            "capacity": self.capacity,
            "stored_substance": self.stored_substance,
        }
        return json_ast


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


class SampleId(db.Model, BaseEntity):
    __tablename__ = "sample_id"

    sample_id = db.Column(db.Integer, primary_key=True, unique=True)
    facility_id = db.Column(db.ForeignKey("facility.facility_id"))
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    geometry = db.Column(Geometry(geometry_type="POINT", srid=4326))
    sample_type = db.Column(db.String(24))

    facility = db.relationship("Facility")

    __mapper_args__ = {
        "polymorphic_identity": "sample_id",
        "polymorphic_on": sample_type,
    }

    def __repr__(self):
        return f"SampleId('{self.sample_id}', '{self.facility.name}', '{self.sample_type}')"

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
        return SampleId(sample_id=sample_id, sample_type=sample_type)


class Boring(db.Model, BaseEntity):
    __tablename__ = "boring"

    boring_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class MonitoringWell(SampleId, BaseEntity):
    __tablename__ = "monitoring_well"

    sample_id = db.Column(
        db.Integer, db.ForeignKey("sample_id.sample_id"), primary_key=True
    )
    well_id = db.Column(db.Integer, primary_key=True)
    boring_id = db.Column(db.Integer, db.ForeignKey("boring.boring_id"))
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

    __mapper_args__ = {"polymorphic_identity": "monitoring_well"}


class Piezometer(SampleId, BaseEntity):
    __tablename__ = "piezometer"

    sample_id = db.Column(
        db.Integer, db.ForeignKey("sample_id.sample_id"), primary_key=True
    )
    piezometer_id = db.Column(db.Integer, primary_key=True)
    boring_id = db.Column(db.Integer, db.ForeignKey("boring.boring_id"))
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

    __mapper_args__ = {"polymorphic_identity": "piezometer"}


class SampleResult(db.Model, BaseEntity):
    __tablename__ = "sample_result"
    __table_args__ = (
        db.UniqueConstraint(
            "lab_id", "sample_id", "sample_date", "param_cd", "analysis_result"
        ),
    )

    result_id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Text)
    facility_id = db.Column(db.ForeignKey("facility.facility_id"), nullable=False)
    sample_id = db.Column(db.ForeignKey("sample_id.sample_id"), nullable=False)
    param_cd = db.Column(db.ForeignKey("sample_parameter.param_cd"), nullable=False)
    sample_date = db.Column(db.Date, nullable=False)
    sample_time = db.Column(db.Time, nullable=True)
    medium_cd = db.Column(db.ForeignKey("medium_code.medium_cd"))
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
