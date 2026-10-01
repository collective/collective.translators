"""Migration from the single monolithic profile to one profile per service."""

from collective.translators import PACKAGE_NAME
from collective.translators.interfaces import IBrowserLayer
from collective.translators.setuphandlers import HiddenProfiles
from plone.browserlayer.utils import register_layer
from plone.browserlayer.utils import registered_layers
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from services import AVAILABLE
from services import MISSING
from services import SERVICES
from zope.component import getUtility
from zope.dottedname.resolve import resolve

import pytest

API_KEY = "a-key-the-upgrade-must-not-touch"


def api_key_record(service: str) -> str:
    return f"{SERVICES[service]['schema']}.api_key"


@pytest.fixture
def old_state(portal, setup_tool):
    """Rebuild what the 1000 profile used to leave in a site.

    Every service had its records in the registry and its configlet in
    ``portal_controlpanel``, whether its library was installed or not, and the
    add-on registered a single shared browser layer.
    """
    registry = getUtility(IRegistry)
    controlpanel = portal.portal_controlpanel

    for service, info in SERVICES.items():
        registry.records[api_key_record(service)] = Record(
            field.TextLine(title="API Key"), API_KEY
        )
        controlpanel.registerConfiglet(
            id=info["action_id"],
            name=service,
            action=f"string:${{portal_url}}/@@{info['action_id']}",
            category="Products",
            appId=info["action_id"],
            permission="Manage portal",
        )

    if IBrowserLayer not in registered_layers():
        register_layer(IBrowserLayer, name=PACKAGE_NAME)

    for service in AVAILABLE:
        setup_tool.unsetLastVersionForProfile(f"{PACKAGE_NAME}.{service}:default")
    setup_tool.setLastVersionForProfile(f"{PACKAGE_NAME}:default", "1000")
    return setup_tool


class TestUpgradeIsOffered:
    """The add-ons control panel must lead the integrator to the upgrade."""

    def test_base_profile_is_visible_while_the_upgrade_is_pending(self, old_state):
        """The base profile comes out of hiding exactly when it has work to do."""
        hidden = HiddenProfiles().getNonInstallableProfiles()

        assert f"{PACKAGE_NAME}:default" not in hidden

    def test_upgrade_is_listed(self, old_state, portal, grant_roles):
        """A site left at 1000 sees the upgrade at /prefs_install_products_form.

        ``marshall_addons`` skips a hidden profile before it builds the entry
        of its product, so a hidden base profile would keep its upgrade steps
        out of this list.
        """
        grant_roles(portal, ["Manager"])
        view = portal.restrictedTraverse("@@prefs_install_products_form")
        upgrades = [addon["id"] for addon in view.get_upgrades()]

        assert PACKAGE_NAME in upgrades

    def test_upgrade_reports_the_new_version(self, old_state, installer):
        info = installer.upgrade_info(PACKAGE_NAME)

        assert info["installedVersion"] == "1000"
        assert info["newVersion"] == "1002"
        assert info["required"] is True
        assert info["available"] is True


class TestUpgradeTo1001:
    @pytest.fixture(autouse=True)
    def upgraded(self, old_state):
        """Run the step the way portal_setup runs it.

        Calling the handler directly would leave the profile at 1000, and it
        would not prove that the step is registered for this profile.
        """
        old_state.upgradeProfile(f"{PACKAGE_NAME}:default")

    @pytest.mark.parametrize("service", AVAILABLE)
    def test_available_service_keeps_its_settings(self, service):
        """The upgrade must not overwrite the configured API keys."""
        registry = getUtility(IRegistry)

        assert registry.records[api_key_record(service)].value == API_KEY

    @pytest.mark.parametrize("service", AVAILABLE)
    def test_available_service_profile_is_marked_installed(self, service, installer):
        assert installer.is_product_installed(f"{PACKAGE_NAME}.{service}") is True

    @pytest.mark.parametrize("service", AVAILABLE)
    def test_available_service_keeps_its_configlet(self, service, controlpanel_actions):
        assert SERVICES[service]["action_id"] in controlpanel_actions

    @pytest.mark.parametrize("service", AVAILABLE)
    def test_available_service_layer_is_registered(self, service, browser_layers):
        layer = resolve(SERVICES[service]["layer"])

        assert layer in browser_layers

    @pytest.mark.parametrize("service", MISSING)
    def test_missing_service_records_are_purged(self, service):
        registry = getUtility(IRegistry)

        assert api_key_record(service) not in registry.records

    @pytest.mark.parametrize("service", MISSING)
    def test_missing_service_configlet_is_purged(self, service, controlpanel_actions):
        assert SERVICES[service]["action_id"] not in controlpanel_actions

    def test_shared_browserlayer_is_unregistered(self, browser_layers):
        """Each service now brings its own layer extending the shared one."""
        assert IBrowserLayer not in browser_layers

    def test_base_profile_hides_itself_again(self):
        """Once migrated, the base profile has nothing left to offer."""
        hidden = HiddenProfiles().getNonInstallableProfiles()

        assert f"{PACKAGE_NAME}:default" in hidden

    def test_upgrade_is_no_longer_listed(self, portal, grant_roles):
        grant_roles(portal, ["Manager"])
        view = portal.restrictedTraverse("@@prefs_install_products_form")
        upgrades = [addon["id"] for addon in view.get_upgrades()]

        assert PACKAGE_NAME not in upgrades
