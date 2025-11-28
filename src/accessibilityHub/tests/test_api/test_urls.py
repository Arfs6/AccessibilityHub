"""Test for the api app.
The test includes testing the url patterns
and using `django.test.client` on all urls.
"""

from api import urls, views
from django.test import SimpleTestCase


class TestURLPatterns(SimpleTestCase):
    """Test all the url patterns in core.url"""

    def test_appName(self):
        """Core should Have a namespace."""
        self.assertEqual(urls.app_name, "api")

    def test_hasName(self):
        """All urlpatterns should have a name."""
        for urlPattern in urls.urlpatterns:
            self.assertIsNotNone(urlPattern.name)

    def test_createReview(self):
        """Test for the create review url pattern."""
        createReview = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "createReview":
                createReview = urlPattern

        self.assertIsNotNone(createReview)
        self.assertEqual(str(createReview.pattern), "tools/<int:toolId>/reviews")
        self.assertIs(createReview.callback, views.createReview)

    def test_newOwner(self):
        """Test for the new owner url pattern."""
        newOwner = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "newOwner":
                newOwner = urlPattern

        self.assertIsNotNone(newOwner)
        self.assertEqual(str(newOwner.pattern), "owners")
        self.assertIs(newOwner.callback, views.newOwner)

    def test_newTool(self):
        """Test for the new tool url pattern."""
        newTool = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "newTool":
                newTool = urlPattern

        self.assertIsNotNone(newTool)
        self.assertEqual(str(newTool.pattern), "tools")
        self.assertIs(newTool.callback, views.newTool)
