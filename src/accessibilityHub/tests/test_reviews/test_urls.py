"""Tests for url in the reviews app."""

from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from reviews import forms, models, urls, views


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


class TestURLS(TestCase):
    """Test for urls
    This tests are high level.
    Test includes checks for templates, status codes and context (where applicable).
    """

    fixtures = ["User.json", "Tool.json", "Owner.json", "Review.json"]

    def setup(self):
        """Setup for each test."""
        self.client = Client(ensure_csrf_check=True)

    def test_index(self):
        """Test for the index page."""
        indexUrl = "reviews:index"
        response = self.client.get(reverse(indexUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/index.html")
        self.assertQuerySetEqual(
            response.context["tools"].order_by("pk"),
            models.Tool.allVerified().order_by("pk"),
        )

    def test_owner(self):
        """Test for the owner url."""
        ownerUrl = "reviews:owner"
        owner = models.Owner.allVerified().first()
        self.assertIsNotNone(owner, "A verified `Owner` is required for testing.")
        response = self.client.get(
            reverse(ownerUrl, kwargs={"base36Id": owner.base36Id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/owner.html")
        self.assertEqual(response.context["owner"], owner)
        self.assertQuerySetEqual(
            response.context["tools"], owner.tools.filter(verified=True).all()
        )

        owner = models.Owner.objects.filter(verified=False).first()
        response = self.client.get(
            reverse(ownerUrl, kwargs={"base36Id": owner.base36Id})
        )
        self.assertEqual(response.status_code, 404)

        toolUrl = "reviews:tool"

    def test_tool(self):
        """Test for the tool url."""
        toolUrl = "reviews:tool"
        tool = models.Tool.allVerified().first()
        response = self.client.get(
            reverse(
                toolUrl,
                kwargs={"ownerBase36Id": tool.owner.base36Id, "toolSlug": tool.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/tool.html")
        self.assertEqual(response.context["owner"], tool.owner)
        self.assertEqual(response.context["tool"], tool)
        self.assertQuerySetEqual(
            response.context["reviews"].order_by("pk"),
            tool.reviews.exclude(comment="").order_by("pk"),
        )
        self.assertIsNone(response.context["form"])  # user is anonymous
        self.assertIsNone(response.context["userReview"])

        # Test for verified=False
        tool = models.Tool.objects.filter(verified=False).first()
        response = self.client.get(
            reverse(
                toolUrl,
                kwargs={"ownerBase36Id": tool.owner.base36Id, "toolSlug": tool.slug},
            )
        )
        self.assertEqual(response.status_code, 404)

        # Test with logged in user.
        tool = models.Tool.allVerified().first()
        user = User.objects.exclude(
            reviews__tool=tool
        ).first()  # user hasn't reviewed tool
        self.assertRaises(models.Review.DoesNotExist, tool.reviews.get, user=user)
        self.client.force_login(user)
        response = self.client.get(
            reverse(
                toolUrl,
                kwargs={"ownerBase36Id": tool.owner.base36Id, "toolSlug": tool.slug},
            )
        )
        self.assertIsNotNone(response.context["form"])
        _form = forms.ReviewForm()
        self.assertDictEqual(_form.initial, response.context["form"].initial)

        # Let's create a review.
        response = self.client.post(
            reverse(
                toolUrl,
                kwargs={"ownerBase36Id": tool.owner.base36Id, "toolSlug": tool.slug},
            ),
            data={"rating": 3},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/tool.html")
        _form = forms.ReviewForm(instance=user.reviews.get(tool=tool))
        self.assertEqual(response.context["form"].instance, _form.instance)

        # Test for put.
        response = self.client.put(
            reverse(
                toolUrl,
                kwargs={"ownerBase36Id": tool.owner.base36Id, "toolSlug": tool.slug},
            ),
            data={"comment": "This is a long text.\nIt could be multiple lines."},
        )
        self.assertEqual(response.status_code, 200)
        _form = forms.ReviewForm(instance=tool.reviews.get(user=user))

    def test_new(self):
        """Test for the new url."""
        newUrl = "reviews:newTool"
        response = self.client.get(reverse(newUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/new_tool.html")
        self.assertEqual(response.context["title"], "Request New Tool")

    def test_search(self):
        """Test for the search url."""
        searchUrl = "reviews:search"
        tool = models.Tool.allVerified().first()
        response = self.client.get(reverse(searchUrl), data={"searchTerm": tool.name[1:4]})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/search.html")
        self.assertIn(tool,response.context["tools"] )

        response = self.client.get(reverse(searchUrl))
        self.assertEqual(response.status_code, 400)
