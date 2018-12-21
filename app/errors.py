""" Error classes for USGS Paremeter Codes"""


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AlreadyExistsError(Error):
    """Raises an error when data already exists"""

    def __init__(self, *args, **kwargs):
        Error.__init__(self, *args, **kwargs)
