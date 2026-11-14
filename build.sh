#!/bin/bash
# Build scottwillsey.com (no deploy — use deploy.sh for that).
#
# Pipeline: prebuild (refresh generated stubs/data/display fields from the
# single authoring tree content/ + data/) → zola build → feed
# postprocessing → Pagefind index. See ZOLA-MIGRATION.md.
# There is no CSS step: static/css/global.css is plain CSS that Zola copies
# as written (the tailwindcss step was removed 2026-11-14, after the redesign
# left no Tailwind utilities to build).
#
# One-time setup on a fresh clone:
#   brew install zola
#   uv venv --python /opt/homebrew/bin/python3 .venv && uv pip install --python .venv/bin/python "pagefind[extended]"

set -e
cd "$(dirname "$0")"

# A running `zola serve` FOR THIS SITE rebuilds dist/ on every file change
# (Zola 0.23 writes output_dir even in serve mode — diagnosed 2026-08-07
# after "Directory not empty" delete races). Refuse to fight it. Other
# sites' zola serve processes are harmless — matched by process cwd
# (multi-site collision, 2026-08-16).
for pid in $(pgrep -f "zola serve" 2>/dev/null); do
    if [ "$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')" = "$PWD" ]; then
        echo "zola serve is running for this site — stop it before building (it rewrites dist/)."
        exit 1
    fi
done
# Clear dist/ by renaming aside (atomic; .DS_Store/mdworker races can still
# make direct rm -rf flaky). Old trees are cleaned on the next run.
rm -rf .dist-trash-* 2>/dev/null || true
if [ -d dist ]; then mv dist ".dist-trash-$$"; fi

/opt/homebrew/bin/python3 tools/prebuild.py
zola build --force
/opt/homebrew/bin/python3 tools/postbuild.py
.venv/bin/python -m pagefind --site dist

echo "Build complete: dist/"
