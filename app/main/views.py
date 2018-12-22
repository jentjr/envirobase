from flask import render_template, url_for, current_app
from . import main
from .. import db
from ..models import (
    Boring,
    MediumCode,
    SampleParameter,
    Site,
    Unit,
    SampleLocation,
    SampleResult,
    Well,
)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/sites")
def sites():
    sites = Site.query.all()
    return render_template("sites.html", sites=sites)


@main.route("/units")
def units():
    units = Unit.query.all()
    return render_template("units.html", units=units)


@main.route("/sample_locations")
def sample_locations():
    sample_locations = SampleLocation.query.all()
    return render_template("sample_locations.html", sample_locations=sample_locations)


@main.route("/sample_results")
def sample_results():
    sample_results = SampleResult.query.all()
    return render_template("sample_results.html", sample_results=sample_results)


@main.route("/parameters")
def parameters():
    parameters = SampleParameter.query.all()
    return render_template("parameters.html", parameters=parameters)


@main.route("/mediums")
def mediums():
    mediums = MediumCode.query.all()
    return render_template("mediums.html", mediums=mediums)
