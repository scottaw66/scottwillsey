# Scott Willsey

This is version 7.0.0 of my website, [scottwillsey.com](https://scottwillsey.com) — the [Zola](https://www.getzola.org/) version. After years of Astro (versions 3 through 6.x), the site now builds with a single Rust binary and **zero npm dependencies**. The full migration story lives in [ZOLA-MIGRATION.md](ZOLA-MIGRATION.md) and the evaluation that led here in [SSG-ALTERNATIVES.md](SSG-ALTERNATIVES.md).

Pages inspired by fun trends on the web: a [now](https://scottwillsey.com/now/) page, a [links](https://scottwillsey.com/links/) page, a [uses](https://scottwillsey.com/uses/) page, and [reviews](https://scottwillsey.com/reviews/) of books, movies, TV shows, and music.

## License

Split license — see [LICENSE](LICENSE) for the exact boundaries:

- **Code** (templates, build scripts, `tools/` and `hooks/` tooling, site CSS/JS): MIT.
- **Content** (posts, pages, reviews, photos, artwork, and the content data files): &copy; Scott Willsey, **all rights reserved**. It's in the repo because the site is built from it, not as an invitation to republish it or train on it.

## How it works

There is one authoring tree, and it is what Zola reads (since 2026-10-25; before that a YAML `src/` tree was converted into `content/` on every build — see ZOLA-MIGRATION.md).

- **`content/`** — the posts (`content/*.md`), weekly reads (`content/reads/`) and single pages (`content/pages/`: links, now, uses, changelog, reviews, plus the about/search stubs), as markdown with **TOML frontmatter** (`+++ … +++`). Edit these files directly; the dashboard scripts (`~/Brain/Areas/Sites/Repos/website-scripts/scottwillsey/`) write them too. Body images are component calls, `{{<img src="posts/x.png" alt="…" />}}`, and social embeds are `{{<youtube id="…" />}}`, `{{<mastodon … />}}`, `{{<threads … />}}` (all in `templates/components.html`). Literal `{{`/`{%` in prose or code samples must be wrapped in `{% raw %}…{% endraw %}` because Zola 0.23 renders content as Tera templates.
- **`data/`** — the hand/script-edited JSON: `reviews/*.json` (review image lists), `reviews_meta.json` (each review category's title, description and `date`), `spotlight.json` (Cool Site Spotlight), and `title-case-exceptions.txt` (words the display-title casing leaves alone, e.g. `npm`).
- **`src/assets/images/`** — only the image store that `resize_image` reads (post images, covers, review images). Nothing else lives under `src/`.
- **`tools/prebuild.py`** (zero-dependency Python, build step 1) refreshes the generated bits in place and never rewrites a hand-authored body: the `[extra]` display fields in every post/read/single (`display_title`, `display_date`, `rfc2822_date`, `display_modified` — Tera v2 can't produce them from `date`/`title`), the markdown list under any `## Contents` heading, the list-page stubs in `content/listpages/` (the only wholly generated files left), `data/changelog.json`, `display_modified` in `data/reviews_meta.json`, and the alttext sort order of `data/reviews/*.json`. It is idempotent and only writes files that actually change. It fails the build if a body still contains Astro-era `![alt](../../assets/images/…)` image syntax outside code.
- **[Zola](https://www.getzola.org/)** builds the site: Tera v2 templates in `templates/`, taxonomies, pagination, sitemap, section RSS feeds.
- **`tools/postbuild.py`** post-processes the feeds (absolute URLs, script/style stripping) like ultrahtml used to.
- **[Tailwind CSS](https://tailwindcss.com/) standalone binary** compiles `css/global.css` → `static/css/global.css` (gitignored).
- **[Pagefind](https://pagefind.app/)** (official PyPI package, extended build) indexes `dist/` post-build and provides the search UI.
- **[Barefoot](https://github.com/philgruneich/barefoot)** still does the pop-up footnotes.

## Building

```bash
./build.sh    # prebuild → tailwind → zola → postbuild → pagefind
./deploy.sh   # build.sh + rsync deploy (update-site.sh)
```

## Dev server / previewing

**1. Writing/preview mode — `./dev.sh`** (the normal way):

```bash
./dev.sh              # http://127.0.0.1:1111, live reload, opens the browser
./dev.sh --drafts     # same, including draft posts
```

One command, leave it running. It starts the Zola dev server AND watches `content/`, `data/` and `src/assets`, re-running `tools/prebuild.py` on every save (plus Tailwind in watch mode for template/CSS edits) — so saving a post reloads the browser with its display fields, TOC and list stubs already refreshed, and a newly landed image triggers a rebuild even though Zola doesn't watch `src/assets`. Ctrl-C stops everything.

Caveats:

- Search boxes render but return nothing in dev mode — the Pagefind index only exists after a full `./build.sh`.
- **Stop `dev.sh` before running `./build.sh`** — Zola 0.23's serve mode rewrites `dist/` on every change and the two fight over the directory (build.sh refuses to run and tells you if it detects this).

**2. Production preview — `./preview.sh`** (the real built site: search working, feeds post-processed — exactly what production will serve):

```bash
./preview.sh          # builds, serves http://127.0.0.1:1818, opens the browser
```

Ctrl-C stops it. No live reload — re-run it after changes (or use `./dev.sh` while actively writing).

## One-time setup on a fresh clone

```bash
brew install zola tailwindcss
uv venv .venv && uv pip install --python .venv/bin/python "pagefind[extended]"
./hooks/install.sh   # pre-commit hook: date bumps, Recent Updates, prebuild in the same commit
```

Updating the toolchain: `brew upgrade zola tailwindcss` and `uv pip install --python .venv/bin/python -U "pagefind[extended]"`. That's the entire supply chain.

_All content &copy; 2022&ndash;2026 by Scott Willsey_
