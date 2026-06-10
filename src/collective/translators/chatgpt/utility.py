from .controlpanel import IChatGPTControlPanel
from openai import OpenAI
from plone import api


class ChatGPTFactory:
    """Factory for ChatGPT translation service."""

    @property
    def order(self):
        return api.portal.get_registry_record(
            name="order", interface=IChatGPTControlPanel
        )

    @property
    def translator(self):
        """Get the OpenAI client with configured settings."""
        api_key = api.portal.get_registry_record(
            name="api_key", interface=IChatGPTControlPanel
        )
        base_url = api.portal.get_registry_record(
            name="base_url", interface=IChatGPTControlPanel
        )

        # If base_url is provided, use it; otherwise use OpenAI's default
        if base_url:
            return OpenAI(api_key=api_key, base_url=base_url)
        return OpenAI(api_key=api_key)

    def is_available(self):
        """Check if the service is enabled."""
        value = api.portal.get_registry_record(
            name="enabled", interface=IChatGPTControlPanel
        )
        return value

    def available_languages(self):
        """ChatGPT supports a wide range of languages.

        Return empty list as ChatGPT can translate between any language pair.
        """
        return []

    def translate_content(self, content, source_language, target_language):
        """Translate content using ChatGPT API.

        Args:
            content: Text to translate
            source_language: Source language code
            target_language: Target language code

        Returns:
            Translated text or None if translation fails
        """
        try:
            client = self.translator

            # Get model from settings
            model = api.portal.get_registry_record(
                name="model", interface=IChatGPTControlPanel
            )

            # Get temperature from settings
            temperature = api.portal.get_registry_record(
                name="temperature", interface=IChatGPTControlPanel
            )

            # Get max_tokens from settings
            max_tokens = api.portal.get_registry_record(
                name="max_tokens", interface=IChatGPTControlPanel
            )

            response = client.chat.completions.create(
                model=model,
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
                max_tokens=max_tokens,
                temperature=temperature,
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


ChatGPT = ChatGPTFactory()
