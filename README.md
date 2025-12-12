# collective.translators

This package extends [plone.app.multilingual](https://github.com/plone/plone.app.multilingual) by providing pluggable external translation utilities for automatic content translation in Plone. It enables seamless integration with multiple translation providers, allowing site administrators to configure and use services such as DeepL, AWS Translate, LibreTranslate, DeepSeek, and Ollama for translating site content.

## Translator Utilities

This package provides pluggable translation utilities for multiple providers. Each utility exposes a similar interface for translating content and checking available languages.

Each utility is registered as a factory and can be enabled/configured via the Plone control panel. They provide a consistent API for translation tasks, making it easy to switch between providers.

### 1. DeepL Translator (`DeeplTranslatorFactory`)

Integrates with the DeepL API (Free and Pro endpoints supported). Reads the API key from the Plone registry. Supports autodetection of source language and translation of text or HTML.

### 2. AWS Translate (`AWSTranslatorFactory`)

Uses Amazon AWS Translate. Reads credentials and region from the Plone registry. Handles translation and language autodetection fallback.

### 3. LibreTranslate (`LibreTranslateTranslatorFactory`)

Integrates with the open-source LibreTranslate server. The server URL and API key can be configured. Supports autodetection and both text and HTML formats.

### 4. DeepSeek Translator (`DeepSeekFactory`)

Integrates with DeepSeek, an LLM-based translation API. Reads the API key from the registry. Uses chat completions for translation.

### 5. Ollama Translator (`OllamaTranslatorFactory`)

Integrates with the Ollama local LLM server. Allows translation using models running on your own hardware. The Ollama server URL and model can be configured. Useful for private or offline translation tasks.

### 6. Google Translate (`GoogleTranslateCloudAPIFactory`)

Integrates wiht the Google Translate Cloud API.

---

## Installation and usage

Install this product as a dependency of your project: `collective.translators`

If you require AWS, Deepl, DeepSeek or Ollama support, install the product requiring the required extra:

- `collective.translators[deepl]`
- `collective.translators[deepl,aws]`

Google Translate and Libre Translate support is embbeded because they just require HTTP requests to work.

## Adding a New Tool

You can contribute a new translation tool (utility) by either:

- Proposing it via a pull request (PR) within this package, following the structure below, or
- Creating a separate Plone add-on package that provides an external translation utility implementing the same interface and registration pattern.

To add a new translation tool (utility) follow these steps:

1. **Implement and Register Your Utility**

   - Your utility class must implement the `IExternalTranslationService` interface from `plone.app.multilingual.interfaces`.
   - It should provide at least these methods:
     - `is_available()`: Returns True if the service is enabled and ready.
     - `available_languages()`: Returns a list of supported language codes or pairs.
     - `translate_content(content, source_language, target_language, ...)`: Performs the translation and returns the translated text.
   - Register your utility in its `configure.zcml` using:
     ```xml
     <utility
         provides="plone.app.multilingual.interfaces.IExternalTranslationService"
         name="your_tool_name"
         component=".utility.YourTranslator"
     />
     ```
   - Follow the structure and API of the existing utilities (see `utility.py` and `configure.zcml` in other tool folders) to ensure compatibility.

2. **Register Your Tool**

   - In `src/collective/translators/configure.zcml`, add:
     ```xml
     <include package=".mytool" />
     ```

3. **(Optional) Create a Control Panel**

   - If you want user-configurable settings for your tool, add:
     - A registry interface in `interfaces.py`.
     - Registry configuration defaults in `profiles/default/registry/youtool.xml`
     - Add ontrolpanel registration in `profiles/default/controlpanel.xml`
     - A control panel form and adapter in `controlpanel/controlpanel.py`, and register it in the relevant ZCML and `controlpanel/configure.zcml`.
   - See the existing tools for concrete examples of each file and configuration.

4. **Test Your Tool**
   - Restart your site, access your tool's control panel, add your API key or settings, and test translation.

Refer to the code of existing tools (e.g. DeepL, AWS, LibreTranslate, DeepSeek, Ollama, Google) for examples of each file and configuration.

## Contribute

- [Issue Tracker](https://github.com/collective/collective.translators/issues)
- [Source Code](https://github.com/collective/collective.translators/)

## License

The project is licensed under GPLv2.
