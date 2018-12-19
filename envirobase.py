import os
from app import create_app, db
from app.models import Boring, MediumCode, SampleParameter, Site, SampleLocation, Unit, SampleResult, Well

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

