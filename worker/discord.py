import os
import requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord(message: str):
    if not WEBHOOK_URL:
        raise RuntimeError("Missing DISCORD_WEBHOOK_URL")

    requests.post(WEBHOOK_URL, json={"content": message}, timeout=5)
