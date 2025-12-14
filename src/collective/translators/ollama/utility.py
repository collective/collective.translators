from .controlpanel import IControlPanel
from plone import api

import ollama


class OllamaFactory:
    model = "zongwei/gemma3-translator:1b"
    prompt = "Translate the following text from {source_language} to {target_language}: {content}"

    @property
    def order(self):
        return api.portal.get_registry_record(name="order", interface=IControlPanel)

    def is_available(self):
        value = api.portal.get_registry_record(name="enabled", interface=IControlPanel)
        return value

    def available_languages(self):
        return []

    def translate_content(self, content, source_language, target_language):
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": self.prompt.format(
                            source_language=source_language,
                            target_language=target_language,
                            content=content,
                        ),
                    }
                ],
            )
            return response.message.content
        # TODO: specific exception
        except ollama.ResponseError:
            # TODO: show_message here is useless, remove and return the error as
            return None


Ollama = OllamaFactory()
