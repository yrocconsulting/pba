#!/usr/bin/env python3
"""Generate the Home page block markup (content/home.html).

Usage: build_home.py media.json   (media.json = /wp-json/wp/v2/media?per_page=100)
"""
import json, sys, html, pathlib

media = {m["id"]: m for m in json.load(open(sys.argv[1]))}
url = lambda i: media[i]["source_url"]
alt = lambda i: media[i].get("alt_text") or "Bass caught on a Prestige Bass Adventures guided fishing trip in Middle Tennessee"

HERO_VIDEO, HERO_POSTER, CAPTAIN = 78, 79, 65
CATCHES = [10, 13, 24, 57, 26, 31, 12, 65, 45, 32, 62, 42, 25, 69, 8, 53, 30, 16, 22, 49, 59, 71, 9, 75]

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
      <p class="pba-eyebrow">Middle Tennessee &middot; Guided Bass Fishing</p>
      <h1><span>See them.</span><span>Hunt them.</span><span><em>Land them.</em></span></h1>
      <p class="pba-hero__lede">Live-sonar bass trips with Captain Cory Anderson on Percy Priest, Old Hickory, Tims Ford and the best lakes in Middle Tennessee. First-timers, kids and seasoned anglers welcome.</p>
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
words = ["Largemouth", "Smallmouth", "Spotted Bass", "Live Forward-Facing Sonar", "Half &amp; Full Day Trips", "All Skill Levels", "Kids Welcome", "Middle Tennessee"]
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

# 4. CAPTAIN -----------------------------------------------------------
captain = f"""<!-- wp:columns {{"verticalAlignment":"center","className":"pba-captain"}} -->
<div class="wp-block-columns are-vertically-aligned-center pba-captain"><!-- wp:column {{"verticalAlignment":"center","width":"42%"}} -->
<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:42%">{image(CAPTAIN)}</div>
<!-- /wp:column -->

<!-- wp:column {{"verticalAlignment":"center"}} -->
<div class="wp-block-column is-vertically-aligned-center">{p("Your captain", "pba-eyebrow")}{h("Meet Captain <em>Cory Anderson</em>.")}{p("Cory has spent years chasing largemouth and smallmouth across Middle Tennessee, and every one of those days on the water goes to work for you. You&rsquo;ll fish from his black-and-gold bass boat rigged with live forward-facing sonar, so you can watch fish track your bait on the screen and learn exactly why they bite.")}{p("Your first bass or your next personal best, every trip is built around you: your skill level, your goals, and what the fish are doing that day.")}{buttons(button("Fish with Cory", "#book"))}</div>
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

# 6. LAKES -------------------------------------------------------------
LAKES = [
    ("Percy Priest Lake", "Rocky points, bluff walls and standing timber.", "Nashville &middot; Smyrna &middot; La Vergne &middot; Mt. Juliet"),
    ("Old Hickory Lake", "Cumberland River grass, docks and current.", "Hendersonville &middot; Gallatin &middot; Old Hickory"),
    ("Tims Ford Lake", "Deep, clear water and big smallmouth.", "Winchester &middot; Tullahoma"),
    ("Normandy Lake", "Small, clear Duck River lake. Finesse fishing.", "Tullahoma &middot; Manchester"),
    ("Center Hill Lake", "Deep highland lake for smallmouth and spots.", "Smithville &middot; Lancaster"),
    ("Cheatham Lake", "Cumberland River backwaters and current breaks.", "Ashland City &middot; west Nashville"),
]
cells = "".join(group(p(f"{n:02d}", "pba-lake__num") + h(name, 3) + p(desc) + p(towns), "pba-lake")
                for n, (name, desc, towns) in enumerate(LAKES, 1))
out.append(group("".join([
    group(group(p("Where we fish", "pba-eyebrow") + h("Lakes we <em>fish</em>."), "pba-section__head-copy")
          + p("Based in College Grove, between Franklin and Murfreesboro, with the best bass water in Middle Tennessee a short drive away. Cory picks the lake and the pattern for the season, or you can request your favorite.", "pba-section__lede"), "pba-section__intro pba-reveal"),
    group(cells, "pba-lakes pba-reveal"),
    group(p("<strong>Serving anglers from</strong> Nashville &middot; Franklin &middot; Brentwood &middot; Murfreesboro &middot; Spring Hill &middot; Nolensville &middot; Smyrna &middot; Columbia"), "pba-towns"),
]), "pba-section pba-section--alt pba-section--rule", tag="section", anchor="lakes"))

# 7. FAQ ---------------------------------------------------------------
FAQ = [
    ("I&rsquo;ve never bass fished. Is that OK?", "Absolutely. Cory coaches every angler from the first cast: how to work the bait, feel the bite and set the hook. Plenty of first-timers leave with their best fish ever."),
    ("Can I bring my kids?", "Yes. Kids are welcome, and some of our favorite catches have come from young anglers. A half-day trip is a great fit for younger kids."),
    ("Do I need a fishing license?", "Yes. Tennessee requires a fishing license for anglers 13 and older. You can buy one online from the Tennessee Wildlife Resources Agency (TWRA) in a few minutes."),
    ("What should I bring?", "Your license, sunglasses, sunscreen, layers or rain gear for the season, and food and drinks for the day. Rods, reels and tackle are on the boat."),
    ("Where do we meet?", "It depends on the lake. Cory sends the boat ramp location and start time when he confirms your trip."),
    ("How do I book?", "Send a request with the form below or call or text (615) 310-1058. Cory confirms every trip personally."),
]
det = "".join(f'<!-- wp:details -->\n<details class="wp-block-details"><summary>{q}</summary>{p(a)}</details>\n<!-- /wp:details -->' for q, a in FAQ)
out.append(group("".join([
    group(group(p("Good to know", "pba-eyebrow") + h("Before you <em>go</em>."), "pba-section__head-copy"), "pba-section__intro pba-reveal"),
    group(det, "pba-faq"),
]), "pba-section pba-section--rule", tag="section", anchor="faq"))

# 8. BOOK --------------------------------------------------------------
book = f"""<!-- wp:columns {{"className":"pba-book"}} -->
<div class="wp-block-columns pba-book"><!-- wp:column {{"width":"40%","className":"pba-book__aside"}} -->
<div class="wp-block-column pba-book__aside" style="flex-basis:40%">{p("Book a trip", "pba-eyebrow")}{h("Your personal best is <em>waiting</em>.")}{p("Send a request and Cory will call or text to confirm your date, lake and meeting spot. Rather talk it through? Call or text:")}{p('<a href="tel:+16153101058">(615) 310-1058</a>', "pba-big-phone")}{p("Based in College Grove, TN. Trips across Middle Tennessee.")}</div>
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
