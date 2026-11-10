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
		if (wall.classList.contains('pba-catch-wall--all') || wall.querySelectorAll('img').length < 13) return;
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

	// Play short clips only while they're on screen.
	var clips = document.querySelectorAll('video.pba-inview');
	var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches || (navigator.connection && navigator.connection.saveData);
	if (clips.length && 'IntersectionObserver' in window && !still) {
		var vio = new IntersectionObserver(function (entries) {
			entries.forEach(function (en) {
				var v = en.target;
				if (en.isIntersecting) {
					var pr = v.play();
					if (pr && pr.catch) pr.catch(function () {});
				} else {
					v.pause();
				}
			});
		}, { threshold: 0.35 });
		clips.forEach(function (v) { vio.observe(v); });
	}

	// Mark sections that get the contour layer.
	['trips', 'water', 'captain', 'faq', 'book'].forEach(function (id) {
		var el = document.getElementById(id);
		if (el) el.classList.add('pba-contours');
	});

	// Gentle parallax on the contour layers.
	var layers = document.querySelectorAll('.pba-contours');
	if (layers.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
		var ticking = false;
		var update = function () {
			var vh = window.innerHeight;
			layers.forEach(function (el) {
				var r = el.getBoundingClientRect();
				if (r.bottom < 0 || r.top > vh) return;
				var mid = r.top + r.height / 2 - vh / 2;
				el.style.setProperty('--pba-par', (mid * -0.12).toFixed(1) + 'px');
			});
			ticking = false;
		};
		window.addEventListener('scroll', function () {
			if (!ticking) { ticking = true; requestAnimationFrame(update); }
		}, { passive: true });
		update();
	}

	// Cursor light on cards and panels.
	if (window.matchMedia('(hover: hover)').matches) {
		document.querySelectorAll('.pba-card, .pba-lake, .pba-form').forEach(function (el) {
			el.addEventListener('pointermove', function (e) {
				var r = el.getBoundingClientRect();
				el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
				el.style.setProperty('--my', (e.clientY - r.top) + 'px');
			});
		});
	}

	// Footer year.
	document.querySelectorAll('[data-pba-year]').forEach(function (el) {
		el.textContent = new Date().getFullYear();
	});
})();
