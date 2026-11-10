/* Prestige Bass Adventures — small progressive enhancements. */
(function () {
	var doc = document.documentElement;
	doc.classList.add('pba-js');

	// Solid header once the page scrolls.
	var header = document.querySelector('.pba-header-wrap');
	if (header) {
		var onScroll = function () {
			header.classList.toggle('is-scrolled', window.scrollY > 40);
		};
		onScroll();
		window.addEventListener('scroll', onScroll, { passive: true });
	}

	// Close the mobile menu after tapping an in-page link.
	document.addEventListener('click', function (e) {
		var link = e.target.closest('.wp-block-navigation__responsive-container.is-menu-open a[href*="#"]');
		if (!link) return;
		var close = document.querySelector('.wp-block-navigation__responsive-container-close');
		if (close) close.click();
	});

	// Reveal sections as they scroll into view.
	var targets = document.querySelectorAll('.pba-reveal');
	if ('IntersectionObserver' in window && targets.length) {
		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (en) {
				if (en.isIntersecting) {
					en.target.classList.add('is-in');
					io.unobserve(en.target);
				}
			});
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
		targets.forEach(function (t) { io.observe(t); });
	} else {
		targets.forEach(function (t) { t.classList.add('is-in'); });
	}

	// Catch wall: show a taste, then "see more".
	document.querySelectorAll('.pba-catch-wall').forEach(function (wall) {
		if (wall.querySelectorAll('img').length < 13) return;
		wall.classList.add('is-collapsed');
		var wrap = document.createElement('p');
		wrap.className = 'pba-more';
		var btn = document.createElement('button');
		btn.type = 'button';
		btn.className = 'wp-element-button pba-btn';
		btn.textContent = 'See all catches';
		btn.addEventListener('click', function () {
			wall.classList.remove('is-collapsed');
			wrap.remove();
		});
		wrap.appendChild(btn);
		wall.insertAdjacentElement('afterend', wrap);
	});

	// Hero video: respect reduced motion and save data.
	var vid = document.querySelector('.pba-screen video');
	if (vid) {
		var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		var saveData = navigator.connection && navigator.connection.saveData;
		if (reduce || saveData) {
			vid.removeAttribute('autoplay');
			vid.pause();
		}
	}

	// Footer year.
	document.querySelectorAll('[data-pba-year]').forEach(function (el) {
		el.textContent = new Date().getFullYear();
	});
})();
