# Getting scottwillsey.com off npm: Python/Rust SSG alternatives

*Analysis date: 2026-08-06. Site version at time of analysis: 6.1.0 (Astro 7.1.6).*

## Why

Goal: get out from under the npm/JavaScript supply chain. The current build pulls
in **~460 packages** (per `package-lock.json`) to build what is, structurally, a
markdown blog with a sidebar. Every `ncu` run is a new roll of the dice on
transitive dependencies, and Astro itself has a history of version churn
(this repo has already lived through Astro 3 → 7).

## What the site actually does (feature inventory)

Everything the Astro build provides, extracted from `src/`, `astro.config.mjs`,
and `ec.config.mjs`:

### Content model (`src/content.config.ts`)
- **11 markdown collections**, all YAML frontmatter + markdown body:
  - `posts` (~160 files) — title, description, optional `link` (link-blog posts),
    date, `keywords` (tags), optional `cover`/`coverAlt` image, optional `series`,
    optional `draft` (drafts render in dev, excluded in prod)
  - `reads` (~45 files) — weekly reads, title/description/date/keywords
  - Single-page collections: `links`, `now`, `uses`, `changelog`, plus
    `reviews`/`books`/`movies`/`music`/`tvshows` index pages
- **JSON data**: `src/data/site.json` (site config), `spotlight.json` (Cool Site
  Spotlight), `reviews/*.json` (review image lists keyed to image filenames)

### Routing / pages (`src/pages/`)
- `/{slug}` — individual posts (slug = filename)
- `/{page}` — paginated post list, 7 per page, with windowed pagination controls
- `/reads/{slug}`, `/reads/{page}` — same pattern for weekly reads
- `/tags/` (tag cloud) and `/tags/{tag}` — generated from post `keywords`
- `/reviews/` + `/reviews/{books,movies,music,tv}/{page}` — paginated image
  grids driven by the JSON lists (10 per page), sorted by alt text
- Static pages: `/`, `/about`, `/now`, `/links`, `/uses`, `/changelog`,
  `/search`, `/404`
- `rss.xml` and `/reads/rss.xml` — **full-content** feeds: each post is rendered
  to HTML, relative `href`/`src` rewritten to absolute URLs, `<script>`/`<style>`
  stripped (ultrahtml), RFC-2822 dates

### Markdown pipeline (the "dynamic" part)
- **remark-toc** — builds a table of contents under a `## Contents` heading
  (used by `links.md` and some posts)
- **remark-social-links** (custom, `src/components/utilities/remark-social-links.mjs`)
  — a bare YouTube / Mastodon / Threads URL on its own line becomes an embed
  (iframe / blockquote markup)
- **rehype-accessible-emojis** — wraps emoji in `role="img"` spans
- **expressive-code** — fenced code blocks → themed, framed code blocks with
  line numbers plugin; three themes switched by `[data-theme='…']` selector
- **Footnotes** — rendered by markdown, enhanced client-side by
  `public/scripts/barefoot.min.js` (littlefoot-style popovers; not an npm dep,
  just a static file)
- `remark-modified-time.mjs` exists (git-date extraction via `execSync`) but is
  **not currently wired into the config** — vestigial

### Image optimization (astro:assets / sharp)
Three distinct uses:
1. **Markdown body images**: `![alt](../../assets/images/posts/X.png)` —
   Astro/sharp emits hashed, optimized (webp) copies with intrinsic
   width/height (CLS-safe). Post markdown wraps these in links to full-size
   JPGs in `public/images/posts/` (originals served as-is).
2. **`<Image>` component**: `Spotlight.astro` (width 300, densities 2x/3x
   srcset), review `[page].astro` grids, post `cover` images (width 950).
3. **`public/` passthrough**: favicons, full-size review/post JPGs, fonts —
   copied verbatim (no processing).

### Templates / layout
- One layout (`Base.astro`): HTML shell, font preloads (self-hosted woff2 in
  `public/fonts/` — the `astro-font` dep is installed but unused), RSS `<link>`,
  CSS grid shell (header / sidebar+main / footer)
- ~15 small components (Header, Menu, Sidebar, Footer, Post, PostTitle,
  LatestPosts, RecentUpdates, Changelog, Spotlight, TagCloud, Search, Read) and
  ~25 inline-SVG icon components taking size/fill props
- Conditional rendering: sidebar shows LatestPosts/RecentUpdates only off-home;
  link-posts get a link icon; series banner if `series` set
- `RecentUpdates.astro` is **rewritten by a pre-commit hook** — any replacement
  needs an equivalent includable fragment the hook can write

### Styling
- Tailwind 4 utility classes throughout templates (via `@tailwindcss/vite`)
- `src/styles/global.css` (758 lines): CSS custom properties, light/dark themes
  via `[data-theme]`, typography, pagefind UI overrides

### Search
- **Pagefind** (`astro-pagefind`): post-build indexer + static JS search UI;
  templates use `data-pagefind-ignore` annotations

### Utilities
- `DateFormat.js` — date-fns wrappers: "MMMM d, yyyy" post dates, RFC 2822 for
  RSS
- `StringFormat.js` — `titleCase`, `slugify`

### Build/deploy
- `npm run build` → `astro build` + `update-site.sh` (scp deploy — independent
  of the SSG choice)
- Sitemap: `@astrojs/sitemap` is installed but **not registered** in
  `astro.config.mjs` integrations — apparently not actually in use

### Vestigial deps found during this audit
`astro-font`, `markdown-it`, `normalize.css`, `@astrojs/sitemap` (unregistered),
`remark-modified-time.mjs` — none referenced by the live build.

---

## The candidates

### Option A — Zola (Rust) ⭐ recommended

**You never write or read Rust.** Zola is a single ~25 MB binary
(`brew install zola`) with everything compiled in: markdown, syntax
highlighting, taxonomies, pagination, feeds, sitemap, image processing, Sass,
live-reload server. Templates are **Tera**, a Jinja2 clone — if you can read
Python, you can read Tera. Actively maintained: v0.23.1 released 2026-08-05.

Supply chain after migration: **1 binary (Zola) + 1 pip package (Pagefind) +
optionally 1 binary (Tailwind standalone)**. No package tree at all. Nothing to
`ncu`. A Zola upgrade is one binary swap, and staying on an old version
indefinitely is safe because there are no transitive deps to rot.

| Site feature | Zola equivalent | Effort |
|---|---|---|
| Collections + schemas | `content/` sections with TOML frontmatter; schema enforcement is gone (or a 30-line Python lint script) | Frontmatter conversion script (YAML→TOML), one-off |
| `/{slug}`, pagination | Sections with `paginate_by`; slugs from filenames | Config |
| Tags from `keywords` | Built-in taxonomies (`tags`), auto tag pages + per-tag feeds | Rename `keywords` → `taxonomies.tags` in same script |
| Drafts | `draft = true`, `zola serve --drafts` | Free |
| Astro components | Tera partials/macros (`{% include %}`, `{{ macros::icon(...) }}`) | Port ~15 templates + icons; mechanical |
| Markdown images (auto-optimize) | `resize_image()` in a shortcode, webp output, or post-process (see below) | Script + shortcode |
| `<Image>` w/ densities | Same `resize_image()` calls in templates | Small |
| expressive-code | Built-in syntect highlighting, themes, `linenos` annotation | Config; different look, close enough |
| remark-toc | `page.toc` in templates / shortcode | Small |
| Social-link embeds | Shortcodes (`{{ youtube(id="…") }}` etc.); one-off regex conversion of bare URLs in content, or keep bare URLs and pre-process | Script, one-off |
| Footnotes | CommonMark footnotes built-in; barefoot.min.js unchanged | Free |
| Full-content RSS | Feed templates get `page.content` (HTML); Zola renders internal links absolute via `base_url` | Custom `rss.xml` template, moderate |
| Pagefind | Unchanged — `pip install 'pagefind[extended]'`, run against output dir; same client JS, same CSS overrides | Trivial |
| Tailwind | Standalone Tailwind CLI binary (no npm), or fold utilities into global.css | Keep binary = zero template changes |
| Sitemap | Built-in | Free (an upgrade — it's currently broken/absent) |
| Deploy script | Unchanged (`zola build` then scp) | Trivial |
| Pre-commit RecentUpdates rewrite | Hook writes a Tera partial or a JSON data file instead | Trivial |

**Real gaps:** (1) TOML-only frontmatter — needs the one-off conversion script;
(2) markdown body images aren't auto-optimized — either convert `![…]` to an
image shortcode (script) or run a small Python/Pillow post-build pass over the
HTML (works for any SSG, see Option C); (3) Zod schema validation disappears;
(4) expressive-code's exact styling won't be reproduced, just approximated.

### Option B — Pelican (Python)

The mature Python SSG (Jinja2 + Python-Markdown + Pygments), active since 2010,
plugin ecosystem included. Best choice **if you want the generator itself to be
hackable in Python** rather than configured.

- Feeds, tags, pagination, drafts (`Status: draft`) built in; YAML-ish metadata
  natively (no frontmatter conversion needed with the right reader)
- **image-process plugin** (Pillow): responsive srcset/derivatives from plain
  markdown images by rewriting the output HTML — the closest match to Astro's
  automatic markdown image optimization of any option
- Custom remark-type logic (social embeds, TOC placement) = ordinary Python
  markdown extensions or Pelican plugins — the part you'd actually enjoy owning
- Pygments code highlighting with line numbers (different look from
  expressive-code)
- Pagefind and Tailwind standalone work the same as with Zola

**Trade-off:** you swap the npm tree for a PyPI tree — much smaller (~15–25
packages: pelican, jinja2, markdown, pygments, pillow, feedgenerator…) and
PyPI's blast radius for this stack is far smaller than npm's, but it is not
zero like Zola. Pelican's templates/config also have their own conventions to
learn, and theme structure is more opinionated than Zola's.

### Option C — Bespoke Python build script

~600–900 lines: `markdown-it-py` (the *Python port of the same markdown-it
parser family* the site already depends on — plugins for footnotes/TOC exist),
`Jinja2`, `Pillow`, `PyYAML`, `feedgen`. Six well-known PyPI deps, all
boring and stable. Total control, zero framework churn forever, and the site's
logic (~160 posts, 11 collections, simple routing) genuinely fits in a single
readable script.

**Trade-off:** you own pagination edge cases, incremental rebuild/dev-server
(or just rebuild everything — a site this size builds in seconds), feed
correctness, and CLS-safe image dimension injection. It's a fun project and a
maintenance commitment. Reasonable as a later evolution *after* proving the
content migration on Zola/Pelican, or if the scripting itself is the appeal.

## Recommendation

**Zola, with Python doing the one-off migration and any pre/post-processing.**
It's the only option that takes the package count to ~zero, it needs no Rust
knowledge (Tera ≈ Jinja2), it's fast and actively maintained, and its built-ins
cover ~90% of this site's feature list. Use Python where Zola is rigid:

1. One-off migration script: YAML→TOML frontmatter, `keywords`→taxonomy tags,
   bare social URLs→shortcodes, markdown images→image shortcode.
2. Optional post-build Pillow pass if shortcode-based image handling feels
   clunky (this also de-risks a later move to Pelican or Option C — the same
   script works everywhere).
3. Keep Pagefind via pip; keep Tailwind via standalone binary (or migrate
   utilities into global.css over time to reach true zero-binary-deps).

**Pelican is the fallback** if hands-on Tera templating turns out to be
unpleasant or automatic markdown-image processing matters more than a
zero-package supply chain.

### Suggested proof-of-concept (a weekend, not a rewrite)

1. `brew install zola`, `zola init` in a scratch dir
2. Write the frontmatter conversion script; run it over `posts/` + `reads/`
3. Port `Base.astro` + Post + Sidebar to Tera with Tailwind standalone watching
4. Wire taxonomy tags, pagination, one feed template
5. Run Pagefind over `public/` output; compare against the live site

If steps 2–4 feel good, the rest (reviews grids, links/now/uses pages, icons)
is mechanical.

## Sources

- [Zola](https://www.getzola.org/) / [getzola/zola releases](https://github.com/getzola/zola) — v0.23.1, 2026-08-05
- [Pagefind installation docs](https://pagefind.app/docs/installation/) — `python3 -m pip install 'pagefind[extended]'`, no Node required
- [pagefind on PyPI](https://pypi.org/project/pagefind/)
