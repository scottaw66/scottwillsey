---
title: Creating Drafts in Astro 5
description: I did something I should have done a long time ago and added draft functionality to this website.
date: "2025-03-25T00:10:00-08:00"
keywords: ["astro", "blog"]
slug: "creating-drafts-in-astro"
---
Last week or so, I started writing a blog post as I sometimes do, this one pertaining to my [Automation Workflow for Media Reviews](https://scottwillsey.com/media-reviews-automation/). Unfortunately, I wanted to preview it as I went along, so I copied it in progress to my git main branch of the local copy of the website.

You can see where this is going.

Yes, I updated something else on the website and published it, INCLUDING the partial draft of the blog post I was working on. This wasn’t a super huge deal, except that I use [EchoFeed](https://echofeed.app/) to automatically post to [Bluesky](https://bsky.app/profile/scottwillsey.com) and [Mastodon](https://social.lol/@scottwillsey) whenever I post something new on the site.

Sigh.

The good news is that this finally pushed me to add drafts functionality to my site, so that I could have drafts render when running locally in development mode, but not actually get written when doing a site build. It’s a good, basic feature to have.

Initially I started with the method shared by [Alex Curtis](https://jacurtis.com/) in his post [How to Create a Draft Post in Astro](https://jacurtis.com/notes/astro-draft-posts/), but his filter didn’t actually work for me. I think this is because his example was for a different version of Astro, possibly. I wound up using the Astro Docs example for [Filtering Content Collection Queries](https://docs.astro.build/en/guides/content-collections/#filtering-collection-queries).

Basically, there are three steps to adding draft posts to Astro 5:

1. Add an optional draft data property to your blog post collection in your content.config.ts, as below,

```typescript title="src/content.config.ts" {17}
const postCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/posts" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      link: z.string().optional(),
      date: z
        .string()
        .transform((str) => new Date(str))
        .optional()
        .nullable(),
      keywords: z.string().array(),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      series: z.string().optional(),
      draft: z.boolean().optional(),
    }),
});
```

2. Filter based on this in any page that uses this content collection, [the way the Astro Docs show](https://docs.astro.build/en/guides/content-collections/#filtering-collection-queries),

```javascript title="src/pages/[page].astro" {9-11}
---
import Base from "../layouts/Base.astro";
import Post from "../components/Post.astro";
import Pager from "../components/Pager.astro";
import { getCollection } from "astro:content";
import site from "../data/site.json";

export async function getStaticPaths({ paginate }) {
  let posts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });

  posts = posts.sort(
    (a, b) => new Date(b.data.date).valueOf() - new Date(a.data.date).valueOf(),
  );

  return paginate(posts, {
    pageSize: site.posts.paginationSize,
  });
}
const { page } = Astro.props;

const title = site.title;
const description = `Posts Page ${page.currentPage}`;
---

<Base title={title} description={description}>
  <section aria-label="Post list" data-pagefind-ignore>
    {
      page.data.map((post, index) => {
        return <Post post={post} />;
      })
    }
    <Pager page={page} />
  </section>
</Base>
```

3. And finally, use it in a draft post!

```markdown {6}
---
title: Creating Drafts in Astro
description: describe
date: "2025-03-25T00:10:00-08:00"
keywords: ["keyword"]
draft: true
slug: "creating-drafts-in-astro"
---
I’ve always wanted to be a writer, and I’ve always wanted to create drafts in Astro that won’t get published until I want them to.

[Now I can!](https://jacurtis.com/notes/astro-draft-posts/)
```

One more thing though – none of this keeps the post page itself from being rendered during a build. It just keeps anything from linking to it or showing it in a list of posts. This means that it will show up in your RSS feed unless you edit your RSS template to also filter it out.

```javascript title="src/pages/rss.xml.js" {12}
import rss from "@astrojs/rss";
import sanitizeHtml from "sanitize-html";
import { rfc2822 } from "../components/utilities/DateFormat";
import { globalImageUrls } from "../components/utilities/StringFormat";
import site from "../data/site.json";

export function GET(context) {
  const postImportResult = import.meta.glob("../content/posts/**/*.md", {
    eager: true,
  });
  const posts = Object.values(postImportResult)
    .filter((post) => post.frontmatter.draft !== true)
    .sort(
      (a, b) =>
        new Date(b.frontmatter.date).valueOf() -
        new Date(a.frontmatter.date).valueOf(),
    );

  return rss({
    title: site.title,
    description: site.description,
    site: context.site,
    xmlns: {
      atom: "http://www.w3.org/2005/Atom/",
      dc: "http://purl.org/dc/elements/1.1/",
      content: "http://purl.org/rss/1.0/modules/content/",
    },
    items: posts.map((post) => ({
      title: post.frontmatter.title,
      link: `${site.url}${post.frontmatter.slug}`,
      pubDate: rfc2822(post.frontmatter.date),
      description: post.frontmatter.description,
      customData: `<summary>${post.frontmatter.description}</summary>`,
      content: globalImageUrls(
        site.url,
        sanitizeHtml(post.compiledContent(), {
          allowedTags: sanitizeHtml.defaults.allowedTags.concat(["img"]),
        }),
      ),
    })),
  });
}
```

That’s it! Hit me up on [Bluesky](https://bsky.app/profile/scottwillsey.com) or [Mastodon](https://social.lol/@scottwillsey) if you have any questions.
