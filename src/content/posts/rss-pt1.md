---
title: RSS, Astro, and Me – Part 1
description: Astro makes some things incredibly simple, and other things not nearly so.
date: "2022-09-06T14:00:00-08:00"
keywords: ["blog", "javascript", "astro", "rss"]
series: "Astro"
slug: "rss-pt1"
---

The first [Astro](https://astro.build) site I put on the web was [Siracusa Says](https://siracusasays.com), which went live on August 7th. The second Astro site was this site, on August 21st. If you think about how bare bones this site is, and that there's a 3 week gap there, you might be tempted to think that Astro doesn't allow for particularly quick development. The truth is, it _does_, but I also have a day job that was more demanding than normal during that time. In fact, this site was super simple to build. The thing that took me the longest was figuring out a look that I would only have to be 90% ashamed of.

I'm not a designer.

But it's not all unicorns and fluffy kitties with Astro. Astro is a very new framework and it's very much a work in progress. One of the late design decisions taken by the development team before Astro 1.0 was released was to stop developing customized markdown with component support, and make markdown just markdown, and use [MDX](https://mdxjs.com) for markdown with component support.

MDX is an interesting animal. If you create an MDX file, the MDX spec will give you access to parts of that file in different ways. For example, the body of the document (in other words, the actual content) is exposed as a component. It's an object. And being able to access that object depends on whatever framework you're using supporting MDX and providing that access for you.

Astro does provide this ability to access MDX content as an object. Let's say you grab all your site's posts, which happen to be mdx files, using [Astro.glob](https://docs.astro.build/en/reference/api-reference/#astroglob), like this:

```javascript
let allPosts = await Astro.glob("../content/*.mdx");
allPosts = allPosts.sort(
  (a, b) =>
    new Date(b.frontmatter.date).valueOf() -
    new Date(a.frontmatter.date).valueOf(),
);
```

You now have an array of posts in the variable allPosts. You can use JavaScript's [map function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) to deal with them individually, like this:

```javascript
{
  allPosts.map((mdxpost) => {
    return (
      <Post content={mdxpost}>
        <mdxpost.Content />
      </Post>
    );
  });
}
```

Without worrying too much about the rest of the details here, just understand that `<mdxpost.Content />` is a component object that exposes the content from one post. The map contains all the posts, and each mapped mdxpost has a .Content component that holds the content.

If it makes your head hurt and you find it weird, you're not alone. I guess people coming from JavaScript frameworks like React might be used to things like this - I'm not really sure because I don't know anything about React. At any rate, this type of JavaScript component is not an unknown thing, it's just new to me.

Now that you have some of the backstory on how MDX works, let me just say that it created a bit of a problem for me with respect to my RSS feed. The reason for this is that Astro components output HTML. Only HMTL. They can't output JSON or XML or anything other than HTML. This means the [@astrojs/rss package](https://www.npmjs.com/package/@astrojs/rss) that provides RSS support to Astro doesn't _use_ Astro components to create the RSS file, it uses JavaScript (most likely [TypeScript](https://www.typescriptlang.org)). It therefore does not support the MDX file Content component object, and it therefore means that creating an RSS feed that Astro way limits me to a summary type feed, without full body content for each item in the feed.

Here's my rss.xml.js for the Siracusa Says RSS feed as an example:

```javascript title="rss.xml.js"
export const get = () =>
  rss({
    stylesheet: "/rss/styles.xsl",
    title: config.get("title"),
    description: config.get("description"),
    site: config.get("url"),
    items: Array.from(episodes)
      .reverse()
      .map((episode) => ({
        title: episode.frontmatter.title,
        link: new URL(
          path.join(config.get("episodes.path"), episode.frontmatter.slug),
          config.get("url"),
        ),
        pubDate: rfc2822(episode.frontmatter.pubDate),
        description: episode.frontmatter.description,
        customData: `<enclosure url="${config.get("episodes.audioPrefix")}/${
          episode.frontmatter.audiofile
        }" length="${episode.frontmatter.bytes}" type="audio/mpeg" />`,
      })),
  });
```

Initially I thought I could use the customData property of the rss package to stuff my MDX file content into, but there is literally no way to get add the .Content component in a way that this JavaScript understands. The best I can do is see the function that returns it or see [object Object]. Not very useful.

To summarize all the above: using MDX as my post content files and @astrojs/rss to support rss feed creation in Astro resulted in my only being able to provide truncated RSS feed items. In order to solve this, I would have to take the advice of Astro Discord member Chris-Adiante and use an Astro component to render the RSS, allowing access to each posts .Content component, and then writing the rss to the filesystem as an rss.xml file.

That's exactly what I did. I'll show you how in [Part 2](/rss-pt2).
