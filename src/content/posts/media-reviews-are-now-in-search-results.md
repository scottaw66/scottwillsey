---
title: Media Reviews Are Now in Search Results
description: My media reviews now show up in site search results for easier discovery.
date: "2025-04-08T00:10:00-08:00"
keywords: ["blog"]
cover: "../../assets/images/covers/AstroHeader.png"
coverAlt: "Astro"
series: "Astro"
slug: "media-reviews-are-now-in-search-results"
---
When I added a [Reviews](https://scottwillsey.com/reviews/) page, I wanted to be able to have individual reviews show up in [my site search](https://scottwillsey.com/search/). Due to some complexities I won’t go into of how Pagefind indexes things and how I optimize my images using the Astro Image component, this was easier said than done – until I remembered the good old HTML [hidden](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/hidden) global attribute. Then I just made a hidden span and populated it with the image alt text.

```javascript
<div class="review">
      <p>
        {
          page.data.map((book) => (
            <span hidden>{`${book.alttext}`}</span>
            <a href={`/images/posts/${book.review}.jpg`}>
              <Image
                src={import(`../../../assets/images/posts/${book.review}.png`)}
                alt={`${book.alttext}`}
              />
            </a>
          ))
        }
      </p>
    </div>
```

Now all my media reviews show up in site seach results!

[![SearchReviewsResults](../../assets/images/posts/SearchReviewsResults-839dff80-b68f-4f1c-972a-ee70ca88f0b5.png)](/images/posts/SearchReviewsResults-839dff80-b68f-4f1c-972a-ee70ca88f0b5.jpg)

Enjoy the [reviews](https://scottwillsey.com/reviews/), and don’t forget there are separate categories for [Book Reviews](https://scottwillsey.com/reviews/books/1/), [Movie Reviews](https://scottwillsey.com/reviews/movies/1/), [TV Show Reviews](https://scottwillsey.com/reviews/tv/1/), and [Music Reviews](https://scottwillsey.com/reviews/music/1/). I will be actively adding more reviews from this point forward.
