#!/usr/bin/env bash
# Package the theme and install it on the live site via /wp-json/pba/v1/deploy.
# Auth: admin Application Password (injected for pba.fish by the session proxy).
set -euo pipefail
cd "$(dirname "$0")/.."
SITE="${SITE:-https://pba.fish}"
./tools/package.sh >/dev/null
curl -sS -X POST "$SITE/wp-json/pba/v1/deploy" -H "Content-Type: application/zip" --data-binary @dist/prestige-bass.zip
echo
