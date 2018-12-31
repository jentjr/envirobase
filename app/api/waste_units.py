"""
API for WasteUnit
"""

from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import WasteUnit


@api.route("/waste-units/", methods=["GET"])
def get_waste_units():
    waste_units = WasteUnit.query.all()
    data = [
        {
            "type": "Feature",
            "properties": {
                "facility": waste_unit.facility.name,
                "name": waste_unit.name,
                "constructed_date": waste_unit.constructed_date,
                "unit_type": waste_unit.unit_type,
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [waste_unit.longitude, waste_unit.latitude],
            },
        }
        for waste_unit in waste_units
    ]
    return jsonify({"type": "FeatureCollection", "features": data})
