"""Tests for Reviews page templates and shared listing components."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from reviews.models import Owner, Review, Tool


class TestReviewsTemplates(TestCase):
    """Verify the Reviews pages expose the planned card-based structure."""

    def setUp(self):
        self.owner = Owner.objects.create(
            name='Example Owner',
            url='https://example.com',
            description='An accessible tool publisher.',
            verified=True,
        )
        self.tool = Tool.objects.create(
            name='Example Tool',
            url='https://example.com/tool',
            description='A tool description long enough to appear in a listing card.',
            owner=self.owner,
            verified=True,
        )

    def test_indexUsesListingCardsAndRatings(self):
        """The index should render responsive cards with accessible rating text."""
        user = get_user_model().objects.create_user(username='reviewer')
        Review.objects.create(user=user, tool=self.tool, rating=3, comment='Useful.')
        second_user = get_user_model().objects.create_user(username='second-reviewer')
        Review.objects.create(
            user=second_user, tool=self.tool, rating=4, comment='Good.'
        )

        response = self.client.get(reverse('reviews:index'))
        self.assertContains(response, '<h1>Tool Reviews</h1>')
        self.assertContains(response, 'class="col s12 m6 l4"')
        self.assertContains(response, 'class="card listing-card"')
        self.assertContains(response, 'Rating: 3.5 out of 5')
        self.assertContains(response, 'class="material-icons">star</i>', count=3)
        self.assertContains(response, 'class="material-icons">star_half</i>', count=1)
        self.assertContains(response, 'class="material-icons">star_border</i>', count=1)

    def test_indexShowsEmptyStateWhenNoToolsExist(self):
        """The listing should explain how to proceed when it is empty."""
        Tool.objects.all().delete()

        response = self.client.get(reverse('reviews:index'))

        self.assertContains(response, 'No tools yet. Be the first to request one.')
        self.assertContains(response, 'class="card empty-state"')

    def test_toolAndOwnerUseCardsUniqueReviewIdsAndExternalLinkSafety(self):
        """Detail and owner pages should use cards and stable review anchors."""
        user = get_user_model().objects.create_user(
            username='reviewer',
            first_name='Review',
            last_name='Author',
        )
        first = Review.objects.create(
            user=user, tool=self.tool, rating=4, comment='First.'
        )
        second = Review.objects.create(
            user=user, tool=self.tool, rating=3, comment='Second.'
        )

        tool_response = self.client.get(
            reverse(
                'reviews:tool',
                kwargs={
                    'ownerBase36Id': self.owner.base36Id,
                    'toolSlug': self.tool.slug,
                },
            )
        )
        self.assertContains(tool_response, f'id="review-{first.pk}"')
        self.assertContains(tool_response, f'id="review-{second.pk}"')
        self.assertContains(tool_response, 'class="card"')
        self.assertContains(tool_response, 'rel="noopener"')
        self.assertContains(tool_response, 'Average rating: 3.5 out of 5')
        self.assertContains(tool_response, 'class="material-icons">star_half</i>')

        owner_response = self.client.get(
            reverse('reviews:owner', kwargs={'base36Id': self.owner.base36Id})
        )
        self.assertContains(owner_response, '<h2>Tools</h2>')
        self.assertContains(owner_response, 'class="card listing-card"')
        self.assertContains(owner_response, 'rel="noopener"')
        self.assertNotContains(owner_response, 'id="review-')

    def test_searchUsesTheSameListingCardPartial(self):
        """Search results should use the same card and empty-state components."""
        response = self.client.get(
            reverse('reviews:search'),
            {'searchTerm': self.tool.name},
        )

        self.assertContains(response, '<h2>Search Results</h2>')
        self.assertContains(response, 'class="card listing-card"')

        empty_response = self.client.get(
            reverse('reviews:search'),
            {'searchTerm': 'does-not-exist'},
        )
        self.assertContains(empty_response, 'class="card empty-state"')

    def test_reviewFormPreservesCreateAndUpdateHtmxBranches(self):
        """New reviews use POST fallback while existing reviews use PUT."""
        user = get_user_model().objects.create_user(username='reviewer')
        self.client.force_login(user)
        url = reverse(
            'reviews:tool',
            kwargs={
                'ownerBase36Id': self.owner.base36Id,
                'toolSlug': self.tool.slug,
            },
        )

        create_response = self.client.get(url)
        self.assertContains(create_response, 'method="post"')
        self.assertContains(create_response, 'hx-post=')
        self.assertContains(create_response, 'hx-target="#main-content"')
        self.assertContains(create_response, 'hx-swap="innerHTML"')

        Review.objects.create(user=user, tool=self.tool, rating=4, comment='Existing.')
        update_response = self.client.get(url)
        self.assertContains(update_response, 'hx-put=')
        self.assertNotContains(update_response, 'method="post"')

    def test_newToolSuccessIsACompleteSwapFragment(self):
        """The successful two-step response should render the planned card."""
        user = get_user_model().objects.create_user(username='requester')
        self.client.force_login(user)
        response = self.client.post(
            reverse('reviews:newOwnerAndTool'),
            {
                'formName': 'ToolForm',
                'name': 'New Tool',
                'description': 'New tool.',
                'url': 'https://tool.example.com',
                'ownerName': 'New Owner',
                'ownerDescription': 'New owner.',
                'ownerUrl': 'https://new.example.com',
            },
        )
        self.assertContains(response, 'class="card"')
        self.assertContains(response, 'Thank you!')
        self.assertContains(response, 'Your request has been received')
        self.assertContains(response, 'Return to the reviews page')
