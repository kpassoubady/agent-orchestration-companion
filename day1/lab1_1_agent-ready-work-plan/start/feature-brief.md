# Feature Brief: Shipment Notifications

Customers need email and short-message updates when an order ships. Each notification must use the approved shipment event, respect saved channel preferences, and create an audit record. Existing platform services already handle authentication, rate limiting, and message delivery.

The work plan must cover the event contract, email rendering, short-message rendering, preference lookup, audit recording, and final router integration. Do not redesign platform infrastructure or implement the feature during this lab.

A human architect must approve the shipment-event schema before consumers begin. The integration owner must run the complete notification and security checks before handoff.
