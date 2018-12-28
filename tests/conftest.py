import os
import pytest
from app import create_app, db
from app.models import Facility


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
    facility1 = Facility(
        name="test site 1",
        address="1234 test rd.",
        city="Test",
        state="OH",
        zipcode="12345",
        longitude=-80.0,
        latitude=40.0,
    )
    facility2 = Facility(
        name="test site 2",
        address="1234 pytest rd.",
        city="Test",
        state="IN",
        zipcode="12345",
        longitude=-81.0,
        latitude=41.0,
    )
    db.session.add(facility1)
    db.session.add(facility2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="module")
def new_facility():
    facility = Facility(
        name="test site",
        address="1234 test rd.",
        city="Test",
        state="OH",
        zipcode="12345",
        longitude=-80.0,
        latitude=40.0,
    )
    return facility
