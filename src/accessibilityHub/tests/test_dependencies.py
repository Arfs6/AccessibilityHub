"""
This module contains tests for the availability of the packages AccessibilityHub depends on.
It uses `importlib.import_module` because ruff ruff keeps warning about unused import,
it moves the import line when formatting.
"""

import importlib
import unittest


class TestDependencies(unittest.TestCase):
    """unittest test case for project dependencies"""

    def test_django(self):
        """Test if django was installed."""
        importlib.import_module('django')

    def test_django_htmx(self):
        """Check if django-htmx has been installed."""
        importlib.import_module('django_htmx')

    def test_dotenv(self):
        """Check if the dotenv package was installed."""
        importlib.import_module('dotenv')
