#!/usr/bin/env python3
"""Generate the Home page block markup (content/home.html).

Usage: build_home.py media.json   (media.json = /wp-json/wp/v2/media?per_page=100)
"""
import pathlib
from site_blocks import *  # noqa: F401,F403

out = []

# 1. HERO --------------------------------------------------------------
out.append(raw(f"""
<section class="pba-hero" aria-label="Prestige Bass Adventures">
  <div class="pba-hero__sonar" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="pba-hero__inner">
    <div class="pba-hero__copy">
      <p class="pba-eyebrow">Percy Priest Lake &middot; Nashville, TN</p>
      <h1><span>See them.</span><span>Hunt them.</span><span><em>Land them.</em></span></h1>
      <p class="pba-hero__lede">Live-sonar bass trips on Percy Priest Lake with Captain Cory, just east of Nashville. First-timers, kids and seasoned anglers welcome.</p>
      <div class="pba-hero__ctas">
        <a class="wp-element-button pba-btn" href="#book">Book a Trip</a>
        <a class="pba-hero__phone" href="tel:+16153101058">Call or text <b>(615) 310-1058</b></a>
      </div>
    </div>
    <div class="pba-screen">
      <div class="pba-screen__hud" aria-hidden="true"><span class="pba-screen__live">Live</span><span>Forward sonar</span></div>
      <video src="{url(HERO_VIDEO)}" poster="{url(HERO_POSTER)}" autoplay muted loop playsinline preload="metadata" aria-label="Live forward-facing sonar showing bass under the boat, then fishing from the deck"></video>
      <div class="pba-screen__scan" aria-hidden="true"></div>
      <p class="pba-screen__tag" aria-hidden="true">Watch them bite</p>
    </div>
  </div>
  <a class="pba-hero__scroll" href="#trips">Scroll</a>
</section>
"""))

# 2. MARQUEE -----------------------------------------------------------
words = ["Largemouth", "Smallmouth", "Spotted Bass", "Live Forward-Facing Sonar", "Half &amp; Full Day Trips", "All Skill Levels", "Kids Welcome", "Percy Priest Lake"]
lis = "".join(f"<li>{w}</li>" for w in words)
out.append(raw(f'<div class="pba-marquee" aria-hidden="true"><div class="pba-marquee__track"><ul>{lis}</ul><ul>{lis}</ul></div></div>'))

out += [trips_section(), reels_section(), captain_section(), catch_wall_section(),
        crew_section(), lake_section(), faq_section(), book_section()]

pathlib.Path(__file__).resolve().parent.parent.joinpath("content/home.html").write_text("\n\n".join(out) + "\n")
print("ok", sum(len(x) for x in out), "chars")
