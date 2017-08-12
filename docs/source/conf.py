#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('../../server'))


# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages',
    'sphinx.ext.imgmath',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'YouShouldRead'
globals()['copyright'] = '2017, Kevin James'
author = 'Kevin James'

version = '0.0.0'
release = '0.0.0'

language = None

exclude_patterns = []

pygments_style = 'sphinx'

todo_include_todos = True


# -- Options for HTML output ----------------------------------------------
html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------
htmlhelp_basename = 'YouShouldReaddoc'


# -- Options for LaTeX output ---------------------------------------------
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'YouShouldRead.tex', 'YouShouldRead Documentation',
     'Kevin James', 'manual'),
]


# -- Options for manual page output ---------------------------------------
man_pages = [
    (master_doc, 'youshouldread', 'YouShouldRead Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------
texinfo_documents = [
    (master_doc, 'YouShouldRead', 'YouShouldRead Documentation',
     author, 'YouShouldRead', 'One line description of project.',
     'Miscellaneous'),
]
