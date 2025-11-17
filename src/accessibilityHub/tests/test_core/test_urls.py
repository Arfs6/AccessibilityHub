"""Test for the core app.
The test includes testing the url patterns
and using `django.test.client` on all urls.
"""

from django.test import SimpleTestCase, TestCase, client
from django.views.generic import TemplateView

from core import urls
from core import views


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
            if urlPattern.name == 'home':
                home = urlPattern

        self.assertIsNotNone(home)
        self.assertEqual(str(home.pattern), '')
        self.assertIs(home.callback.view_class, TemplateView)

    def test_urlpattern_login(self):
        """Verify the data in the login pattern."""
        login = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'login':
                login = urlPattern

        self.assertIsNotNone(login)
        self.assertEqual(str(login.pattern), 'accounts/login')
        self.assertIs(login.callback.view_class, views.CoreLoginView)

    def test_urlpattern_logout(self):
        """Verify the data in the logout pattern."""
        logout = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'logout':
                logout = urlPattern

        self.assertIsNotNone(logout)
        self.assertEqual(str(logout.pattern), 'accounts/logout')
        self.assertEqual(logout.callback, views.coreLogoutView)

    def test_urlpattern_signup(self):
        """Verify the data in the signup pattern."""
        signup = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'signup':
                signup = urlPattern

        self.assertIsNotNone(signup)
        self.assertEqual(str(signup.pattern), 'accounts/signup')
        self.assertEqual(signup.callback, views.coreSignupView)

    def test_urlpattern_about(self):
        """Verify the data in the about pattern."""
        about = None
        for urlPattern in urls.urlpatterns:
            if urlPattern.name == 'about':
                about = urlPattern

        self.assertIsNotNone(about)
        self.assertEqual(str(about.pattern), 'about')
        self.assertIs(about.callback.view_class, TemplateView)
