from collective.translators import _
from collective.translators.interfaces import IControlPanel
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IAWSTranslateControlPanel(IControlPanel):
    access_key = schema.TextLine(
        title=_("Access key"),
        description=_("The key for the access to AWS Translate service."),
        required=False,
    )
    secret_key = schema.TextLine(
        title=_("Secret key"),
        description=_("The secret key for the access to AWS Translate service."),
        required=False,
    )
    region_name = schema.TextLine(
        title=_("Region"),
        description=_("The region for the AWS Translate service."),
        required=True,
        default="eu-west-3",
    )


class AWSTranslateControlPanel(controlpanel.RegistryEditForm):
    id = "AWSTranslateControlPanel"
    label = _("AWS Translate Service")
    schema = IAWSTranslateControlPanel


@adapter(Interface, Interface)
class AWSTranslateRegistryConfigletPanel(RegistryConfigletPanel):
    """AWS Translate control panel"""

    schema = IAWSTranslateControlPanel
    schema_prefix = "aws_translate"
    configlet_id = "aws-translator-controlpanel"
    configlet_category_id = "Products"
    title = _("AWS Translate Settings")
    group = "Products"
