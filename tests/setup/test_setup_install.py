from collective.translators import PACKAGE_NAME
from collective.translators.setuphandlers import HiddenProfiles


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if collective.translators is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1002"

    def test_base_profile_is_hidden_when_up_to_date(self):
        """With no upgrade to offer, the base profile is noise."""
        hidden = HiddenProfiles().getNonInstallableProfiles()

        assert f"{PACKAGE_NAME}:default" in hidden
        assert f"{PACKAGE_NAME}:uninstall" in hidden

    def test_base_profile_is_absent_from_the_addons_control_panel(
        self, portal, grant_roles
    ):
        """An up to date site sees only the services it can install."""
        grant_roles(portal, ["Manager"])
        view = portal.restrictedTraverse("@@prefs_install_products_form")

        assert PACKAGE_NAME not in view.marshall_addons()

    def test_base_profile_is_still_reported_as_installed(self, installer):
        """Hiding the profile must not make the product look uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_base_profile_registers_no_browserlayer(self, browser_layers):
        """Each service registers its own layer, the base registers none."""
        from collective.translators.interfaces import IBrowserLayer

        assert IBrowserLayer not in browser_layers

    def test_base_profile_registers_no_configlet(self, controlpanel_actions):
        """Each service brings its own configlet."""
        translators_actions = [
            action
            for action in controlpanel_actions
            if "translator-controlpanel" in action or "translate-controlpanel" in action
        ]

        assert translators_actions == []

    def test_multilingual_installed(self, installer):
        """plone.app.multilingual is a dependency of the base profile."""
        assert installer.is_product_installed("plone.app.multilingual") is True


class TestBaseProfileVisibilityEdgeCases:
    def test_hidden_outside_a_site(self):
        """getNonInstallableProfiles runs before a site exists too."""
        from collective.translators.setuphandlers import (
            base_profile_has_pending_upgrades,
        )
        from zope.component.hooks import site

        with site(None):
            assert base_profile_has_pending_upgrades() is False

    def test_hidden_when_the_profile_was_never_applied(self, portal, setup_tool):
        """A site that never installed the add-on sees no base profile."""
        setup_tool.unsetLastVersionForProfile(f"{PACKAGE_NAME}:default")
        hidden = HiddenProfiles().getNonInstallableProfiles()

        assert f"{PACKAGE_NAME}:default" in hidden
