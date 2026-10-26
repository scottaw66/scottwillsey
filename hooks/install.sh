#!/bin/bash
# Install the repo's pre-commit hook into .git/hooks (fresh clones need this
# once; re-run after editing hooks/pre-commit — it is a copy, not a symlink).
# The hook bumps dates on watched pages (TOML frontmatter, or
# data/reviews_meta.json for review categories), rewrites the Recent Updates
# partial, and runs tools/prebuild.py so derived files land in the same
# commit. Note: the user-level git config sets
# core.hooksPath to a global guard hook, which chains to .git/hooks — so
# installing here is still effective.

set -e
cd "$(dirname "$0")/.."
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "Installed hooks/pre-commit -> .git/hooks/pre-commit"
