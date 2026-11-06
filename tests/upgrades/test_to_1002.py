from collective.translators import PACKAGE_NAME
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import pytest

PREFIX = "collective.translators.google.controlpanel.IGoogleTranslateControlPanel"
ACTION_ID = "google-translate-controlpanel"


@pytest.fixture
def google_leftovers(portal, setup_tool):
    """Rebuild what the removed Google service left in a site at 1001."""
    registry = getUtility(IRegistry)
    registry.records[f"{PREFIX}.enabled"] = Record(field.Bool(title="Enabled"), True)
    portal.portal_controlpanel.registerConfiglet(
        id=ACTION_ID,
        name="Google",
        action=f"string:${{portal_url}}/@@{ACTION_ID}",
        category="Products",
        appId=ACTION_ID,
        permission="Manage portal",
    )
    setup_tool.setLastVersionForProfile(f"{PACKAGE_NAME}:default", "1001")
    return setup_tool


class TestUpgradeTo1002:
    @pytest.fixture(autouse=True)
    def upgraded(self, google_leftovers):
        google_leftovers.upgradeProfile(f"{PACKAGE_NAME}:default")

    def test_profile_reaches_1002(self, profile_last_version):
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1002"

    def test_google_registry_records_are_purged(self):
        registry = getUtility(IRegistry)

        assert not [k for k in registry.records if "translators.google." in k]

    def test_google_configlet_is_purged(self, controlpanel_actions):
        assert ACTION_ID not in controlpanel_actions

    def test_step_is_idempotent(self, setup_tool):
        from collective.translators.upgrades import to_1002

        to_1002(setup_tool)
