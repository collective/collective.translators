from .controlpanel import IAWSTranslateControlPanel
from plone import api

import boto3


class AWSTranslatorFactory:
    @property
    def order(self):
        return api.portal.get_registry_record(
            name="order",
            interface=IAWSTranslateControlPanel,
        )

    @property
    def translator(self):
        access_key = api.portal.get_registry_record(
            name="access_key",
            interface=IAWSTranslateControlPanel,
        )
        secret_key = api.portal.get_registry_record(
            name="secret_key",
            interface=IAWSTranslateControlPanel,
        )
        region_name = api.portal.get_registry_record(
            name="region_name",
            interface=IAWSTranslateControlPanel,
        )
        return boto3.client(
            "translate",
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def is_available(self):
        return api.portal.get_registry_record(
            name="enabled", interface=IAWSTranslateControlPanel
        )

    def available_languages(self):
        try:
            # Check if the translator client is available
            if not self.translator:
                return ["Not set"]

            # Get all available languages
            response = self.translator.list_languages(DisplayLanguageCode="en")

            # Extract source languages
            source_lang_codes = [
                lang["LanguageCode"].lower() for lang in response["Languages"]
            ]

            # Create a list of tuples (source_lang, target_lang)
            translation_pairs = [
                (source_lang, target_lang)
                for source_lang in source_lang_codes
                for target_lang in source_lang_codes
            ]

            return translation_pairs

        except boto3.exceptions.Boto3Error:
            return ["Not set"]

    def translate_content(self, content, source_language, target_language):
        try:
            res = self.translator.translate_text(
                Text=content,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
            return res["TranslatedText"]
        except boto3.exceptions.Boto3Error:
            # Retry with autodetect
            try:
                res = self.translator.translate_text(
                    Text=content, TargetLanguageCode=target_language
                )
                return res["TranslatedText"]
            except boto3.exceptions.Boto3Error:
                return "Language not supported"


AWSTranslator = AWSTranslatorFactory()
