#!/usr/bin/env python3
"""Create or update the inner pages on the live site from content/pages/.

Uses curl so requests go through the session proxy (which adds auth for pba.fish).
Usage: publish_pages.py [slug ...]   (default: every page in manifest.json)
"""
import json
import pathlib
import subprocess
import sys
import time

SITE = "https://pba.fish"
DIR = pathlib.Path(__file__).resolve().parent.parent / "content/pages"


def api(method, path, data=None):
    cmd = ["curl", "-sS", "-X", method, f"{SITE}/wp-json/wp/v2/{path}"]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
    for attempt in range(4):
        r = subprocess.run(cmd, input=json.dumps(data) if data is not None else None,
                           capture_output=True, text=True, check=True)
        try:
            return json.loads(r.stdout)
        except json.JSONDecodeError:  # EasyWP rate limit returns HTML
            time.sleep(20 * (attempt + 1))
    raise SystemExit(f"{method} {path} failed: {r.stdout[:200]}")


manifest = json.loads((DIR / "manifest.json").read_text())
only = set(sys.argv[1:])
for pg in manifest:
    if only and pg["slug"] not in only:
        continue
    body = {
        "title": pg["title"],
        "slug": pg["slug"],
        "excerpt": pg["excerpt"],
        "content": (DIR / f"{pg['slug']}.html").read_text(),
        "status": "publish",
        "template": "page-landing",
    }
    found = api("GET", f"pages?slug={pg['slug']}&status=publish,draft&context=edit")
    if found:
        res = api("POST", f"pages/{found[0]['id']}", body)
        verb = "updated"
    else:
        res = api("POST", "pages", body)
        verb = "created"
    if "id" not in res:
        raise SystemExit(f"{pg['slug']}: {res.get('code')} {res.get('message')}")
    print(f"{verb:8} {res['id']:>4}  {res['link']}")
    time.sleep(2)
