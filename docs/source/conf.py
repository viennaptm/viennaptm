# docs/source/conf.py

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = "viennaptm"
author = "ViennaPTM Team"
release = "0.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinxcontrib.bibtex"
]

autosummary_generate = True
add_module_names = False
autosummary_short_names = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True
}

# Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# ---- READ THE DOCS THEME ----
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": -1,
    "titles_only": True
}

html_css_files = [
    'custom.css',
    ('print.css', {'media': 'print'}),
]

templates_path = ["_templates"]
exclude_patterns = []

bibtex_bibfiles = ["references.bib"]

# ---- PTM data tables ----
html_css_files = [
    "https://cdn.datatables.net/1.13.8/css/jquery.dataTables.min.css",
]

html_js_files = [
    "https://code.jquery.com/jquery-3.7.1.min.js",
    "https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js",
    "datatable-init.js",
]
