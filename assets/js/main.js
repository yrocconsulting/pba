/* Premier Bass Adventures — small progressive enhancements. */
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

	// Hero sonar: a slow sweep with fish marks that light up as it passes.
	var sonar = document.querySelector('.pba-hero__sonar');
	if (sonar && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
		var period = 9;
		sonar.style.setProperty('--pba-sweep-t', period + 's');
		var sweep = document.createElement('div');
		sweep.className = 'pba-sweep';
		sonar.appendChild(sweep);
		for (var b = 0; b < 10; b++) {
			var ang = Math.random() * 360;
			var rad = 10 + Math.random() * 19;           // % of the sonar box
			var dot = document.createElement('i');
			dot.className = 'pba-blip' + (Math.random() < 0.35 ? ' pba-blip--arc' : '');
			dot.style.left = (50 + rad * Math.sin(ang * Math.PI / 180)) + '%';
			dot.style.top = (50 - rad * Math.cos(ang * Math.PI / 180)) + '%';
			dot.style.animationDelay = (ang / 360 * period - period) + 's';
			sonar.appendChild(dot);
		}
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
			// The intro screen decides about music with its own buttons.
			if (document.querySelector('.pba-intro.is-open') || (e.target.closest && e.target.closest('.pba-intro'))) return;
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

		// Let the intro screen switch music on or off.
		window.pbaMusic = {
			on: function () { store('localStorage', 'pba-music', 'on'); start(); },
			off: function () { store('localStorage', 'pba-music', 'off'); off(); if (playing) stop(); else ui('off'); }
		};

		mbtn.hidden = false;
		if (pref === 'on') {
			['pointerup', 'touchend', 'click', 'keydown'].forEach(function (t) { document.addEventListener(t, onGesture, true); });
			start();
		} else {
			ui('off');
		}
	}

	// Opening screen: hook-set montage, once per visit. Its "Turn it up" tap is
	// the click browsers need before sound can play, so music starts on entry.
	var intro = document.getElementById('pba-intro-data');
	var seen = false;
	try { seen = !!sessionStorage.getItem('pba-intro'); } catch (e) {}
	if (intro && !seen && !/[?&](booking|nointro)=/.test(location.search)) {
		var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		var wide = window.innerWidth / window.innerHeight > 1;
		var ov = document.createElement('div');
		ov.className = 'pba-intro';
		ov.setAttribute('role', 'dialog');
		ov.setAttribute('aria-modal', 'true');
		ov.setAttribute('aria-label', 'Welcome to ' + (intro.dataset.site || 'our site'));
		ov.innerHTML =
			'<video class="pba-intro__video" muted playsinline loop preload="auto" poster="' + intro.dataset.poster + '"' + (still ? '' : ' autoplay') + '>' +
				'<source src="' + (wide ? intro.dataset.landscape : intro.dataset.portrait) + '" type="video/mp4"></video>' +
			'<div class="pba-intro__shade" aria-hidden="true"></div>' +
			'<button type="button" class="pba-intro__skip" data-act="skip">Skip intro <span aria-hidden="true">&times;</span></button>' +
			'<div class="pba-intro__copy">' +
				'<p class="pba-eyebrow">Percy Priest Lake &middot; Nashville, TN</p>' +
				'<p class="pba-intro__title">Set the <em>hook.</em></p>' +
				'<p class="pba-intro__brand">' + (intro.dataset.site || '') + '</p>' +
				'<div class="pba-intro__ctas">' +
					'<button type="button" class="wp-element-button pba-btn pba-intro__go" data-act="loud"><span class="pba-intro__eq" aria-hidden="true"><i></i><i></i><i></i></span>Turn it up</button>' +
					'<button type="button" class="pba-intro__quiet" data-act="quiet">Enter quietly</button>' +
				'</div>' +
			'</div>' +
			'<div class="pba-intro__bar" aria-hidden="true"><span></span></div>';
		document.body.appendChild(ov);
		document.documentElement.classList.add('pba-intro-lock');
		requestAnimationFrame(function () { ov.classList.add('is-open'); });

		var v = ov.querySelector('video');
		var bar = ov.querySelector('.pba-intro__bar span');
		v.addEventListener('timeupdate', function () {
			if (v.duration) bar.style.transform = 'scaleX(' + (v.currentTime / v.duration) + ')';
		});
		var p = v.play && !still ? v.play() : null;
		if (p && p.catch) p.catch(function () {});

		var go = ov.querySelector('.pba-intro__go');
		setTimeout(function () { try { go.focus({ preventScroll: true }); } catch (e) {} }, 50);

		var close = function () {
			try { sessionStorage.setItem('pba-intro', 'seen'); } catch (e) {}
			ov.classList.remove('is-open');
			ov.classList.add('is-closing');
			document.documentElement.classList.remove('pba-intro-lock');
			document.removeEventListener('keydown', onKey, true);
			setTimeout(function () { v.pause(); ov.remove(); }, 650);
		};
		var onKey = function (e) {
			if (e.key === 'Escape') { e.preventDefault(); close(); return; }
			if (e.key === 'Tab') { // keep focus inside the intro
				var f = ov.querySelectorAll('button');
				var first = f[0], last = f[f.length - 1];
				if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
				else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
			}
		};
		document.addEventListener('keydown', onKey, true);
		ov.addEventListener('click', function (e) {
			var b = e.target.closest('[data-act]');
			if (!b) return;
			var act = b.getAttribute('data-act');
			if (act === 'loud' && window.pbaMusic) window.pbaMusic.on();
			if (act === 'quiet' && window.pbaMusic) window.pbaMusic.off();
			close();
		});
	}

	// Footer year.
	document.querySelectorAll('[data-pba-year]').forEach(function (el) {
		el.textContent = new Date().getFullYear();
	});
})();
