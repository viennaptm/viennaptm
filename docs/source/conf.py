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

    "titles_only": True,
}

html_css_files = [
    'custom.css',
    ('print.css', {'media': 'print'}),
]

templates_path = ["_templates"]
exclude_patterns = []

bibtex_bibfiles = ["references.bib"]
