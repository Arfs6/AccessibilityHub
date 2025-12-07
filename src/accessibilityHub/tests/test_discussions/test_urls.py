"""Tests for url in the discussions app."""

import typing

from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from discussions import models, urls, views


class TestURLPatterns(SimpleTestCase):
    """Tests for the urlpatterns of the discussions apps."""

    def test_app_name(self):
        """Verify the app name."""
        self.assertEqual(urls.app_name, 'discussions')

    def test_hasName(self):
        """All urlpatterns should have a name."""
        for urlPattern in urls.urlpatterns:
            self.assertTrue(urlPattern.name)

    def test_landing(self):
        """Tests for the landing url pattern."""
        landing = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'landing':
                landing = urlPattern

        self.assertIsNotNone(landing)
        self.assertEqual(landing.callback, views.landing)
        self.assertEqual(str(landing.pattern), '')

    def test_index(self):
        """Test for the index url pattern."""
        index = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'index':
                index = urlPattern

        self.assertIsNotNone(index)
        self.assertEqual(str(index.pattern), 'topics')
        self.assertEqual(index.callback, views.index)

    def test_newTopic(self):
        """Test for the new topic url pattern."""
        newTopic = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'newTopic':
                newTopic = urlPattern

        self.assertIsNotNone(newTopic)
        self.assertEqual(str(newTopic.pattern), 'topics/new')
        self.assertEqual(newTopic.callback, views.newTopic)

    def test_topicPage(self):
        """Test for the topic page url pattern."""
        topicPage = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'topicPage':
                topicPage = urlPattern
        self.assertIsNotNone(topicPage)
        self.assertEqual(str(topicPage.pattern), 'topics/<str:base36Id>')
        self.assertEqual(topicPage.callback, views.topicPage)

    def test_search(self):
        """Test for the search url pattern."""
        search = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'search':
                search = urlPattern

        self.assertIsNotNone(search)
        self.assertEqual(str(search.pattern), 'search')
        self.assertEqual(search.callback, views.search)


class TestURLS(TestCase):
    """A higher level test for each url in discussions."""

    fixtures: typing.ClassVar = ['User.json', 'Topic.json', 'Comment.json']

    def setup(self):
        """Setup for each tests."""
        self.client = Client(ensure_csrf_check=True)

    def test_landing(self):
        """Tests for the landing url."""
        landingUrl = 'discussions:landing'
        response = self.client.get(reverse(landingUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/landing.html')

    def test_index(self):
        """Tests for the index url."""
        indexUrl = 'discussions:index'
        response = self.client.get(reverse(indexUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/index.html')
        self.assertQuerySetEqual(response.context['latestTopics'], models.Topic.objects.all()[:5])

    def test_newTopic(self):
        """Test for the new topic url."""
        newTopicUrl = 'discussions:newTopic'
        response = self.client.get(reverse(newTopicUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/newTopic.html')
        self.assertIsNone(response.context['form'])  # Not signed in.

        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse(newTopicUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/newTopic.html')
        self.assertIsNone(response.context['form'].instance.pk)

        response = self.client.post(
            reverse(newTopicUrl),
            data={'name': 'topic name', 'description': 'topic description'},
        )
        topic = models.Topic.objects.get(name='topic name', description='topic description')
        self.assertEqual(
            response.headers['hx-redirect'],
            reverse('discussions:topicPage', kwargs={'base36Id': topic.base36Id}),
        )

        # test without name and without descriptions in data.
        response = self.client.post(reverse(newTopicUrl), data={'name': 'Second Topic Name'})
        self.assertTrue(response.context['form'].errors)
        response = self.client.post(reverse(newTopicUrl), data={'description': 'Second topic description'})
        self.assertTrue(response.context['form'].errors)

    def test_topicPage(self):
        """Test for the topic page url."""
        topicPageUrl = 'discussions:topicPage'
        topic = models.Topic.objects.exclude(comments=None).first()
        response = self.client.get(reverse(topicPageUrl, kwargs={'base36Id': topic.base36Id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/topic.html')
        self.assertEqual(response.context['topic'], topic)
        self.assertQuerySetEqual(response.context['comments'], topic.comments.all())

        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse(topicPageUrl, kwargs={'base36Id': topic.base36Id}))
        self.assertIsNone(response.context['form'].instance.pk)

        # test for post with empty comment.
        response = self.client.post(reverse(topicPageUrl, kwargs={'base36Id': topic.base36Id}))
        self.assertTrue(response.context['form'].errors)

        # Test for post method with content data
        response = self.client.post(
            reverse(topicPageUrl, kwargs={'base36Id': topic.base36Id}),
            data={'content': 'Comment on a topic.'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/topic.html')
        self.assertTrue(topic.comments.get(content='Comment on a topic.'))

    def test_search(self):
        """Test for the search url."""
        searchUrl = 'discussions:search'
        response = self.client.get(reverse(searchUrl), data={'q': '2025'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/searchResults.html')
        self.assertQuerySetEqual(
            response.context['topics'],
            models.Topic.objects.filter(name__icontains='2025').all(),
        )

        # test for q is empty.
        response = self.client.get(reverse(searchUrl))
        self.assertEqual(response.status_code, 400)
