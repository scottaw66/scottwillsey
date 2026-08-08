#!/bin/bash
# Production preview: full build (convert → tailwind → zola → postbuild →
# pagefind), then serve the real dist/ — search works, feeds post-processed;
# exactly what production will get. Opens the browser, Ctrl-C stops it.
# No live reload: re-run after changes (or use ./dev.sh while writing).

set -e
cd "$(dirname "$0")"

# Sweep leftovers from previous dev.sh/preview.sh runs (stale servers,
# watchers, orphaned instances) — also lets this run even if dev.sh's zola
# serve is up, which build.sh would otherwise refuse to build against.
lsof -ti tcp:1111 -ti tcp:1818 2>/dev/null | xargs kill 2>/dev/null || true
pkill -f "tailwindcss -i css/global.css.*--watch" 2>/dev/null || true
for pid in $(pgrep -f "bash.*(dev|preview)\.sh" 2>/dev/null); do
    [ "$pid" != "$$" ] && [ "$pid" != "$PPID" ] && kill "$pid" 2>/dev/null || true
done

./build.sh

cleanup() { kill $(jobs -p) 2>/dev/null; }
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
trap cleanup EXIT

( sleep 1 && open "http://127.0.0.1:1818" ) &
python3 -m http.server 1818 --bind 127.0.0.1 --directory dist &
wait $!
