from collective.translators import PACKAGE_NAME
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from zope.component.hooks import getSite
from zope.interface import implementer

#: Services shipping their own install/uninstall profile. Their profiles are
#: only registered when the matching library is importable, see the
#: ``zcml:condition`` in ``configure.zcml``.
SERVICES = (
    "aws",
    "chatgpt",
    "deepl",
    "deepseek",
    "libretranslate",
    "ollama",
)

BASE_PROFILE = f"{PACKAGE_NAME}:default"


def base_profile_has_pending_upgrades():
    """Does the base profile of the current site have upgrade steps to run?

    Returns ``False`` outside a site, and for a site where the base profile
    was never applied.
    """
    setup_tool = getToolByName(getSite(), "portal_setup", None)
    if setup_tool is None:
        return False
    try:
        if setup_tool.getLastVersionForProfile(BASE_PROFILE) == "unknown":
            return False
        return bool(setup_tool.listUpgrades(BASE_PROFILE))
    except KeyError:
        # The profile is not registered in this instance.
        return False


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide the uninstall profiles, and the base profile when it is idle.

        The base profile carries no configuration of its own, so it is noise in
        the add-ons control panel, except while it has an upgrade to offer.

        It cannot be hidden unconditionally. ``marshall_addons`` drops a hidden
        profile before it builds the entry of its product, so a hidden base
        profile takes its upgrade steps down with it, and those steps are the
        migration path of the sites installed with the single profile of
        1.0.0a2 and older. Keying the decision on pending upgrades rather than
        on one version number keeps later migrations reachable too.

        Listing a profile that is not registered is harmless.
        """
        profiles = [f"{PACKAGE_NAME}:uninstall"]
        profiles.extend(f"{PACKAGE_NAME}.{service}:uninstall" for service in SERVICES)
        if not base_profile_has_pending_upgrades():
            profiles.append(BASE_PROFILE)
        return profiles
