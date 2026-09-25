"""Upgrade steps for the collective.translators base profile."""

from collective.translators import logger
from collective.translators import PACKAGE_NAME
from plone import api
from plone.browserlayer.utils import unregister_layer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


#: For every service: the dotted name of its control panel schema (used as the
#: registry record prefix) and the ``action_id`` of its configlet.
SERVICES = {
    "aws": (
        "collective.translators.aws.controlpanel.IAWSTranslateControlPanel",
        "aws-translator-controlpanel",
    ),
    "chatgpt": (
        "collective.translators.chatgpt.controlpanel.IChatGPTControlPanel",
        "chatgpt-translator-controlpanel",
    ),
    "deepl": (
        "collective.translators.deepl.controlpanel.IDeeplControlPanel",
        "deepl-translator-controlpanel",
    ),
    "deepseek": (
        "collective.translators.deepseek.controlpanel.IDeepSeekControlPanel",
        "deepseek-translator-controlpanel",
    ),
    "google": (
        "collective.translators.google.controlpanel.IGoogleTranslateControlPanel",
        "google-translate-controlpanel",
    ),
    "libretranslate": (
        "collective.translators.libretranslate.controlpanel.ILibreTranslateControlPanel",
        "libretranslate-translator-controlpanel",
    ),
    "ollama": (
        "collective.translators.ollama.controlpanel.IControlPanel",
        "ollama-translator-controlpanel",
    ),
}


def _adopt_service_profile(setup_tool, profile_id):
    """Mark a service profile as installed without touching its settings.

    Re-running the registry import step would overwrite the configured values
    (API keys included) with the profile defaults, so only the steps that
    create the missing registrations are imported.
    """
    for step in ("browserlayer", "controlpanel"):
        setup_tool.runImportStepFromProfile(
            f"profile-{profile_id}", step, run_dependencies=False
        )
    setup_tool.setLastVersionForProfile(profile_id, "1000")


def _purge_service(registry, controlpanel, prefix, action_id):
    """Drop the leftovers of a service whose library is not installed."""
    for key in list(registry.records.keys()):
        if key.startswith(f"{prefix}."):
            del registry.records[key]
    controlpanel.unregisterConfiglet(action_id)


def to_1001(setup_tool):
    """Split the monolithic profile into one profile per service.

    Services whose library is installed keep their settings and get their
    profile marked as installed. The others lose their orphaned registry
    records and configlets: without the library their control panel view is
    not registered, so the configlet only led to a 404.
    """
    registry = getUtility(IRegistry)
    controlpanel = api.portal.get_tool("portal_controlpanel")

    for service, (prefix, action_id) in SERVICES.items():
        profile_id = f"{PACKAGE_NAME}.{service}:default"
        try:
            setup_tool.getProfileInfo(profile_id)
        except KeyError:
            logger.info("%s is not available, removing its settings.", service)
            _purge_service(registry, controlpanel, prefix, action_id)
        else:
            logger.info("Adopting the %s profile, settings are kept.", service)
            _adopt_service_profile(setup_tool, profile_id)

    # The common browser layer is no longer registered on its own: every
    # service now installs a layer extending it.
    try:
        unregister_layer(PACKAGE_NAME)
    except KeyError:
        pass
