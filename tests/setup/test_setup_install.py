from collective.translators import PACKAGE_NAME
from collective.translators.setuphandlers import HiddenProfiles


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if collective.translators is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1001"

    def test_base_profile_is_hidden(self):
        """The base profile is installed as a dependency, not on its own."""
        hidden = HiddenProfiles().getNonInstallableProfiles()

        assert f"{PACKAGE_NAME}:default" in hidden
        assert f"{PACKAGE_NAME}:uninstall" in hidden

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
