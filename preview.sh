#!/bin/bash
# Production preview: full build (convert → tailwind → zola → postbuild →
# pagefind), then serve the real dist/ — search works, feeds post-processed;
# exactly what production will get. Serves on the first free port at/above
# 1818 — the port is checked at startup so previews of several sites can run
# at once. Opens the browser, Ctrl-C stops it.
# No live reload: re-run after changes (or use ./dev.sh while writing).

set -e
cd "$(dirname "$0")"

# Sweep leftovers from previous runs of THIS site only — matched by process
# working directory, never by bare port or script name, so other sites'
# previews and dev servers survive (multi-site collision, 2026-08-16).
kill_mine() {
    for pid in $(pgrep -f "$1" 2>/dev/null); do
        { [ "$pid" = "$$" ] || [ "$pid" = "$PPID" ]; } && continue
        case "$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')" in
            "$PWD"|"$PWD"/*) kill "$pid" 2>/dev/null || true ;;
        esac
    done
}
kill_mine "python3 -m http.server"
kill_mine "zola serve"
kill_mine "tailwindcss -i css/global.css.*--watch"
kill_mine "bash.*(dev|preview)\.sh"

./build.sh

# First free TCP port at/above the preferred one.
PORT=1818
while lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
done

cleanup() { kill $(jobs -p) 2>/dev/null; }
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
trap cleanup EXIT

echo "Serving dist/ at http://127.0.0.1:$PORT"
( sleep 1 && open "http://127.0.0.1:$PORT" ) &
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory dist &
wait $!
