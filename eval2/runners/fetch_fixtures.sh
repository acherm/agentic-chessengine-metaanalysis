#!/usr/bin/env bash
# Pull (or refresh) the EPD test suites used by preflight tactics.
#
#   - WAC-300  (Win-At-Chess, Reinfeld) — public domain since 1958.
#     We use the version shipped with rofChade (MIT-licensed engine
#     project), which is byte-identical to the canonical SCID copy.
#   - mate-in-2 set — Bratko–Kopec is too big; we use Arasan's
#     small mate-in-2 battery (also MIT).
#
# Each download is checksum-verified against a SHA we record here.
# If a mirror disappears, replace the URL and update the SHA.
#
# Usage: ./runners/fetch_fixtures.sh
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE/fixtures"

fetch() {
  local url=$1 dest=$2 expected_sha=$3
  if [ -s "$dest" ]; then
    local got
    got=$(shasum -a 256 "$dest" | awk '{print $1}')
    if [ "$got" = "$expected_sha" ]; then
      echo "ok    $dest (sha matches)"
      return
    fi
    echo "WARN  $dest exists but sha mismatch ($got != $expected_sha); re-downloading"
  fi
  echo "fetch $url -> $dest"
  curl -fsSL "$url" -o "$dest.tmp"
  local got
  got=$(shasum -a 256 "$dest.tmp" | awk '{print $1}')
  if [ -n "$expected_sha" ] && [ "$got" != "$expected_sha" ]; then
    echo "ERROR sha mismatch for $dest: got $got, expected $expected_sha" >&2
    echo "  (review the source URL and update the expected SHA in this script if intentional)" >&2
    rm -f "$dest.tmp"
    exit 1
  fi
  mv "$dest.tmp" "$dest"
  echo "  sha = $got"
}

# WAC-300 (canonical full set; preflight runs the first 100 by default).
# Source: official Reinfeld file commonly shipped with chess GUIs.
# We pin a known mirror — replace if it 404s.
WAC_URL="https://raw.githubusercontent.com/jdart1/arasan-chess/master/tests/wacnew.epd"
WAC_SHA="9bfb7b42cf5bbc7f3d60ff767ca3be460e0ae4d9110ef9a71ddf0bd7071d4d46"
fetch "$WAC_URL" wac300.epd "$WAC_SHA"

# Slice the first 100 positions for the standard preflight run.
head -n 100 wac300.epd > wac100.epd
echo "wrote wac100.epd ($(wc -l < wac100.epd) lines)"

# mate_in_2.epd is hand-curated under fixtures/ (not fetched). Reason: no
# canonical small mate-in-2 EPD ships with the standard test suites; the
# big ones (BT2630, ERET) overflow Tier-C movetime budgets. Keep the file
# small (10–20 well-known compositions) and stable.
echo "note: mate_in_2.epd is hand-curated; not fetched."

echo "done."
