#!/usr/bin/env bash
# Package the theme as dist/prestige-bass.zip (theme files only).
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir -p dist/stage/prestige-bass
cp -r style.css theme.json functions.php inc templates parts assets dist/stage/prestige-bass/
(cd dist/stage && zip -qr ../prestige-bass.zip prestige-bass)
rm -rf dist/stage
echo "dist/prestige-bass.zip"
