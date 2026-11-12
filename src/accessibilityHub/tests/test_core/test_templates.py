"""Tests for core templates and their supporting frontend assets."""

import re
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.template import loader
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from discussions.models import Topic
from reviews.models import Owner, Tool


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
        script = Path(scriptPath).read_text(encoding='utf-8')

        self.assertIn('accessibilityhub-demo-banner-seen', script)
        self.assertIn('rememberSeen', script)
        self.assertIn('hasBeenViewed = true', script)

    def test_mainJs_dismissesWhenBannerLeavesViewport(self):
        """Leaving the viewport after viewing the banner should dismiss it."""
        scriptPath = finders.find('core/main.js')
        self.assertIsNotNone(scriptPath)
        script = Path(scriptPath).read_text(encoding='utf-8')

        self.assertIn('IntersectionObserver', script)
        self.assertIn('threshold: 0.25', script)
        self.assertIn('observer.disconnect()', script)
        self.assertIn('hasBeenViewed', script)

    def test_banner_livesOutsideMainSwapTarget(self):
        """A htmx swap must not destroy the banner while its timer is running."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertLess(
            html.index('id="demo-banner"'), html.index('<main id="main-content"')
        )


class TestNavigationHeader(TestCase):
    """Tests for the responsive navigation header."""

    def test_homePage_usesFrameworkResponsiveNavigation(self):
        """The menus should use Materialize's 993 px visibility utilities."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertIn('hide-on-med-and-down', html)
        self.assertIn('show-on-medium-and-down', html)
        self.assertNotIn('hide-on-large-only', html)
        self.assertIn(
            '<nav class="sidenav" id="mobile-sidenav" aria-label="Mobile" aria-hidden="true" inert>',
            html,
        )
        self.assertIn('aria-label="Open navigation menu"', html)
        self.assertIn('aria-controls="mobile-sidenav"', html)
        self.assertIn('aria-expanded="false"', html)
        self.assertIn('id="nav-primary"', html)

    def test_authenticated_logoutIsKeyboardFocusable(self):
        """Logout performs an action, so it must be a real focusable button."""
        user = get_user_model().objects.create_user(
            username='logout-test',
            password='unused-password',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertIn('type="button" class="nav-link" hx-delete="', html)
        self.assertNotIn('<a hx-delete=', html)

    def test_mainCss_removesCustomNavigationBreakpoint(self):
        """The custom 1100 px breakpoint is replaced by the framework utility."""
        cssPath = finders.find('core/main.css')
        self.assertIsNotNone(cssPath)
        css = Path(cssPath).read_text(encoding='utf-8')

        self.assertNotIn('1099.98px', css)
        self.assertNotIn('1100px', css)
        self.assertIn('.navbar', css)

    def test_page_marksCurrentSection(self):
        """The active section should carry aria-current, not only colour."""
        response = self.client.get(reverse('reviews:index'))
        html = response.content.decode()
        reviewsUrl = reverse('reviews:index')

        self.assertRegex(
            html,
            rf'<a href="{re.escape(reviewsUrl)}"[^>]*aria-current="page"',
        )


class TestThemeSystem(TestCase):
    """Tests for the dual-theme boot, toggle, and assets."""

    def test_head_bootsThemeAndBannerState(self):
        """The single early script should set the theme and remember the banner."""
        response = self.client.get(reverse('core:home'))

        self.assertContains(response, 'accessibilityhub-theme')
        self.assertContains(response, 'document.documentElement.dataset.theme')
        self.assertContains(response, 'prefers-color-scheme: light')
        self.assertContains(response, 'name="theme-color"')

    def test_navigation_hasThemeToggle(self):
        """Every navigation copy should expose the same accessible toggle state."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()
        toggles = re.findall(r'<button[^>]*data-theme-toggle[^>]*>', html)

        self.assertEqual(len(toggles), 2)
        for toggle in toggles:
            self.assertIn('aria-pressed="false"', toggle)
        self.assertEqual(html.count('>Light theme</span>'), 2)
        self.assertEqual(html.count('theme-icon-dark'), 2)
        self.assertEqual(html.count('theme-icon-light'), 2)

    def test_mainCss_choosesThemeIconFromAttribute(self):
        """The correct icon should paint before JavaScript updates the toggle."""
        cssPath = finders.find('core/main.css')
        self.assertIsNotNone(cssPath)
        css = Path(cssPath).read_text(encoding='utf-8')

        self.assertIn(':root[data-theme="light"] .theme-toggle .theme-icon-dark', css)
        self.assertIn(':root[data-theme="light"] .theme-toggle .theme-icon-light', css)

    def test_mainJs_appliesAndPersistsTheme(self):
        """The toggle should update the attribute and save the choice."""
        scriptPath = finders.find('core/main.js')
        self.assertIsNotNone(scriptPath)
        script = Path(scriptPath).read_text(encoding='utf-8')

        self.assertIn('applyTheme', script)
        self.assertIn('accessibilityhub-theme', script)
        self.assertIn('localStorage.setItem', script)
        self.assertIn('aria-pressed', script)
        self.assertIn('prefers-reduced-motion: reduce', script)

    def test_mainJs_drivesSidenavFromInstance(self):
        """Sidenav focus, inert state, and escape handling should follow the instance."""
        scriptPath = finders.find('core/main.js')
        self.assertIsNotNone(scriptPath)
        script = Path(scriptPath).read_text(encoding='utf-8')

        self.assertIn('onOpenStart', script)
        self.assertIn('onCloseStart', script)
        self.assertIn('onCloseEnd', script)
        self.assertIn('sidenavInstance.close()', script)
        self.assertIn('sidenavEl.inert = !open', script)
        self.assertIn(
            "sidenavEl.setAttribute('aria-hidden', open ? 'false' : 'true')", script
        )
        self.assertIn('!sidenavInstance || !sidenavInstance.isOpen', script)
        self.assertIn('if (!sidenavInstance || sidenavInstance.isOpen) {', script)
        self.assertIn("querySelector('.navbar .brand-logo')", script)
        self.assertIn('clearPrimaryNavAriaHidden', script)
        self.assertIn('shouldRestoreFocus', script)

    def test_mainJs_trapsFocusAndClosesAtDesktopBreakpoint(self):
        """The drawer must contain Tab focus and close when the layout becomes desktop."""
        scriptPath = finders.find('core/main.js')
        self.assertIsNotNone(scriptPath)
        script = Path(scriptPath).read_text(encoding='utf-8')

        self.assertIn('getSidenavControls', script)
        self.assertIn('event.shiftKey', script)
        self.assertIn('(min-width: 993px)', script)
        self.assertIn('closeSidenavOnDesktop', script)

    def test_mainCss_definesLightAndDarkThemes(self):
        """Both palettes and the background layer should be in main.css."""
        cssPath = finders.find('core/main.css')
        self.assertIsNotNone(cssPath)
        css = Path(cssPath).read_text(encoding='utf-8')

        self.assertIn(':root[data-theme="light"]', css)
        self.assertIn('--md-sys-color-primary', css)
        self.assertIn('--control-border', css)
        self.assertIn('color-scheme: dark', css)
        self.assertIn('body::before', css)
        self.assertIn('prefers-contrast: more', css)
        self.assertNotIn('#A5C6FF', css)
        self.assertNotIn('#1A1C1E', css)

    def test_themeAssetsExist(self):
        """The favicon and both background patterns should be real static assets."""
        for asset in (
            'core/img/favicon.svg',
            'core/img/background-dark.webp',
            'core/img/background-light.webp',
        ):
            with self.subTest(asset=asset):
                assetPath = finders.find(asset)
                self.assertIsNotNone(assetPath)
                data = Path(assetPath).read_bytes()
                self.assertGreater(len(data), 0)
                if asset.endswith('.webp'):
                    self.assertEqual(data[:4], b'RIFF')
                    self.assertEqual(data[8:12], b'WEBP')


class TestPageFrame(TestCase):
    """Tests for the document skeleton and footer."""

    def test_homePage_hasSkipLinkAndMainTarget(self):
        """The skip link should target the real main element."""
        response = self.client.get(reverse('core:home'))

        self.assertContains(response, 'class="skip-link"')
        self.assertContains(response, 'href="#main-content"')
        self.assertContains(response, '<main id="main-content"')
        self.assertContains(response, 'tabindex="-1"')

    def test_head_hasDescriptionAndFavicon(self):
        """The document should expose description metadata and a favicon."""
        response = self.client.get(reverse('core:home'))

        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'rel="icon"')
        self.assertContains(response, 'favicon.svg')

    def test_materialize_isPinnedTo240(self):
        """The CSS and JS assets should use the verified 2.4.0 build."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertIn('materialize@2.4.0', html)
        self.assertNotIn('materialize@2.0.3', html)
        self.assertLess(
            html.index('materialize@2.4.0/dist/css/materialize.min.css'),
            html.index('core/main.css'),
        )

    def test_cdnAssetsUseSubresourceIntegrity(self):
        """Pinned CDN scripts and styles should be verified by the browser."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertGreaterEqual(html.count('integrity="sha384-'), 3)
        self.assertGreaterEqual(html.count('crossorigin="anonymous"'), 3)
        self.assertIn('unpkg.com/htmx.org@1.9.6', html)

    def test_footer_usesCurrentYearAndWorkingLinks(self):
        """The footer should not keep the stale year or dead personal domain."""
        response = self.client.get(reverse('core:home'))
        html = response.content.decode()

        self.assertIn(str(timezone.localdate().year), html)
        self.assertIn('github.com/arfs6', html)
        self.assertIn('GitHub', html)
        self.assertNotIn('arfs6.me', html)

    def test_footer_template_usesDynamicYear(self):
        """The template source should use Django's now tag for the year."""
        template = loader.get_template('core/footer.html')
        source = Path(template.origin.name).read_text(encoding='utf-8')

        self.assertIn('{% now "Y" %}', source)


class TestSharedComponents(TestCase):
    """Tests for the shared card, button, and search-toolbar patterns."""

    def test_authForms_useCardsAndFrameworkButtons(self):
        """Login and signup should use card shells and framework buttons."""
        for urlName, label in (('core:login', 'Login'), ('core:signup', 'Signup')):
            with self.subTest(page=urlName):
                response = self.client.get(reverse(urlName))
                html = response.content.decode()

                self.assertIn('class="card"', html)
                self.assertIn('class="btn btn-filled"', html)
                self.assertIn(f'>{label}</button>', html)
                self.assertNotIn('<input type="submit"', html)

    def test_logout_keepsHtmxDeleteWithCardButton(self):
        """Logout must keep its DELETE action when restyled as a button."""
        response = self.client.get(
            reverse('core:logout'),
            {'next': reverse('reviews:index')},
        )
        html = response.content.decode()

        self.assertIn('class="card"', html)
        self.assertIn('class="btn btn-filled"', html)
        self.assertIn('hx-delete="', html)
        self.assertIn('?next=', html)
        self.assertNotIn('<input type="submit"', html)

    def test_reviewAndNewToolForms_useCardsAndFrameworkButtons(self):
        """The review and two-step new-tool forms should share the form card."""
        user = get_user_model().objects.create_user(
            username='reviewer',
            password='unused-password',
        )
        owner = Owner.objects.create(
            name='Example Owner',
            url='https://example.com',
            verified=True,
        )
        tool = Tool.objects.create(
            name='Example Tool',
            url='https://example.com/tool',
            owner=owner,
            verified=True,
        )
        self.client.force_login(user)

        pages = (
            (
                reverse(
                    'reviews:tool',
                    kwargs={
                        'ownerBase36Id': owner.base36Id,
                        'toolSlug': tool.slug,
                    },
                ),
                'Submit',
            ),
            (reverse('reviews:newOwnerAndTool'), 'Submit'),
        )
        for url, label in pages:
            with self.subTest(page=url):
                html = self.client.get(url).content.decode()

                self.assertIn('class="card"', html)
                self.assertIn('class="btn btn-filled"', html)
                self.assertIn(f'>{label}</button>', html)
                self.assertNotIn('<input type="submit"', html)

    def test_topicForms_useCardsAndFrameworkButtons(self):
        """Topic creation and commenting should use the shared form card."""
        user = get_user_model().objects.create_user(
            username='topic-user',
            password='unused-password',
        )
        topic = Topic.objects.create(
            name='Example Topic',
            description='A topic for testing.',
            createdBy=user,
        )
        self.client.force_login(user)

        pages = (
            (reverse('discussions:newTopic'), 'Create Topic'),
            (
                reverse(
                    'discussions:topicPage',
                    kwargs={'base36Id': topic.base36Id},
                ),
                'Comment',
            ),
        )
        for url, label in pages:
            with self.subTest(page=url):
                html = self.client.get(url).content.decode()

                self.assertIn('class="card"', html)
                self.assertIn('class="btn btn-filled"', html)
                self.assertIn(f'>{label}</button>', html)
                self.assertNotIn('<input type="submit"', html)

    def test_searchToolbars_useVisibleLabelsAndLiveRegions(self):
        """Both indexes should expose labelled search and announced results."""
        reviews = self.client.get(reverse('reviews:index')).content.decode()
        self.assertIn('class="search-form"', reviews)
        self.assertIn('for="search-term">Search tools</label>', reviews)
        self.assertIn('role="search"', reviews)
        self.assertIn('class="btn btn-tonal"', reviews)
        self.assertIn('col s12 m6 l9', reviews)
        self.assertIn('col s12 m6 l3', reviews)
        self.assertIn('id="tool-listing" aria-live="polite"', reviews)
        self.assertNotIn('type="submit" value=', reviews)

        discussions = self.client.get(reverse('discussions:index')).content.decode()
        self.assertIn('class="search-form"', discussions)
        self.assertIn('for="search-term">Search topics</label>', discussions)
        self.assertIn('role="search"', discussions)
        self.assertNotIn('role="Search"', discussions)
        self.assertIn('class="btn btn-tonal"', discussions)
        self.assertIn('col s12 m6 l9', discussions)
        self.assertIn('col s12 m6 l3', discussions)
        self.assertIn('id="topics-listing" aria-live="polite"', discussions)
        self.assertNotIn('type="submit" value=', discussions)

    def test_mainCss_definesSharedComponents(self):
        """The shared component classes should live in the site stylesheet."""
        cssPath = finders.find('core/main.css')
        self.assertIsNotNone(cssPath)
        css = Path(cssPath).read_text(encoding='utf-8')

        for token in (
            '.card {',
            '.card .card-content',
            '.listing-description',
            '.empty-state',
            '.stars',
            '.search-controls',
            '.btn .material-icons',
        ):
            with self.subTest(token=token):
                self.assertIn(token, css)

        self.assertNotIn('form input[type="submit"]', css)
