"""Browser layer for the DeepL service."""

from collective.translators.interfaces import IBrowserLayer


class IDeeplLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.deepl profile."""
