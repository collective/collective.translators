"""Module where all interfaces, events and exceptions live."""

from collective.translators import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IControlPanel(Interface):
    enabled = schema.Bool(
        title=_("Enabled"),
        description=_(
            "If enabled this service will be enabled used to get the translations."
        ),
        required=False,
        default=True,
    )
    order = schema.Int(
        title=_("Order"),
        description=_(
            "Ordering of this service. The lower the sooner this service will be used."
        ),
        default=30,
        required=True,
    )
    source_languages = schema.List(
        title=_("Source languages"),
        description=_("Select which source languages does this service allow"),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.AvailableContentLanguages"
        ),
    )
    target_languages = schema.List(
        title=_("Target languages"),
        description=_("Select which target languages does this service allow"),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.AvailableContentLanguages"
        ),
    )
