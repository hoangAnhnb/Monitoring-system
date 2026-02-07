import os
from celery import Celery

celery_app = Celery(
    "monitoring",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)
