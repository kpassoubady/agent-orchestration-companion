import unittest

from channels.email import render_email
from channels.sms import render_sms

EVENT = {
    "order_id": "A100",
    "customer_name": "Riley",
    "carrier": "SwiftShip",
    "tracking_url": "https://track.example/A100",
}


class RendererTest(unittest.TestCase):
    def test_email_preserves_expected_content(self):
        result = render_email(EVENT)
        self.assertEqual(result["subject"], "Order A100 shipped")
        self.assertIn("Hello Riley", result["body"])
        self.assertIn(EVENT["tracking_url"], result["body"])

    def test_sms_preserves_expected_content(self):
        result = render_sms(EVENT)
        self.assertIn("order A100", result)
        self.assertIn("SwiftShip", result)
        self.assertLessEqual(len(result), 160)


if __name__ == "__main__":
    unittest.main()
