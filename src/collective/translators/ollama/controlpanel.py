# from collective.translators import _
# import zope.schema
from collective.translators import _
from collective.translators.interfaces import IControlPanel
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


class IControlPanel(IControlPanel):
    pass
    # api_key = zope.schema.TextLine(
    #     title=_("API Key"),
    #     description=_("The API key for the DeepSeek service."),
    #     required=False,
    # )


class ControlPanel(controlpanel.RegistryEditForm):
    id = "OllamaControlPanel"
    label = _("Ollama Translation Service")
    schema = IControlPanel


@adapter(Interface, Interface)
class RegistryConfigletPanel(RegistryConfigletPanel):
    """Ollama control panel"""

    schema = IControlPanel
    schema_prefix = "ollama"
    configlet_id = "ollama-translator-controlpanel"
    configlet_category_id = "Products"
    title = _("Ollama Settings")
    group = "Products"
