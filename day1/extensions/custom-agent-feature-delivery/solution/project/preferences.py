CHANNEL_ORDER = ("email", "sms")


def enabled_channels(event):
    requested = event.get("preferred_channels")
    if requested is None:
        return CHANNEL_ORDER
    if not isinstance(requested, list):
        raise ValueError("preferred_channels must be a list")
    unknown = sorted(set(requested) - set(CHANNEL_ORDER))
    if unknown:
        raise ValueError(f"Unsupported preferred channel: {', '.join(unknown)}")
    return tuple(channel for channel in CHANNEL_ORDER if channel in requested)
