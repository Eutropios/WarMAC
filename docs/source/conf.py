"""
conf.py for Sphinx.

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Date of Creation: August 20, 2023
"""

import sys
from pathlib import Path

python_path = str(Path("../../warmac/").resolve())
sys.path.insert(0, python_path)


project = "WarMAC"
copyright = "2023, Noah Jenner"  # noqa: A001
author = "Noah Jenner"
release = "0.0.4"
language = "en"

# -- General configuration --------------------------------------------

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_last_updated_by_git",
    "notfound.extension",
    # install this https://github.com/readthedocs/sphinx-hoverxref
]

master_doc = "index"
source_suffix = ".rst"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "urllib3": ("https://urllib3.readthedocs.io/en/stable/", None),
}

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
}
# autodoc_type_aliases = {str, str}
# nitpicky = True
autodoc_typehints = "signature"
autodoc_preserve_defaults = True

# ---- Options for HTML output ----------------------------------------

_static_path = Path("../_static")
templates_path = [str(Path("../_templates"))]
html_static_path = [str(_static_path)]
html_theme = "furo"
html_css_files = [str(_static_path / "custom.css")]
htmlhelp_basename = "warmacdoc"
highlight_language = "python"
pygments_style = "one-dark"
pygments_dark_style = "one-dark"

html_theme_options = {
    "globaltoc_collapse": True,
    "source_repository": "https://github.com/Eutropios/WarMAC",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-link--hover": "#35939a",
    },
    "dark_css_variables": {
        "color-api-name": "#ff6b6b",
        "color-api-pre-name": "#4ec9b0",
        "color-link--hover": "#59e5ee",
    },
}
