---
title: "Astro RSS Compiled Content"
description: Astro RSS now supports full content RSS feed items.
date: "2022-12-13T05:00:00-07:00"
keywords: ["blog", "rss", "astro"]
series: "Astro"
slug: "astro-rss-compiledcontent"
---

It's been awhile and I have lots of news, but just a short one today: [Astro](https://astro.build) now supports full [RSS feed](https://docs.astro.build/en/guides/rss/) content if you use md files for your content. It works like this:

```javascript title="src/pages/rss.xml.js"
export const get = () =>
  rss({
    title: config.get("title"),
    description: config.get("description"),
    site: config.get("url"),
    items: Array.from(episodes).map((episode) => ({
      title: episode.frontmatter.title,
      link: `${config.get("url")}${config.get("episodes.path")}${
        episode.frontmatter.slug
      }`,
      pubDate: rfc2822(episode.frontmatter.pubDate),
      description: episode.frontmatter.description,
      customData: `<enclosure url="${config.get("episodes.audioPrefix")}/${
        episode.frontmatter.audiofile
      }" length="${episode.frontmatter.bytes}" type="audio/mpeg" />`,
      content: sanitizeHtml(episode.compiledContent()),
    })),
  });
```

See the last line of code?

```javascript
content: sanitizeHtml(episode.compiledContent());
```

That's directly telling Astro RSS that for a given item, the content is equal to the post's compiledContent property (and run through [sanitize-html](https://www.npmjs.com/package/sanitize-html) for good measure).

You can find the [Astro docs](https://docs.astro.build/en/getting-started/) for it here: [Including Full Post Content](https://docs.astro.build/en/guides/rss/#including-full-post-content)

There is one caveat I need to mention that directly affects this site. If you use [mdx](https://mdxjs.com) instead of md for your posts like I do here, compiledContent() doesn't work. Since I don't like my [current RSS feed generation tweak](/rss-pt2) for this site in order to get full content RSS items, my plan is to work on converting back to md and figuring out a way to process images such that I get the benefit of [Astro Image](https://www.npmjs.com/package/@astrojs/image)'s Picture and Image components while using standard markdown files.
