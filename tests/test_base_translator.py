from collective.translators.base import BaseTranslatorFactory
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import pytest

#: service, library it needs, translator instance, browser layer
TRANSLATORS = [
    ("aws", "boto3", "AWSTranslator", "IAWSLayer"),
    ("chatgpt", "openai", "ChatGPT", "IChatGPTLayer"),
    ("deepl", "deepl", "DeeplTranslator", "IDeeplLayer"),
    ("deepseek", "openai", "DeepSeek", "IDeepSeekLayer"),
    ("libretranslate", None, "LibreTranslateTranslator", "ILibreTranslateLayer"),
    ("ollama", "ollama", "Ollama", "IOllamaLayer"),
]


@pytest.fixture(params=TRANSLATORS, ids=lambda p: p[0])
def service(request):
    name, library, instance, layer = request.param
    if library:
        pytest.importorskip(library)
    base = f"collective.translators.{name}"
    translator = getattr(pytest.importorskip(f"{base}.utility"), instance)
    layer = getattr(pytest.importorskip(f"{base}.interfaces"), layer)
    return name, translator, layer


class TestLayerVerification:
    def test_unavailable_without_layer(self, portal, http_request, service):
        _, translator, layer = service
        if layer.providedBy(http_request):
            noLongerProvides(http_request, layer)

        assert translator.is_available() is False
        assert translator.is_enabled() is False

    def test_follows_registry_with_layer(
        self, portal, setup_tool, http_request, service
    ):
        name, translator, layer = service
        setup_tool.runAllImportStepsFromProfile(
            f"profile-collective.translators.{name}:default"
        )
        alsoProvides(http_request, layer)
        try:
            assert translator.is_available() is bool(translator.is_enabled())
            assert translator.order != 9999
        finally:
            noLongerProvides(http_request, layer)


def test_base_factory_without_controlpanel_is_unavailable(portal):
    factory = BaseTranslatorFactory()

    assert factory.is_available() is False
    assert factory.order == 9999
