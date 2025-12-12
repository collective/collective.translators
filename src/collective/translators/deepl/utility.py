from plone import api

import deepl
from .controlpanel import IDeeplControlPanel


class DeeplTranslatorFactory:
    # TODO: manage settings in the registry
    # Free API -> https://api-free.deepl.com
    # Pro API -> https://api.deepl.com

    server_url = "https://api-free.deepl.com"
    autodetect_source_language = False

    @property
    def order(self):
        return api.portal.get_registry_record(
            name="order", interface=IDeeplControlPanel
        )

    @property
    def translator(self):
        api_key = api.portal.get_registry_record(
            name="api_key", interface=IDeeplControlPanel
        )
        return deepl.Translator(server_url=self.server_url, auth_key=api_key)

    def is_available(self):
        return api.portal.get_registry_record(
            name="enabled", interface=IDeeplControlPanel
        )

    def available_languages(self):
        try:
            if not self.translator:
                return {"Error": "Key not set"}

            # Obtain the list of supported languages
            source_languages = self.translator.get_source_languages()
            target_languages = self.translator.get_target_languages()

            # Ensure that en e pt are included in the list of supported languages
            additional_languages = ["en", "pt"]
            for lang in additional_languages:
                if lang not in [lang.code.lower() for lang in source_languages]:
                    source_languages.append(
                        deepl.Language(code=lang, name=lang.upper())
                    )
                if lang not in [lang.code.lower() for lang in target_languages]:
                    target_languages.append(
                        deepl.Language(code=lang, name=lang.upper())
                    )

            # Create a list of supported translations
            translation_pairs = [
                (source_lang.code.lower(), target_lang.code.lower())
                for source_lang in source_languages
                for target_lang in target_languages
                if source_lang.code != target_lang.code
            ]

            return translation_pairs

        except deepl.DeepLException as e:
            return {"Error": str(e)}

    def normalize_language(self, language):
        if language == "en":
            return "en-us"
        elif language == "pt":
            return "pt-pt"
        return language

    def translate_content(self, content, source_language, target_language):
        try:
            target_language = self.normalize_language(target_language)
            if self.autodetect_source_language:
                res = self.translator.translate_text(
                    content, target_lang=target_language
                )
            else:
                res = self.translator.translate_text(
                    content, source_lang=source_language, target_lang=target_language
                )
            return res.text
        except deepl.DeepLException:
            # If the language is not supported, try to autodetect it
            # If there's an other error, return an empty string
            if not self.autodetect_source_language:
                try:
                    res = self.translator.translate_text(
                        content, target_lang=target_language
                    )
                    return res.text
                except deepl.DeepLException:
                    return ""
            return "Language not supported"


DeeplTranslator = DeeplTranslatorFactory()
