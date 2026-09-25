"""Browser layer for the LibreTranslate service."""

from collective.translators.interfaces import IBrowserLayer


class ILibreTranslateLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.libretranslate profile."""
