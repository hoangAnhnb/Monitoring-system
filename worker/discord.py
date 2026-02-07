import os
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


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
