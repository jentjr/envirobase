import json
from . import db
from datetime import datetime
from geoalchemy2 import functions
from geoalchemy2.types import Geography
from flask import current_app, request, url_for


class BaseExtension(db.MapperExtension):
    """Base extension for all entities."""
    
    def before_insert(self, mapper, connection, instance):
        instance.created_on = datetime.now()
        
    def before_update(self, mapper, connection, instance):
        instance.updated_on = datetime.now()
        

class BaseEntity(object):
    __mapper_args__ = {'extension': BaseExtension()}
    
    created_on = db.Column(db.DateTime(6))


class Boring(db.Model, BaseEntity):
    __tablename__ = "boring"

    boring_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class MediumCode(db.Model, BaseEntity):
    __tablename__ = "medium_code"

    medium_cd = db.Column(db.String(3), primary_key=True)
    medium_name = db.Column(db.String(64))
    medium_description = db.Column(db.Text)
    legacy_cd = db.Column(db.CHAR(1))


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


class Site(db.Model, BaseEntity):
    __tablename__ = "site"

    site_id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.Text, nullable=False, unique=True)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.CHAR(2))
    zipcode = db.Column(db.String)
    site_geog = db.Column(Geography("POINT", 4326))
    coords = db.column_property(functions.ST_AsGeoJSON(site_geog))
    
    def __repr__(self):
        return "<Site(site_name='%s', address='%s', city='%s', state='%s', zipcode='%s')>" % (self.site_name, self.address, self.city, self.state, self.zipcode)

    def to_json(self):
        json_site = {
                'url': url_for('api.get_site', site_id=self.site_id),
                'site_name': self.site_name,
                'address': self.address,
                'city': self.city,
                'state': self.state,
                'geometry': json.loads(self.coords)
        }
        return json_site


class SampleLocation(db.Model, BaseEntity):
    __tablename__ = "sample_location"
    __table_args__ = (db.UniqueConstraint("location_id", "site_id"),)

    location_id = db.Column(db.Text, primary_key=True)
    site_id = db.Column(
        db.ForeignKey("site.site_id", ondelete="CASCADE", onupdate="CASCADE")
    )
    location_type = db.Column(db.Text)
    location_geog = db.Column(Geography("POINT", 4326))
    coords = db.column_property(functions.ST_AsGeoJSON(location_geog))
    
    site = db.relationship("Site")

    def __repr__(self):
        return "<SampleLocation(location_id='%s', location_type='%s')>" % (self.location_id, self.location_type)
    
    def to_json(self):
        json_sample_location = {
                'url': url_for('api.get_sample_location', location_id_id=self.location_id),
                'site': self.site.site_name,
                'location_id': self.location_id,
                'location_type': self.location_type,
                'geometry': json.loads(self.coords)
        }
        return json_sample_location

        
class Unit(db.Model, BaseEntity):
    __tablename__ = "unit"

    unit_id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.ForeignKey("site.site_id"))
    unit_name = db.Column(db.Text, nullable=False, unique=True)
    unit_geog = db.Column(Geography("POLYGON", 4326))

    site = db.relationship("Site")


class SampleResult(db.Model, BaseEntity):
    __tablename__ = "sample_result"
    __table_args__ = (
        db.UniqueConstraint(
            "lab_id", "location_id", "sample_date", "param_cd", "analysis_result"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.ForeignKey("site.site_id"), nullable=False)
    lab_id = db.Column(db.Text)
    location_id = db.Column(
        db.ForeignKey("sample_location.location_id"), nullable=False
    )
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

    location = db.relationship("SampleLocation")
    medium_code = db.relationship("MediumCode")
    sample_parameter = db.relationship("SampleParameter")
    site = db.relationship("Site")


class Well(db.Model, BaseEntity):
    __tablename__ = "well"
    
    well_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Text, db.ForeignKey("sample_location.location_id"), nullable=False)
    boring_id = db.Column(db.Integer, db.ForeignKey("boring.boring_id"), nullable=False)
    install_date = db.Column(db.Date)
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
    sample_location = db.relationship("SampleLocation")
