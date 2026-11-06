"""Browser layer for the AWS Translate service."""

from collective.translators.interfaces import IBrowserLayer


class IAWSLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.aws profile."""
