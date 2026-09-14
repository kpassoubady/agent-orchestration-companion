"""Render shipment events for the short-message channel."""

MAX_LENGTH = 160


def render_sms(event):
    values = {key: " ".join(str(value).split()) for key, value in event.items()}
    message = (
        f"Order {values['order_id']} shipped via {values['carrier']}. "
        f"Track: {values['tracking_url']}"
    )
    return message[:MAX_LENGTH]
