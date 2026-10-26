#!/usr/bin/env python3
"""Build step 1: refresh the generated artifacts the Zola templates need.

content/ (TOML frontmatter markdown) and data/ (JSON) are the ONE authoring
tree — edit them directly; the dashboard scripts and the pre-commit hook
write them too. There is no converter and no second copy (the YAML src/
tree and migrate/convert.py were retired 2026-10-25, see ZOLA-MIGRATION.md).

This script owns ONLY generated artifacts and never rewrites a hand-authored
body (the single exception is the list under a `## Contents` heading, which
is itself generated — see insert_toc). It is idempotent: a second run right
after the first writes nothing. Run from any cwd; exit 1 on any error.

What it refreshes:

  1. Display fields in each page's [extra] table, in place, editing only
     those `key = …` lines: posts (content/*.md) get display_title (title
     case, exceptions in data/title-case-exceptions.txt), display_date and
     rfc2822_date; reads (content/reads/*.md) get display_date and
     rfc2822_date; the singles in content/pages/ (links, now, uses,
     changelog, reviews) get display_modified. Templates use these because
     Tera v2's title filter downcases acronyms and its date filter no
     longer parses ISO 8601 datetimes.
  2. The markdown list under a `## Contents` heading (posts, reads, singles).
  3. content/listpages/*.md — list-page stubs for /1…/N, /reads/1…/N and
     /reviews/<cat>/1…/N (counted from content/, content/reads/ and
     data/reviews/*.json); stale stubs are deleted.
  4. data/reviews/*.json sorted by alttext (casefold) in place — the review
     templates assume that order and the review-images script appends
     unsorted (checked 2026-10-25).
  5. data/reviews_meta.json — display_modified per category recomputed from
     that category's `date`. title/description/date in that file are hand
     (or hook) edited source; the file has no comments because JSON can't.
  6. data/changelog.json — last three entries of content/pages/changelog.md,
     markdown links turned into HTML, for the homepage.

It also fails the build on Astro-era image syntax left in a body
(`![alt](../../assets/images/x.png)` outside code) — that means old
converter INPUT was pasted in; the Zola form is {{<img src="posts/x.png"
alt="…" />}}.

Zero dependencies on purpose: TOML is read with the stdlib tomllib and
written by editing single lines, so everything else in a file is preserved
byte for byte.
"""

import json
import re
import sys
import tomllib
from datetime import date as date_type, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"
DATA = REPO / "data"
LISTPAGES = CONTENT / "listpages"

LIST_PAGE_SIZE = 7  # zola.toml extra.posts_paginate_by — used by both lists
REVIEW_PAGE_SIZE = 10  # zola.toml extra.reviews_paginate_by

# Single pages under content/pages/ whose display_modified this script
# maintains. about.md and search.md there are hand-maintained template stubs
# with no date and are not touched.
SINGLES = ("links", "now", "uses", "changelog", "reviews")

# Review categories: (data/reviews/<coll>.json, URL segment / reviews_meta key)
REVIEW_CATS = [("books", "books"), ("movies", "movies"),
               ("tvshows", "tv"), ("music", "music")]

errors: list[str] = []
warnings: list[str] = []


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def write_if_changed(path: Path, text: str) -> bool:
    """Skip byte-identical writes. Zola's dev server watches content/ — the
    old wipe-everything-and-rewrite approach fired hundreds of file events
    per run and `zola serve` could catch the tree mid-wipe, fail the rebuild,
    and wedge (observed 2026-08-07). Now a normal edit touches one file.
    This is also what lets dev.sh re-run this script on every content/ or
    data/ change without looping: the run triggered by our own writes
    writes nothing."""
    if path.exists() and path.read_text() == text:
        return False
    path.write_text(text)
    print(f"wrote {rel(path)}")
    return True


def prune_stale(dir: Path, keep: set, protected: tuple = ("_index.md",)) -> None:
    """Delete generated stubs that no longer correspond to a list page."""
    for old in dir.glob("*.md"):
        if old.name not in keep and old.name not in protected:
            old.unlink()
            print(f"removed {rel(old)}")


def toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --- frontmatter -----------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^\+\+\+\n(.*?)\n\+\+\+\n(.*)\Z", re.S)
TABLE_HEADER_RE = re.compile(r"^\s*\[")
KEY_LINE_RE = re.compile(r"^([A-Za-z0-9_-]+)\s*=")


def split_frontmatter(text: str, path: Path) -> tuple[str, str, dict] | None:
    """Return (frontmatter text, body, parsed frontmatter) or None on error.
    The body is everything after the closing +++ line, kept verbatim."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append(f"{rel(path)}: no +++ frontmatter block")
        return None
    fm_text, body = m.groups()
    try:
        fm = tomllib.loads(fm_text)
    except tomllib.TOMLDecodeError as e:
        errors.append(f"{rel(path)}: frontmatter is not valid TOML: {e}")
        return None
    return fm_text, body, fm


def set_extra_fields(fm_text: str, fm: dict, wanted: dict[str, str],
                     path: Path) -> str:
    """Return fm_text with each wanted key = value present in the [extra]
    table, editing only those lines: an existing `key = …` line is replaced,
    a missing key is appended at the end of the table, and a missing [extra]
    table is created at the end of the frontmatter. Returns fm_text unchanged
    when every value already matches.

    Layout assumption (verified across the whole tree 2026-10-25): [extra] is
    a plain table whose entries each START on their own `key = …` line (a
    multi-line array is fine; dotted keys are not). The edited text is
    re-parsed and the wanted values re-read before it is accepted, so a
    layout this can't handle fails loudly instead of corrupting a file."""
    extra = fm.get("extra", {})
    if all(extra.get(k) == v for k, v in wanted.items()):
        return fm_text
    lines = fm_text.split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "[extra]") + 1
    except StopIteration:
        lines.append("[extra]")
        start = len(lines)
    end = start
    while end < len(lines) and not TABLE_HEADER_RE.match(lines[end]):
        end += 1
    key_lines = {m.group(1): i for i in range(start, end)
                 if (m := KEY_LINE_RE.match(lines[i]))}
    if set(key_lines) != set(extra):
        errors.append(f"{rel(path)}: [extra] has entries this script can't edit "
                      f"line-by-line (multi-line or dotted keys?) — fix by hand")
        return fm_text
    for k, v in wanted.items():
        if extra.get(k) == v:
            continue
        new_line = f"{k} = {toml_str(v)}"
        if k in key_lines:
            lines[key_lines[k]] = new_line
        else:
            # Insert before any blank lines that end the table so the entry
            # stays inside it.
            at = end
            while at > start and not lines[at - 1].strip():
                at -= 1
            lines.insert(at, new_line)
            end += 1
            for kk in key_lines:
                if key_lines[kk] >= at:
                    key_lines[kk] += 1
            key_lines[k] = at
    new_text = "\n".join(lines)
    try:
        check = tomllib.loads(new_text)
    except tomllib.TOMLDecodeError as e:  # should be unreachable
        errors.append(f"{rel(path)}: edited frontmatter is not valid TOML: {e}")
        return fm_text
    if any(check.get("extra", {}).get(k) != v for k, v in wanted.items()):
        errors.append(f"{rel(path)}: [extra] edit did not take — fix by hand")
        return fm_text
    return new_text


# --- display fields --------------------------------------------------------

SMALL_WORDS_RE = re.compile(
    r"^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$",
    re.I,
)
TITLE_TOKEN_RE = re.compile(r"[A-Za-z0-9À-ÿ]+[^\s\-]*")
TITLE_WORD_RE = re.compile(r"[A-Za-z0-9À-ÿ]+")

TITLE_CASE_EXCEPTIONS_FILE = DATA / "title-case-exceptions.txt"


def load_title_case_exceptions() -> dict[str, str]:
    """Words title_case keeps exactly as spelled (e.g. npm), from a
    user-editable file: one word per line, # comments, blank lines ignored.
    Keyed by lowercase so matching ignores case. A missing file just means
    no exceptions."""
    if not TITLE_CASE_EXCEPTIONS_FILE.exists():
        return {}
    words = {}
    for line in TITLE_CASE_EXCEPTIONS_FILE.read_text(encoding="utf-8").splitlines():
        word = line.split("#", 1)[0].strip()
        if word:
            words[word.lower()] = word
    return words


TITLE_CASE_EXCEPTIONS = load_title_case_exceptions()


def title_case(title: str) -> str:
    """Port of the Astro site's StringFormat.js titleCase — templates use the
    precomputed result (extra.display_title) because Tera's title filter
    behaves differently (it would downcase acronyms like GPT). Words listed
    in data/title-case-exceptions.txt are emitted exactly as spelled there
    (checked first, so they win over every rule below)."""

    def char_at(i: int) -> str:
        return title[i] if 0 <= i < len(title) else ""

    def repl(m: re.Match) -> str:
        match, index = m.group(0), m.start()
        # A token can carry trailing punctuation ("npm:", "npm's"), so compare
        # only its leading word and keep the rest as-is
        word = TITLE_WORD_RE.match(match).group(0)
        if word.lower() in TITLE_CASE_EXCEPTIONS:
            return TITLE_CASE_EXCEPTIONS[word.lower()] + match[len(word):]
        if (
            index > 0
            and index + len(match) != len(title)
            and SMALL_WORDS_RE.search(match)
            and char_at(index - 2) != ":"
            and (char_at(index + len(match)) != "-" or char_at(index - 1) == "-")
            and not re.search(r"[^\s\-]", char_at(index - 1))
        ):
            return match.lower()
        if re.search(r"[A-Z]|\..", match[1:]):
            return match
        return match[0].upper() + match[1:]

    return TITLE_TOKEN_RE.sub(repl, title)


def page_date(fm: dict, path: Path) -> datetime | None:
    """The TOML `date` as a datetime. tomllib already parses an offset
    datetime (`date = 2024-04-13T12:00:00-08:00`, the only form in this
    tree as of 2026-10-25); a quoted string or a bare date is an error so a
    typo can't silently produce an empty display date."""
    d = fm.get("date")
    if isinstance(d, datetime):
        return d
    if isinstance(d, date_type):
        errors.append(f"{rel(path)}: date has no time — use YYYY-MM-DDTHH:MM:SS-08:00")
    elif d is None:
        errors.append(f"{rel(path)}: missing date")
    else:
        errors.append(f"{rel(path)}: date must be a bare TOML datetime, not {d!r}")
    return None


def display_date(d: datetime) -> str:
    """Port of DateFormat.js postdate ("eeee, dd MMM yyyy") — precomputed
    because Tera v2's date filter no longer parses ISO 8601 datetimes."""
    return d.strftime("%A, %d %b %Y")


def rfc2822_date(d: datetime) -> str:
    """Feed pubDate: RFC 2822 in UTC labeled "GMT", matching the live feeds
    exactly (verified item-by-item against the Astro build's rss.xml
    2026-08-07)."""
    return d.astimezone(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S") + " GMT"


def modified_date(d: datetime) -> str:
    """Port of DateFormat.js modifieddate ("eeee, dd MMM yyyy HH:mm:ss")."""
    return d.strftime("%A, %d %b %Y %H:%M:%S")


# --- body: TOC and validation ------------------------------------------------

FENCE_RE = re.compile(r"^ {0,3}(```|~~~)")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.*?)\s*$")
TOC_ITEM_RE = re.compile(r"^\s*- \[")
# Astro-era body image syntax (anything under the old src/assets/images
# root). The converter used to rewrite these; now they mean someone pasted
# old-style markdown. Checked outside code fences and inline code only —
# tutorial posts show this exact syntax in code samples.
ASSET_IMG_RE = re.compile(r"\]\(\s*(?:\.\./)*assets/images/")


def zola_anchor(text: str, seen: dict) -> str:
    """Replicate Zola's heading-anchor slugifier: lowercase, every run of
    non-alphanumerics becomes one dash, trimmed; duplicates get -1, -2 …
    (verified against Zola 0.23 output for the links page and TOC posts —
    NOT github-slugger, which e.g. drops dots where Zola dashes them)."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    n = seen.get(slug)
    seen[slug] = 0 if n is None else n + 1
    return slug if n is None else f"{slug}-{seen[slug]}"


def insert_toc(body: str, path: Path) -> str:
    """remark-toc replacement: if a '## Contents' heading exists, (re)generate
    the nested markdown list of links to every following heading directly
    under it, replacing exactly the list that is already there (blank lines
    plus consecutive `- [` items) and nothing else. Idempotent, so it is
    safe on every run; a fresh `## Contents` with nothing under it gets the
    list inserted.

    Why not a Tera component reading page.toc: content .md files are Tera
    templates rendered BEFORE the markdown pass, and page.toc is built by
    that markdown pass — tested 2026-10-25 with Zola 0.23.6: `{{ page.toc |
    length }}` inside a post body renders 0, and a component can't see
    `page` at all ("Variable `page` is not defined")."""
    lines = body.split("\n")
    toc_at = None
    in_fence = False
    headings = []  # (level, label, text, after_toc) in document order —
    # pre-TOC headings still consume anchor slugs in Zola's dedupe.
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        text = m.group(2).strip()
        if toc_at is None and m.group(1) == "##" and text.lower() == "contents":
            toc_at = i
            headings.append((2, "Contents", "Contents", False))
            continue
        # Link label: heading text minus inline-code backticks. Bare
        # [brackets] render literally and slugify fine (verified against the
        # astro-icon-v1 baseline) — only real links or emphasis need review.
        label = text.replace("`", "")
        if re.search(r"\]\(|[*_]", label):
            warnings.append(f"{rel(path)}: TOC heading has markdown formatting: {text!r}")
        headings.append((len(m.group(1)), label, text, toc_at is not None))
    if toc_at is None:
        return body
    entries = [(lvl, label, text) for lvl, label, text, after in headings if after]
    if not entries:
        warnings.append(f"{rel(path)}: '## Contents' with no following headings")
        return body
    seen: dict = {}
    min_level = min(lvl for lvl, _, _ in entries)
    toc = []
    for lvl, label, text, after in headings:
        anchor = zola_anchor(re.sub(r"`", "", text), seen)
        if after:
            toc.append("  " * (lvl - min_level) + f"- [{label}](#{anchor})")
    # The existing list: blank lines after the heading, then `- [` items. If
    # there are no items (fresh heading), keep the author's blank lines so
    # the list is inserted between them, as remark-toc did.
    end = toc_at + 1
    while end < len(lines) and not lines[end].strip():
        end += 1
    if end < len(lines) and TOC_ITEM_RE.match(lines[end]):
        while end < len(lines) and TOC_ITEM_RE.match(lines[end]):
            end += 1
    else:
        end = toc_at + 1
    return "\n".join(lines[: toc_at + 1] + [""] + toc + lines[end:])


def check_body(body: str, path: Path) -> None:
    in_fence = False
    for n, line in enumerate(body.split("\n"), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose = "".join(seg for seg in re.split(r"(`[^`]*`)", line)
                        if not seg.startswith("`"))
        if ASSET_IMG_RE.search(prose):
            errors.append(f"{rel(path)}: Astro-era image syntax at body line {n} — "
                          "use {{<img src=\"posts/x.png\" alt=\"…\" />}}")


# --- per-page refresh --------------------------------------------------------

def refresh_page(path: Path, kind: str) -> None:
    """kind: 'post', 'read' or 'single'. Refreshes the [extra] display fields
    and the Contents TOC; writes only if something changed."""
    text = path.read_text()
    parsed = split_frontmatter(text, path)
    if parsed is None:
        return
    fm_text, body, fm = parsed
    d = page_date(fm, path)
    if d is None:
        return
    if kind == "single":
        wanted = {"display_modified": modified_date(d)}
    else:
        wanted = {"display_date": display_date(d), "rfc2822_date": rfc2822_date(d)}
        if kind == "post":
            if "title" not in fm:
                errors.append(f"{rel(path)}: missing title")
                return
            wanted["display_title"] = title_case(str(fm["title"]))
    new_fm = set_extra_fields(fm_text, fm, wanted, path)
    new_body = insert_toc(body, path)
    check_body(new_body, path)
    write_if_changed(path, "+++\n" + new_fm + "\n+++\n" + new_body)


# --- generated stubs and data ------------------------------------------------

STUB_BANNER = ("# GENERATED by tools/prebuild.py (list stub) — do not edit; "
               "regenerated on every build")


def write_list_stubs(kind: str, url_base: str, template: str,
                     count: int, names: set) -> int:
    """List pages /1…/N and /reads/1…/N: Zola's paginator can't serve these
    (/ is the standalone homepage, /reads/ never existed), so each list URL
    gets a stub page whose template slices the section itself. `count` is
    the number of page files, drafts included (as the converter counted)."""
    pages = -(-count // LIST_PAGE_SIZE)
    for n in range(1, pages + 1):
        fname = f"{kind}-{n}.md"
        write_if_changed(LISTPAGES / fname,
            "+++\n" + STUB_BANNER + "\n"
            f'title = "{kind} page {n}"\n'
            f'path = "{url_base}{n}"\n'
            f'template = "{template}"\n'
            "[extra]\n"
            f"page_num = {n}\n"
            "+++\n"
        )
        names.add(fname)
    return pages


def sort_reviews_data() -> dict[str, int]:
    """Keep data/reviews/*.json sorted by alttext (casefold — the
    localeCompare order the Astro pages used) and return item counts."""
    counts = {}
    for coll, _seg in REVIEW_CATS:
        f = DATA / "reviews" / f"{coll}.json"
        items = json.loads(f.read_text())
        items.sort(key=lambda x: x["alttext"].casefold())
        write_if_changed(f, json.dumps(items, indent=2, ensure_ascii=False) + "\n")
        counts[coll] = len(items)
    return counts


def write_review_stubs(counts: dict[str, int], names: set) -> None:
    for coll, seg in REVIEW_CATS:
        pages = -(-counts[coll] // REVIEW_PAGE_SIZE)
        for n in range(1, pages + 1):
            fname = f"reviews-{seg}-{n}.md"
            write_if_changed(LISTPAGES / fname,
                "+++\n" + STUB_BANNER + "\n"
                f'title = "{seg} reviews page {n}"\n'
                f'path = "/reviews/{seg}/{n}"\n'
                'template = "reviews_category.html"\n'
                "[extra]\n"
                f"page_num = {n}\n"
                f'category = "{seg}"\n'
                f'data_file = "reviews/{coll}.json"\n'
                "+++\n"
            )
            names.add(fname)


def refresh_reviews_meta() -> None:
    """data/reviews_meta.json holds each review category's title,
    description and date (the pre-commit hook bumps `date` when that
    category's JSON is committed); only display_modified is derived."""
    f = DATA / "reviews_meta.json"
    meta = json.loads(f.read_text())
    for _coll, seg in REVIEW_CATS:
        if seg not in meta:
            errors.append(f"{rel(f)}: missing category {seg!r}")
            continue
        try:
            d = datetime.fromisoformat(meta[seg]["date"])
        except (KeyError, ValueError):
            errors.append(f"{rel(f)}: {seg}: date must be ISO 8601 like 2026-10-06T18:34:53-08:00")
            continue
        meta[seg]["display_modified"] = modified_date(d)
    write_if_changed(f, json.dumps(meta, indent=2, ensure_ascii=False) + "\n")


def write_changelog_json() -> None:
    """Port of Changelog.astro's entry parsing: last 3 '### date' entries of
    the changelog, image links stripped, markdown links → HTML. Templates
    read the result via load_data (markdown munging is easier in Python)."""
    body = (CONTENT / "pages" / "changelog.md").read_text()
    body = re.sub(r"^\+\+\+\n.*?\n\+\+\+\n?", "", body, flags=re.S)
    entries = [e for e in re.split(r"^### ", body, flags=re.M) if e.strip()]
    out = []
    for entry in entries[:3]:
        date, *description = entry.split("\n")
        desc = " ".join(description).strip()
        desc = re.sub(r"\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)", "", desc)
        desc = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", desc)
        desc = re.sub(
            r"\[([^\]]+)\]\(([^)]*\.(jpg|jpeg|png|gif|webp|svg)[^)]*)\)",
            "", desc, flags=re.I)
        desc = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', desc)
        out.append({"date": date.strip(), "html": desc})
    write_if_changed(DATA / "changelog.json",
                     json.dumps({"entries": out}, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    posts = sorted(p for p in CONTENT.glob("*.md") if p.name != "_index.md")
    reads = sorted(p for p in (CONTENT / "reads").glob("*.md") if p.name != "_index.md")
    for p in posts:
        refresh_page(p, "post")
    for p in reads:
        refresh_page(p, "read")
    for name in SINGLES:
        f = CONTENT / "pages" / f"{name}.md"
        if not f.exists():
            errors.append(f"{rel(f)}: missing single page")
            continue
        refresh_page(f, "single")

    LISTPAGES.mkdir(exist_ok=True)
    stub_names: set = set()
    p_pages = write_list_stubs("posts", "/", "postlist.html", len(posts), stub_names)
    r_pages = write_list_stubs("reads", "/reads/", "readslist.html", len(reads), stub_names)
    counts = sort_reviews_data()
    write_review_stubs(counts, stub_names)
    prune_stale(LISTPAGES, stub_names)
    refresh_reviews_meta()
    write_changelog_json()

    print(f"prebuild: {len(posts)} posts, {len(reads)} reads, {len(SINGLES)} singles checked; "
          f"list stubs /1…/{p_pages}, /reads/1…/{r_pages}, reviews "
          + ", ".join(f"{seg} {-(-counts[coll] // REVIEW_PAGE_SIZE)}" for coll, seg in REVIEW_CATS))
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s) — fix and re-run.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
