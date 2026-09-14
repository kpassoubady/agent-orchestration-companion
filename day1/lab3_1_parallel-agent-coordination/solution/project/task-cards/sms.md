# SMS Renderer Task

Objective: Render a safe shipment short message from the locked version 1 event schema.

Owned files:

- `channels/sms.py`
- `handoffs/sms.json`

Do not edit `router.py`, `schemas/`, `tests/`, email files, dependencies, or project configuration.

Acceptance:

```bash
python3 -m unittest tests.test_sms tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace
```

The message must identify the order, carrier, and tracking address, contain no control newlines, and remain within 160 characters. Commit the implementation before recording its commit and evidence in the handoff.
