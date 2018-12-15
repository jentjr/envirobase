import psycopg2
import psycopg2.extras
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
    cur = conn.cursor()
    try:
        cur.execute("SELECT site_name, address, city, state, zipcode FROM SITE")
    except:
        print("Error executing select")
    sites = cur.fetchall()
    return render_template("site.html", sites=sites)

@app.route("/parameter")
def parameter():
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT param_cd, group_name, srsname, description, parameter_unit FROM sample_parameter")
    except:
        print("Error executing select")
    parameters = cur.fetchall()
    return render_template("parameter.html", parameters=parameters)
