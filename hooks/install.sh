#!/bin/bash
# Install the repo's pre-commit hook into .git/hooks (fresh clones need this
# once). The hook bumps frontmatter dates on watched pages, rewrites the
# Recent Updates partial, and regenerates Zola content so generated files
# land in the same commit. Note: the user-level git config sets
# core.hooksPath to a global guard hook, which chains to .git/hooks — so
# installing here is still effective.

set -e
cd "$(dirname "$0")/.."
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "Installed hooks/pre-commit -> .git/hooks/pre-commit"
