from plone import api
from .controlpanel import IGoogleTranslateControlPanel

import json
import urllib


class GoogleCloudTranslationAPIFactory:
    """implement the external translation using Google Cloud Translation API"""

    def is_available(self):
        return api.portal.get_registry_record(
            name="enabled", interface=IGoogleTranslateControlPanel
        )

    def available_languages(self):
        return []

    @property
    def order(self):
        return api.portal.get_registry_record(
            name="order", interface=IGoogleTranslateControlPanel
        )

    def translate_content(self, content, source_language, target_language):
        google_translation_key = api.portal.get_registry_record(
            name="api_key", interface=IGoogleTranslateControlPanel
        )

        question = content
        length = len(question)
        translated = ""
        url = "https://www.googleapis.com/language/translate/v2"
        temp_question = question
        while length > 400:
            temp_question = question[:399]
            index = temp_question.rfind(" ")
            temp_question = temp_question[:index]
            question = question[index:]
            length = len(question)
            data = {
                "key": google_translation_key,
                "target": target_language,
                "source": source_language,
                "q": temp_question,
            }
            params = urllib.parse.urlencode(data)

            result = urllib.request.urlopen(url + "?" + params)
            translated += json.loads(result.read())["data"]["translations"][0][
                "translatedText"
            ]

        data = {
            "key": google_translation_key,
            "target": target_language,
            "source": source_language,
            "q": temp_question,
        }
        params = urllib.parse.urlencode(data)

        result = urllib.request.urlopen(url + "?" + params)
        translated += json.loads(result.read())["data"]["translations"][0][
            "translatedText"
        ]
        return translated


GoogleCloudTranslationAPI = GoogleCloudTranslationAPIFactory()
