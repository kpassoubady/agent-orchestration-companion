CHANNEL_ORDER = ("email", "sms")


def enabled_channels(event):
    raise NotImplementedError("Implement preference-based channel selection")
