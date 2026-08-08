# Scott Willsey

This is version 7.0.0 of my website, [scottwillsey.com](https://scottwillsey.com) — the [Zola](https://www.getzola.org/) version. After years of Astro (versions 3 through 6.x), the site now builds with a single Rust binary and **zero npm dependencies**. The full migration story lives in [ZOLA-MIGRATION.md](ZOLA-MIGRATION.md) and the evaluation that led here in [SSG-ALTERNATIVES.md](SSG-ALTERNATIVES.md).

Pages inspired by fun trends on the web: a [now](https://scottwillsey.com/now/) page, a [links](https://scottwillsey.com/links/) page, a [uses](https://scottwillsey.com/uses/) page, and [reviews](https://scottwillsey.com/reviews/) of books, movies, TV shows, and music.

## How it works

- **Authoring** stays in `src/` — YAML-frontmatter markdown in `src/content/`, JSON data in `src/data/`, images in `src/assets/images/`. All the site automation scripts (`~/Scripts/Sites/scottwillsey/`, run from the dashboard) write here, unchanged from the Astro era.
- **`migrate/convert.py`** (zero-dependency Python) turns that into Zola content: TOML frontmatter, tags, precomputed display dates/titles, automatic Contents TOCs, social embeds and images as Tera components, `{% raw %}` protection.
- **[Zola](https://www.getzola.org/)** builds the site: Tera v2 templates in `templates/`, taxonomies, pagination, sitemap, section RSS feeds.
- **`migrate/postbuild.py`** post-processes the feeds (absolute URLs, script/style stripping) like ultrahtml used to.
- **[Tailwind CSS](https://tailwindcss.com/) standalone binary** compiles `css/global.css` → `static/css/global.css` (gitignored).
- **[Pagefind](https://pagefind.app/)** (official PyPI package, extended build) indexes `dist/` post-build and provides the search UI.
- **[Barefoot](https://github.com/philgruneich/barefoot)** still does the pop-up footnotes.

## Building

```bash
./build.sh    # convert → tailwind → zola → postbuild → pagefind
./deploy.sh   # build.sh + rsync deploy (update-site.sh)
```

## Dev server / previewing

**1. Writing/preview mode — `./dev.sh`** (the normal way):

```bash
./dev.sh              # http://127.0.0.1:1111, live reload, opens the browser
./dev.sh --drafts     # same, including draft posts
```

One command, leave it running. It starts the Zola dev server AND watches the `src/` authoring tree, auto-running the converter on every save (plus Tailwind in watch mode for template/CSS edits) — so editing `src/content/whatever.md` just reloads in the browser like it did under Astro. Ctrl-C stops everything.

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
./hooks/install.sh   # pre-commit hook: date bumps, Recent Updates, content regeneration
```

Updating the toolchain: `brew upgrade zola tailwindcss` and `uv pip install --python .venv/bin/python -U "pagefind[extended]"`. That's the entire supply chain.

_All content &copy; 2026 by Scott Willsey_
