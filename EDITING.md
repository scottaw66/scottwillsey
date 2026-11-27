# What to edit

Everything Scott edits by hand is in `content/` (pages and posts) and `data/` (review lists and a few settings). Some files in those folders are **written by the build or the scripts** and must never be edited by hand; they're listed at the bottom. When in doubt: if a file is in the "never edit" list, edit its source instead.

## Add a changelog entry

Edit **`content/pages/changelog.md`** and nothing else.

Add the entry at the top, under the frontmatter, newest first:

```
### 2026-11-27

What changed, in plain sentences. Links work as normal markdown.
```

- Screenshots: put them in `website-scripts/scottwillsey/scottwillsey-images/In`, run **Process Blog Image** (Brain Control's Run page), and paste what it puts on the clipboard under the entry.
- The home page shows the newest three entries straight from this file (screenshots left out). There is no other changelog file: `data/changelog.json` was removed on 2026-11-27.

## Add a media review (book, movie, TV show, music)

1. Export the review image from Quick Reviews into ~/Downloads. The Shortcuts automation runs **Media Review Images** (or run it from the Run page with the image in `website-scripts/scottwillsey/scottwillsey-images/In`).
2. The clipboard now holds two things, one after the other:
   - a markdown block (starts with `[<span hidden>`): paste it into **`content/pages/now.md`**, inside `<div class="review-now">`, under the right heading (`### TV Shows`, `### Movies`, `### Books`, `### Music`; add the heading if it isn't there);
   - a JSON entry (starts with `{` and has `"id"`, `"review"`, `"alttext"`): paste it into **`data/reviews/<category>.json`** as one more item in the list. Category files: `books.json`, `movies.json`, `tvshows.json`, `music.json`. Put a comma between it and its neighbour; the order doesn't matter (the build sorts the list).
3. Commit. The commit hook sets that category's "Last updated" date (in `data/reviews_meta.json`) and adds it to Recent Updates. Don't change those yourself.

To fix a review's text, edit its `"alttext"` in `data/reviews/<category>.json`.

`data/reviews_meta.json` holds each category's title and description: edit those two if you ever want to rename a category, nothing else in that file.

## Everything else, quickly

| To change | Edit |
|---|---|
| A blog post | `content/<post>.md` (the new-blog-post script makes new ones) |
| /now, /links, /uses | `content/pages/now.md`, `links.md`, `uses.md` (the podcast and YouTube lists on /now are written by their scripts) |
| /about | `templates/about.html` (the words live in the template) |
| Cool Site Spotlight | `data/spotlight.json` (the Cool Site Spotlight script writes it) |
| Words the title-casing leaves alone | `data/title-case-exceptions.txt` |
| The look | `static/css/global.css` |

## Never edit by hand

The build (`tools/prebuild.py`) or the commit hook rewrites these, so a hand edit is overwritten or contradicts the source:

- `content/listpages/`: the stub pages behind /1, /2…, /reads/1… and /reviews/<category>/1…
- In any page's `[extra]` block: `display_title`, `display_date`, `rfc2822_date`, `display_modified`.
- The list under a `## Contents` heading in a post.
- `display_modified` and `date` in `data/reviews_meta.json` (the hook sets `date`).
- `date` in the frontmatter of `content/pages/now.md`, `links.md`, `uses.md`, `reviews.md` (the hook sets it on commit).
- `templates/partials/recent_updates.html` (the hook writes it).
- `dist/` and `static/processed_images/` (build output, not committed).
