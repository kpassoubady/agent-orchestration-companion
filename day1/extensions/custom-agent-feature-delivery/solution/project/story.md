# User Story: Respect Notification Preferences

As a shopper, I want shipment updates sent only through my selected channels so that I control how the retailer contacts me.

## Acceptance Criteria

1. When `preferred_channels` is absent, send both email and SMS notifications.
2. When it contains one supported channel, send only that notification.
3. When it contains both supported channels in any order, return notifications in canonical email-then-SMS order.
4. When it is an empty list, return no notifications.
5. Reject a non-list preference value or any unsupported channel with a `ValueError`.
6. Preserve required-field validation, renderer behavior, signatures, and the standard-library-only constraint.

## Ownership

The implementation agent may change only `preferences.py` and `router.py`. Agent definitions belong under `.claude/agents/`. Tests are an immutable acceptance contract.
