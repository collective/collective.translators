from collective.translators import _
from collective.translators.interfaces import IControlPanel
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IChatGPTControlPanel(IControlPanel):
    """Control panel interface for ChatGPT translation service."""

    api_key = schema.TextLine(
        title=_("API Key"),
        description=_("The API key for the ChatGPT service."),
        required=False,
    )

    base_url = schema.TextLine(
        title=_("API Base URL"),
        description=_(
            "The base URL for the ChatGPT API (e.g., https://api.openai.com/v1). Leave empty to use default."
        ),
        required=False,
    )

    model = schema.TextLine(
        title=_("Model"),
        description=_(
            "The ChatGPT model to use (e.g., gpt-4o, gpt-4-turbo, gpt-3.5-turbo)."
        ),
        default="gpt-3.5-turbo",
        required=False,
    )

    temperature = schema.Float(
        title=_("Temperature"),
        description=_(
            "Controls randomness: 0 for deterministic, higher values for more random. Value between 0 and 2."
        ),
        default=0.3,
        min=0.0,
        max=2.0,
        required=False,
    )

    max_tokens = schema.Int(
        title=_("Max Tokens"),
        description=_(
            "Maximum number of tokens to generate in the translation response."
        ),
        default=1000,
        required=False,
    )


class ChatGPTControlPanel(controlpanel.RegistryEditForm):
    id = "ChatGPTControlPanel"
    label = _("ChatGPT Translation Service")
    schema = IChatGPTControlPanel


@adapter(Interface, Interface)
class ChatGPTRegistryConfigletPanel(RegistryConfigletPanel):
    """ChatGPT control panel adapter."""

    schema = IChatGPTControlPanel
    schema_prefix = "chatgpt"
    configlet_id = "chatgpt-controlpanel"
    configlet_category_id = "Products"
    title = _("ChatGPT Settings")
    group = "Products"
