"""Setup collective.translators"""

from setuptools import setup


setup(
    # metadata in setup.cfg
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api",
        "plone.app.multilingual",
        "plone.app.registry",
        "plone.base",
        "plone.restapi",
        "Products.CMFCore",
        "Products.CMFPlone",
        "requests",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.contenttypes",
            "plone.app.testing",
            "plone.restapi[test]",
            "plone.testing",
        ],
        "aws": ["boto3"],
        "deepseek": ["openai"],
        "deepl": ["deepl"],
        "ollama": ["ollama"],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
