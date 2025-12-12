from .controlpanel import ILibreTranslateControlPanel
from plone import api

import requests


class LibreTranslateTranslatorFactory:
    timeout = 5

    @property
    def order(self):
        return api.portal.get_registry_record(
            name="order", interface=ILibreTranslateControlPanel
        )

    @property
    def api_key(self):
        return api.portal.get_registry_record(
            name="api_key", interface=ILibreTranslateControlPanel
        )

    @property
    def server_url(self):
        return api.portal.get_registry_record(
            name="server_url", interface=ILibreTranslateControlPanel
        )

    @property
    def autodetect_source_language(self):
        return api.portal.get_registry_record(
            name="autodetect_source_language", interface=ILibreTranslateControlPanel
        )

    def is_available(self):
        return api.portal.get_registry_record(
            name="enabled", interface=ILibreTranslateControlPanel
        )

    def available_languages(self):
        # TODO
        return []

    def translate_content(self, content, source_language, target_language, format=None):
        if self.autodetect_source_language:
            source_language = "auto"

        # guess format
        if format is None:
            if "<" in content and ">" in content:
                format = "html"
            else:
                format = "text"

        res = requests.post(
            f"{self.server_url}/translate",
            json={
                "q": content,
                "source": source_language,
                "target": target_language,
                "format": format,
                "alternatives": 0,
                "api_key": self.api_key,
            },
            timeout=self.timeout,
        ).json()
        if res.ok:
            return res["translatedText"]

        return ""


LibreTranslateTranslator = LibreTranslateTranslatorFactory()
