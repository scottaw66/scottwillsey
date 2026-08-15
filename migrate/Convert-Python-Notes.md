Why convert.py runs on every build

It was conceived as a one-time migration, but you changed the plan mid-migration — ZOLA-MIGRATION.md records it as an architecture decision (yours, 2026-08-07): "YAML authoring stays, converter is permanent." All your dashboard scripts in ~/Scripts/Sites/scottwillsey/ and the pre-commit hook write YAML-frontmatter markdown into src/content/ and src/data/. Rather than rewrite all that automation to emit Zola's TOML dialect, the decision was: src/ stays the permanent source of truth you author in, and convert.py translates it into Zola-flavored content/ as build step 1, forever. (The migrate/ directory name is the historical part, not the script.)

On each run it regenerates content/ from src/: TOML front matter, the precomputed [extra] fields (display_title, display_date, rfc2822_date — the titleCase/date formatting Tera can't reproduce), image-link rewriting (below), {% raw %} guards around literal {{/{% in code fences, the list-page stubs in content/listpages/, and so on. It's change-aware — only writes files whose content actually changed — so zola serve's watcher doesn't get spammed and dev rebuilds stay fast.

build.sh, step by step

1. Guard against zola serve — Zola 0.23's serve mode rewrites dist/ on every change (diagnosed 2026-08-07 after "Directory not empty" races), so building while it runs means two processes fighting over the same output dir. It refuses instead.
2. Clear dist/ by renaming it aside to .dist-trash-$$ rather than rm -rf in place — the rename is atomic, dodging the macOS .DS_Store/Spotlight-worker races that made direct deletion flaky. Old trash dirs get swept at the start of the next run.
3. convert.py — src/ → content/, as above.
4. Tailwind — compiles css/global.css → static/css/global.css (gitignored; it's a build product).
5. zola build --force — renders content/ + templates/ into dist/.
6. postbuild.py — post-processes the RSS feed so it byte-matches what @astrojs/rss + your old ultrahtml transforms produced (keeping feed readers from seeing every item as "new").
7. Pagefind — indexes dist/ for site search.

Image optimization for inline markdown images

Two-stage relay, replacing Astro's sharp-based astro:assets:

Stage 1 — convert.py rewrites the markdown. ASSET_IMG_RE (migrate/convert.py:59) matches ![alt](../../assets/images/foo.png)-style links and rewrites each to a component call: {{<img src="foo.png" alt="…" />}}. It's careful to skip code fences and inline backticks (your posts literally discuss these paths), and it errors on anything under assets/images it couldn't convert, so nothing slips through raw. Images that were already static URLs like /images/... pass through untouched — they were never optimized under Astro either.

Stage 2 — the img component optimizes at zola build time. Defined at templates/components.html:14: it calls get_image_metadata() to read the original dimensions, then resize_image(op="fit", width=orig, height=orig, format="webp", quality=80) — same dimensions in and out, so it's not downscaling, just re-encoding to webp. Zola writes the processed file to static/processed_images/ (gitignored, content-hashed) and the component emits an <img> with intrinsic width/height attributes and loading="lazy" decoding="async". The migration doc records that the output markup is attribute-identical to the old sharp output and the file sizes matched (93 KB vs 93 KB for the same 672 KB source PNG).

Cover images take a slightly different path: the post_article component calls resize_image directly with width=950, op="fit_width" (templates/site_components.html:30), so those do get downscaled.

Also: I fixed that one stale comment in convert.py (it claimed templates resolve images under astro/src/assets/images/; the astro/ prefix died at cutover). That's the only working-tree change — say the word if you want it committed.