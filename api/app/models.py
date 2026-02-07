from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    device_id = Column(String)
    metric = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)
    status = Column(String)


class Threshold(Base):
    __tablename__ = "thresholds"

    metric = Column(String, primary_key=True)
    normal = Column(Float)
    warning = Column(Float)
    critical = Column(Float)
