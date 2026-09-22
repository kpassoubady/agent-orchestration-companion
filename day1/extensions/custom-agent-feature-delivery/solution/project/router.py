from channels.email import render_email
from channels.sms import render_sms
from preferences import enabled_channels

REQUIRED_FIELDS = ("order_id", "customer_name", "carrier", "tracking_url")


def validate_event(event):
    missing = [field for field in REQUIRED_FIELDS if field not in event]
    if missing:
        raise ValueError(f"Missing shipment fields: {', '.join(missing)}")


def notify(event):
    validate_event(event)
    renderers = {"email": render_email, "sms": render_sms}
    return {channel: renderers[channel](event) for channel in enabled_channels(event)}
