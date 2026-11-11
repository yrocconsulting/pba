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

	// Background music: on by default, starts on the first tap/click (browsers
	// block sound before that), remembers "off", resumes across pages.
	var mbtn = document.querySelector('.pba-music');
	if (mbtn && mbtn.dataset.src) {
		var store = function (area, k, v) {
			try { if (v === undefined) return window[area].getItem(k); window[area].setItem(k, v); } catch (e) { return null; }
		};
		var pref = store('localStorage', 'pba-music') || 'on';
		var maxVol = Math.min(1, parseFloat(mbtn.dataset.volume) || 0.4);
		var audio = new Audio();
		audio.loop = true;
		audio.preload = pref === 'on' ? 'auto' : 'none';
		audio.src = mbtn.dataset.src;
		var label = mbtn.querySelector('.pba-music__label');
		var fadeTimer = null;
		var playing = false;
		var resumeAt = parseFloat(store('sessionStorage', 'pba-music-t')) || 0;

		var ui = function (state) {
			playing = state === 'playing';
			mbtn.classList.toggle('is-playing', playing);
			mbtn.classList.toggle('is-waiting', state === 'waiting');
			mbtn.setAttribute('aria-pressed', playing ? 'true' : 'false');
			mbtn.setAttribute('aria-label', playing ? 'Turn music off' : 'Turn music on');
			label.textContent = playing ? 'Sound on' : (state === 'waiting' ? 'Tap for sound' : 'Sound off');
		};
		var fade = function (to, done) {
			clearInterval(fadeTimer);
			fadeTimer = setInterval(function () {
				var v = audio.volume + (to > audio.volume ? 0.04 : -0.06);
				if ((to > audio.volume && v >= to) || (to <= audio.volume && v <= to)) {
					audio.volume = Math.max(0, Math.min(1, to));
					clearInterval(fadeTimer);
					if (done) done();
				} else {
					audio.volume = Math.max(0, Math.min(1, v));
				}
			}, 60);
		};
		var start = function () {
			if (playing) return;
			if (resumeAt && !audio.currentTime) {
				try { audio.currentTime = resumeAt; } catch (e) {}
			}
			audio.volume = 0;
			var pr = audio.play();
			if (pr && pr.then) {
				pr.then(function () { ui('playing'); fade(maxVol); off(); })
					.catch(function () { ui('waiting'); });
			} else {
				ui('playing'); fade(maxVol); off();
			}
		};
		var stop = function () {
			ui('off');
			fade(0, function () { audio.pause(); });
		};
		var onGesture = function (e) {
			if (mbtn.contains(e.target)) return;
			if ((store('localStorage', 'pba-music') || 'on') === 'on') start();
		};
		var off = function () {
			['pointerup', 'touchend', 'click', 'keydown'].forEach(function (t) { document.removeEventListener(t, onGesture, true); });
		};

		mbtn.addEventListener('click', function () {
			if (playing) { store('localStorage', 'pba-music', 'off'); off(); stop(); }
			else { store('localStorage', 'pba-music', 'on'); start(); }
		});
		document.addEventListener('visibilitychange', function () {
			if (document.hidden && playing) { audio.pause(); mbtn.dataset.resume = '1'; }
			else if (!document.hidden && mbtn.dataset.resume) { delete mbtn.dataset.resume; audio.play().catch(function () {}); }
		});
		var saveTime = function () { if (!audio.paused) store('sessionStorage', 'pba-music-t', String(audio.currentTime)); };
		setInterval(saveTime, 2000);
		window.addEventListener('pagehide', saveTime);

		mbtn.hidden = false;
		if (pref === 'on') {
			['pointerup', 'touchend', 'click', 'keydown'].forEach(function (t) { document.addEventListener(t, onGesture, true); });
			start();
		} else {
			ui('off');
		}
	}

	// Footer year.
	document.querySelectorAll('[data-pba-year]').forEach(function (el) {
		el.textContent = new Date().getFullYear();
	});
})();
