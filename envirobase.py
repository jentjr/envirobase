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


@app.route("/site")
def site():
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
    return render_template("site.html", sites=sites)

@app.route("/parameter")
def parameter():
    conn = connect_db()
    cur = conn.cursor(cursor_factory = DictCursor)
    try:
        cur.execute("SELECT param_cd, group_name, srsname, description, parameter_unit FROM sample_parameter")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    parameters = cur.fetchall()
    return render_template("parameter.html", parameters=parameters)
