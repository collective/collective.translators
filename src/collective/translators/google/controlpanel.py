from collective.translators import _
from collective.translators.interfaces import IControlPanel
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IGoogleTranslateControlPanel(IControlPanel):
    api_key = schema.TextLine(
        title=_("API Key"),
        description=_("The API key for the Goole Translate service."),
        required=False,
    )


class GoogleTranslateControlPanel(controlpanel.RegistryEditForm):
    id = "GoogleTranslateControlPanel"
    label = _("Google Translate Translation Service")
    schema = IGoogleTranslateControlPanel


@adapter(Interface, Interface)
class GoogleTranslateRegistryConfigletPanel(RegistryConfigletPanel):
    """Google Translate control panel"""

    schema = IGoogleTranslateControlPanel
    schema_prefix = "google-translate"
    configlet_id = "google-translate-controlpanel"
    configlet_category_id = "Products"
    title = _("Google Translate Settings")
    group = "Products"
