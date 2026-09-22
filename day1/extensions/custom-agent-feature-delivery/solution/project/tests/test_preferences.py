import unittest

from router import notify

EVENT = {
    "order_id": "A100",
    "customer_name": "Riley",
    "carrier": "SwiftShip",
    "tracking_url": "https://track.example/A100",
}


class PreferenceRoutingTest(unittest.TestCase):
    def test_defaults_to_both_channels(self):
        self.assertEqual(list(notify(EVENT)), ["email", "sms"])

    def test_routes_only_to_selected_channel(self):
        event = {**EVENT, "preferred_channels": ["sms"]}
        self.assertEqual(list(notify(event)), ["sms"])

    def test_uses_canonical_order(self):
        event = {**EVENT, "preferred_channels": ["sms", "email"]}
        self.assertEqual(list(notify(event)), ["email", "sms"])

    def test_empty_preferences_disable_notifications(self):
        event = {**EVENT, "preferred_channels": []}
        self.assertEqual(notify(event), {})

    def test_rejects_unsupported_channel(self):
        event = {**EVENT, "preferred_channels": ["push"]}
        with self.assertRaisesRegex(ValueError, "Unsupported preferred channel: push"):
            notify(event)

    def test_rejects_non_list_preferences(self):
        event = {**EVENT, "preferred_channels": "sms"}
        with self.assertRaisesRegex(ValueError, "preferred_channels must be a list"):
            notify(event)

    def test_preserves_required_field_validation(self):
        event = {key: value for key, value in EVENT.items() if key != "tracking_url"}
        with self.assertRaisesRegex(ValueError, "tracking_url"):
            notify(event)


if __name__ == "__main__":
    unittest.main()
