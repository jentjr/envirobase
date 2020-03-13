from setuptools import find_packages, setup

setup(
    name='envirobase',
    version='0.1.0',
    packages=find_packages(),
    include_package_date=True,
    install_requires=[
        'flask',
        'pyodbc',
        'pandas',
        'psycopg2',
        'flask_wtf',
        'flask_bootstrap',
        'flask_sqlalchemy',
        'flask_migrate',
        'geoalchemy2',
    ],
)