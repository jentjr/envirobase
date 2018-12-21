import os
import pytest
from app import create_app, db
from app.models import Site


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(os.getenv("FLASK_CONFIG") or "default")

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert Site data
    site1 = Site(
        site_name="test site 1",
        address="1234 test rd.",
        city="Test",
        state="OH",
        zipcode="12345",
        site_geog="POINT(-80.0, 40.0)",
    )
    site2 = Site(
        site_name="test site 2",
        address="1234 pytest rd.",
        city="Test",
        state="IN",
        zipcode="12345",
        site_geog="POINT(-81.0, 41.0)",
    )
    db.session.add(site1)
    db.session.add(site2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="module")
def new_site():
    site = Site(
        site_name="test site",
        address="1234 test rd.",
        city="Test",
        state="OH",
        zipcode="12345",
        site_geog="POINT(-80.0, 40.0)",
    )
    return site
