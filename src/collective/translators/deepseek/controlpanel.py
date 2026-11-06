from collective.translators import _
from collective.translators.interfaces import IControlPanel
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IDeepSeekControlPanel(IControlPanel):
    api_key = schema.TextLine(
        title=_("API Key"),
        description=_("The API key for the DeepSeek service."),
        required=False,
    )


class DeepSeekControlPanel(controlpanel.RegistryEditForm):
    id = "DeepSeekControlPanel"
    label = _("DeepSeek Translation Service")
    schema = IDeepSeekControlPanel


@adapter(Interface, Interface)
class DeepSeekRegistryConfigletPanel(RegistryConfigletPanel):
    """DeepSeek control panel"""

    schema = IDeepSeekControlPanel
    schema_prefix = "deepseek"
    configlet_id = "deepseek-translator-controlpanel"
    configlet_category_id = "Products"
    title = _("DeepSeek Settings")
    group = "Products"
