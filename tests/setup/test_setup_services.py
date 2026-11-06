"""Install and uninstall of the per service profiles."""

from collective.translators import PACKAGE_NAME
from collective.translators.setuphandlers import HiddenProfiles
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from services import AVAILABLE
from services import MISSING
from services import SERVICES
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.dottedname.resolve import resolve
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest

import pytest


def product_id(service: str) -> str:
    return f"{PACKAGE_NAME}.{service}"


class TestServiceProfilesRegistration:
    def test_available_services_are_registered(self, setup_tool):
        """A service profile exists only when its library is importable."""
        registered = {info["id"] for info in setup_tool.listProfileInfo()}

        for service in AVAILABLE:
            assert f"{product_id(service)}:default" in registered
            assert f"{product_id(service)}:uninstall" in registered

    @pytest.mark.skipif(not MISSING, reason="every optional library is installed")
    def test_missing_services_are_not_registered(self, setup_tool):
        """No profile is registered for a service without its library."""
        registered = {info["id"] for info in setup_tool.listProfileInfo()}

        for service in MISSING:
            assert f"{product_id(service)}:default" not in registered

    def test_uninstall_profiles_are_hidden(self):
        """Only the install profiles show up in the add-ons control panel."""
        hidden = HiddenProfiles().getNonInstallableProfiles()

        for service in SERVICES:
            assert f"{product_id(service)}:uninstall" in hidden
            assert f"{product_id(service)}:default" not in hidden


@pytest.mark.parametrize("service", AVAILABLE)
class TestServiceInstall:
    @pytest.fixture(autouse=True)
    def installed(self, installer, service):
        installer.install_product(product_id(service))

    def test_product_installed(self, installer, service):
        assert installer.is_product_installed(product_id(service)) is True

    def test_base_profile_installed_as_dependency(self, installer):
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer_registered(self, browser_layers, service):
        layer = resolve(SERVICES[service]["layer"])

        assert layer in browser_layers

    def test_configlet_registered(self, controlpanel_actions, service):
        assert SERVICES[service]["action_id"] in controlpanel_actions

    def test_registry_records_created(self, service):
        registry = getUtility(IRegistry)
        schema = resolve(SERVICES[service]["schema"])

        assert registry.forInterface(schema).enabled is False

    def test_controlpanel_view_available(self, portal, service):
        """The view the configlet links to is registered for the own layer."""
        request = TestRequest()
        alsoProvides(request, resolve(SERVICES[service]["layer"]))
        view = queryMultiAdapter((portal, request), name=SERVICES[service]["action_id"])

        assert isinstance(view, RegistryEditForm)

    def test_controlpanel_view_needs_the_layer(self, portal, service):
        """Without the layer of the service the view is not available."""
        view = queryMultiAdapter(
            (portal, TestRequest()), name=SERVICES[service]["action_id"]
        )

        assert not isinstance(view, RegistryEditForm)


@pytest.mark.parametrize("service", AVAILABLE)
class TestServiceUninstall:
    @pytest.fixture(autouse=True)
    def uninstalled(self, installer, service):
        installer.install_product(product_id(service))
        installer.uninstall_product(product_id(service))

    def test_product_uninstalled(self, installer, service):
        assert installer.is_product_installed(product_id(service)) is False

    def test_browserlayer_removed(self, browser_layers, service):
        layer = resolve(SERVICES[service]["layer"])

        assert layer not in browser_layers

    def test_configlet_removed(self, controlpanel_actions, service):
        assert SERVICES[service]["action_id"] not in controlpanel_actions

    def test_registry_records_removed(self, service):
        registry = getUtility(IRegistry)
        prefix = SERVICES[service]["schema"]

        assert [key for key in registry.records if key.startswith(f"{prefix}.")] == []

    def test_base_profile_still_installed(self, installer):
        """Removing one service does not remove the shared base."""
        assert installer.is_product_installed(PACKAGE_NAME) is True


@pytest.mark.parametrize("service", sorted(SERVICES))
def test_configlet_id_matches_action_id(service):
    """plone.restapi looks the configlet up by its action_id."""
    panel = resolve(SERVICES[service]["panel"])

    assert panel.configlet_id == SERVICES[service]["action_id"]
