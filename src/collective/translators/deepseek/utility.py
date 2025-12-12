from openai import OpenAI
from plone import api
from .controlpanel import IDeepSeekControlPanel


class DeepSeekFactory:
    server_url = "https://api.deepseek.com"

    @property
    def order(self):
        return api.portal.get_registry_record(
            name="order", interface=IDeepSeekControlPanel
        )

    @property
    def translator(self):
        key = api.portal.get_registry_record(
            name="api_key", interface=IDeepSeekControlPanel
        )
        client = OpenAI(api_key=key, base_url=self.server_url)
        return client

    def is_available(self):
        value = api.portal.get_registry_record(
            name="enabled", interface=IDeepSeekControlPanel
        )
        return value

    def available_languages(self):
        # Deepseek is a chatbot, so it doesn't have a list of supported languages
        # We assume that it can translate between any language
        return []

    def translate_content(self, content, source_language, target_language):
        try:
            client = self.translator
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Translate the user's text accurately and only return the translated content without additional explanations.",
                    },
                    {
                        "role": "user",
                        "content": f"Translate the following text from {source_language} to {target_language}: {content}",
                    },
                ],
                max_tokens=1000,
                temperature=0.3,
                top_p=1,
            )
            translated_text = response.choices[0].message.content
            return translated_text
        except Exception as e:
            api.portal.show_message(
                message=f"Translation error: {str(e)}",
                request=api.portal.get().REQUEST,
                type="error",
            )
            return None


DeepSeek = DeepSeekFactory()
