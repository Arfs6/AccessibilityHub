"""Tests for url in the reviews app."""

from django.test import TestCase, SimpleTestCase, Client


from reviews import urls
from reviews import views

class TestURLPatterns(SimpleTestCase):
    """Tests for the urlpatterns of the review apps."""

    def test_app_name(self):
        """Verify the app name."""
        self.assertEqual(urls.app_name, "reviews")

    def test_hasName(self):
        """All urlpatterns should have a name."""
        for urlPattern in urls.urlpatterns:
            self.assertTrue(urlPattern.name)

    def test_index(self):
        """Tests for the index url pattern."""
        index = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "index":
                index = urlPattern

        self.assertIsNotNone(index)
        self.assertEqual(index.callback, views.index)
        self.assertEqual(str(index.pattern), "")

    def test_owner(self):
        """Test for the owner url pattern."""
        owner = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "owner":
                owner = urlPattern

        self.assertIsNotNone(owner)
        self.assertEqual(str(owner.pattern), "owners/<str:base36Id>")
        self.assertEqual(owner.callback, views.owner)

    def test_tool(self):
        """Test for the tool url pattern."""
        tool = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "tool":
                tool = urlPattern

        self.assertIsNotNone(tool)
        self.assertEqual(str(tool.pattern), "owners/<str:ownerBase36Id>/<str:toolSlug>")
        self.assertEqual(tool.callback, views.tool)

    def test_newTool(self):
        """Test for the new tool url pattern."""
        newTool = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "newTool":
                newTool = urlPattern
        self.assertIsNotNone(newTool)
        self.assertEqual(str(newTool.name), "newTool")
        self.assertEqual(newTool.callback, views.newTool)

    def test_search(self):
        """Test for the search url pattern."""
        search = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "search":
                search = urlPattern

        self.assertIsNotNone(search)
        self.assertEqual(str(search.pattern), "search")
        self.assertEqual(search.callback, views.search)
