#!/usr/bin/env python3
"""Shared block-markup helpers and sections for pba.fish pages."""
import json, sys, html, pathlib

MEDIA_FILE = sys.argv[1] if len(sys.argv) > 1 else "media.json"
media = {m["id"]: m for m in json.load(open(MEDIA_FILE))}
url = lambda i: media[i]["source_url"]
by_name = {m["source_url"].rsplit("/", 1)[-1]: m["source_url"] for m in media.values()}
def vid(name):
    """URL of an uploaded file by its file name."""
    return by_name[name]
alt = lambda i: media[i].get("alt_text") or "Bass caught on a Premier Bass Adventures guided fishing trip on Percy Priest Lake"

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
    return _undent(f'<!-- wp:group {json.dumps(attrs, separators=(",", ":"))} -->\n'
            f'<{tag}{idattr} class="wp-block-group {cls}">{inner}</{tag}>\n<!-- /wp:group -->')

def ul(items):
    li = "".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{li}</ul>\n<!-- /wp:list -->'

def button(label, href, outline=False):
    if outline:
        return (f'<!-- wp:button {{"className":"is-style-outline"}} -->\n<div class="wp-block-button is-style-outline">'
                f'<a class="wp-block-button__link wp-element-button" href="{href}">{label}</a></div>\n<!-- /wp:button -->')
    return _undent(f'<!-- wp:button -->\n<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{href}">{label}</a></div>\n<!-- /wp:button -->')

def buttons(*b):
    return '<!-- wp:buttons -->\n<div class="wp-block-buttons">' + "".join(b) + '</div>\n<!-- /wp:buttons -->'

def image(i, lightbox=False, caption=None):
    a = {"id": i, "sizeSlug": "full", "linkDestination": "none"}
    if lightbox: a = {"lightbox": {"enabled": True}, **a}
    cap = f'<figcaption class="wp-element-caption">{caption}</figcaption>' if caption else ""
    return (f'<!-- wp:image {json.dumps(a, separators=(",", ":"))} -->\n'
            f'<figure class="wp-block-image size-full"><img src="{url(i)}" alt="{html.escape(alt(i))}" class="wp-image-{i}"/>{cap}</figure>\n<!-- /wp:image -->')

def raw(s):
    return f"<!-- wp:html -->\n{s.strip()}\n<!-- /wp:html -->"

def _undent(s):
    """Section bodies were indented one level; strip it from multi-line strings."""
    return s.replace("\n    ", "\n")


def card(title, meta, items, cta, price, feature=False, book="#book"):
    cls = "pba-card pba-card--feature" if feature else "pba-card"
    return group("".join([
        h(title, 3),
        p(meta, "pba-card__meta"),
        ul(items),
        p(f"{price}<small>Per boat &middot; 1&ndash;2 anglers</small>", "pba-card__price"),
        buttons(button(cta, book, outline=not feature)),
    ]), cls + " pba-reveal")

def trips_section(anchor="trips", book="#book"):
    trips_head = group(p("The trips", "pba-eyebrow") + h("Pick your <em>trip</em>."), "pba-section__head-copy")
    return _undent(group("".join([
        group(trips_head + p("Two ways to get on the water. Every trip is fully guided. One price per boat, for 1 or 2 anglers.", "pba-section__lede"), "pba-section__intro pba-reveal"),
        group("".join([
            card("Half Day", "About 4 hours &middot; Morning or afternoon",
                 ["Perfect first trip, or a quick hit before work", "Great for kids and new anglers", "Fished on the pattern that&rsquo;s hot right now"],
                 "Book a half day", "$550", book=book),
            card("Full Day", "About 8 hours &middot; Sunrise start",
                 ["Cover more water and run more patterns", "Your best shot at a personal-best bass", "Ideal for serious anglers and tournament prep"],
                 "Book a full day", "$950", feature=True, book=book),
        ]), "pba-trips"),
        p("<strong>$150 deposit</strong> secures your date <span>&middot;</span> Half day or full day", "pba-included pba-deposit pba-reveal"),
        p("<strong>On board:</strong> Rigged bass boat <span>&middot;</span> Live forward-facing sonar <span>&middot;</span> Rods, reels &amp; tackle <span>&middot;</span> Photos of every catch", "pba-included pba-reveal"),
    ]), "pba-section", tag="section", anchor=anchor))


def reels_section():
    # 3b. ON THE WATER (video reels) ----------------------------------------
    REELS = [("01", "Hook set", "pba-reel-hookup"), ("02", "In the net", "pba-reel-net"), ("03", "Back he goes", "pba-reel-release")]
    reels = "".join(f"""
      <figure class="pba-reel">
        <video class="pba-inview" src="{vid(n + '.mp4')}" poster="{vid(n + '-poster.jpg')}" muted loop playsinline preload="none" aria-label="{c}: clip from a guided trip on Percy Priest Lake"></video>
        <figcaption><span>{num}</span>{c}</figcaption>
      </figure>""" for num, c, n in REELS)
    return _undent(group("".join([
        group(group(p("On the water", "pba-eyebrow") + h("Every bite, <em>live</em>."), "pba-section__head-copy")
              + p("This is what a day on the boat looks like: the hookup, the scramble for the net, and the release.", "pba-section__lede"), "pba-section__intro pba-reveal"),
        raw(f'<div class="pba-reels pba-reveal">{reels}</div>'),
    ]), "pba-section pba-section--rule", tag="section", anchor="water"))


def captain_section(book="#book"):
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
    <div class="wp-block-column is-vertically-aligned-center">{p("Your captains", "pba-eyebrow")}{h("Meet your <em>captains</em>.")}{p("Captain Cory started Premier Bass Adventures and fishes Percy Priest all year, and every one of those days on the water goes to work for you. With live forward-facing sonar on board, you&rsquo;ll watch fish track your bait on the screen and learn exactly why they bite.")}{p("Bringing a bigger crew? Each boat fishes 1 or 2 anglers, so for larger parties we add a second boat with Captain John Boy and everyone gets a guide.")}{raw(CAPTAINS)}{p("Your first bass or your next personal best, every trip is built around you: your skill level, your goals, and what the fish are doing that day.")}{buttons(button("Book a trip", book))}</div>
    <!-- /wp:column --></div>
    <!-- /wp:columns -->"""
    return _undent(group(captain, "pba-section pba-section--alt pba-section--rule", tag="section", anchor="captain"))


def catch_wall_section(ids=None, title="The catch <em>wall</em>.", eyebrow="Proof"):
    # 5. CATCH WALL --------------------------------------------------------
    imgs = "".join(image(i, lightbox=True) for i in (ids or CATCHES))
    gallery = (f'<!-- wp:gallery {{"columns":4,"linkTo":"none","className":"pba-catch-wall"}} -->\n'
               f'<figure class="wp-block-gallery has-nested-images columns-4 is-cropped pba-catch-wall">{imgs}</figure>\n<!-- /wp:gallery -->')
    return _undent(group("".join([
        group(group(p(eyebrow, "pba-eyebrow") + h(title), "pba-section__head-copy")
              + p("Real fish from real trips. Tap any photo to see it up close.", "pba-section__lede"), "pba-section__intro pba-reveal"),
        gallery,
    ]), "pba-section pba-section--rule", tag="section", anchor="catches"))


def crew_section(book="#book"):
    # 5b. CREW FEATURE --------------------------------------------------------
    crew = f"""<!-- wp:columns {{"verticalAlignment":"center","className":"pba-crew"}} -->
    <div class="wp-block-columns are-vertically-aligned-center pba-crew"><!-- wp:column {{"verticalAlignment":"center","width":"50%","className":"pba-crew__media"}} -->
    <div class="wp-block-column is-vertically-aligned-center pba-crew__media" style="flex-basis:50%">{image(CREW)}</div>
    <!-- /wp:column -->

    <!-- wp:column {{"verticalAlignment":"center","className":"pba-crew__copy"}} -->
    <div class="wp-block-column is-vertically-aligned-center pba-crew__copy">{p("Bring the crew &middot; or a client", "pba-eyebrow")}{h("Fish with friends. <em>Leave with stories.</em>")}{p("Bring a buddy, your kid or your dad. The best days on Percy Priest end on the dock with everybody holding a fish.")}{p("<strong>Bring your client, too.</strong> Skip another steakhouse dinner. A day on the boat means hours of easy conversation and a story they&rsquo;ll still be telling at the next meeting.", "pba-crew__client")}{buttons(button("Plan your trip", book))}</div>
    <!-- /wp:column --></div>
    <!-- /wp:columns -->"""
    return _undent(group(crew, "pba-feature", tag="section", anchor="crew"))


def lake_section():
    # 6. THE LAKE ----------------------------------------------------------
    STATS = [("14,000+", "Acres of water"), ("200+", "Miles of shoreline"), ("4", "Bass species")]
    stats = "".join(group(p(n, "pba-stat__num") + p(l, "pba-stat__label"), "pba-stat") for n, l in STATS)
    CELLS = [
        ("The water", "Rocky points, bluff walls, standing timber, creek channels and offshore humps. Plenty of places for big bass to hide, and live sonar shows us exactly where they are."),
        ("The fish", "Largemouth, smallmouth and spotted bass, plus the occasional striped bass. Some days you&rsquo;ll catch all three black bass before lunch."),
        ("The seasons", "Shallow spawners in spring, offshore schools in summer and fall, and slow, heavy fish in winter. Your captain runs the pattern that&rsquo;s working right now."),
    ]
    cells = "".join(group(p(f"{n:02d}", "pba-lake__num") + h(t, 3) + p(d), "pba-lake")
                    for n, (t, d) in enumerate(CELLS, 1))
    return _undent(group("".join([
        group(group(p("Home water", "pba-eyebrow") + h("Percy Priest <em>Lake</em>."), "pba-section__head-copy")
              + p("Just east of downtown Nashville, Percy Priest is one of Middle Tennessee&rsquo;s best bass lakes, and it&rsquo;s Captain Cory&rsquo;s home water. He fishes it year-round, so he knows where the fish are and where they&rsquo;re headed next.", "pba-section__lede"), "pba-section__intro pba-reveal"),
        group(stats, "pba-stats pba-reveal"),
        group(cells, "pba-lakes pba-reveal"),
        group(p("<strong>Minutes from</strong> Nashville &middot; Murfreesboro &middot; Smyrna &middot; La Vergne &middot; Mt. Juliet &middot; Hermitage &middot; Antioch &middot; Franklin &middot; Brentwood"), "pba-towns"),
    ]), "pba-section pba-section--alt pba-section--rule", tag="section", anchor="lake"))


FAQ = [
    ("I&rsquo;ve never bass fished. Is that OK?", "Absolutely. Your captain coaches every angler from the first cast: how to work the bait, feel the bite and set the hook. Plenty of first-timers leave with their best fish ever."),
    ("Can you take a large group?", "Yes. Each boat fishes 1 or 2 anglers. For larger parties, we add a second boat with Captain John Boy, priced per boat. Put your party size on the booking form or call or text (615) 310-1058 to plan it."),
    ("Can I bring a client?", "Absolutely. A guided trip is a great way to entertain or thank a client: hours of relaxed time together and a day they won&rsquo;t forget. We take care of everything on the water so you can focus on your guest."),
    ("Can I bring my kids?", "Yes. Kids are welcome, and some of our favorite catches have come from young anglers. A half-day trip is a great fit for younger kids."),
    ("Do I need a fishing license?", "Yes. Tennessee requires a fishing license for anglers 13 and older. You can buy one online from the Tennessee Wildlife Resources Agency (TWRA) in a few minutes."),
    ("What should I bring?", "Your license, sunglasses, sunscreen, layers or rain gear for the season, and food and drinks for the day. Rods, reels and tackle are on the boat."),
    ("Where do we meet?", "Trips launch from a boat ramp on Percy Priest Lake. We send the exact ramp and start time when we confirm your trip."),
    ("How much does a trip cost?", "A half-day guided trip is $550 and a full-day guided trip is $950. Prices are per boat, for 1 or 2 anglers. A $150 deposit secures your date, for either trip."),
    ("How do I book?", "Send a request with the form below or call or text (615) 310-1058. Once we confirm your date, a $150 deposit locks it in."),
]

def faq_section(items=None, title="Before you <em>go</em>."):
    det = "".join(f'<!-- wp:details -->\n<details class="wp-block-details"><summary>{q}</summary>{p(a)}</details>\n<!-- /wp:details -->' for q, a in (items or FAQ))
    return _undent(group("".join([
        group(group(p("Good to know", "pba-eyebrow") + h(title), "pba-section__head-copy"), "pba-section__intro pba-reveal"),
        group(det, "pba-faq"),
    ]), "pba-section pba-section--rule", tag="section", anchor="faq"))


def book_section():
    # 8. BOOK --------------------------------------------------------------
    book = f"""<!-- wp:columns {{"className":"pba-book"}} -->
    <div class="wp-block-columns pba-book"><!-- wp:column {{"width":"40%","className":"pba-book__aside"}} -->
    <div class="wp-block-column pba-book__aside" style="flex-basis:40%">{p("Book a trip", "pba-eyebrow")}{h("Your personal best is <em>waiting</em>.")}{p("Send a request and we&rsquo;ll call or text to confirm your date and meeting spot. A $150 deposit secures it. Rather talk it through? Call or text:")}{p('<a href="tel:+16153101058">(615) 310-1058</a>', "pba-big-phone")}{p("Trips on Percy Priest Lake, minutes from Nashville, Murfreesboro and Mt. Juliet.")}</div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column"><!-- wp:shortcode -->
    [pba_booking_form]
    <!-- /wp:shortcode --></div>
    <!-- /wp:column --></div>
    <!-- /wp:columns -->"""
    return _undent(group(book, "pba-section pba-section--alt pba-section--rule", tag="section", anchor="book"))




BOAT, BOAT_STERN = 123, 122


def boat_section(book="#book"):
    """Black-and-gold boat feature (image right)."""
    copy = (p("The boat", "pba-eyebrow") + h("2026 21 VLE <em>IKON</em>")
            + p("Rigged to find fish and hold on them: live forward-facing sonar up front, shallow-water anchors on the back, and a wide-open front deck with room for two anglers.")
            + group(image(BOAT_STERN), "pba-boat__inset")
            + buttons(button("Book a trip", book)))
    return group(f"""<!-- wp:columns {{"verticalAlignment":"center","className":"pba-crew pba-crew--flip"}} -->
<div class="wp-block-columns are-vertically-aligned-center pba-crew pba-crew--flip"><!-- wp:column {{"verticalAlignment":"center","className":"pba-crew__copy"}} -->
<div class="wp-block-column is-vertically-aligned-center pba-crew__copy">{copy}</div>
<!-- /wp:column -->

<!-- wp:column {{"verticalAlignment":"center","width":"58%","className":"pba-crew__media"}} -->
<div class="wp-block-column is-vertically-aligned-center pba-crew__media" style="flex-basis:58%">{image(BOAT)}</div>
<!-- /wp:column --></div>
<!-- /wp:columns -->""", "pba-feature pba-feature--boat", tag="section", anchor="boat")
