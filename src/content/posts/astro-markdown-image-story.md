---
title: "Astro Markdown Image Story"
description: "Astro's in a good place - native markdown image optimization is coming, and there is already an excellent third-party option for those who need it now."
date: "2023-03-13T05:00:00-08:00"
keywords: ["blog", "images", "responsive", "astro"]
series: "Responsive Images"
slug: "astro-markdown-image-story"
---

Until now, Astro hasn't had a built-in way to dump image links in straight Markdown content files and have Astro generate optimized images and responsive HTML for them. This caused me a problem, which I partially solved by using [MDX](https://mdxjs.com) instead of Markdown for blog posts, and importing and calling [Astro Image](https://www.npmjs.com/package/@astrojs/image) inside the MDX post files. This SOUNDS great, because this is the whole purpose of MDX, [in MDX's own words](https://mdxjs.com):

> MDX allows you to use JSX in your markdown content. You can import components, such as interactive charts or alerts, and embed them within your content. This makes writing long-form content with components a blast. 🚀

There are, however, a couple problems with this. One of them I've spoken about on this site, which is MDX makes it very hard to generate full-content RSS feeds with Astro ([part 1](https://scottwillsey.com/rss-pt1/) and [part 2](https://scottwillsey.com/rss-pt2/) of that saga [here](https://scottwillsey.com/rss-pt1/) and [here](https://scottwillsey.com/rss-pt2/)).

Also, using the Astro Image component directly in my content means mixing writing and implementation details, something I strongly dislike. When I'm writing a blog post, I don't WANT to have to remember Astro Image syntax, and I don't WANT to have to remember exactly what widths I like to specify and what media-query-ish styling I put in the `sizes` attribute. I just want to write and to let my system handle all that by itself. That's what computers are for.

Here's what it looks like when I want to put an image in one of my posts using MDX as my content file format and the Astro Image component directly inside my blog post:

```astro
---
import { Picture } from "@astrojs/image/components";
import somethingSomething from "/images/posts/somethingsomething.png";
---

<Picture
  src={somethingSomething}
  widths={[600, 900, 1200, 1500]}
  sizes="(max-width: 800px) 90vw, 800px"
  formats={["avif", "webp", "png"]}
  alt={"This is a lot of work just to drop an image in a blog post"}
/>
```

I don't want to remember that. I never want to think about that at all. I want to put an image link in using standard markdown and have Astro do all that for me.

```markdown
[![This is a lot of work just to drop an image in a blog post](../../assets/images/posts/somethingsomething.png)](/images/posts/somethingsomething.png)
```

I have two pieces of good news for you if you're in the same boat as me:

1. The wonderful people at Astro are building an [Astro Assets integration](https://docs.astro.build/en/guides/assets/) that can create optimized versions of and responsive img tags for images linked to in Markdown.

2. In the meantime, you can use the really nice and fully functional [Astro Markdown Eleventy Image Astro component](https://github.com/ChrisOh431/astro-remark-eleventy-image) by [CJ Ohanaja](https://cjohanaja.com/). As you may have guessed, it uses [Eleventy Image](https://www.11ty.dev/docs/plugins/image/) to do the work of intercepting Markdown image links and replacing them with responsive ones (and generating the responsive images themselves, of course).

The Astro Assets integration loudly proclaims itself as experimental, and that's not self-deprecation: it won't build. It runs great in the dev server, but it gives all kinds of wacky errors when trying to build. But just using it in dev mode is enough to see the future, and it's great.

As for Astro Markdown Eleventy Image, it works great in build, but it doesn't bother to optimize anything in dev mode. That means if you use the browser inspector tools to look at your images while testing in dev mode, you'll see gigantic original file sizes. You'll have to build and run preview to serve up the built pages locally to see its handiwork.

But the good news is, you can quit or never start using MDX right this minute, and you can still have optimized images from Markdown image links with Astro.

By the way, in case you've forgotten my RSS story at the start of this, now that I'm using straight Markdown files for my posts again, I can just straight up go back to using [Astro RSS](https://www.npmjs.com/package/@astrojs/rss) and generate an RSS feed with full post content, and not have to do my hacky custom nonsense anymore.

That's such good news for me, because that hack only generated the RSS file in dev mode, so every time I did a build I had to copy the RSS.xml to the dist folder, AND remember to change all the link prefixes from `http://localhost:3000` to `https://scottwillsey.com`.

Another annoying implementation detail I never want to think about again, vanquished!
