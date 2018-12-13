from . import main
from .forms import SiteForm
from .. import db
from ..models import Site, Unit
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response


@main.route('/', methods=['GET', 'POST'])
def index():
    form  = SiteForm()
    return render_template('index.html', form=form)



