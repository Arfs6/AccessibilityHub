"""Test for the api app.
The test includes testing the url patterns
and using `django.test.client` on all urls.
"""

from api import urls, views
from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from reviews import forms


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


class TestUrls(TestCase):
    """A higher level test for api urls."""

    fixtures = ["User.json", "Tool.json", "Review.json", "Owner.json"]

    def setup(self):
        """Setup for all tests."""
        self.client = Client(ensure_csrf_check=True)
        self.user = User.objects.all().first()
        self.client.force_login(self.user)

    def test_newOwner(self):
        """Test for new owner url."""
        newOwnerUrl = "api:newOwner"
        response = self.client.post(
            reverse(newOwnerUrl),
            data={
                "name": "New Owner",
                "url": "https://owner.new",
                "description": "New owner description.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/new_tool_form.html")
        self.assertIsInstance(response.context["form"], forms.ToolForm)

        # Test for failed test.
        response = self.client.post(reverse(newOwnerUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/new_owner_form.html")
        self.assertIsInstance(response.context["form"], forms.OwnerForm)
        self.assertTrue(response.context["form"].errors)

    def test_newTool(self):
        """Test for the new tool url."""
        newToolUrl = "api:newTool"
        response = self.client.post(
            reverse(newToolUrl),
            data={
                "name": "New Tool",
                "url": "https://tool.new",
                "description": "New tool description",
                "ownerName": "New Owner",
                "ownerUrl": "https://owner.new",
                "ownerDescription": "New owner description",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/new_tool_success.html")

        # Test for invalid data.
        response = self.client.post(reverse(newToolUrl))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/new_tool_form.html")
        self.assertIsInstance(response.context["form"], forms.ToolForm)
