"""
This file (test_models.py) contains the unit tests for the models.py file.
"""


def test_new_site(new_site):
    """Test Site model when a new Site is created"""
    assert new_site.site_name == 'test site'
    assert new_site.address == '1234 test rd.'
    assert new_site.city == 'Test'
    assert new_site.state == 'OH'
    assert new_site.zipcode == '12345'