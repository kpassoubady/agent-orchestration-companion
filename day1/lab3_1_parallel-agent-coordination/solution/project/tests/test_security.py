import unittest

from channels.email import render_email
from channels.sms import render_sms

UNTRUSTED_EVENT = {
    "order_id": "A100",
    "customer_name": "<script>alert('x')</script>",
    "carrier": "Swift\nShip",
    "tracking_url": "https://track.example/A100",
}


class ChannelSecurityTest(unittest.TestCase):
    def test_email_escapes_untrusted_html(self):
        body = render_email(UNTRUSTED_EVENT)["body"]
        self.assertNotIn("<script>", body)
        self.assertIn("&lt;script&gt;", body)

    def test_sms_normalizes_control_whitespace(self):
        message = render_sms(UNTRUSTED_EVENT)
        self.assertNotIn("\n", message)
        self.assertIn("Swift Ship", message)


if __name__ == "__main__":
    unittest.main()
