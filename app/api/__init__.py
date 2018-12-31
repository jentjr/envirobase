from flask import Blueprint

api = Blueprint("api", __name__)

from . import facilities, waste_units, storage_tanks
