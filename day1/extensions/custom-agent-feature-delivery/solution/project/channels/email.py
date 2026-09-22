from html import escape


def render_email(event):
    order_id = escape(str(event["order_id"]))
    customer_name = escape(str(event["customer_name"]))
    carrier = escape(str(event["carrier"]))
    tracking_url = escape(str(event["tracking_url"]), quote=True)
    return {
        "subject": f"Order {order_id} shipped",
        "body": f"Hello {customer_name}, your order shipped via {carrier}. Track it at {tracking_url}",
    }
