(function () {
	'use strict';

	function getTheme() {
		return document.documentElement.dataset.theme === 'light' ? 'light' : 'dark';
	}

	function updateThemeControls(theme) {
		var toggles = document.querySelectorAll('[data-theme-toggle]');
		var isLight = theme === 'light';

		for (var i = 0; i < toggles.length; i++) {
			toggles[i].setAttribute('aria-pressed', isLight ? 'true' : 'false');
		}
	}

	function applyTheme(theme, persist) {
		var nextTheme = theme === 'light' ? 'light' : 'dark';
		document.documentElement.dataset.theme = nextTheme;

		var themeColor = document.querySelector('meta[name="theme-color"]');
		if (themeColor) {
			themeColor.setAttribute('content', nextTheme === 'light' ? '#E0F2F1' : '#04201C');
		}

		updateThemeControls(nextTheme);

		if (persist) {
			try {
				window.localStorage.setItem('accessibilityhub-theme', nextTheme);
			} catch (error) {}
		}
	}

	document.addEventListener('DOMContentLoaded', function () {
		applyTheme(getTheme(), false);

		var toggles = document.querySelectorAll('[data-theme-toggle]');
		for (var i = 0; i < toggles.length; i++) {
			toggles[i].addEventListener('click', function () {
				applyTheme(getTheme() === 'light' ? 'dark' : 'light', true);
			});
		}

		var sidenavTriggers = document.querySelectorAll('.sidenav-trigger');
		var sidenavEl = document.getElementById('mobile-sidenav');
		var primaryNav = document.querySelector('.nav-wrapper ul');
		var sidenavInstance = null;
		var supportsInert = 'inert' in HTMLElement.prototype;
		var desktopQuery = window.matchMedia
			? window.matchMedia('(min-width: 993px)')
			: null;
		var reducedMotion = window.matchMedia
			&& window.matchMedia('(prefers-reduced-motion: reduce)').matches;

		function setSidenavExpanded(expanded) {
			for (var j = 0; j < sidenavTriggers.length; j++) {
				sidenavTriggers[j].setAttribute('aria-expanded', expanded ? 'true' : 'false');
			}
		}

		function setSidenavState(open) {
			setSidenavExpanded(open);

			if (!sidenavEl) {
				return;
			}

			sidenavEl.setAttribute('aria-hidden', open ? 'false' : 'true');

			if (supportsInert) {
				sidenavEl.inert = !open;
				return;
			}

			var controls = sidenavEl.querySelectorAll(
				'a, button, input, select, textarea'
			);
			for (var k = 0; k < controls.length; k++) {
				if (open) {
					controls[k].removeAttribute('tabindex');
				} else {
					controls[k].setAttribute('tabindex', '-1');
				}
			}
		}

		function getSidenavControls() {
			if (!sidenavEl) {
				return [];
			}

			return Array.prototype.filter.call(
				sidenavEl.querySelectorAll('a[href], button:not([disabled])'),
				function (control) {
					return control.getClientRects().length > 0;
				}
			);
		}

		function closeSidenavOnDesktop(event) {
			if (event.matches && sidenavInstance && sidenavInstance.isOpen) {
				sidenavInstance.close();
			}

			clearPrimaryNavAriaHidden();
		}

		function clearPrimaryNavAriaHidden() {
			if (primaryNav) {
				primaryNav.removeAttribute('aria-hidden');
			}
		}

		if (window.M && M.Sidenav && sidenavEl) {
			var sidenavOptions = {
				onOpenStart: function () {
					setSidenavState(true);
				},
				onOpenEnd: function () {
					if (!sidenavInstance || !sidenavInstance.isOpen) {
						return;
					}

					var controls = getSidenavControls();
					if (
						controls.length
						&& !sidenavEl.contains(document.activeElement)
					) {
						controls[0].focus();
					}

					clearPrimaryNavAriaHidden();
				},
				onCloseStart: function () {
					setSidenavState(false);
				},
				onCloseEnd: function () {
					if (!sidenavInstance || sidenavInstance.isOpen) {
						return;
					}

					var active = document.activeElement;
					var shouldRestoreFocus = !active
						|| active === document.body
						|| sidenavEl.contains(active);

					if (shouldRestoreFocus) {
						var trigger = sidenavTriggers[0];
						if (trigger && trigger.getClientRects().length) {
							trigger.focus();
						} else {
							var logo = document.querySelector('.navbar .brand-logo');
							if (logo) {
								logo.focus();
							}
						}
					}

					clearPrimaryNavAriaHidden();
				},
			};

			if (reducedMotion) {
				sidenavOptions.inDuration = 1;
				sidenavOptions.outDuration = 1;
			}

			M.Sidenav.init([sidenavEl], sidenavOptions);
			sidenavInstance = M.Sidenav.getInstance(sidenavEl);
		}

		setSidenavState(false);
		clearPrimaryNavAriaHidden();

		if (desktopQuery) {
			if (desktopQuery.addEventListener) {
				desktopQuery.addEventListener('change', closeSidenavOnDesktop);
			} else if (desktopQuery.addListener) {
				desktopQuery.addListener(closeSidenavOnDesktop);
			}
		}

		document.addEventListener('keydown', function (event) {
			var sidenavOpen = Boolean(sidenavInstance && sidenavInstance.isOpen);

			if (event.key === 'Escape') {
				if (sidenavOpen) {
					sidenavInstance.close();
				}
				return;
			}

			if (
				event.key !== 'Tab'
				|| !sidenavOpen
				|| event.ctrlKey
				|| event.altKey
				|| event.metaKey
			) {
				return;
			}

			var controls = getSidenavControls();
			if (!controls.length) {
				return;
			}

			var first = controls[0];
			var last = controls[controls.length - 1];
			var active = document.activeElement;
			var inside = sidenavEl.contains(active);

			if (event.shiftKey) {
				if (!inside || active === first) {
					event.preventDefault();
					last.focus();
				}
			} else if (!inside || active === last) {
				event.preventDefault();
				first.focus();
			}
		});

		var banner = document.getElementById('demo-banner');
		if (!banner) {
			return;
		}

		if (document.documentElement.classList.contains('demo-banner-seen')) {
			banner.remove();
			return;
		}

		var closeButton = document.getElementById('demo-banner-close');
		var dismissTimer;
		var observer;
		var hasBeenViewed = false;

		function rememberSeen() {
			try {
				window.localStorage.setItem('accessibilityhub-demo-banner-seen', 'true');
			} catch {}
		}

		function markSeen() {
			rememberSeen();
			document.documentElement.classList.add('demo-banner-seen');
		}

		function dismiss() {
			window.clearTimeout(dismissTimer);
			markSeen();
			if (observer) {
				observer.disconnect();
			}
			banner.classList.add('demo-banner-closing');
			window.setTimeout(function () {
				if (banner.parentNode) {
					banner.remove();
				}
			}, 250);
		}

		if (closeButton) {
			closeButton.addEventListener('click', dismiss);
		}

		if ('IntersectionObserver' in window) {
			observer = new IntersectionObserver(
				function (entries) {
					entries.forEach(function (entry) {
						if (entry.isIntersecting) {
							hasBeenViewed = true;
							rememberSeen();
							window.clearTimeout(dismissTimer);
							dismissTimer = window.setTimeout(dismiss, 10000);
						} else {
							window.clearTimeout(dismissTimer);
							if (hasBeenViewed) {
								dismiss();
							}
						}
					});
				},
				{ threshold: 0.25 }
			);
			observer.observe(banner);
		} else {
			dismissTimer = window.setTimeout(dismiss, 10000);
		}
	});
})();
