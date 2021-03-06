from flask import render_template, url_for, redirect, current_app, flash, request
from . import main
from .. import db
from .forms import FacilityForm, StorageTankForm, WasteUnitForm, WellForm
from ..models import (
    Boring,
    MediumCode,
    SampleParameter,
    Facility,
    WasteUnit,
    Landfill,
    Impoundment,
    StorageTank,
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
    return render_template("facilities.html", facilities=facilities)


@main.route("/facilities/<int:facility_id>", methods=["GET"])
def facility_by_id(facility_id):
    facilities = Facility.query.filter_by(facility_id=facility_id)
    return render_template("facilities.html", facilities=facilities)


@main.route("/facilities/<name>", methods=["GET"])
def facility_by_name(name):
    facilities = Facility.query.filter(Facility.name.ilike("%" + name + "%")).all()
    return render_template("facilities.html", facilities=facilities)


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
            return redirect(url_for(".facilities"))
        else:
            flash("The facility already exists.")
    return render_template("edit_facility.html", form=form)


@main.route("/edit-facility/<int:facility_id>", methods=["GET", "POST"])
def edit_facility_id(facility_id):
    facility = Facility.query.get_or_404(facility)
    form = FacilityForm()
    if form.validate_on_submit():
        facility.name = form.name.data
        facility.address = form.address.data
        facility.city = form.address.data
        facility.state = form.state.data
        facility.zipcode = form.zipcode.data
        facility.longitude = form.longitude.data
        facility.latitude = form.latitude.data
        db.session.add(facility)
        db.session.commit()
        flash("The facility has been updated.")
        return redirect(url_for(".facilities"))
    form.name.data = facility.name
    form.address.data = facility.address
    form.city.data = facility.cityieldWaterQualityForm
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
        facility.name = form.name.data
        facility.address = form.address.data
        facility.city = form.address.data
        facility.state = form.state.data
        facility.zipcode = form.zipcode.data
        facility.longitude = form.longitude.data
        facility.latitude = form.latitude.data
        db.session.add(facility)
        db.session.commit()
        flash("The facility has been updated.")
        return redirect(url_for(".facilities"))
    form.name.data = facility.name
    form.address.data = facility.address
    form.city.data = facility.city
    form.state.data = facility.state
    form.zipcode.data = facility.zipcode
    form.longitude.data = facility.longitude
    form.latitude.data = facility.latitude
    return render_template("edit_facility.html", form=form)


@main.route("/storage-tanks")
def storage_tanks():
    storage_tanks = StorageTank.query.all()
    return render_template("storage_tanks.html", storage_tanks=storage_tanks)


@main.route("/facilities/<int:facility_id>/add-storage-tank", methods=["GET", "POST"])
def add_storage_tank(facility_id):
    form = StorageTankForm()
    if form.validate_on_submit():
        tank_registration_id = StorageTank.query.filter_by(
            tank_registration_id=form.tank_registration_id.data, facility_id=facility_id
        ).first()
        if tank_registration_id is None:
            storage_tank = StorageTank(
                facility_id=facility_id,
                tank_registration_id=form.tank_registration_id.data,
                capacity=form.capacity.data,
                stored_substance=form.stored_substance.data,
                status=form.status.data,
                tank_type=form.tank_type.data,
                longitude=form.longitude.data,
                latitude=form.latitude.data,
            )
            db.session.add(storage_tank)
            db.session.commit()
            return redirect(url_for(".storage_tanks"))
        else:
            flash("The storage tank already exists.")
    return render_template("edit_storage_tank.html", form=form)


@main.route("/underground-tanks")
def underground_tanks():
    underground_tanks = UndergroundStorageTank.query.all()
    return render_template(
        "underground_tanks.html", underground_tanks=underground_tanks
    )


@main.route("/aboveground-tanks")
def aboveground_tanks():
    aboveground_tanks = AbovegroundStorageTank.query.all()
    return render_template(
        "aboveground_tanks.html", aboveground_tanks=aboveground_tanks
    )


@main.route("/waste-units")
def waste_units():
    waste_units = WasteUnit.query.all()
    return render_template("waste_units.html", waste_units=waste_units)


@main.route("/facilities/<int:facility_id>/add-waste-unit", methods=["GET", "POST"])
def add_waste_unit(facility_id):
    form = WasteUnitForm()
    if form.validate_on_submit():
        name = WasteUnit.query.filter_by(
            name=form.name.data, facility_id=facility_id
        ).first()
        if name is None:
            waste_unit = WasteUnit(
                facility_id=facility_id,
                name=form.name.data,
                constructed_date=form.constructed_date.data,
                unit_type=form.unit_type.data,
            )
            db.session.add(waste_unit)
            db.session.commit()
            return redirect(url_for(".waste_units"))
        else:
            flash("The waste unit already exists.")
    return render_template("edit_waste_unit.html", form=form)


@main.route("/landfills")
def landfills():
    landfills = Landfill.query.all()
    return render_template("landfills.html", landfills=landfills)


@main.route("/impoundments")
def impoundments():
    impoundments = Impoundment.query.all()
    return render_template("impoundments.html", impoundments=impoundments)


@main.route("/sample-ids")
def sample_ids():
    sample_ids = SampleId.query.all()
    return render_template("sample_ids.html", sample_ids=sample_ids)

    
@main.route("/wells")
def wells():
    wells = Well.query.all()
    return render_template("wells.html", wells=wells)
    
 
@main.route("/facilities/<int:facility_id>/wells", methods=["GET"])
def facility_wells(facility_id):
    wells = Well.query.filter_by(facility_id=facility_id).all()
    return render_template("wells.html", wells=wells)
 
 
@main.route("/facilities/<int:facility_id>/add-well", methods=["GET", "POST"])
def add_well(facility_id):
    form = WellForm()
    if form.validate_on_submit():
        well_id = Well.query.filter_by(
            well_id=form.well_id.data, facility_id=facility_id
        ).first()
        if well_id is None:
            well = Well(
                facility_id=facility_id,
                well_id=form.well_id.data,
                well_type=form.well_type.data,
                longitude=form.longitude.data,
                latitude=form.latitude.data,
                installation_date=form.installation_date.data,
                abandoned_date=form.abandoned_date.data,
                top_riser=form.top_riser.data,
                top_bent_seal=form.top_bent_seal.data,
                top_gravel_pack=form.top_gravel_pack.data,
                top_screen=form.top_screen.data,
            )
            db.session.add(well)
            db.session.commit()
            return redirect(url_for(".wells"))
        else:
            flash("The well already exists.")
    return render_template("edit_well.html", form=form)
    
@main.route("/facilities/<int:facility_id>/well/<int:sample_id>", methods=["GET", "POST"])
def edit_well(facility_id, sample_id):
    well = Well.query.get_or_404((facility_id, sample_id))
    form = WellForm()
    if form.validate_on_submit():
        facility_id=facility_id
        well_id=form.well_id.data
        well_type=form.well_type.data
        longitude=form.longitude.data
        latitude=form.latitude.data
        installation_date=form.installation_date.data
        abandoned_date=form.abandoned_date.data
        top_riser=form.top_riser.data
        top_bent_seal=form.top_bent_seal.data
        top_gravel_pack=form.top_gravel_pack.data
        top_screen=form.top_screen.data
        db.session.add(well)
        db.session.commit()
        flash("The well has been updated.")
        return redirect(url_for(".wells"))
    facility_id=facility_id
    well_id=form.well_id.data
    well_type=form.well_type.data
    longitude=form.longitude.data
    latitude=form.latitude.data
    installation_date=form.installation_date.data
    abandoned_date=form.abandoned_date.data
    top_riser=form.top_riser.data
    top_bent_seal=form.top_bent_seal.data
    top_gravel_pack=form.top_gravel_pack.data
    top_screen=form.top_screen.data
    return render_template("edit_well.html", form=form)   

    
@main.route("/sample-results")
def sample_results():
    sample_results = SampleResult.query.all()
    return render_template("sample_results.html", sample_results=sample_results)


@main.route("/parameters")
def parameters():
    page = request.args.get("page", 1, type=int)
    pagination = SampleParameter.query.paginate(
        page, per_page=current_app.config["ENVIROBASE_PER_PAGE"], error_out=False
    )
    parameters = pagination.items
    return render_template(
        "parameters.html", parameters=parameters, pagination=pagination
    )


@main.route("/parameters/<search_description>", methods=["GET"])
def parameters_search(search_description):
    page = request.args.get("page", 1, type=int)
    pagination = SampleParameter.query.filter(
        SampleParameter.description.ilike("%" + search_description + "%")
    ).paginate(
        page, per_page=current_app.config["ENVIROBASE_PER_PAGE"], error_out=False
    )
    parameters = pagination.items
    return render_template(
        "parameters.html", parameters=parameters, pagination=pagination
    )


@main.route("/mediums")
def mediums():
    page = request.args.get("page", 1, type=int)
    pagination = MediumCode.query.paginate(
        page, per_page=current_app.config["ENVIROBASE_PER_PAGE"], error_out=False
    )
    mediums = pagination.items
    return render_template("mediums.html", mediums=mediums, pagination=pagination)


@main.route("/mediums/<search_description>", methods=["GET"])
def mediums_search(search_description):
    page = request.args.get("page", 1, type=int)
    pagination = MediumCode.query.filter(
        MediumCode.medium_name.ilike("%" + search_description + "%")
    ).paginate(
        page, per_page=current_app.config["ENVIROBASE_PER_PAGE"], error_out=False
    )
    mediums = pagination.items
    return render_template("mediums.html", mediums=mediums, pagination=pagination)
