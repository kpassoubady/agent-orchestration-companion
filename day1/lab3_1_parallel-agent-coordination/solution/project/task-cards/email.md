# Email Renderer Task

Objective: Render safe shipment email content from the locked version 1 event schema.

Owned files:

- `channels/email.py`
- `handoffs/email.json`

Do not edit `router.py`, `schemas/`, `tests/`, SMS files, dependencies, or project configuration.

Acceptance:

```bash
python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html
```

The subject must identify the order, the body must include customer, carrier, and tracking data, and untrusted HTML must be escaped. Commit the implementation before recording its commit and evidence in the handoff.
