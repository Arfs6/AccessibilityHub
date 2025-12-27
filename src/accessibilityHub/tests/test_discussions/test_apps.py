"""
This module contains tests for the `apps` module of the `discussions` django app.
It will check for the class fields.
"""

import unittest

from discussions.apps import DiscussionsConfig


class TestAppConfig(unittest.TestCase):
    """Test for `discussions.apps.DiscussionsConfig` class."""

    def test_name(self):
        """Verify the app name."""
        self.assertEqual(DiscussionsConfig.name, 'discussions')

    def test_default_auto_field(self):
        """Make sure the default auto field is set to big auto fields."""
        self.assertEqual(DiscussionsConfig.default_auto_field, 'django.db.models.BigAutoField')
