"""
API for Sites
"""

from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Site


@api.route("/sites/", methods=["GET"])
def get_sites():
    sites = Site.query.all()
    data = [
        {
            "type": "Feature",
            "properties": {
                "site_id": site.site_id,
                "name": site.name,
                "address": site.address,
                "city": site.city,
                "state": site.state,
                "zipcode": site.zipcode,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [site.longitude, site.latitude],
            },
        }
        for site in sites
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/sites/<int:site_id>", methods=["GET"])
def get_site(site_id):
    site = Site.query.get_or_404(site_id)
    data = [
        {
            "type": "Feature",
            "properties": {
                "site_id": site.site_id,
                "name": site.name,
                "address": site.address,
                "city": site.city,
                "state": site.state,
                "zipcode": site.zipcode,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [site.longitude, site.latitude],
            },
        }
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/sites/<name>", methods=["GET"])
def get_site_name(name):
    sites = Site.query.filter(Site.name.ilike(name + "%")).all()
    data = [
        {
            "type": "Feature",
            "properties": {
                "site_id": site.site_id,
                "name": site.name,
                "address": site.address,
                "city": site.city,
                "state": site.state,
                "zipcode": site.zipcode,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [site.longitude, site.latitude],
            },
        }
        for site in sites
    ]
    return jsonify({"type": "FeatureCollection", "features": data})


@api.route("/sites/", methods=["POST"])
def new_site():
    site = Site.from_json(request.json)
    db.session.add(site)
    db.session.commit()
    return (
        jsonify(site.to_json()),
        201,
        {"Location": url_for("api.get_site", site_id=site.site_id)},
    )


@api.route("/sites/<int:site_id>", methods=["PUT"])
def edit_site(site_id):
    site = Site.query.get_or_404(site_id)
    site.name = request.json.get("name", site.name)
    site.address = request.json.get("address", site.address)
    site.city = request.json.get("city", site.city)
    site.state = request.json.get("state", site.state)
    site.zipcode = request.json.get("zipcode", site.zipcode)
    site.latitude = request.json.get("latitude", site.latitude)
    site.longitude = request.json.get("longitude", site.longitude)
    db.session.add(site)
    db.session.commit()
    return jsonify(site.to_json())
