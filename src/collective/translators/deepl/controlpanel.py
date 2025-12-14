from collective.translators import _
from collective.translators.interfaces import IControlPanel
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface

import zope.schema


class IDeeplControlPanel(IControlPanel):
    api_key = zope.schema.TextLine(
        title=_("API Key"),
        description=_("The API key for the Deepl translation service."),
        required=False,
    )

    use_pro = zope.schema.Bool(
        title=_("Use the Pro API?"),
        description=_("If disabled it will use the free API."),
        default=False,
        required=False,
    )

    autodetect_source_language = zope.schema.Bool(
        title=_("Auto detect the source language?"),
        description=_("If enabled the source language will be autodetected."),
        default=False,
        required=False,
    )


class DeeplControlPanel(controlpanel.RegistryEditForm):
    id = "DeeplControlPanel"
    label = _("Deepl Translation Service")
    schema = IDeeplControlPanel


@adapter(Interface, Interface)
class DeeplRegistryConfigletPanel(RegistryConfigletPanel):
    """Deepl control panel"""

    schema = IDeeplControlPanel
    schema_prefix = "deepl"
    configlet_id = "deepl-controlpanel"
    configlet_category_id = "Products"
    title = _("Deepl Settings")
    group = "Products"
