"""
This module contains tests for the `apps` module of the `core` django app.
It will check for the class fields.
"""

import unittest

from core.apps import CoreConfig


class TestAppConfig(unittest.TestCase):
    """Test for `core.apps.AppConfig` class."""

    def test_name(self):
        """Verify the app name."""
        self.assertEqual(CoreConfig.name, 'core')

    def test_default_auto_field(self):
        """Make sure the default auto field is set to big integers."""
        self.assertEqual(CoreConfig.default_auto_field, 'django.db.models.BigAutoField')
