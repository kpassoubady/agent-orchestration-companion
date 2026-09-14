import unittest

from router import notify

EVENT = {
    "order_id": "A100",
    "customer_name": "Riley",
    "carrier": "SwiftShip",
    "tracking_url": "https://track.example/A100",
}


class NotificationIntegrationTest(unittest.TestCase):
    def test_routes_to_both_channels(self):
        result = notify(EVENT)
        self.assertEqual(set(result), {"email", "sms"})

    def test_rejects_incomplete_event(self):
        with self.assertRaisesRegex(ValueError, "tracking_url"):
            notify({key: value for key, value in EVENT.items() if key != "tracking_url"})


if __name__ == "__main__":
    unittest.main()
