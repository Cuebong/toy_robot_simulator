# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

project = 'Toy Robot Simulator Application'
copyright = '2026, Cuebong Wong'
author = 'Cuebong Wong'
release = 'v0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'enum_tools.autoenum'
    ]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_typehints = "description"

sys.path.insert(0, os.path.abspath('../toy_robot_simulator/classes'))
sys.path.insert(0, os.path.abspath('../toy_robot_simulator'))
sys.path.insert(0, os.path.abspath('../classes'))
sys.path.insert(0, os.path.abspath('../'))
