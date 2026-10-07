# Things to revisit

## /reviews random picks: move candidate lists out of the HTML if reviews grow a lot

`templates/reviews.html` embeds every review in each category (image URL,
width, height, alt text) as a `data-reviews` attribute, so the inline script
can re-pick one per category on each page load. Only the four images shown
are downloaded; the cost is the text of the lists.

Measured 2026-10-06 with 127 reviews: the lists are ~52 KB of the 81 KB raw
HTML, adding ~20 KB compressed per visit (gzip estimate; the site serves
Brotli, which is a bit smaller). It grows linearly with review count, mostly
from alt text.

If the review count grows a lot (hundreds more), move the lists into a
separate JSON file the page fetches. It caches across visits, at the cost of
one extra request on a first visit.
