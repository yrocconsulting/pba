#!/usr/bin/env python3
"""Generate the inner pages (content/pages/<slug>.html + manifest.json).

Usage: build_pages.py media.json
Publish with: publish_pages.py
"""
import json
import pathlib

from site_blocks import (  # noqa: F401
    FAQ, CATCHES, media, p, h, group, button, buttons, raw,
    trips_section, reels_section, captain_section, catch_wall_section,
    crew_section, lake_section, faq_section, book_section,
)

BOOK = "/book/"
OUT = pathlib.Path(__file__).resolve().parent.parent / "content/pages"


def heading1(text):
    return f'<!-- wp:heading {{"level":1}} -->\n<h1 class="wp-block-heading">{text}</h1>\n<!-- /wp:heading -->'


def subhero(eyebrow, title, lede, variant="", ctas=True):
    cta = buttons(button("Book a trip", BOOK), button("Call (615) 310-1058", "tel:+16153101058", outline=True)) if ctas else ""
    cls = "pba-subhero" + (f" pba-subhero--{variant}" if variant else "")
    return group(p(eyebrow, "pba-eyebrow") + heading1(title) + p(lede, "pba-subhero__lede") + cta, cls, tag="section")


def cells(items, cls="pba-lakes"):
    return group("".join(group(p(f"{n:02d}", "pba-lake__num") + h(t, 3) + p(d), "pba-lake")
                         for n, (t, d) in enumerate(items, 1)), cls + " pba-reveal")


def section(eyebrow, title, lede, body, anchor=None, alt=False):
    intro = group(group(p(eyebrow, "pba-eyebrow") + h(title), "pba-section__head-copy")
                  + (p(lede, "pba-section__lede") if lede else ""), "pba-section__intro pba-reveal")
    cls = "pba-section pba-section--rule" + (" pba-section--alt" if alt else "")
    return group(intro + body, cls, tag="section", anchor=anchor)


def cta_band(title="Ready when they&rsquo;re <em>biting</em>.", lede="Half day $550 &middot; Full day $950 &middot; Per boat, 1&ndash;2 anglers &middot; $150 deposit secures your date."):
    return group(h(title) + p(lede, "pba-cta__lede")
                 + buttons(button("Book a trip", BOOK), button("Call or text (615) 310-1058", "tel:+16153101058", outline=True)),
                 "pba-cta", tag="section")


STEPS = [
    ("Send a request", "Pick half day or full day, your date and party size on the booking form, or just call or text."),
    ("We confirm", "Captain Cory reaches out to confirm the date, start time and boat ramp."),
    ("$150 deposit", "A $150 deposit locks in your date. Same deposit for a half day or a full day."),
    ("Go fishing", "Show up with your license, sunglasses and snacks. Everything else is on the boat."),
]

INCLUDED = [
    ("Rigged bass boat", "A fully rigged bass boat with a clean, roomy front deck for two anglers."),
    ("Live sonar", "Forward-facing sonar, so you can watch fish react to your bait in real time."),
    ("Rods, reels &amp; tackle", "Everything you need is on board and matched to the pattern of the day."),
    ("Catch photos", "We&rsquo;ll get photos of your fish so you can show them off."),
]

SEASONS = [
    ("Spring", "Bass move shallow to feed and spawn. Great time for numbers and big females on the banks and flats."),
    ("Summer", "Fish group up offshore on ledges, humps and points. Live sonar shines here: we find the school, then go to work."),
    ("Fall", "Bass chase bait into the creeks and pockets. Fast, fun fishing when the shad move."),
    ("Winter", "Slower, deeper fish, but some of the heaviest of the year. Patient, precise fishing pays off."),
]

TOWNS = ["Nashville", "Murfreesboro", "Smyrna", "La Vergne", "Mt. Juliet", "Hermitage", "Antioch", "Franklin", "Brentwood", "Nolensville", "Lebanon", "Gallatin"]

EXTRA_FAQ = [
    ("How long are the trips?", "A half day is about 4 hours, morning or afternoon. A full day is about 8 hours with a sunrise start."),
    ("What&rsquo;s included?", "A rigged bass boat with live forward-facing sonar, rods, reels and tackle, and photos of your catch. Bring your license, sunglasses, layers and food and drinks."),
    ("Do I need experience?", "No. Trips are built around your skill level, from first-timers and kids to tournament anglers looking to learn live sonar."),
]

# Photos for the gallery: every catch photo, minus near-duplicates and our own posters.
SKIP = {41, 54, 61, 63, 36}
GALLERY = [i for i in sorted(media, reverse=True)
           if media[i]["media_type"] == "image"
           and not media[i]["source_url"].rsplit("/", 1)[-1].startswith("pba-")
           and i not in SKIP]

PAGES = []


def page(slug, title, excerpt, blocks):
    PAGES.append({"slug": slug, "title": title, "excerpt": excerpt})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.html").write_text("\n\n".join(blocks) + "\n")


page("trips", "Trips & Rates",
     "Guided bass fishing trips on Percy Priest Lake with Captain Cory: half day $550, full day $950, per boat for 1 or 2 anglers. $150 deposit secures your date.",
     [
         subhero("Guided bass trips", "Trips &amp; <em>rates</em>.",
                 "Two guided trips on Percy Priest Lake. One price per boat for 1 or 2 anglers, and a $150 deposit secures your date."),
         trips_section(anchor="rates", book=BOOK),
         section("What&rsquo;s on board", "Everything&rsquo;s <em>included</em>.", "Show up ready to fish. The boat, the electronics and the gear are covered.", cells(INCLUDED, "pba-lakes pba-lakes--4"), anchor="included", alt=True),
         section("How booking works", "Four steps to the <em>water</em>.", None, cells(STEPS, "pba-lakes pba-lakes--4"), anchor="how"),
         section("Big groups", "Bring the whole <em>crew</em>.",
                 "Each boat fishes 1 or 2 anglers. For larger parties, Captain John Boy runs a second boat alongside Captain Cory, priced per boat, so everybody gets a guide.",
                 buttons(button("Plan a group trip", BOOK)), anchor="groups", alt=True),
         faq_section(items=[f for f in FAQ if "cost" in f[0] or "large group" in f[0] or "book" in f[0].lower()] + EXTRA_FAQ[:2], title="Trip <em>questions</em>."),
         cta_band(),
     ])

page("percy-priest-lake", "Percy Priest Lake Bass Fishing",
     "Guided bass fishing on Percy Priest Lake near Nashville, TN. Largemouth, smallmouth and spotted bass year-round with Captain Cory and live forward-facing sonar.",
     [
         subhero("Home water &middot; Nashville, TN", "Bass fishing on <em>Percy Priest</em>.",
                 "Just east of downtown Nashville, Percy Priest is one of Middle Tennessee&rsquo;s best bass lakes, and it&rsquo;s Captain Cory&rsquo;s home water.", variant="lake"),
         lake_section(),
         section("Season by season", "When to <em>go</em>.", "Bass are catchable on Percy Priest all year. The pattern changes with the seasons, and Cory runs whatever is working right now.", cells(SEASONS, "pba-lakes pba-lakes--4"), anchor="seasons"),
         section("Close to home", "Minutes from <em>you</em>.", "Percy Priest sits on the east side of Nashville, an easy drive from across Middle Tennessee.",
                 group(p(" &middot; ".join(TOWNS)), "pba-towns pba-towns--big"), anchor="towns", alt=True),
         cta_band(),
     ])

page("captain-cory", "Captain Cory",
     "Meet Captain Cory, owner and guide at Prestige Bass Adventures. Live-sonar guided bass trips on Percy Priest Lake for every skill level.",
     [
         subhero("Your captain", "Captain <em>Cory</em>.",
                 "Every Prestige Bass Adventures trip is guided by Captain Cory. Your first bass or your next personal best, every trip is built around you."),
         captain_section(book=BOOK),
         reels_section(),
         crew_section(book=BOOK),
         cta_band(title="Fish with <em>Cory</em>."),
     ])

page("gallery", "Gallery",
     "Photos and videos from guided bass fishing trips on Percy Priest Lake with Prestige Bass Adventures: largemouth, smallmouth and spotted bass.",
     [
         subhero("Gallery", "The catch <em>wall</em>.", "Real fish from real trips on Percy Priest Lake. Tap any photo to see it up close.", ctas=False),
         reels_section(),
         catch_wall_section(ids=GALLERY, title="Every <em>catch</em>.", eyebrow="Photos").replace("pba-catch-wall", "pba-catch-wall pba-catch-wall--all", 2),
         cta_band(title="Your fish <em>next</em>."),
     ])

page("faq", "FAQ",
     "Answers about guided bass fishing trips on Percy Priest Lake: prices, deposit, licenses, kids, large groups, what to bring and where to meet.",
     [
         subhero("Good to know", "Frequently asked <em>questions</em>.", "Everything you need to know before you book. Still have a question? Call or text (615) 310-1058."),
         faq_section(items=FAQ + EXTRA_FAQ, title="Before you <em>go</em>."),
         cta_band(),
     ])

page("book", "Book a Trip",
     "Book a guided bass fishing trip on Percy Priest Lake. Half day $550, full day $950, per boat for 1 or 2 anglers. $150 deposit secures your date.",
     [
         subhero("Book a trip", "Lock in your <em>date</em>.", "Send a request and Captain Cory will confirm your date and meeting spot. A $150 deposit secures it.", ctas=False),
         book_section(),
         section("How booking works", "Four steps to the <em>water</em>.", None, cells(STEPS, "pba-lakes pba-lakes--4"), anchor="how", alt=True),
     ])

(OUT / "manifest.json").write_text(json.dumps(PAGES, indent=2) + "\n")
print("built", [x["slug"] for x in PAGES], "gallery photos:", len(GALLERY))
