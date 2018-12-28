from flask import render_template, url_for, redirect, current_app, flash
from . import main
from .. import db
from .forms import FacilityForm
from ..models import (
    Boring,
    MediumCode,
    SampleParameter,
    Facility,
    Landfill,
    Impoundment,
    UndergroundStorageTank,
    AbovegroundStorageTank,
    SampleId,
    SampleResult,
    Well,
)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/facilities", methods=["GET"])
def facilities():
    facilities = Facility.query.order_by(Facility.name).all()
    return render_template("facilites.html", facilites=facilities)


@main.route("/facilities/<int:facility_id>", methods=["GET"])
def facility_by_id(facility_id):
    facilites = Facility.query.filter_by(facility_id=facility_id)
    return render_template("facilites.html", facilites=facilites)


@main.route("/facilites/<name>", methods=["GET"])
def facility_by_name(name):
    facilities = Facility.query.filter(
        Facility.name.ilike(name + "%")
    ).first()  # Site must be unique
    return render_template("facilites.html", facilites=facilites)


@main.route("/add-facility", methods=["GET", "POST"])
def add_facility():
    form = FacilityForm()
    if form.validate_on_submit():
        facility = Facility.query.filter_by(name=form.name.data).first()
        if facility is None:
            facility = Facility(
                name=form.name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zipcode=form.zipcode.data,
                longitude=form.longitude.data,
                latitude=form.latitude.data,
            )
            db.session.add(facility)
            db.session.commit()
            return redirect(url_for(".facilites"))
        else:
            flash("The facility already exists.")
    return render_template("edit_facility.html", form=form)


@main.route("/edit-facility/<int:facility_id>", methods=["GET", "POST"])
def edit_facility_id(site_id):
    facility = Facility.query.get_or_404(facility)
    form = FacilityForm()
    if form.validate_on_submit():
        name = form.name.data
        site.address = form.address.data
        site.city = form.address.data
        site.state = form.state.data
        site.zipcode = form.zipcode.data
        site.longitude = form.longitude.data
        site.latitude = form.latitude.data
        db.session.add(facility)
        db.session.commit()
        flash("The facility has been updated.")
        return redirect(url_for(".facilites"))
    form.name.data = facility.name
    form.address.data = facility.address
    form.city.data = facility.city
    form.state.data = facility.state
    form.zipcode.data = facility.zipcode
    form.longitude.data = facility.longitude
    form.latitude.data = facility.latitude
    return render_template("edit_facility.html", form=form)


@main.route("/edit-facility/<name>", methods=["GET", "POST"])
def edit_facility_name(name):
    facility = Facility.query.filter(Facility.name.ilike(name + "%")).first()
    form = FacilityForm()
    if form.validate_on_submit():
        name = form.name.data
        site.address = form.address.data
        site.city = form.address.data
        site.state = form.state.data
        site.zipcode = form.zipcode.data
        site.longitude = form.longitude.data
        site.latitude = form.latitude.data
        db.session.add(facility)
        db.session.commit()
        flash("The facility has been updated.")
        return redirect(url_for(".facilites"))
    form.name.data = facility.name
    form.address.data = facility.address
    form.city.data = facility.city
    form.state.data = facility.state
    form.zipcode.data = facility.zipcode
    form.longitude.data = facility.longitude
    form.latitude.data = facility.latitude
    return render_template("edit_facility.html", form=form)


@main.route("/units")
def units():
    units = Unit.query.all()
    return render_template("units.html", units=units)


@main.route("/sample-ids")
def sample_ids():
    sample_ids = SampleId.query.all()
    return render_template("sample_ids.html", sample_ids=sample_ids)


@main.route("/sample-results")
def sample_results():
    sample_results = SampleResult.query.all()
    return render_template("sample_results.html", sample_results=sample_results)


@main.route("/parameters")
def parameters():
    parameters = SampleParameter.query.all()
    return render_template("parameters.html", parameters=parameters)


@main.route("/parameters/<search_description>", methods=["GET"])
def parameters_search(search_description):
    parameters = SampleParameter.query.filter(
        SampleParameter.description.ilike(search_description + "%")
    ).all()
    return render_template("parameters.html", parameters=parameters)


@main.route("/mediums")
def mediums():
    mediums = MediumCode.query.all()
    return render_template("mediums.html", mediums=mediums)
