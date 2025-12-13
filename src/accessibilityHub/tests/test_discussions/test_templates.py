"""Tests for discussions templates."""

from django.contrib.auth.models import AnonymousUser, User
from django.template import RequestContext, loader
from django.test import RequestFactory, TestCase
from django.urls import reverse


class TestNewTopic(TestCase):
    """Tests for the `discussions/newTopic` template."""

    def setUp(self):
        """Setup for each test."""
        self.templateName = 'discussions/newTopic.html'
        factory = RequestFactory(csrf_check=True)
        self.request = factory.get(reverse('discussions:newTopic'))
        self.request.user = AnonymousUser()
        self.context = RequestContext(self.request)
        self.user = User.objects.create_user(username='test', email='test@example.com')

    def test_name(self):
        """Verify the name of the template."""
        template = loader.get_template(self.templateName)
        self.assertEqual(template.origin.template_name, self.templateName)

    def test_withAnonymousUser(self):
        """Test with anonymous user."""
        template = loader.get_template(self.templateName)
        renderedHtml = template.render({}, self.request)
        self.assertInHTML(
            f'You need to <a href="{reverse("core:login")}">login</a> to create a topic.',
            renderedHtml,
        )
