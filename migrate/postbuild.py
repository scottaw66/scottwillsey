#!/usr/bin/env python3
"""Post-build feed transforms — the Zola-era equivalent of the ultrahtml step
in the old Astro rss.xml.js:

  1. Rewrite site-relative href/src in feed item content to absolute URLs
     (feed readers can't resolve relative links).
  2. Drop <script>/<style> elements from item content (the mastodon/threads
     embed components emit scripts that don't belong in feeds).

Operates on the XML-escaped text inside <content:encoded> directly (patterns
are matched in their escaped form), so nothing is unescaped/re-escaped.

Run after `zola build`:  python3 migrate/postbuild.py
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE_URL = "https://scottwillsey.com"
FEEDS = [REPO / "dist" / "rss.xml", REPO / "dist" / "reads" / "rss.xml"]

CONTENT_RE = re.compile(r"(<content:encoded>)(.*?)(</content:encoded>)", re.S)
# Escaped forms: href="/… is href=&quot;&#x2F;? — Tera escapes " as &quot;
# and leaves / alone, so the patterns below match the escaped content.
SCRIPT_RE = re.compile(r"&lt;script\b.*?&lt;/script&gt;", re.S | re.I)
STYLE_RE = re.compile(r"&lt;style\b.*?&lt;/style&gt;", re.S | re.I)


def fix_content(m: re.Match) -> str:
    inner = m.group(2)
    inner = SCRIPT_RE.sub("", inner)
    inner = STYLE_RE.sub("", inner)
    inner = inner.replace("href=&quot;&#x2F;", f"href=&quot;{BASE_URL}&#x2F;")
    inner = inner.replace("href=&quot;/", f"href=&quot;{BASE_URL}/")
    inner = inner.replace("src=&quot;&#x2F;", f"src=&quot;{BASE_URL}&#x2F;")
    inner = inner.replace("src=&quot;/", f"src=&quot;{BASE_URL}/")
    return m.group(1) + inner + m.group(3)


def main() -> int:
    ok = True
    for feed in FEEDS:
        if not feed.exists():
            print(f"ERROR missing feed: {feed}")
            ok = False
            continue
        xml = feed.read_text()
        fixed = CONTENT_RE.sub(fix_content, xml)
        feed.write_text(fixed)
        n_items = fixed.count("<item>")
        print(f"{feed.relative_to(REPO)}: {n_items} items processed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
