"""
This file (test_models.py) contains the unit tests for the models.py file.
"""


def test_new_facility(new_facility):
    """Test Facility model when a new Facility is created"""
    assert new_facility.name == "test site"
    assert new_facility.address == "1234 test rd."
    assert new_facility.city == "Test"
    assert new_facility.state == "OH"
    assert new_facility.zipcode == "12345"
    assert new_facility.longitude == -80.0
    assert new_facility.latitude == 40.0
