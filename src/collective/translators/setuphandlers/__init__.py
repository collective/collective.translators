from collective.translators import PACKAGE_NAME
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

#: Services shipping their own install/uninstall profile. Their profiles are
#: only registered when the matching library is importable, see the
#: ``zcml:condition`` in ``configure.zcml``.
SERVICES = (
    "aws",
    "chatgpt",
    "deepl",
    "deepseek",
    "google",
    "libretranslate",
    "ollama",
)


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide the uninstall profiles.

        The base profile stays visible on purpose. ``marshall_addons`` drops a
        hidden profile before it builds the entry of its product, so a hidden
        base profile would never offer its upgrade steps in the add-ons control
        panel, and those steps are the migration path of the sites installed
        with the single profile of 1.0.0a2 and older.

        Listing a profile that is not registered is harmless.
        """
        profiles = [f"{PACKAGE_NAME}:uninstall"]
        profiles.extend(f"{PACKAGE_NAME}.{service}:uninstall" for service in SERVICES)
        return profiles
