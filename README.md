# collective.translators

This package extends [plone.app.multilingual](https://github.com/plone/plone.app.multilingual) with pluggable external translation utilities for automatic content translation in Plone.
It integrates several translation providers, so you can configure DeepL, AWS Translate, LibreTranslate, DeepSeek, Ollama, or ChatGPT and use them to translate your content.

This add-on requires [plone.app.multilingual PR #468](https://github.com/plone/plone.app.multilingual/pull/468).
No released version of `plone.app.multilingual` provides the `IExternalTranslationService` interface yet.

## Translation services

Each service registers a named utility that provides `IExternalTranslationService`.
The utilities share the same interface for translating content and for reporting the languages they support, so you can switch between providers without changing anything else.

Configure each service from its own control panel.

Google Translate is not part of this package.
`plone.app.multilingual` already ships it, and you configure it with the Google API key in the *Languages* site setup.

| Service | Utility name | Factory |
| --- | --- | --- |
| AWS Translate | `aws_translate` | `AWSTranslatorFactory` |
| ChatGPT | `chatgpt_translate` | `ChatGPTFactory` |
| DeepL | `deepl_translate` | `DeeplTranslatorFactory` |
| DeepSeek | `deepseek` | `DeepSeekFactory` |
| LibreTranslate | `libretranslate_translate` | `LibreTranslateTranslatorFactory` |
| Ollama | `ollama` | `OllamaFactory` |

### AWS Translate

Uses Amazon AWS Translate.
Reads the credentials and the region from the Plone registry.
Falls back to language autodetection when the source language is unknown.

### ChatGPT

Uses the OpenAI API.
Reads the credentials from the Plone registry.

### DeepL

Uses the DeepL API, on either the Free or the Pro endpoint.
Reads the API key from the Plone registry.
Detects the source language on request, and translates both text and HTML.

### DeepSeek

Uses DeepSeek, a translation API backed by a large language model.
Reads the API key from the Plone registry.
Translates through chat completions.

### LibreTranslate

Uses an [open source LibreTranslate server](https://libretranslate.com/).
You set the server URL and the API key.
Detects the source language on request, and translates both text and HTML.

### Ollama

Uses an Ollama server, so the models run on your own hardware.
You set the server URL and the model.
Use this service for private or offline translation.

## Installation

Add `collective.translators` to the dependencies of your project.

LibreTranslate works out of the box, because it only needs HTTP requests.
The other services need a client library, which you pull in through an extra:

```text
collective.translators[deepl]
collective.translators[deepl,aws]
```

### Add-ons control panel

Every translation service ships its own install and uninstall profile, and appears as a separate entry in the add-ons control panel.

| Add-on | Extra it needs |
| --- | --- |
| Collective Translators: AWS Translate | `collective.translators[aws]` |
| Collective Translators: ChatGPT | `collective.translators[chatgpt]` |
| Collective Translators: DeepL | `collective.translators[deepl]` |
| Collective Translators: DeepSeek | `collective.translators[deepseek]` |
| Collective Translators: LibreTranslate | none |
| Collective Translators: Ollama | `collective.translators[ollama]` |

An entry appears only when the library it needs is importable.
A control panel therefore never points at a service that your site cannot use.

Installing any service also installs the shared `collective.translators:default` profile as a dependency.
That profile holds no configuration of its own, so it stays out of the list while it has nothing to offer.
It appears as `Collective Translators: shared base` only while an upgrade of the add-on is waiting to run, because the control panel reaches the upgrade steps of a product only through a profile it lists.

### Upgrade from 1.0.0a2 or older

Older versions installed every service from a single profile.
To migrate a site, open `/prefs_install_products_form` and run the upgrade that Collective Translators offers there.
The same step is also available from `/portal_setup/manage_upgrades`, under the `collective.translators:default` profile.

The upgrade keeps the settings of the services whose library you installed, API keys included.
It removes the leftover registry records and configlets of the other services.
Install those services again from the add-ons control panel once you add their library.

## Add a new service

Contribute a new translation service in either of two ways:

- Open a pull request against this package, following the structure below.
- Publish a separate Plone add-on that provides an external translation utility with the same interface and the same registration pattern.

Read the code of an existing service, such as DeepL or LibreTranslate, for a concrete example of every file below.

### 1. Implement and register the utility

Your utility class must implement `IExternalTranslationService` from `plone.app.multilingual.interfaces`, with at least these methods:

- `is_available()` returns `True` when the service is enabled and ready.
- `available_languages()` returns the supported language codes, or the supported source and target pairs.
- `translate_content(content, source_language, target_language)` translates the content and returns the translated text.

Register a module level instance of the class in `mytool/configure.zcml`:

```xml
<utility
    provides="plone.app.multilingual.interfaces.IExternalTranslationService"
    name="your_tool_name"
    component=".utility.YourTranslator"
    />
```

### 2. Include the package

Add the include to `src/collective/translators/configure.zcml`.
Guard it with a `zcml:condition` when your service needs a client library:

```xml
<include
    package=".mytool"
    zcml:condition="installed yourlibrary"
    />
```

### 3. Add a control panel

This step is optional.
Skip it when your service needs no configuration.

Write the registry schema and the control panel form in `mytool/controlpanel.py`, then register the browser page and the `plone.restapi` adapter in `mytool/configure.zcml`.
Give the adapter a `configlet_id` that matches the `action_id` of the configlet, otherwise `plone.restapi` leaves your panel out of `@controlpanels`.

Declare a browser layer that extends `collective.translators.interfaces.IBrowserLayer` in `mytool/interfaces.py`, and bind the browser page to that layer.

### 4. Ship an install and an uninstall profile

Register both profiles in `mytool/profiles.zcml`, and include that file from `mytool/configure.zcml`.
The profiles then exist only when the ZCML of your service loads, which is what hides the add-on when the library is missing.

```xml
<genericsetup:registerProfile
    name="default"
    title="Collective Translators: My Tool"
    provides="Products.GenericSetup.interfaces.EXTENSION"
    directory="profiles/default"
    />
```

Put `metadata.xml`, `browserlayer.xml`, `registry.xml`, and `controlpanel.xml` in `mytool/profiles/default/`.
Make `metadata.xml` depend on `profile-collective.translators:default`.

Put `browserlayer.xml`, `registry.xml`, and `controlpanel.xml` in `mytool/profiles/uninstall/`, each one with `remove="true"`.

Add the name of your service to `collective.translators.setuphandlers.SERVICES`, so that its uninstall profile stays hidden from the add-ons control panel.

### 5. Test the service

Restart your site.
Install your add-on from the add-ons control panel.
Open the control panel of your service, enter your API key or your settings, and translate a page.

## Contribute

- [Issue tracker](https://github.com/collective/collective.translators/issues)
- [Source code](https://github.com/collective/collective.translators/)

## License

GPL version 2.
