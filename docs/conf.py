"""Sphinx configuration for Read the Docs.

This file replaces on-the-fly generation via `jupyter-book config sphinx docs/`
to avoid interactive Node.js prompts in non-interactive CI environments.
"""

from datetime import datetime

project = "comfree_warp Documentation"
author = "ASU IRIS"
copyright = f"{datetime.now().year}, {author}"

extensions = [
    "myst_nb",
    "sphinx_external_toc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex",
    "sphinx_inline_tabs",
    "sphinx_proof",
    "sphinx_examples",
    "hoverxref.extension",
]

# Use Jupyter Book-style table of contents from docs/_toc.yml
external_toc_path = "_toc.yml"
external_toc_exclude_missing = False

root_doc = "intro"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Execute notebook content during builds, matching docs/_config.yml intent.
nb_execution_mode = "force"

# Basic MyST features commonly expected in Jupyter Book content.
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_image",
    "html_admonition",
    "linkify",
    "substitution",
]

intersphinx_mapping = {
    "ebp": ("https://executablebooks.org/en/latest/", None),
    "myst-parser": ("https://myst-parser.readthedocs.io/en/latest/", None),
    "myst-nb": ("https://myst-nb.readthedocs.io/en/latest/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "nbformat": ("https://nbformat.readthedocs.io/en/latest", None),
    "sd": ("https://sphinx-design.readthedocs.io/en/latest", None),
    "sphinxproof": ("https://sphinx-proof.readthedocs.io/en/latest/", None),
}

hoverxref_intersphinx = ["sphinxproof"]

mathjax3_config = {
    "tex": {
        "macros": {
            "N": "\\mathbb{N}",
            "floor": ["\\lfloor#1\\rfloor", 1],
            "bmat": ["\\left[\\begin{array}"],
            "emat": ["\\end{array}\\right]"],
        }
    }
}

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_theme_options = {
    "repository_url": "https://github.com/asu-iris/comfree-sim-doc",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": True,
    "use_issues_button": True,
}

bibtex_bibfiles = ["references.bib"]

latex_documents = [(root_doc, "book.tex", project, author, "manual")]
