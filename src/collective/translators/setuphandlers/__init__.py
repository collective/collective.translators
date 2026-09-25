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
        """Hide the base and the uninstall profiles.

        The base profile is installed as a dependency of any service profile,
        so it does not need its own entry in the add-ons control panel. Listing
        a profile that is not registered is harmless.
        """
        profiles = [
            f"{PACKAGE_NAME}:default",
            f"{PACKAGE_NAME}:uninstall",
        ]
        profiles.extend(f"{PACKAGE_NAME}.{service}:uninstall" for service in SERVICES)
        return profiles
