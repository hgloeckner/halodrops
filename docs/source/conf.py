# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.insert(0, os.path.abspath("../../src"))

project = "HALO-DROPS"
copyright = "2023, Geet George"
author = "Geet George"
release = "v0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "nbsphinx",
    "autodoc2",
    "sphinx_last_updated_by_git",
]

myst_enable_extensions = ["colon_fence", "dollarmath"]
autodoc2_packages = [
    {
        "path": "../../src/halodrops/",
    },
]
autodoc2_render_plugin = "myst"
autosectionlabel_prefix_document = True
exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
# html_static_path = ["_static"]
html_context = {"default_mode": "light"}
html_theme_options = {
    "repository_url": "https://github.com/Geet-George/halodrops",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_fullscreen_button": False,
}
# Set link name generated in the top bar.
html_title = "HALO-DROPS"
