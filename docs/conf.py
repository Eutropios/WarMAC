"""
Configuration file for Sphinx.

------------------------------------------------------------------------

Copyright (C) 2024 Noah Jenner under CC BY-SA 4.0.
To view a copy of this license, visit https://creativecommons.org/licenses/by-sa/4.0/
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# -- Metadata ----------------------------------------------------------

python_path = str(Path("../src/warmac").resolve())
sys.path.insert(0, python_path)

project = "WarMAC"
copyright = "2023–2026, Noah Jenner"  # noqa: A001, RUF001
author = "Noah Jenner"
release = "0.0.6"
version = "0.0.6"
language = "en"

# -- General Config ----------------------------------------------------
os.environ["SPHINX_AUTODOC_RELOAD_MODULES"] = "1"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_last_updated_by_git",
    "notfound.extension",
    "sphinx_inline_tabs",
]

master_doc = "index"
source_suffix = ".rst"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "urllib3": ("https://urllib3.readthedocs.io/en/stable/", None),
    "msgspec": ("https://jcristharif.com/msgspec/", None),
}

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
}
autodoc_class_signature = "separated"
nitpicky = True
autodoc_typehints = "signature"
autodoc_preserve_defaults = True
copybutton_selector = "div:not(.no-copybutton) > div.highlight > pre"
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# ---- Options for HTML output ----------------------------------------

_static_path = Path("_static")
html_static_path = [str(_static_path)]
html_theme = "furo"
html_css_files = [str(_static_path / "custom.css")]
htmlhelp_basename = "warmacdoc"
highlight_language = "python"
pygments_style = "default"
pygments_dark_style = "one-dark"

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
