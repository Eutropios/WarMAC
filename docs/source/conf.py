import sys
from pathlib import Path

python_path = str(Path("../../warmac/").resolve())
sys.path.insert(0, python_path)

project = "WarMAC"
copyright = "2023, Noah Jenner"  # noqa: A001
author = "Noah Jenner"
release = "0.0.4"
langauge = "en"

# -- General configuration ---------------------------------------------

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
]

master_doc = "index"
source_suffix = ".rst"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------

html_theme = "furo"
pygments_style = "sphinx"
htmlhelp_basename = "warmacdoc"

_static_path = str(Path("../_static"))
html_static_path = [_static_path]
