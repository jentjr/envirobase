"""
API for Sites
"""

from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Site


@api.route("/sites/")
def get_sites():
    sites = Site.query.all()
    return jsonify({"sites": [site.to_json() for site in sites]})


@api.route("/sites/<int:site_id>")
def get_site(site_id):
    site = Site.query.get_or_404(site_id)
    return jsonify(site.to_json())


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
    site.site_name = request.json.get("site_name", site.site_name)
    site.address = request.json.get("address", site.address)
    site.city = request.json.get("city", site.city)
    site.state = request.json.get("state", site.state)
    site.zipcode = request.json.get("zipcode", site.zipcode)
    site.site_geog = request.json.get("site_geog", site.site_geog)
    db.session.add(site)
    db.session.commit()
    return jsonify(site.to_json())
