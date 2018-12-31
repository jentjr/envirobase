"""
API for StorageTank
"""

from datetime import datetime
from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import StorageTank


@api.route("/storage-tanks/", methods=["GET"])
def get_storage_tanks():
    storage_tanks = StorageTank.query.all()
    data = [
        {
            "type": "Feature",
            "properties": {
                "facility": storage_tank.facility.name,
                "tank_id": storage_tank.tank_id,
                "tank_registration_id": storage_tank.tank_registration_id,
                "capacity": storage_tank.capacity,
                "stored_substance": storage_tank.stored_substance,
                "tank_type": stored_substance.tank_type,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [storage_tank.longitude, storage_tank.latitude],
            },
        }
        for storage_tank in storage_tanks
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/storage-tanks/<int:tank_id>", methods=["GET"])
def get_storage_tank(tank_id):
    storage_tank = StorageTank.query.get_or_404(tank_id)
    data = [
        {
            "type": "Feature",
            "properties": {
                "facility": storage_tank.facility.name,
                "tank_id": storage_tank.tank_id,
                "tank_registration_id": storage_tank.tank_registration_id,
                "capacity": storage_tank.capacity,
                "stored_substance": storage_tank.stored_substance,
                "tank_type": stored_substance.tank_type,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [storage_tank.longitude, storage_tank.latitude],
            },
        }
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/storage-tanks/", methods=["POST"])
def new_storage_tank():
    storage_tank = StorageTank.from_json(request.json)
    db.session.add(storage_tank)
    db.session.commit()
    return (
        jsonify(storage_tank.to_json()),
        201,
        {"Location": url_for("api.get_storage_tank", tank_id=storage_tank.tank_id)},
    )


@api.route("/storage-tanks/<int:tank_id>", methods=["PUT"])
def edit_storage_tank(tank_id):
    storage_tank = StorageTank.query.get_or_404(tank_id)
    storage_tank.facility_id = request.json.get("facility_id", storage_tank.facility_id)
    storage_tank.tank_registration_id = request.json.get(
        "tank_registration_id", storage_tank.tank_registration_id
    )
    storage_tank.capacity = request.json.get("capacity", storage_tank.capacity)
    storage_tank.stored_substance = request.json.get(
        "stored_substance", storage_tank.stored_substance
    )
    storage_tank.status = request.json.get("status", storage_tank.status)
    storage_tank.tank_type = request.json.get("tank_type", storage_tank.tank_type)
    storage_tank.latitude = request.json.get("latitude", storage_tank.latitude)
    storage_tank.longitude = request.json.get("longitude", storage_tank.longitude)
    storage_tank.updated_on = datetime.utcnow()
    db.session.add(storage_tank)
    db.session.commit()
    return jsonify(storage_tank.to_json())
