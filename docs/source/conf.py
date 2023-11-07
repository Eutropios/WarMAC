"""
conf.py for Sphinx.

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Date of Creation: August 20, 2023
"""

from __future__ import annotations

import sys
from pathlib import Path

# -- General configuration --------------------------------------------

python_path = str(Path("../../warmac/").resolve())
sys.path.insert(0, python_path)

author = "Noah Jenner"
copyright = "2023, Noah Jenner"  # noqa: A001
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "en"
master_doc = "index"
project = "WarMAC"
release = "0.0.4"
source_suffix = ".rst"
templates_path = ["_templates"]

# -- Extensions --------------------------------------------------------

extensions = [
    "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinx_last_updated_by_git",
    # install this https://github.com/readthedocs/sphinx-hoverxref
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "urllib3": ("https://urllib3.readthedocs.io/en/stable/", None),
}

autodoc_default_options = {
    "members": True,
    "private-members": True,
    "undoc-members": True,
}
# autodoc_type_aliases = {str, str}
autodoc_preserve_defaults = True
autodoc_typehints = "signature"
copybutton_selector = "div:not(.no-copybutton) > div.highlight > pre"

# ---- Options for HTML output ----------------------------------------

_static_path = Path("_static")
highlight_language = "python"
html_static_path = [str(_static_path)]
html_css_files = [str(_static_path / "custom.css")]
html_theme = "furo"
htmlhelp_basename = "warmacdoc"
nitpicky = True
pygments_dark_style = "one-dark"
pygments_style = "one-dark"

html_theme_options = {
    "globaltoc_collapse": True,
    "source_branch": "main",
    "source_directory": "docs/",
    "source_repository": "https://github.com/Eutropios/WarMAC",
    # -- CSS Variables --
    "dark_css_variables": {
        "color-api-name": "#ff6b6b",
        "color-api-pre-name": "#4ec9b0",
        "color-link--hover": "#59e5ee",
    },
    "light_css_variables": {
        "color-link--hover": "#35939a",
    },
}
