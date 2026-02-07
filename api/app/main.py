from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Alert, Threshold
from .schemas import MetricIn, ThresholdIn
from .celery_app import celery_app

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/thresholds")
def set_threshold(data: ThresholdIn, db: Session = Depends(get_db)):
    t = Threshold(**data.dict())
    db.merge(t)
    db.commit()
    return {"message": "threshold saved"}


@app.post("/metrics")
def ingest_metric(data: MetricIn, db: Session = Depends(get_db)):
    alert = Alert(
        device_id=data.device_id,
        metric=data.metric,
        value=data.value,
        timestamp=data.timestamp,
        status="pending",
    )
    db.add(alert)
    db.commit()

    celery_app.send_task("worker.process_metric", args=[data.dict()])
    return {"message": "metric received"}
