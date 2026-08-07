---
title: Adding to Allowed Tags in sanitize-html
description: sanitize-html is a great utility for cleaning up HTML to include in RSS, among other things, but it has a limited set of allowed tags. Here's how to add to that list.
date: "2023-06-27T05:00:00-08:00"
keywords: ["javascript", "rss", "astro"]
slug: "sanitize-html"
---

Because I include full body text in my RSS feed, I use an html sanitizer called [sanitize-html](https://www.npmjs.com/package/sanitize-html) to sanitize, escape, and encode everything in the item body. One thing I didn't realize until today is that by default, it strips out img tags. I knew that images were missing from my posts when viewed in RSS readers, but I thought this was due to me using relative URLs for them and not including the full URL including domain name. This may actually still matter, but it turns out my images never got that far, because sanitize-html was removing them whenever my RSS feed was rebuilt.

The good news is, there's an easy way around this because sanitize-html provides an easy way to add tags to those allowed, and their documentation even includes the img tag example:

```javascript
const clean = sanitizeHtml(dirty, {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat(["img"]),
});
```

Here's the entirety of my original Astro RSS template before I realized this:

```javascript title="src/pages/rss.xml.js"
import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import sanitizeHtml from "sanitize-html";
import MarkdownIt from "markdown-it";
import config from "config";
import { rfc2822, year } from "../components/utilities/DateFormat";
import { globalImageUrls } from "../components/utilities/StringFormat";

const parser = new MarkdownIt();
export async function get(context) {
  let posts = await getCollection("posts");
  posts = posts.sort(
    (a, b) => new Date(b.data.date).valueOf() - new Date(a.data.date).valueOf()
  );

  return rss({
    title: config.get("title"),
    description: config.get("description"),
    site: context.site,
    xmlns: {
      atom: "http://www.w3.org/2005/Atom/",
      dc: "http://purl.org/dc/elements/1.1/",
      content: "http://purl.org/rss/1.0/modules/content/",
    },
    items: posts.map((post) => ({
      title: post.data.title,
      link: `${config.get("url")}${post.slug}`,
      pubDate: rfc2822(post.data.date),
      description: post.data.description,
      content: sanitizeHtml(parser.render(post.body)),
    })),
  });
}
```

Fixing it is as easy as modifying the content section like this:

```javascript
content: sanitizeHtml(parser.render(post.body), {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat(["img"]),
});
```

In my case I run all this through yet another custom function called globalImageUrls, which just takes relative URLs from the post body and converts them to absolute urls including the domain:

```javascript

content: globalImageUrls(
 sanitizeHtml(parser.render(post.body), {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat(["img"]),
 })
),

```

That function is in a utility file called StringFormat.js and looks look this:

```javascript title="src/components/utilities/StringFormat.js"
export function globalImageUrls(str) {
  let baseUrl = config.get("url");
  let regex =
    /<img src="\/images\/([^"]+)\/([^"]+\.(?:jpg|jpeg|gif|png))"(?: alt="([^"]*)")?\s?\/?>/g;

  return str
    .replaceAll(regex, '<img src="' + baseUrl + '/images/$1/$2" alt="$3" />')
    .replaceAll("//images", "/images");
}
```

Anyway, if you use sanitize-html be aware that this is its list of allowed tags by default:

```javascript

allowedTags: [
      "address", "article", "aside", "footer", "header", "h1", "h2", "h3", "h4",
      "h5", "h6", "hgroup", "main", "nav", "section", "blockquote", "dd", "div",
      "dl", "dt", "figcaption", "figure", "hr", "li", "main", "ol", "p", "pre",
      "ul", "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "dfn",
      "em", "I", "kbd", "mark", "q", "rb", "rp", "rt", "rtc", "ruby", "s", "samp",
      "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr", "caption",
      "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr"
    ],
```
