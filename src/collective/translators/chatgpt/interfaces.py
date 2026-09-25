"""Browser layer for the ChatGPT service."""

from collective.translators.interfaces import IBrowserLayer


class IChatGPTLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.chatgpt profile."""
