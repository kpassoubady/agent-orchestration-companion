import unittest

from channels.email import render_email

EVENT = {
    "order_id": "A100",
    "customer_name": "Riley",
    "carrier": "SwiftShip",
    "tracking_url": "https://track.example/A100",
}


class EmailRendererTest(unittest.TestCase):
    def test_renders_subject_and_body(self):
        result = render_email(EVENT)
        self.assertEqual(result["subject"], "Order A100 shipped")
        self.assertIn("Hello Riley", result["body"])
        self.assertIn("SwiftShip", result["body"])
        self.assertIn(EVENT["tracking_url"], result["body"])


if __name__ == "__main__":
    unittest.main()
