import json
import psycopg2
from psycopg2.extras import DictCursor
from config import config
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request

bootstrap = Bootstrap()

app = Flask(__name__)
bootstrap.init_app(app)

def connect_db():
    try:
        print("Connecting to database...")
        params = config(filename="database.ini", section="postgresql")
        return psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sites")
def sites():
    conn = connect_db()
    cur = conn.cursor(cursor_factory = DictCursor)
    try:
        cur.execute(
            """
            SELECT row_to_json(fc)
              FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features
              FROM (SELECT 'Feature' AS type
                 , ST_AsGeoJSON(sg.site_geog)::json AS geometry
                 , row_to_json((SELECT s FROM (SELECT site_id, site_name, address, city, state, zipcode) AS s
                    )) AS properties
               FROM site AS sg   ) AS f )  AS fc
            """
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    sites = cur.fetchall()
    sites = sites[0][0]
    return render_template("sites.html", sites=sites)

@app.route("/sample_locations")
def sample_locations():
    conn = connect_db()
    cur = conn.cursor(cursor_factory = DictCursor)
    try:
        cur.execute(
            """
            SELECT row_to_json(fc)
              FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features
              FROM (SELECT 'Feature' AS type
                 , ST_AsGeoJSON(sg.location_geog)::json AS geometry
                 , row_to_json((SELECT sl FROM (SELECT location_id, location_type) AS sl
                    )) AS properties
               FROM sample_location AS sg   ) AS f )  AS fc
            """
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    sample_locations = cur.fetchall()
    sample_locations = sample_locations[0][0]
    return render_template("sample_locations.html", sample_locations=sample_locations)

@app.route("/parameters")
def parameters():
    conn = connect_db()
    cur = conn.cursor(cursor_factory = DictCursor)
    try:
        cur.execute("SELECT param_cd, group_name, srsname, description, parameter_unit FROM sample_parameter")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    parameters = cur.fetchall()
    return render_template("parameters.html", parameters=parameters)
	

@app.route("/sample_results")
def sample_results():
    conn = connect_db()
    cur = conn.cursor(cursor_factory = DictCursor)
    try:
        cur.execute("""
		        SELECT site.site_name, sample_location.location_id, sample_result.sample_date, 
				    sample_result.analysis_flag, sample_result.analysis_result, 
				    sample_result.analysis_unit, sample_result.detection_limit, 
					sample_result.prac_quant_limit, sample_result.analysis_qualifier,
					sample_parameter.description
		        FROM site 
				    INNER JOIN sample_location 
				        ON site.site_id = sample_location.site_id
				    INNER JOIN sample_result
					    ON sample_location.location_id = sample_result.location_id
					INNER JOIN sample_parameter
					    ON sample_result.param_cd = sample_parameter.param_cd
				 """)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    sample_results = cur.fetchall()
    return render_template("sample_results.html", sample_results=sample_results)

if __name__ == '__main__':
    app.run(debug=True)
