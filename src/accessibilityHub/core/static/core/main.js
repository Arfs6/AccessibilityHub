document.addEventListener('DOMContentLoaded', function () {
	if (window.M && M.Sidenav) {
		M.Sidenav.init(document.querySelectorAll('.sidenav'));
	}

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
