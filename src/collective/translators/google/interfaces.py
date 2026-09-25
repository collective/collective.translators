"""Browser layer for the Google Translate service."""

from collective.translators.interfaces import IBrowserLayer


class IGoogleLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.google profile."""
