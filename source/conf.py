# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SphinxDocs'
copyright = '2026, Oleh Shynkarenko'
author = 'Oleh Shynkarenko'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinxcontrib.httpdomain',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
exclude_patterns = []


language = 'y'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Вказуємо папку зі статикою
html_static_path = ['_static']

# Вказуємо назву файлу логотипа
html_logo = "_static/logo.png"

# Опціонально: можна додати іконку сайту (favicon), яка відображається на вкладці браузера
html_favicon = "_static/favicon.ico"
