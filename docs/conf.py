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
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon',
]

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
