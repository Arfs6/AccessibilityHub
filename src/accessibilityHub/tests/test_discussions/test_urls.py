"""Tests for url in the discussions app."""

from django.test import SimpleTestCase
from discussions import urls


class TestURLPatterns(SimpleTestCase):
    """Tests for the urlpatterns of the discussions apps."""

    def test_app_name(self):
        """Verify the app name."""
        self.assertEqual(urls.app_name, "discussions")

    def test_hasName(self):
        """All urlpatterns should have a name."""
        for urlPattern in urls.urlpatterns:
            self.assertTrue(urlPattern.name)

    def test_landing(self):
        """Tests for the landing url pattern."""
        landing = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "landing":
                landing = urlPattern

        self.assertIsNotNone(landing)
        self.assertEqual(landing.callback, views.landing)
        self.assertEqual(str(landing.pattern), "")

    def test_index(self):
        """Test for the index url pattern."""
        index = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "index":
                index = urlPattern

        self.assertIsNotNone(index)
        self.assertEqual(str(index.pattern), "topics")
        self.assertEqual(index.callback, views.index)

    def test_newTopic(self):
        """Test for the new topic url pattern."""
        newTopic = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "newTopic":
                newTopic = urlPattern

        self.assertIsNotNone(newTopic)
        self.assertEqual(str(newTopic.pattern), "topics/new")
        self.assertEqual(newTopic.callback, views.newTopic)

    def test_topicPage(self):
        """Test for the topic page url pattern."""
        topicPage = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "topicPage":
                topicPage = urlPattern
        self.assertIsNotNone(topicPage)
        self.assertEqual(str(topicPage.name), "topics/<str:base36Id>")
        self.assertEqual(topicPage.callback, views.topicPage)

    def test_search(self):
        """Test for the search url pattern."""
        search = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "search":
                search = urlPattern

        self.assertIsNotNone(search)
        self.assertEqual(str(search.pattern), "search")
        self.assertEqual(search.callback, views.search)
