"""Test for the core app.
The test includes testing the url patterns
and using `django.test.client` on all urls.
"""

from django.views.generic.base import RedirectView
from core import urls, views
from django.conf import settings
from django.test import SimpleTestCase, TestCase, client
from django.urls import reverse
from django.views.generic import TemplateView


class TestURLPatterns(SimpleTestCase):
    """Test all the url patterns in core.url"""

    def test_appName(self):
        """Core should Have a namespace."""
        self.assertTrue(urls.app_name)
        self.assertIsInstance(urls.app_name, str)

    def test_hasName(self):
        """All urlpatterns should have a name."""
        for urlPattern in urls.urlpatterns:
            self.assertIsNotNone(urlPattern.name)

    def test_urlPattern_home(self):
        """Verify the data in the home url pattern."""
        home = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "home":
                home = urlPattern

        self.assertIsNotNone(home)
        self.assertEqual(str(home.pattern), "")
        self.assertIs(home.callback.view_class, TemplateView)

    def test_urlpattern_login(self):
        """Verify the data in the login pattern."""
        login = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "login":
                login = urlPattern

        self.assertIsNotNone(login)
        self.assertEqual(str(login.pattern), "accounts/login")
        self.assertIs(login.callback.view_class, views.CoreLoginView)

    def test_urlpattern_logout(self):
        """Verify the data in the logout pattern."""
        logout = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "logout":
                logout = urlPattern

        self.assertIsNotNone(logout)
        self.assertEqual(str(logout.pattern), "accounts/logout")
        self.assertEqual(logout.callback, views.coreLogoutView)

    def test_urlpattern_signup(self):
        """Verify the data in the signup pattern."""
        signup = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "signup":
                signup = urlPattern

        self.assertIsNotNone(signup)
        self.assertEqual(str(signup.pattern), "accounts/signup")
        self.assertEqual(signup.callback, views.coreSignupView)

    def test_urlpattern_about(self):
        """Verify the data in the about pattern."""
        about = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == "about":
                about = urlPattern

        self.assertIsNotNone(about)
        self.assertEqual(str(about.pattern), "about")
        self.assertIs(about.callback.view_class, TemplateView)


class TestURLS(TestCase):
    """Test all the urls in core.
    This test includes checking requests and response data.
    """

    fixtures = ["User"]

    def setup(self):
        """Setup for each tests."""
        self.client = client.Client(enforce_csrf_checks=True)

    def test_home(self):
        """Test for the home page."""
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_login(self):
        """Test for the login page."""
        loginUrl = reverse("core:login")
        response = self.client.get(loginUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/login.html")

        # Test successful login.
        response = self.client.post(
            loginUrl,
            {"username": "james", "password": "Jones.2020"},
            follow=True,
        )
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.client.logout()

        # Test successful login with next set as not home.
        redirectUrl = reverse("core:about")
        response = self.client.post(
            loginUrl,
            {"username": "james", "password": "Jones.2020", "next": redirectUrl},
            follow=True,
        )
        self.assertRedirects(response, redirectUrl)
        self.assertTemplateUsed(response, "core/about.html")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.client.logout()

        # test for wrong username and wrong password.
        response = self.client.post(
            loginUrl, {"username": "DoesNotExist", "password": "Jones.2020"}
        )
        self.assertTemplateUsed(response, "core/login.html")
        self.assertTrue(response.context["errors"])  # contains errors in it.

        response = self.client.post(
            loginUrl, {"username": "james", "password": "InvalidPassword"}
        )
        self.assertTemplateUsed(response, "core/login.html")
        self.assertTrue(response.context["errors"])

    def test_signup(self):
        """Test for the signup page."""
        signupUrl = reverse("core:signup")
        response = self.client.get(signupUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/signup.html")

        # Test for successful signup.
        data = {
            "username": "test",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password1": "Jones.2020",
            "password2": "Jones.2020",
        }
        response = self.client.post(signupUrl, data, follow=True)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        # reset
        response.wsgi_request.user.delete()
        self.client.logout()

        # test for missing fields.
        for field in ["username", "first_name", "email", "password1", "password2"]:
            _data = data.copy()
            del _data[field]
            response = self.client.post(signupUrl, _data)
            self.assertTemplateUsed(response, "core/signup.html")
            self.assertTrue(response.context['form'].errors)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        """Test for the logout page."""
        logoutUrl = reverse("core:logout")
        response = self.client.get(logoutUrl)
        self.assertTemplateUsed("core/logout.html")
        self.assertEqual(response.status_code, 200)

        # Test for successful logout.
        response = self.client.delete(logoutUrl)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get("hx-redirect"), settings.LOGOUT_REDIRECT_URL)

    def test_about(self):
        """Test for the about page."""
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/about.html")
