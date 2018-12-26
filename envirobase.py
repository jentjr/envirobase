import os
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import (
    Boring,
    MediumCode,
    SampleParameter,
    Site,
    SampleId,
    Unit,
    SampleResult,
    Well,
)

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Site=Site,
        SampleParameter=SampleParameter,
        SampleId=SampleId,
        Unit=Unit,
        Well=Well,
        Boring=Boring,
        MediumCode=MediumCode,
    )
