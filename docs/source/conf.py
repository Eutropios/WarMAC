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

# -- General configuration ---------------------------------------------

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx_immaterial",
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
autodoc_type_aliases = {
    "typing.Dict": "dict",
    "typing.List": "list",
}
nitpicky = True

autodoc_typehints = "signature"
autodoc_preserve_defaults = True


# ---- Static and Template Info ----------------------------------------

templates_path = ["_templates"]

_static_path = str(Path("../_static"))
html_static_path = [_static_path]

# ---- Options for HTML output -----------------------------------------

html_theme = "sphinx_immaterial"
# pygments_style
htmlhelp_basename = "warmacdoc"
highlight_language = "python"

html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://github.com/Eutropios/WarMAC",
    "repo_url": "https://github.com/Eutropios/WarMAC",
    "repo_name": "WarMAC",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        # "navigation.expand",
        # "navigation.tabs",
        # "toc.integrate",
        # "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        # "navigation.top",
        # "navigation.tracking",
        # "search.highlight",
        # "search.share",
        # "toc.follow",
        # "toc.sticky",
        # "content.tabs.link",
        # "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-green",
            "accent": "light-green",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "light-green",
            "accent": "light-green",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
}
