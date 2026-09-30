"""Browser layer for the DeepSeek service."""

from collective.translators.interfaces import IBrowserLayer


class IDeepSeekLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.deepseek profile."""
