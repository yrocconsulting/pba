#!/usr/bin/env python3
"""Save every Media Library item (all pages) as JSON for the build scripts.

Usage: fetch_media.py out.json
"""
import json
import subprocess
import sys

items, page = [], 1
while True:
    r = subprocess.run(["curl", "-sS", f"https://pba.fish/wp-json/wp/v2/media?per_page=100&page={page}"],
                       capture_output=True, text=True, check=True)
    batch = json.loads(r.stdout)
    if not isinstance(batch, list) or not batch:
        break
    items += batch
    if len(batch) < 100:
        break
    page += 1
json.dump(items, open(sys.argv[1], "w"))
print(len(items), "media items")
