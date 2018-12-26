from flask import render_template, url_for, redirect, current_app, flash
from . import main
from .. import db
from .forms import SiteForm
from ..models import (
    Boring,
    MediumCode,
    SampleParameter,
    Site,
    Unit,
    SampleId,
    SampleResult,
    Well,
)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/sites", methods=["GET"])
def sites():
    sites = Site.query.order_by(Site.name).all()
    return render_template("sites.html", sites=sites)


@main.route("/sites/<int:site_id>", methods=["GET"])
def site_by_id(site_id):
    sites = Site.query.filter_by(site_id=site_id)
    return render_template("sites.html", sites=sites)


@main.route("/sites/<name>", methods=["GET"])
def site_by_name(name):
    sites = Site.query.filter(Site.name.ilike(name + "%")).first()  # Site must be unique
    return render_template("sites.html", sites=sites)


@main.route("/add-site", methods=["GET", "POST"])
def add_site():
    form = SiteForm()
    if form.validate_on_submit():
        site = Site.query.filter_by(name=form.name.data).first()
        if site is None:
            site = Site(
                name=form.name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zipcode=form.zipcode.data,
                longitude=form.longitude.data,
                latitude=form.latitude.data,
            )
            db.session.add(site)
            db.session.commit()
            return redirect(url_for(".sites"))
        else:
            flash("The site already exists.")
    return render_template("edit_site.html", form=form)


@main.route("/edit-site/<int:site_id>", methods=["GET", "POST"])
def edit_site_id(site_id):
    site = Site.query.get_or_404(site_id)
    form = SiteForm()
    if form.validate_on_submit():
        name = form.name.data
        site.address = form.address.data
        site.city = form.address.data
        site.state = form.state.data
        site.zipcode = form.zipcode.data
        site.longitude = form.longitude.data
        site.latitude = form.latitude.data
        db.session.add(site)
        db.session.commit()
        flash("The site has been updated.")
        return redirect(url_for(".sites"))
    form.name.data = site.name
    form.address.data = site.address
    form.city.data = site.city
    form.state.data = site.state
    form.zipcode.data = site.zipcode
    form.longitude.data = site.longitude
    form.latitude.data = site.latitude
    return render_template("edit_site.html", form=form)


@main.route("/edit-site/<name>", methods=["GET", "POST"])
def edit_site_name(name):
    site = Site.query.filter(Site.name.ilike(name + "%")).first()
    form = SiteForm()
    if form.validate_on_submit():
        name = form.name.data
        site.address = form.address.data
        site.city = form.address.data
        site.state = form.state.data
        site.zipcode = form.zipcode.data
        site.longitude = form.longitude.data
        site.latitude = form.latitude.data
        db.session.add(site)
        db.session.commit()
        flash("The site has been updated.")
        return redirect(url_for(".sites"))
    form.name.data = site.name
    form.address.data = site.address
    form.city.data = site.city
    form.state.data = site.state
    form.zipcode.data = site.zipcode
    form.longitude.data = site.longitude
    form.latitude.data = site.latitude
    return render_template("edit_site.html", form=form)


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


@main.route("/parameters/<search_description>", methods = ['GET'])
def parameters_search(search_description):
    parameters = SampleParameter.query.filter(SampleParameter.description.ilike(search_description + "%")).all()
    return render_template("parameters.html", parameters=parameters)


@main.route("/mediums")
def mediums():
    mediums = MediumCode.query.all()
    return render_template("mediums.html", mediums=mediums)
