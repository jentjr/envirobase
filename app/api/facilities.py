"""
API for Facilities
"""

from datetime import datetime
from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Facility


@api.route("/facilities/", methods=["GET"])
def get_facilities():
    facilities = Facility.query.all()
    data = [
        {
            "type": "Feature",
            "properties": {
                "facility_id": facility.facility_id,
                "name": facility.name,
                "address": facility.address,
                "city": facility.city,
                "state": facility.state,
                "zipcode": facility.zipcode,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [facility.longitude, facility.latitude],
            },
        }
        for facility in facilities
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/facilities/<int:facility_id>", methods=["GET"])
def get_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    data = [
        {
            "type": "Feature",
            "properties": {
                "facility_id": faciltiy.facility_id,
                "name": facility.name,
                "address": facility.address,
                "city": facility.city,
                "state": facility.state,
                "zipcode": facility.zipcode,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [facility.longitude, facility.latitude],
            },
        }
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/facilities/<name>", methods=["GET"])
def get_facility_name(name):
    facilites = Facility.query.filter(Facility.name.ilike("%" + name + "%")).all()
    data = [
        {
            "type": "Feature",
            "properties": {
                "facility_id": facility.facility_id,
                "name": facility.name,
                "address": facility.address,
                "city": facility.city,
                "state": facility.state,
                "zipcode": facility.zipcode,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [facility.longitude, facility.latitude],
            },
        }
        for facility in facilities
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/facilities/", methods=["POST"])
def new_facility():
    facility = Facility.from_json(request.json)
    db.session.add(facility)
    db.session.commit()
    return (
        jsonify(facility.to_json()),
        201,
        {"Location": url_for("api.get_facility", facility_id=facility.facility_id)},
    )


@api.route("/facilities/<int:facility_id>", methods=["PUT"])
def edit_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    facility.name = request.json.get("name", facility.name)
    facility.address = request.json.get("address", facility.address)
    facility.city = request.json.get("city", facility.city)
    facility.state = request.json.get("state", facility.state)
    facility.zipcode = request.json.get("zipcode", facility.zipcode)
    facility.latitude = request.json.get("latitude", facility.latitude)
    facility.longitude = request.json.get("longitude", facility.longitude)
    facility.updated_on = datetime.utcnow()
    db.session.add(facility)
    db.session.commit()
    return jsonify(facility.to_json())


@api.route("/facilities/<int:facility_id>", methods=["DELETE"])
def delete_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    db.session.delete(facility)
    db.session.commit()
    return {}
