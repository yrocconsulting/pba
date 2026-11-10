#!/usr/bin/env python3
"""Generate the Home page block markup (content/home.html).

Usage: build_home.py media.json   (media.json = /wp-json/wp/v2/media?per_page=100)
"""
import json, sys, html, pathlib

media = {m["id"]: m for m in json.load(open(sys.argv[1]))}
url = lambda i: media[i]["source_url"]
by_name = {m["source_url"].rsplit("/", 1)[-1]: m["source_url"] for m in media.values()}
def vid(name):
    """URL of an uploaded file by its file name."""
    return by_name[name]
alt = lambda i: media[i].get("alt_text") or "Bass caught on a Prestige Bass Adventures guided fishing trip on Percy Priest Lake"

HERO_VIDEO, HERO_POSTER, CREW = 78, 79, 100
CATCHES = [99, 10, 13, 24, 57, 31, 12, 65, 45, 32, 62, 42, 25, 69, 8, 53, 30, 16, 22, 49, 59, 71, 9, 75]

def p(text, cls=None):
    if cls:
        return f'<!-- wp:paragraph {{"className":"{cls}"}} -->\n<p class="{cls}">{text}</p>\n<!-- /wp:paragraph -->'
    return f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->'

def h(text, level=2):
    lv = "" if level == 2 else f' {{"level":{level}}}'
    return f'<!-- wp:heading{lv} -->\n<h{level} class="wp-block-heading">{text}</h{level}>\n<!-- /wp:heading -->'

def group(inner, cls, tag="div", anchor=None):
    attrs = {}
    if tag != "div": attrs["tagName"] = tag
    if anchor: attrs["anchor"] = anchor
    attrs["className"] = cls
    attrs["layout"] = {"type": "default"}
    idattr = f' id="{anchor}"' if anchor else ""
    return (f'<!-- wp:group {json.dumps(attrs, separators=(",", ":"))} -->\n'
            f'<{tag}{idattr} class="wp-block-group {cls}">{inner}</{tag}>\n<!-- /wp:group -->')

def ul(items):
    li = "".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{li}</ul>\n<!-- /wp:list -->'

def button(label, href, outline=False):
    if outline:
        return (f'<!-- wp:button {{"className":"is-style-outline"}} -->\n<div class="wp-block-button is-style-outline">'
                f'<a class="wp-block-button__link wp-element-button" href="{href}">{label}</a></div>\n<!-- /wp:button -->')
    return (f'<!-- wp:button -->\n<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{href}">{label}</a></div>\n<!-- /wp:button -->')

def buttons(*b):
    return '<!-- wp:buttons -->\n<div class="wp-block-buttons">' + "".join(b) + '</div>\n<!-- /wp:buttons -->'

def image(i, lightbox=False):
    a = {"id": i, "sizeSlug": "full", "linkDestination": "none"}
    if lightbox: a = {"lightbox": {"enabled": True}, **a}
    return (f'<!-- wp:image {json.dumps(a, separators=(",", ":"))} -->\n'
            f'<figure class="wp-block-image size-full"><img src="{url(i)}" alt="{html.escape(alt(i))}" class="wp-image-{i}"/></figure>\n<!-- /wp:image -->')

def raw(s):
    return f"<!-- wp:html -->\n{s.strip()}\n<!-- /wp:html -->"

out = []

# 1. HERO --------------------------------------------------------------
out.append(raw(f"""
<section class="pba-hero" aria-label="Prestige Bass Adventures">
  <div class="pba-hero__sonar" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="pba-hero__inner">
    <div class="pba-hero__copy">
      <p class="pba-eyebrow">Percy Priest Lake &middot; Nashville, TN</p>
      <h1><span>See them.</span><span>Hunt them.</span><span><em>Land them.</em></span></h1>
      <p class="pba-hero__lede">Live-sonar bass trips on Percy Priest Lake with Captain Cory and Captain John Boy, just east of Nashville. First-timers, kids and seasoned anglers welcome.</p>
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

# 3. TRIPS -------------------------------------------------------------
def card(title, meta, items, cta, feature=False):
    cls = "pba-card pba-card--feature" if feature else "pba-card"
    return group("".join([
        h(title, 3),
        p(meta, "pba-card__meta"),
        ul(items),
        p("Rates on request<small>Call, text or send a request</small>", "pba-card__price"),
        buttons(button(cta, "#book", outline=not feature)),
    ]), cls + " pba-reveal")

trips_head = group(p("The trips", "pba-eyebrow") + h("Pick your <em>trip</em>."), "pba-section__head-copy")
out.append(group("".join([
    group(trips_head + p("Two ways to get on the water. Every trip is fully guided, one boat, one captain, all focus on you.", "pba-section__lede"), "pba-section__intro pba-reveal"),
    group("".join([
        card("Half Day", "About 4 hours &middot; Morning or afternoon",
             ["Perfect first trip, or a quick hit before work", "Great for kids and new anglers", "Fished on the pattern that&rsquo;s hot right now"],
             "Book a half day"),
        card("Full Day", "About 8 hours &middot; Sunrise start",
             ["Cover more water and run more patterns", "Your best shot at a personal-best bass", "Ideal for serious anglers and tournament prep"],
             "Book a full day", feature=True),
    ]), "pba-trips"),
    p("<strong>On board:</strong> Rigged bass boat <span>&middot;</span> Live forward-facing sonar <span>&middot;</span> Rods, reels &amp; tackle <span>&middot;</span> Photos of every catch", "pba-included pba-reveal"),
]), "pba-section", tag="section", anchor="trips"))

# 3b. ON THE WATER (video reels) ----------------------------------------
REELS = [("01", "Hook set", "pba-reel-hookup"), ("02", "In the net", "pba-reel-net"), ("03", "Back he goes", "pba-reel-release")]
reels = "".join(f"""
  <figure class="pba-reel">
    <video class="pba-inview" src="{vid(n + '.mp4')}" poster="{vid(n + '-poster.jpg')}" muted loop playsinline preload="none" aria-label="{c}: clip from a guided trip on Percy Priest Lake"></video>
    <figcaption><span>{num}</span>{c}</figcaption>
  </figure>""" for num, c, n in REELS)
out.append(group("".join([
    group(group(p("On the water", "pba-eyebrow") + h("Every bite, <em>live</em>."), "pba-section__head-copy")
          + p("This is what a day on the boat looks like: the hookup, the scramble for the net, and the release.", "pba-section__lede"), "pba-section__intro pba-reveal"),
    raw(f'<div class="pba-reels pba-reveal">{reels}</div>'),
]), "pba-section pba-section--rule", tag="section", anchor="water"))

# 4. CAPTAIN -----------------------------------------------------------
CAPTAINS = """
<div class="pba-captains">
  <div class="pba-capt"><span class="pba-capt__mark" aria-hidden="true">C</span><div><p class="pba-capt__name">Captain Cory</p><p class="pba-capt__role">Owner &amp; lead guide</p></div></div>
  <div class="pba-capt"><span class="pba-capt__mark" aria-hidden="true">JB</span><div><p class="pba-capt__name">Captain John Boy</p><p class="pba-capt__role">Guide</p></div></div>
</div>"""

captain = f"""<!-- wp:columns {{"verticalAlignment":"center","className":"pba-captain"}} -->
<div class="wp-block-columns are-vertically-aligned-center pba-captain"><!-- wp:column {{"verticalAlignment":"center","width":"42%"}} -->
<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:42%">{raw(f'<div class="pba-screen pba-screen--flat"><div class="pba-screen__hud" aria-hidden="true"><span class="pba-screen__live">Fish on</span><span>Percy Priest</span></div><video class="pba-inview" src="{vid("pba-deck-hookup.mp4")}" poster="{vid("pba-deck-hookup-poster.jpg")}" muted loop playsinline preload="none" aria-label="Angler hooking a bass from the front deck"></video><div class="pba-screen__scan" aria-hidden="true"></div></div>')}</div>
<!-- /wp:column -->

<!-- wp:column {{"verticalAlignment":"center"}} -->
<div class="wp-block-column is-vertically-aligned-center">{p("Your captains", "pba-eyebrow")}{h("Meet your <em>captains</em>.")}{p("Two guides, one home lake. Captain Cory and Captain John Boy fish Percy Priest all year, and every one of those days on the water goes to work for you. With live forward-facing sonar on board, you&rsquo;ll watch fish track your bait on the screen and learn exactly why they bite.")}{raw(CAPTAINS)}{p("Your first bass or your next personal best, every trip is built around you: your skill level, your goals, and what the fish are doing that day.")}{buttons(button("Book your captain", "#book"))}</div>
<!-- /wp:column --></div>
<!-- /wp:columns -->"""
out.append(group(captain, "pba-section pba-section--alt pba-section--rule", tag="section", anchor="captain"))

# 5. CATCH WALL --------------------------------------------------------
imgs = "".join(image(i, lightbox=True) for i in CATCHES)
gallery = (f'<!-- wp:gallery {{"columns":4,"linkTo":"none","className":"pba-catch-wall"}} -->\n'
           f'<figure class="wp-block-gallery has-nested-images columns-4 is-cropped pba-catch-wall">{imgs}</figure>\n<!-- /wp:gallery -->')
out.append(group("".join([
    group(group(p("Proof", "pba-eyebrow") + h("The catch <em>wall</em>."), "pba-section__head-copy")
          + p("Real fish from real trips. Tap any photo to see it up close.", "pba-section__lede"), "pba-section__intro pba-reveal"),
    gallery,
]), "pba-section pba-section--rule", tag="section", anchor="catches"))

# 5b. CREW FEATURE --------------------------------------------------------
crew = f"""<!-- wp:columns {{"verticalAlignment":"center","className":"pba-crew"}} -->
<div class="wp-block-columns are-vertically-aligned-center pba-crew"><!-- wp:column {{"verticalAlignment":"center","width":"50%","className":"pba-crew__media"}} -->
<div class="wp-block-column is-vertically-aligned-center pba-crew__media" style="flex-basis:50%">{image(CREW)}</div>
<!-- /wp:column -->

<!-- wp:column {{"verticalAlignment":"center","className":"pba-crew__copy"}} -->
<div class="wp-block-column is-vertically-aligned-center pba-crew__copy">{p("Bring the crew", "pba-eyebrow")}{h("Fish with friends. <em>Leave with stories.</em>")}{p("Bring a buddy, your kid or your dad. The best days on Percy Priest end on the dock with everybody holding a fish.")}{buttons(button("Plan your trip", "#book"))}</div>
<!-- /wp:column --></div>
<!-- /wp:columns -->"""
out.append(group(crew, "pba-feature", tag="section", anchor="crew"))

# 6. THE LAKE ----------------------------------------------------------
STATS = [("14,000+", "Acres of water"), ("200+", "Miles of shoreline"), ("3", "Bass species")]
stats = "".join(group(p(n, "pba-stat__num") + p(l, "pba-stat__label"), "pba-stat") for n, l in STATS)
CELLS = [
    ("The water", "Rocky points, bluff walls, standing timber, creek channels and offshore humps. Plenty of places for big bass to hide, and live sonar shows us exactly where they are."),
    ("The fish", "Largemouth, smallmouth and spotted bass. Some days you&rsquo;ll catch all three before lunch."),
    ("The seasons", "Shallow spawners in spring, offshore schools in summer and fall, and slow, heavy fish in winter. Your captain runs the pattern that&rsquo;s working right now."),
]
cells = "".join(group(p(f"{n:02d}", "pba-lake__num") + h(t, 3) + p(d), "pba-lake")
                for n, (t, d) in enumerate(CELLS, 1))
out.append(group("".join([
    group(group(p("Home water", "pba-eyebrow") + h("Percy Priest <em>Lake</em>."), "pba-section__head-copy")
          + p("Just east of downtown Nashville, Percy Priest is one of Middle Tennessee&rsquo;s best bass lakes, and it&rsquo;s home water for Captain Cory and Captain John Boy. They fish it year-round, so they know where the fish are and where they&rsquo;re headed next.", "pba-section__lede"), "pba-section__intro pba-reveal"),
    group(stats, "pba-stats pba-reveal"),
    group(cells, "pba-lakes pba-reveal"),
    group(p("<strong>Minutes from</strong> Nashville &middot; Murfreesboro &middot; Smyrna &middot; La Vergne &middot; Mt. Juliet &middot; Hermitage &middot; Antioch &middot; Franklin &middot; Brentwood"), "pba-towns"),
]), "pba-section pba-section--alt pba-section--rule", tag="section", anchor="lake"))

# 7. FAQ ---------------------------------------------------------------
FAQ = [
    ("I&rsquo;ve never bass fished. Is that OK?", "Absolutely. Your captain coaches every angler from the first cast: how to work the bait, feel the bite and set the hook. Plenty of first-timers leave with their best fish ever."),
    ("Can I pick my captain?", "Yes. Choose Captain Cory or Captain John Boy on the booking form, or leave it open and we&rsquo;ll match you with whoever is free on your date."),
    ("Can I bring my kids?", "Yes. Kids are welcome, and some of our favorite catches have come from young anglers. A half-day trip is a great fit for younger kids."),
    ("Do I need a fishing license?", "Yes. Tennessee requires a fishing license for anglers 13 and older. You can buy one online from the Tennessee Wildlife Resources Agency (TWRA) in a few minutes."),
    ("What should I bring?", "Your license, sunglasses, sunscreen, layers or rain gear for the season, and food and drinks for the day. Rods, reels and tackle are on the boat."),
    ("Where do we meet?", "Trips launch from a boat ramp on Percy Priest Lake. Your captain sends the exact ramp and start time when your trip is confirmed."),
    ("How do I book?", "Send a request with the form below or call or text (615) 310-1058. We confirm every trip personally."),
]
det = "".join(f'<!-- wp:details -->\n<details class="wp-block-details"><summary>{q}</summary>{p(a)}</details>\n<!-- /wp:details -->' for q, a in FAQ)
out.append(group("".join([
    group(group(p("Good to know", "pba-eyebrow") + h("Before you <em>go</em>."), "pba-section__head-copy"), "pba-section__intro pba-reveal"),
    group(det, "pba-faq"),
]), "pba-section pba-section--rule", tag="section", anchor="faq"))

# 8. BOOK --------------------------------------------------------------
book = f"""<!-- wp:columns {{"className":"pba-book"}} -->
<div class="wp-block-columns pba-book"><!-- wp:column {{"width":"40%","className":"pba-book__aside"}} -->
<div class="wp-block-column pba-book__aside" style="flex-basis:40%">{p("Book a trip", "pba-eyebrow")}{h("Your personal best is <em>waiting</em>.")}{p("Send a request and we&rsquo;ll call or text to confirm your date, captain and meeting spot. Rather talk it through? Call or text:")}{p('<a href="tel:+16153101058">(615) 310-1058</a>', "pba-big-phone")}{p("Trips on Percy Priest Lake, minutes from Nashville, Murfreesboro and Mt. Juliet.")}</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:shortcode -->
[pba_booking_form]
<!-- /wp:shortcode --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->"""
out.append(group(book, "pba-section pba-section--alt pba-section--rule", tag="section", anchor="book"))

pathlib.Path(__file__).resolve().parent.parent.joinpath("content/home.html").write_text("\n\n".join(out) + "\n")
print("ok", sum(len(x) for x in out), "chars")
