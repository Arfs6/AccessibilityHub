document.addEventListener('DOMContentLoaded', function () {
	if (window.M) {
		M.AutoInit();
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

	function markSeen() {
		try {
			window.localStorage.setItem('accessibilityhub-demo-banner-seen', 'true');
		} catch {}
		document.documentElement.classList.add('demo-banner-seen');
	}

	function dismiss() {
		window.clearTimeout(dismissTimer);
		markSeen();
		banner.classList.add('demo-banner-closing');
		window.setTimeout(function () {
			banner.remove();
		}, 250);
	}

	if (closeButton) {
		closeButton.addEventListener('click', dismiss);
	}

	if ('IntersectionObserver' in window) {
		var observer = new IntersectionObserver(
			function (entries) {
				entries.forEach(function (entry) {
					if (entry.isIntersecting) {
						dismissTimer = window.setTimeout(dismiss, 10000);
					} else {
						window.clearTimeout(dismissTimer);
					}
				});
			},
			{ threshold: 0.5 }
		);
		observer.observe(banner);
	} else {
		dismissTimer = window.setTimeout(dismiss, 10000);
	}
});
