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


@main.route("/sample_locations")
def sample_locations():
    sample_locations = SampleLocation.query.all()
    return render_template("sample_locations.html", sample_locations=sample_locations)


@main.route("/parameters")
def parameters():
    parameters = SampleParameter.query.all()
    return render_template("parameters.html", parameters=parameters)


@main.route("/sample_results")
def sample_results():
    """
	SELECT site.site_name, sample_location.location_id, sample_result.sample_date, 
	  sample_result.analysis_flag, sample_result.analysis_result, 
	  sample_result.analysis_unit, sample_result.detection_limit, 
	  sample_result.reporting_limit, sample_result.analysis_qualifier,
	  sample_parameter.description
	FROM site 
	  INNER JOIN sample_location 
	    ON site.site_id = sample_location.site_id
	  INNER JOIN sample_result
	    ON sample_location.location_id = sample_result.location_id
	  INNER JOIN sample_parameter
	    ON sample_result.param_cd = sample_parameter.param_cd
	"""
    sample_results = (
        Site.join(SampleLocation.site_id)
        .join(SampleResult.location_id)
        .join(SampleParameter.param_cd)
        .query.all()
    )
    return render_template("sample_results.html", sample_results=sample_results)
