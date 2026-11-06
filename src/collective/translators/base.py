from plone import api
from zope.globalrequest import getRequest


class BaseTranslatorFactory:
    """Base factory class for translation services."""

    controlpanel_interface = None
    layer = None

    @property
    def order(self):
        if not self.controlpanel_interface:
            return 9999
        try:
            return api.portal.get_registry_record(
                name="order",
                interface=self.controlpanel_interface,
            )
        except KeyError:
            return 9999

    def is_available(self):
        """Check if the translation service is available.

        Verifies that:
        1. If a request is active and a browser layer is configured, the request provides the layer.
        2. The service is enabled in the registry.
        """
        request = getRequest()
        if request is not None and self.layer is not None:
            if not self.layer.providedBy(request):
                return False

        if not self.controlpanel_interface:
            return False

        try:
            return api.portal.get_registry_record(
                name="enabled",
                interface=self.controlpanel_interface,
            )
        except KeyError:
            return False

    def is_enabled(self):
        """Alias method for is_available."""
        return self.is_available()
