import unittest

from channels.sms import render_sms

EVENT = {
    "order_id": "A100",
    "customer_name": "Riley",
    "carrier": "SwiftShip",
    "tracking_url": "https://track.example/A100",
}


class SmsRendererTest(unittest.TestCase):
    def test_renders_bounded_message(self):
        result = render_sms(EVENT)
        self.assertIn("Order A100 shipped", result)
        self.assertIn("SwiftShip", result)
        self.assertIn(EVENT["tracking_url"], result)
        self.assertLessEqual(len(result), 160)


if __name__ == "__main__":
    unittest.main()
