"""Browser layer for the Ollama service."""

from collective.translators.interfaces import IBrowserLayer


class IOllamaLayer(IBrowserLayer):
    """Marker interface installed by the collective.translators.ollama profile."""
