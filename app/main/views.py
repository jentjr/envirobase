from . import main
from datetime import datetime
from .forms import SiteForm
from .. import db
from ..models import Site, Unit
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response


@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/site/<name>', methods=['GET', 'POST'])
def site():
    return render_template('site.html', name=name)



