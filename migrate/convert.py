#!/usr/bin/env python3
"""Convert Astro content to Zola content. Re-runnable; see ZOLA-MIGRATION.md Phase 1.

Reads:  astro/src/content/posts/*.md, astro/src/content/reads/*.md
Writes: content/*.md (posts — root-level so the root section paginates them
        and URLs stay /{slug}), content/reads/*.md

Ownership rule: this script owns every content/*.md and content/reads/*.md
EXCEPT _index.md files, which are hand-maintained. It deletes and regenerates
exactly the files it owns, so hand edits to generated files are lost — edit
the Astro source (or after cutover, retire this script) instead.

Zero dependencies on purpose: the frontmatter is simple enough to parse by
hand (verified 2026-08-07: only `key: value` scalars, inline JSON-style
arrays, one folded array continuation, blank lines).
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "astro" / "src" / "content"
OUT = REPO / "content"

# Fields the Astro schema allows (content.config.ts) plus `slug`, which the
# glob loader reads to override the entry id. Anything else is schema drift
# and should fail the run, not be silently carried or dropped.
KNOWN_KEYS = {
    "title", "description", "date", "keywords", "slug",
    "link", "cover", "coverAlt", "series", "draft",
}
REQUIRED_KEYS = {"title", "description", "date", "keywords", "slug"}

# Ported from astro/src/components/utilities/remark-social-links.mjs — the
# remark plugin matched whole text nodes; here a "text node" is a line whose
# entire trimmed content is the bare URL.
YOUTUBE_RE = re.compile(
    r"^<?https://(?:www\.youtube\.com/watch\?v=|youtu\.be/)([\w-]+)(?:\S*)?>?$"
)
MASTODON_RE = re.compile(r"^<?https://([a-zA-Z0-9.-]+)/(@[\w-]+)/(\d{10,20})>?$")
THREADS_RE = re.compile(
    r"^<?https://www\.threads\.net/(@[\w.]+)/post/([A-Za-z0-9_\-]+)(\?.*)?>?$"
)

# Source slugs to correct, with a redirect (Zola alias) from the old URL.
# "updated-sessions…,-2025-edition": the comma is a frontmatter typo that
# shipped to the live URL (found 2026-08-07); Zola's slugifier strips it, so
# adopt the clean slug and keep the old URL working.
SLUG_FIXES = {
    "updated-sessions-raycast-script-command,-2025-edition":
        "updated-sessions-raycast-script-command-2025-edition",
}

# Markdown body images that Astro ran through astro:assets (anything under
# src/assets/images). Images already in static/ (e.g. /images/...) pass through.
ASSET_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(\s*(?:\.\./)*assets/images/([^)\s]+?)\s*\)"
)

errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        errors.append(f"{path}: no frontmatter block")
        return {}, text
    raw, body = m.groups()
    # Fold continuation lines (indented) into the previous key's value.
    lines: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line[0] in " \t":
            lines[-1] += " " + line.strip()
        else:
            lines.append(line)
    fm: dict[str, object] = {}
    for line in lines:
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not key or key != key.split()[0]:
            errors.append(f"{path}: unparseable frontmatter line {line!r}")
            continue
        if key in fm:
            errors.append(f"{path}: duplicate key {key!r}")
        fm[key] = parse_value(key, value, path)
    return fm, body


def parse_value(key: str, value: str, path: Path) -> object:
    if value.startswith("["):
        try:
            arr = json.loads(value)
            assert isinstance(arr, list) and all(isinstance(x, str) for x in arr)
            return arr
        except (json.JSONDecodeError, AssertionError):
            errors.append(f"{path}: cannot parse array for {key!r}: {value!r}")
            return []
    if value in ("true", "false"):
        return value == "true"
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    return value


def toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


FENCE_RE = re.compile(r"^ {0,3}(```|~~~)")
# Since Zola 0.23, content .md files are themselves Tera templates: any
# literal {{ / {% / {# in the source — prose OR code samples — would be
# evaluated (or error) at build time unless wrapped in {% raw %}.
TERA_TOKEN_RE = re.compile(r"\{\{|\{%|\{#")
# Component invocations this script emits (must not be raw-wrapped).
EMITTED_RE = re.compile(r"\{\{<[a-z]+ [^>]*/>\}\}")


def raw_wrap(line: str) -> str:
    return "{% raw %}" + line + "{% endraw %}"


def convert_body(body: str, path: Path) -> str:
    """Transform prose lines; fenced code blocks pass through untouched apart
    from raw-wrapping (tutorial posts contain code samples full of
    assets/images paths and markdown-image syntax that must not be converted,
    but Tera braces in them still need {% raw %} protection)."""

    def img_repl(m: re.Match) -> str:
        alt, src = m.group(1), m.group(2)
        if '"' in alt:
            if "'" in alt:
                errors.append(f"{path}: image alt has both quote types: {alt!r}")
            # Tera string args accept single quotes, so a " in alt is fine.
            return "{{<img src='%s' alt='%s' />}}" % (src, alt)
        return '{{<img src="%s" alt="%s" />}}' % (src, alt)

    out_lines = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif in_fence:
            if TERA_TOKEN_RE.search(line):
                line = raw_wrap(line)
        else:
            stripped = line.strip()
            if m := YOUTUBE_RE.match(stripped):
                line = '{{<youtube id="%s" />}}' % m.group(1)
            elif m := MASTODON_RE.match(stripped):
                line = '{{<mastodon domain="%s" user="%s" id="%s" />}}' % (
                    m.group(1), m.group(2), m.group(3))
            elif m := THREADS_RE.match(stripped):
                line = '{{<threads user="%s" id="%s" />}}' % (m.group(1), m.group(2))
            else:
                # Transform/validate only outside inline code spans — prose
                # often mentions paths like `src/assets/images` in backticks.
                segs = re.split(r"(`[^`]*`)", line)
                for i, seg in enumerate(segs):
                    if seg.startswith("`"):
                        continue
                    seg = ASSET_IMG_RE.sub(img_repl, seg)
                    if "assets/images" in seg:
                        errors.append(
                            f"{path}: unconverted assets/images reference: {stripped[:70]!r}")
                    segs[i] = seg
                line = "".join(segs)
                if TERA_TOKEN_RE.search(EMITTED_RE.sub("", line)):
                    if EMITTED_RE.search(line):
                        # Mixed literal braces + component on one line: raw-
                        # wrapping would break the component. Needs a human.
                        errors.append(
                            f"{path}: literal braces AND component on one line: {stripped[:60]!r}")
                    else:
                        line = raw_wrap(line)
        out_lines.append(line)
    if in_fence:
        errors.append(f"{path}: unclosed code fence")
    return "\n".join(out_lines)


def render(fm: dict, body: str, path: Path, section: str) -> str:
    unknown = set(fm) - KNOWN_KEYS
    if unknown:
        errors.append(f"{path}: unknown frontmatter keys {sorted(unknown)}")
    missing = REQUIRED_KEYS - set(fm)
    if missing:
        errors.append(f"{path}: missing required keys {sorted(missing)}")
        return ""
    date = str(fm["date"])
    try:
        datetime.fromisoformat(date)
    except ValueError:
        errors.append(f"{path}: unparseable date {date!r}")

    # Some keywords arrays contain comma-joined strings ("ai,writing,website")
    # — a data-entry typo that produced garbage tags on the live site. Split
    # and warn so future occurrences surface.
    tags = []
    for kw in fm["keywords"]:
        if "," in kw:
            warnings.append(f"{path}: comma-joined keyword split: {kw!r}")
            tags.extend(k.strip() for k in kw.split(",") if k.strip())
        else:
            tags.append(kw)

    slug = str(fm["slug"])
    aliases = []
    if slug in SLUG_FIXES:
        aliases.append(f"/{slug}/")
        slug = SLUG_FIXES[slug]

    lines = ["+++"]
    lines.append(f"title = {toml_str(str(fm['title']))}")
    lines.append(f"description = {toml_str(str(fm['description']))}")
    lines.append(f"date = {date}")
    lines.append(f"slug = {toml_str(slug)}")
    if aliases:
        lines.append("aliases = [%s]" % ", ".join(toml_str(a) for a in aliases))
    if fm.get("draft") is True:
        lines.append("draft = true")
    if section == "posts":
        # Only posts feed the tags taxonomy — Astro built /tags/ from post
        # keywords alone; reads keywords go to [extra] to keep the data.
        lines.append("[taxonomies]")
        lines.append("tags = [%s]" % ", ".join(toml_str(t) for t in tags))
    extra = {k: fm[k] for k in ("link", "cover", "coverAlt", "series") if k in fm}
    if section != "posts":
        extra["keywords"] = tags
    if extra:
        lines.append("[extra]")
        for k, v in extra.items():
            key = "cover_alt" if k == "coverAlt" else k
            if isinstance(v, list):
                lines.append(f"{key} = [%s]" % ", ".join(toml_str(x) for x in v))
            else:
                lines.append(f"{key} = {toml_str(str(v))}")
    lines.append("+++")
    return "\n".join(lines) + "\n\n" + convert_body(body, path).strip() + "\n"


def convert_section(src_dir: Path, out_dir: Path, section: str) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        if old.name != "_index.md":
            old.unlink()
    count = 0
    for f in sorted(src_dir.glob("*.md")):
        fm, body = parse_frontmatter(f.read_text(), f)
        rendered = render(fm, body, f, section)
        if rendered:
            (out_dir / f.name).write_text(rendered)
            count += 1
    return count


def main() -> int:
    n_posts = convert_section(SRC / "posts", OUT, "posts")
    n_reads = convert_section(SRC / "reads", OUT / "reads", "reads")
    print(f"converted: {n_posts} posts (content/), {n_reads} reads (content/reads/)")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s) — output incomplete, fix and re-run.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
