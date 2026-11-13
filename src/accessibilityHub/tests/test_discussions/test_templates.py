"""Tests for discussions templates."""

from django.contrib.auth.models import AnonymousUser, User
from django.template import RequestContext, loader
from django.test import RequestFactory, TestCase
from django.urls import reverse

from discussions.models import Comment, Topic


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


class TestDiscussionsTemplates(TestCase):
    """Verify the Discussions pages expose the planned card-based structure."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='member',
            email='member@example.com',
            first_name='Member',
            last_name='User',
        )
        self.topic = Topic.objects.create(
            name='Accessible forms',
            description='A discussion about building accessible forms.',
            createdBy=self.user,
        )
        self.comment = Comment.objects.create(
            content='This is a useful comment.',
            topic=self.topic,
            createdBy=self.user,
        )

    def test_landingShowsBrowseAndLoginCtasForAnonymousUsers(self):
        """Anonymous visitors should be able to browse or log in to start a topic."""
        response = self.client.get(reverse('discussions:landing'))

        self.assertContains(response, 'class="button-row"')
        self.assertContains(response, 'class="btn btn-filled"')
        self.assertContains(response, 'class="btn btn-tonal"')
        self.assertContains(response, 'Browse topics')
        self.assertContains(response, reverse('discussions:index'))
        self.assertContains(response, 'Login to start a topic')
        self.assertContains(response, reverse('core:login'))
        self.assertNotContains(response, 'Start a topic')

    def test_landingShowsStartTopicCtaForAuthenticatedUsers(self):
        """Authenticated users should get a direct new-topic CTA."""
        self.client.force_login(self.user)

        response = self.client.get(reverse('discussions:landing'))

        self.assertContains(response, 'Start a topic')
        self.assertContains(response, reverse('discussions:newTopic'))
        self.assertNotContains(response, 'Login to start a topic')

    def test_indexShowsTopicCardsAndEmptyState(self):
        """The index should use listing cards and announce htmx search updates."""
        response = self.client.get(reverse('discussions:index'))

        self.assertContains(response, 'id="topics-listing"')
        self.assertContains(response, 'aria-live="polite"')
        self.assertContains(response, 'class="card listing-card"')
        self.assertContains(response, self.topic.name)
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'hx-target="#topics-listing"')
        self.assertContains(response, 'hx-swap="innerHTML"')
        self.assertContains(response, f'action="{reverse("discussions:search")}"')
        self.assertContains(response, 'method="get"')

        Topic.objects.all().delete()
        empty_response = self.client.get(reverse('discussions:index'))
        self.assertContains(empty_response, 'No topics yet.')
        self.assertContains(empty_response, 'class="card empty-state"')

    def test_searchResultsUseCardsAndEmptyState(self):
        """Search results should use the same cards as the index."""
        response = self.client.get(
            reverse('discussions:search'),
            {'q': 'Accessible'},
        )

        self.assertContains(response, '<h2>Search results</h2>')
        self.assertContains(response, 'class="card listing-card"')
        self.assertContains(response, self.topic.name)

        empty_response = self.client.get(
            reverse('discussions:search'),
            {'q': 'does-not-exist'},
        )
        self.assertContains(empty_response, 'class="card empty-state"')
        self.assertContains(
            empty_response,
            'Your search did not match any topic. Please try a different search term.',
        )

    def test_topicPageShowsCardsCommentsAndCommentForm(self):
        """The topic page should render cards and preserve the comment POST flow."""
        self.client.force_login(self.user)
        topic_url = reverse(
            'discussions:topicPage',
            kwargs={'base36Id': self.topic.base36Id},
        )

        response = self.client.get(topic_url)

        self.assertContains(
            response,
            f'<title>{self.topic.name} - Discussions | Accessibility Hub</title>',
        )
        self.assertContains(response, f'<h1>{self.topic.name}</h1>')
        self.assertContains(response, 'Comment by Member User')
        self.assertContains(response, self.comment.content)
        self.assertContains(response, f'action="{topic_url}"')
        self.assertContains(response, 'method="post"')
        self.assertContains(response, f'hx-post="{topic_url}"')
        self.assertContains(response, 'hx-target="#main-content"')
        self.assertContains(response, 'hx-swap="innerHTML"')
        self.assertInHTML(
            '<button type="submit" class="btn btn-filled">Comment</button>',
            response.content.decode(),
        )
        self.assertNotContains(response, '</P>')

        self.comment.delete()
        empty_response = self.client.get(topic_url)
        self.assertContains(empty_response, 'No comments yet.')
        self.assertContains(empty_response, 'class="card empty-state"')

    def test_topicPageShowsLoginPromptForAnonymousUsers(self):
        """Anonymous users should see the existing login prompt instead of the form."""
        response = self.client.get(
            reverse(
                'discussions:topicPage',
                kwargs={'base36Id': self.topic.base36Id},
            )
        )

        self.assertContains(response, reverse('core:login'))
        self.assertContains(response, 'to add a comment.')
        self.assertNotContains(response, 'method="post"')

    def test_newTopicShowsFormCardForAuthenticatedUsers(self):
        """The authenticated new-topic form should keep its htmx-only behavior."""
        self.client.force_login(self.user)
        new_topic_url = reverse('discussions:newTopic')

        response = self.client.get(new_topic_url)

        self.assertContains(response, '<h1>Create a new topic</h1>')
        self.assertContains(response, 'class="card"')
        self.assertContains(response, f'hx-post="{new_topic_url}"')
        self.assertContains(response, 'hx-target="#main-content"')
        self.assertContains(response, 'hx-swap="innerHTML"')
        self.assertContains(response, 'Create Topic')
        self.assertNotContains(response, f'action="{new_topic_url}"')
