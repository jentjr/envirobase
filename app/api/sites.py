from flask import jsonify, request, current_app, url_for
from . import api
from ..models import Site


@api.route("/sites/")
def get_sites():
    sites = Site.query.all()
    return jsonify({"sites": [site.to_json() for site in sites]})


@api.route("/sites/<int:site_id>")
def get_site(site_id):
    site = Site.query.get_or_404(site_id)
    return jsonify(site.to_json())
