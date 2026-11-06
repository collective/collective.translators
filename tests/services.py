"""Metadata of the translation services, shared by the tests.

Mirrors the ``zcml:condition`` entries in
``src/collective/translators/configure.zcml``: a service profile is only
registered when its library is importable.
"""

from importlib.util import find_spec

BASE = "collective.translators"

SERVICES = {
    "aws": {
        "library": "boto3",
        "action_id": "aws-translator-controlpanel",
        "schema": f"{BASE}.aws.controlpanel.IAWSTranslateControlPanel",
        "layer": f"{BASE}.aws.interfaces.IAWSLayer",
        "panel": f"{BASE}.aws.controlpanel.AWSTranslateRegistryConfigletPanel",
    },
    "chatgpt": {
        "library": "openai",
        "action_id": "chatgpt-translator-controlpanel",
        "schema": f"{BASE}.chatgpt.controlpanel.IChatGPTControlPanel",
        "layer": f"{BASE}.chatgpt.interfaces.IChatGPTLayer",
        "panel": f"{BASE}.chatgpt.controlpanel.ChatGPTRegistryConfigletPanel",
    },
    "deepl": {
        "library": "deepl",
        "action_id": "deepl-translator-controlpanel",
        "schema": f"{BASE}.deepl.controlpanel.IDeeplControlPanel",
        "layer": f"{BASE}.deepl.interfaces.IDeeplLayer",
        "panel": f"{BASE}.deepl.controlpanel.DeeplRegistryConfigletPanel",
    },
    "deepseek": {
        "library": "openai",
        "action_id": "deepseek-translator-controlpanel",
        "schema": f"{BASE}.deepseek.controlpanel.IDeepSeekControlPanel",
        "layer": f"{BASE}.deepseek.interfaces.IDeepSeekLayer",
        "panel": f"{BASE}.deepseek.controlpanel.DeepSeekRegistryConfigletPanel",
    },
    "libretranslate": {
        "library": None,
        "action_id": "libretranslate-translator-controlpanel",
        "schema": f"{BASE}.libretranslate.controlpanel.ILibreTranslateControlPanel",
        "layer": f"{BASE}.libretranslate.interfaces.ILibreTranslateLayer",
        "panel": (
            f"{BASE}.libretranslate.controlpanel.LibreTranslateRegistryConfigletPanel"
        ),
    },
    "ollama": {
        "library": "ollama",
        "action_id": "ollama-translator-controlpanel",
        "schema": f"{BASE}.ollama.controlpanel.IControlPanel",
        "layer": f"{BASE}.ollama.interfaces.IOllamaLayer",
        "panel": f"{BASE}.ollama.controlpanel.RegistryConfigletPanel",
    },
}


def is_available(service: str) -> bool:
    """Is the library needed by this service importable?"""
    library = SERVICES[service]["library"]
    return library is None or find_spec(library) is not None


#: Services whose profile is registered in this environment.
AVAILABLE = sorted(service for service in SERVICES if is_available(service))

#: Services whose profile is not registered in this environment.
MISSING = sorted(service for service in SERVICES if not is_available(service))
