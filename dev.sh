#!/bin/bash
# Preview/writing mode: one command, then just edit and save.
#
#   ./dev.sh            → http://127.0.0.1:1111 with live reload (opens browser)
#   ./dev.sh --drafts   → same, including draft posts
#
# What it runs (all cleaned up on Ctrl-C):
#   - migrate/convert.py once up front, then again automatically whenever
#     anything in src/ (the authoring tree) changes — zola serve only watches
#     the generated content/, so this is what makes "save → browser reloads"
#     work for content edits
#   - tailwindcss --watch, rebuilding static/css/global.css on template/CSS edits
#   - zola serve (foreground)

set -e
cd "$(dirname "$0")"

# Sweep leftovers from previous runs of THIS site only — matched by process
# working directory, never by bare port or script name, so other sites'
# previews and dev servers survive (multi-site collision, 2026-08-16).
# Note: zola serve still binds 1111, so two sites can't run dev.sh at once —
# but the failure is a visible "port in use" error, not a silent kill.
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

python3 migrate/convert.py
tailwindcss -i css/global.css -o static/css/global.css

# Everything (zola, tailwind, watcher) runs as a job; on ANY exit path —
# Ctrl-C, TERM, terminal closing, zola crashing — kill all jobs so nothing
# is left running. (Verified 2026-08-07: a plain foreground zola + EXIT trap
# orphans zola when the script is signaled directly rather than via the
# terminal's process group.)
cleanup() { kill $(jobs -p) 2>/dev/null; }
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
trap cleanup EXIT

tailwindcss -i css/global.css -o static/css/global.css --watch >/dev/null 2>&1 &

# Poll src/ once a second; on any change, re-run the converter (it takes well
# under a second). The stamp file lives outside the repo.
stamp=$(mktemp)
(
  while sleep 1; do
    if [ -n "$(find src -type f -newer "$stamp" -print -quit 2>/dev/null)" ]; then
      touch "$stamp"
      python3 migrate/convert.py || echo "⚠ convert.py failed — fix the error above and save again"
      # If the conversion changed no content files, zola gets no file event —
      # but the src/ change may still matter to it: images referenced by
      # resize_image / get_image_metadata live in src/, which zola doesn't
      # watch. Scripts also write content BEFORE their images finish landing
      # (observed 2026-08-07: yt-history wrote now.md 3s before its thumbs),
      # so a failed build would otherwise never retry. Nudge a rebuild.
      if [ -z "$(find content -name '*.md' -newer "$stamp" -print -quit 2>/dev/null)" ]; then
        touch content/_index.md
      fi
    fi
  done
) &

( sleep 2 && open "http://127.0.0.1:1111" ) &
# --extra-watch-path data: templates read data/*.json via load_data, which
# zola neither watches nor re-reads on unrelated rebuilds (its serve cache
# kept /reviews pages stale after review-JSON changes — observed 2026-08-07).
# Watching data/ makes JSON changes trigger a real reload.
zola serve --extra-watch-path data "$@" &
wait $!
