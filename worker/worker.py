import os
from celery import Celery
from sqlalchemy import create_engine, text
import requests


DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def evaluate(value, threshold):
    if value >= threshold["critical"]:
        return "critical"
    if value >= threshold["warning"]:
        return "warning"
    return "normal"


def send_alert(metric, status):
    if not DISCORD_WEBHOOK_URL:
        print("Missing DISCORD_WEBHOOK_URL")
        return

    msg = (
        f"🚨 ALERT [{status.upper()}]\n"
        f"Device: {metric['device_id']}\n"
        f"Metric: {metric['metric']}\n"
        f"Value: {metric['value']}\n"
        f"Time: {metric['timestamp']}"
    )

    requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": msg},
        timeout=5,
    )


@celery.task(name="worker.process_metric")
def process_metric(metric):
    metric_name = metric["metric"]
    value = metric["value"]

    with engine.begin() as conn:  # auto commit/rollback
        threshold = (
            conn.execute(
                text(
                    """
                    SELECT normal, warning, critical
                    FROM thresholds
                    WHERE metric = :metric
                    """
                ),
                {"metric": metric_name},
            )
            .mappings()
            .first()
        )

        if not threshold:
            print(f"No threshold for {metric_name}")
            return

        status = evaluate(value, threshold)

        conn.execute(
            text(
                """
                UPDATE alerts
                SET status = :status
                WHERE device_id = :device_id
                  AND metric = :metric
                  AND timestamp = :timestamp
                """
            ),
            {
                "status": status,
                "device_id": metric["device_id"],
                "metric": metric_name,
                "timestamp": metric["timestamp"],
            },
        )

    print(f"Processed {metric_name}={value} → {status}")

    if status in ("warning", "critical"):
        send_alert(metric, status)
