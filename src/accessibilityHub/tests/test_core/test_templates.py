"""Tests for core templates and their supporting frontend assets."""

from pathlib import Path

from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse


class TestDemoBanner(TestCase):
    """Tests for the demo banner markup and behaviour."""

    def test_homePage_rendersBannerAndDismissButton(self):
        """The banner and its dismiss button should be rendered."""
        response = self.client.get(reverse('core:home'))

        self.assertContains(response, 'id="demo-banner"')
        self.assertContains(response, 'id="demo-banner-close"')
        self.assertContains(response, 'aria-label="Dismiss demo notice"')

    def test_head_remembersSeenState(self):
        """The head script should hide the banner when it was already seen."""
        response = self.client.get(reverse('core:home'))

        self.assertContains(response, 'accessibilityhub-demo-banner-seen')
        self.assertContains(response, "classList.add('demo-banner-seen')")

    def test_mainJs_persistsSeenStateWhenBannerIsViewed(self):
        """The banner should be remembered as soon as it is visible."""
        scriptPath = finders.find('core/main.js')
        self.assertIsNotNone(scriptPath)
        script = Path(scriptPath).read_text()

        self.assertIn('accessibilityhub-demo-banner-seen', script)
        self.assertIn('rememberSeen', script)
        self.assertIn('hasBeenViewed = true', script)

    def test_mainJs_dismissesWhenBannerLeavesViewport(self):
        """Leaving the viewport after viewing the banner should dismiss it."""
        scriptPath = finders.find('core/main.js')
        self.assertIsNotNone(scriptPath)
        script = Path(scriptPath).read_text()

        self.assertIn('IntersectionObserver', script)
        self.assertIn('threshold: 0.25', script)
        self.assertIn('observer.disconnect()', script)
        self.assertIn('hasBeenViewed', script)


class TestNavigationHeader(TestCase):
    """Tests for the responsive navigation header."""

    def test_homePage_usesSingleResponsiveNavigation(self):
        """The menus should not use conflicting Materialize visibility classes."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertNotIn('hide-on-med-and-down', html)
        self.assertNotIn('hide-on-large-only', html)
        self.assertIn('id="mobile-sidenav"', html)
        self.assertIn('aria-label="Open navigation menu"', html)

    def test_mainCss_switchesNavigationAtTabletBreakpoint(self):
        """The header should switch layouts only when there is room."""
        cssPath = finders.find('core/main.css')
        self.assertIsNotNone(cssPath)
        css = Path(cssPath).read_text()

        self.assertIn('@media only screen and (max-width: 1099.98px)', css)
        self.assertIn('@media only screen and (min-width: 1100px)', css)
        self.assertIn('#mobile-sidenav', css)
