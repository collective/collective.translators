# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0a2 (2026-10-01)


### Breaking changes

- Remove the Google Translate service, with its profile and control panel.
  The 1002 upgrade step cleans its registry records and configlet from existing sites. 
- Split the single GenericSetup profile into one install and one uninstall profile per translation service. Each service is now a separate entry in the add-ons control panel, shown only when the library it needs is importable. The shared `collective.translators:default` profile is hidden and installed as a dependency, and it no longer registers a browser layer of its own: every service registers a layer extending `collective.translators.interfaces.IBrowserLayer`. Existing sites are migrated by the upgrade step to profile version 1001, which keeps the settings of the available services and removes the leftovers of the others. [mamico] 


### Bug fixes

- Align `configlet_id` with the `action_id` of the configlet for AWS Translate, ChatGPT, DeepL, DeepSeek, LibreTranslate and Ollama, so the panels are listed by the `@controlpanels` endpoint of `plone.restapi`. [mamico] 
- Register the missing control panel configlet for Ollama. [mamico] 
- Show the `collective.translators:default` profile in the add-ons control panel while it has upgrade steps to run, and hide it the rest of the time. The control panel drops a hidden profile before it builds the entry of its product, so a permanently hidden base profile kept its upgrade steps out of `/prefs_install_products_form`, and those steps are the migration path of the sites installed with the single profile of 1.0.0a2 and older. Keying the decision on pending upgrades rather than on one version number keeps later migrations reachable as well. The uninstall profiles stay hidden at all times. [mamico] 


### Internal

- Move package metadata from `setup.py` to `pyproject.toml` @plone 
- Require `Manage portal` for every control panel view. DeepSeek, Google Translate and LibreTranslate used to require `plone.app.controlpanel.Language`, while their configlet already required `Manage portal`. [mamico] 


### Tests

- Run the test suite with pytest instead of zope-testrunner, and declare `pytest`, `pytest-cov` and `pytest-plone` in the `test` extra. Add coverage of the per service profiles and of the upgrade step. [mamico] 
- Run the tests in CI against the `plone.app.multilingual` branch that provides `IExternalTranslationService`, checked out by mxdev from `tox -e init`, and move the constraints to the Plone 6.2 set the test matrix already names. Without it the ZCML of the add-on cannot be loaded at all against a released `plone.app.multilingual`. [mamico] 

## 1.0.0a1 (2026-08-24)


### Bug fixes:

- Fixed the issue related to not yet installed package. [mamico] 

## 1.0.0a0 (2026-08-17)


### Internal:

- Update configuration files @plone 

## 100.0.0 (2025-05-11)

No significant changes.


## 1.0.0 (2025-05-11)

No significant changes.
