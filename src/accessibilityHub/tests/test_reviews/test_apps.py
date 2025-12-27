"""
This module contains tests for the `apps` module of the `reviews` django app.
It will check for the class fields.
"""

import unittest

from reviews.apps import ReviewsConfig


class TestAppConfig(unittest.TestCase):
    """Test for `reviews.apps.ReviewsConfig` class."""

    def test_name(self):
        """Verify the app name."""
        self.assertEqual(ReviewsConfig.name, 'reviews')

    def test_default_auto_field(self):
        """Make sure the default auto field is set to big integers."""
        self.assertEqual(ReviewsConfig.default_auto_field, 'django.db.models.BigAutoField')
