import re


def render_sms(event):
    customer_name = re.sub(r"\s+", " ", str(event["customer_name"])).strip()
    carrier = re.sub(r"\s+", " ", str(event["carrier"])).strip()
    tracking_url = re.sub(r"\s+", "", str(event["tracking_url"]))
    message = f"{customer_name}: order {event['order_id']} shipped via {carrier}. {tracking_url}"
    return message[:160]
