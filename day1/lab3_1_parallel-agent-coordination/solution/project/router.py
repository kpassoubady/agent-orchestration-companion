"""Route approved shipment events to channel renderers."""

import json
from pathlib import Path

from channels.email import render_email
from channels.sms import render_sms

CHANNEL_ORDER = ("email", "sms")
SCHEMA_PATH = Path(__file__).parent / "schemas" / "shipment-event.json"


def validate_event(event):
    schema = json.loads(SCHEMA_PATH.read_text())
    missing = [field for field in schema["required"] if field not in event]
    if missing:
        raise ValueError(f"Missing shipment fields: {', '.join(missing)}")


def notify(event, enabled_channels=CHANNEL_ORDER):
    validate_event(event)
    renderers = {"email": render_email, "sms": render_sms}
    return {channel: renderers[channel](event) for channel in enabled_channels}
