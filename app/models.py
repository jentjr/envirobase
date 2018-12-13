from . import db
from geoalchemy2 import Geography
from datetime import datetime
from app.exceptions import ValidationError


class Site(db.Model):
    __tablename__ = "sites"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(256))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(10))
    geog = db.Column(Geography("POINT", 4326))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_json(self):
        json_site = {
            'url': url_for('api.get_site', id=self.id),
            'name': self.name,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id)
        }
        return json_site


class Unit(db.Model):
    __tablename__ = "units"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    geog = db.Column(Geography("POLYGON", 4326))

    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    site = db.relationship("Site", backref=db.backref("units", order_by=id), lazy=True) 

class SampleLocation(db.Model):
    __tablename__ = "sample_locations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    geog = db.Column(Geography("POINT", 4326))

    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    site = db.relationship("Site", backref=db.backref("sample_locations", order_by=id), lazy=True)


class SampleParameter(db.Model):
    __tablename__ = "sample_parameters"
    param_cd = db.Column(db.Text(5), primary_key=True)
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


class SampleResult(db.Model):
    __tablename__ = "sample_results"
    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Text)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("sample_locations.id"))
    param_cd = db.Column(db.Text, db.ForeignKey("sample_parameters.param_cd"))
    sample_date = db.Column(db.DateTime)
    media_matrix = db.Column(db.Text)
    prep_method = db.Column(db.Text)
    analysis_method = db.Column(db.Text)
    analysis_flag = db.Column(db.Text(1))
    analysis_result = db.Column(db.Float)
    analysis_unit = db.Column(db.Text)
    detection_limit = db.Column(db.Float)
    prac_quant_limit = db.Column(db.Float)
    analysis_qualifier = db.Column(db.Text(1))
    disclaimer = db.Column(db.Text)
    analysis_date = db.Column(db.DateTime)
    order_comment = db.Column(db.Text)
    analysis_comment = db.Column(db.Text)

    site = db.relationship("Site", backref=db.backref("sample_results", order_by=id), lazy=True)
    sample_location = db.relationship("SampleLocations", backref=db.backref("sample_results", order_by=id), lazy=True)
