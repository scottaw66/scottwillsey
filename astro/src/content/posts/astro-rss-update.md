---
title: "Astro RSS 1.2.0 Update"
description: Astro fixed a bug with Astro RSS that broke custom content.
date: "2022-12-13T09:00:00-08:00"
keywords: ["blog", "rss", "astro"]
slug: "astro-rss-update"
---

Earlier today I posted about the new compiledContent() property for use in Astro RSS. What I didn't mention was that Astro RSS 1.1.0 had a bug in its XML parsing that ignored custom content (which in my case I am using for audio enclosures) and also choked on my link constructors for my post and audio file links.

Today Astro RSS 1.2.0 was released with a fix for this, thanks to a pull request from [Matt Stein](https://github.com/mattstein), so now my RSS layout for [Siracusa Says](https://siracusasays.com) looks like this:

```javascript title="src/pages/rss.xml.js"
import rss from "@astrojs/rss";
import config from "config";
import path from "path";
import sanitizeHtml from "sanitize-html";
import { rfc2822 } from "../components/utilities/DateFormat";

const episodeImportResult = import.meta.globEager("../content/episodes/*.md");
let episodes = Object.values(episodeImportResult);
episodes = episodes.sort(
  (a, b) =>
    new Date(b.frontmatter.pubDate).valueOf() -
    new Date(a.frontmatter.pubDate).valueOf(),
);

export const get = () =>
  rss({
    title: config.get("title"),
    description: config.get("description"),
    site: config.get("url"),
    items: Array.from(episodes).map((episode) => ({
      title: episode.frontmatter.title,
      link: `${new URL(
        path.join(config.get("episodes.path"), episode.frontmatter.slug),
        config.get("url"),
      )}`,
      pubDate: rfc2822(episode.frontmatter.pubDate),
      description: episode.frontmatter.description,
      customData: `<enclosure url="${new URL(
        path.join(
          config.get("episodes.audioPrefix"),
          episode.frontmatter.audiofile,
        ),
        config.get("url"),
      )}" length="${episode.frontmatter.bytes}" type="audio/mpeg" />`,
      content: sanitizeHtml(episode.compiledContent()),
    })),
  });
```

I noticed today that on my enclosure links I wasn't providing the domain in the enclosure link url, just the path. This fixes that and also makes sure that my post links (which are also used by Astro RSS for item entry GUIDs) are always correct. I hadn't had any problems with them, but this is a safer way of making sure I don't ever get any extra slashes or other malformed URL issues.
