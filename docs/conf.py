from __future__ import annotations

project = "WarMAC"
copyright = "2023, Noah Jenner"  # noqa: A001
author = "Noah Jenner"
release = "0.0.4"

# -- General configuration ---------------------------------------------

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------

html_theme = "nature"
html_static_path = ["_static"]
