from pydantic import BaseModel
from datetime import datetime


class MetricIn(BaseModel):
    device_id: str
    metric: str
    value: float
    timestamp: datetime


class ThresholdIn(BaseModel):
    metric: str
    normal: float
    warning: float
    critical: float
