import os
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import (
    Boring,
    MediumCode,
    SampleParameter,
    Facility,
    StorageTank,
    UndergroundStorageTank,
    AbovegroundStorageTank,
    SampleId,
    WasteUnit,
    Landfill,
    Impoundment,
    SampleResult,
    Piezometer,
    MonitoringWell,
)

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Facility=Facility,
        SampleParameter=SampleParameter,
        SampleId=SampleId,
        WasteUnit=WasteUnit,
        Landfill=Landfill,
        Impoundment=Impoundment,
        StorageTank=StorageTank,
        AbovegroundStorageTank=AbovegroundStorageTank,
        UndergroundStorageTank=UndergroundStorageTank,
        Piezometer=Piezometer,
        MonitoringWell=MonitoringWell,
        Boring=Boring,
        MediumCode=MediumCode,
    )
