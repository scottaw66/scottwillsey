---
title: RSS, Astro, and Me – Part 2
description: The details of my custom RSS feed.
date: "2022-09-12T05:00:00-07:00"
keywords: ["blog", "javascript", "astro", "rss"]
series: "Astro"
slug: "rss-pt2"
---
As I mentioned in [Part 1](rss-pt1) of this installment, while trying to modify my site RSS feed to contain the full body of each post in my feed items, I ran into an inconvenient truth about how [MDX](https://mdxjs.com) exposes its file content as a component and how I could not use that component outside of an [Astro](https://astro.build) component. JavaScript just doesn't know what it is. Support for the MDX Content component has to be built into whatever framework you're using.

Astro, of course, is built to use MDX and take full advantage of the MDX Content component, so [Astro Discord](https://astro.build/chat) member Chris Adiante proposed I simply use an Astro component to create the RSS (with full access to the MDX content) and then have it write the rss file to the file system. Since my site is Astro SSG (fully static, only changing when I rebuild the site) and not [Astro SSR](https://docs.astro.build/en/guides/server-side-rendering/) (server-rendered on demand), I can use this technique without any problems.[^1]

By the way, Chris is the creator of the really amazing looking [Astro M²DX remark plugins](https://astro-m2dx.netlify.app). If you're using MDX with Astro, you should definitely give these a look!

## The Strategy

In order to write an RSS feed using an Astro component, the Astro component has to get called – or to put it another way, it has to be used in a page. It can't just sit in a folder in src. Also, it should be called once and once only. It can't be put inside a layout file used by multiple pages because I want it written just once during the build. And finally, it has to have no effect on the rendering of the page that it's in. Its purpose is to generate the RSS for all site posts and then write that RSS to a file called rss.xml. It has nothing that should be displayed, and it cannot alter the output of the page that hosts it.

To meet these requirements, I decided to use this Astro component in index.astro, the Astro page that gets built into index.html.

## The Components

I use two components to create my RSS file, in the manner suggested by Chris Adiante: WriteFile.astro and RssXml.astro. RssXml.astro generates the RSS and WriteFile takes its output and dumps it to disk in the form a file called rss.xml.

### RssXml.astro

The way RssXml.astro works is dictated by the fact that in order to render, it needs to directly output some html tags outside a javascript loop. This is because Astro components write html. It's how they work.

The fact that Astro components write html should not be overlooked because it can also mess with the actual RSS XML generated, a truth that caused me much grief until I learned about [Fragments](https://docs.astro.build/en/core-concepts/astro-components/#fragments—multiple-elements) and [set:html](https://docs.astro.build/en/reference/directives-reference/#sethtml). Using them in the combination `<Fragment set:html="" />` outputs RSS XML that isn't messed with by Astro trying to ruin the format of XML link elements, for example.

```astro title="src/components/RssXml.astro"

---
import config from "config";
import path from 'path';
import { rfc2822 } from "../components/utilities/DateFormat.js";

const { allPosts } = Astro.props;
const rssHeaderXml = `<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="/rss/styles.xsl" type="text/xsl"?>
<rss version="2.0">
  <channel>
    <title>${config.get("title")}</title>
    <description><![CDATA[ ${config.get("description")} ]]></description>
    <link>${config.get("url")}</link>`;

const rssFooterXml = `  </channel>
  </rss>
  `;
---
<Fragment set:html={rssHeaderXml} />
{allPosts.map(post =>
  <Fragment set:html={`
    <item>
      <title>${post.frontmatter.title}</title>
      <link>${new URL(
        path.join("/", path.basename(post.file, path.extname(post.file))),
        config.get("url")
      )}</link>
      <guid>${new URL(
        path.join("/", path.basename(post.file, path.extname(post.file))),
        config.get("url")
      )}</guid>
      <description><![CDATA[ ${post.frontmatter.description}]]></description>
      <pubDate>${rfc2822(post.frontmatter.date)}</pubDate>
      <content:encoded><![CDATA[`} />
      <post.Content/>
    <Fragment set:html={`]]></content:encoded>
    </item>`} />)}
<Fragment set:html={rssFooterXml} />

```

This is not a complex component. All it has to do is generate and output XML. It doesn't even have to get the posts to include, because those are passed in as a prop.

Some points of note:

- I create a constant for the top of the RSS file above the items which holds all the channel tags, and a constant for the end of the file after the items (which is just the closing channel and RSS tags).
- Secondly, the items are created in a JavaScript .map function which takes the array of posts and maps each item to create HTML fragments for them. It's all very straightforward if you've looked at an RSS feed before.
- The most interesting detail to note by far, and indeed the whole reason behind this custom RSS approach, is the `<post.Content/>` component inside the .map function. For each post being mapped, I have a `<Fragment/>` wrapping everything before the post.Content object, then I end it, reference the post.Content object, and then create another Fragment object to wrap up the item XML.

**It's important to understand that `<post.Content/>` is being accessed directly inside the Rss.Xml Astro component, it's not inside a JavaScript string or any other wrapper.**

It has to be directly written in Astro as a direct Astro component item, or it will be meaningless. It's Astro that understands what to do with this Content component, not JavaScript or any other framework.

### WriteFile.astro

If you're hoping for a giant code listing that requires lots of explanation, WriteFile.astro will make you sad. It's ridiculously simple:

```astro title="src/components/WriteFile.astro"

---
import fs from "node:fs/promises";

export interface Props {
  fileUrl: URL;
}
const { fileUrl } = Astro.props;

if (Astro.slots.has("rss-writer")) {
  const html = await Astro.slots.render("rss-writer");
  await fs.writeFile(fileUrl, html);
}
---


```

It's 100% frontmatter. There is no output.  If this has you thinking "but you just told me you have to have output in an Astro component", that's only true for Astro components that have to output any text. This component does not have to, it takes the text generated by RssXml.astro and writes it to disk. I understand completely if that explanation doesn't clarify things much, but if you start playing with Astro components or pages, you'll find out what happens when you don't write html tags or include other Astro components in the base output.[^2]

The important point with this one is waiting for that slot to render before performing fs.writeFile. I never would have known to do this, or especially how to do this. This was all Chris Adiante. The reason it's necessary to do this is because the page needs to be written up to that point for the RssXml.astro component to do its thing and have something for WriteFile.astro to actually write to disk.

The one thing I did differently to his suggestion is to not look and wait for default slot. Using default slot meant everything before RssXml.astro's output also got written into the file. Not what I want. As a result, I created a [named slot](https://docs.astro.build/en/core-concepts/astro-components/#named-slots) in my Base.astro layout template (which index.astro uses) and then target both WriteFile.astro and RssXml.astro to this slot inside of index.astro.

### index.astro content section

This is just the content section of index.astro without any frontmatter, just to show you how I incorporated my WriteFile and RssXml Astro components so that they do their thing when the index page is built.

```astro title="src/pages/index.astro"

<Base title={title} , description={description}>
  <section aria-label="Blog post list">
    {
      indexPosts.map((mdxpost) => {
        return (
          <Post content={mdxpost}>
            <mdxpost.Content />
          </Post>
        );
      })
    }

    <nav id="pager">
      {
        allPosts.length > pageSize ? (
          <div>
            <a href="/2">Older Posts</a>
          </div>
        ) : null
      }
    </nav>
  </section>

  <WriteFile fileUrl={rssFileUrl} slot="rss-writer">
    <RssXml allPosts={allPosts} slot="rss-writer" />
  </WriteFile>
</Base>


```

The above is everything in index.astro except the frontmatter section. The part that writes the RSS file is at the bottom. One thing about named slots that tripped me up is that both components have to name the slot to use explicitly, not just the outer component. Anything you want to wind up in a named slot needs to name that slot.

### Base.astro

The final piece of the puzzle is just the named slot at the bottom of Base.astro, my layout template used by index.astro and all my other pages.

```astro title="src/layouts/Base.astro"

---
import Header from "../components/Header.astro";
import Footer from "../components/Footer.astro";
import "../styles/sw2.css";

export interface Props {
  title: string;
  description: string;
  url: string;
}

const { title, description } = Astro.props;
---

<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="title" content={title} />
    <meta name="description" content={description} />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <link
      rel="preload"
      href="/fonts/BlinkMacSystemFont-Medium.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
  </head>
  <body>
    <Header />
    <main>
      <slot />
    </main>
    <Footer />
    <script is:inline src="/scripts/barefoot.min.js"></script>
    <script is:inline>
      lf = new BareFoot();
      lf.init();
    </script>
  </body>
  <slot name="rss-writer" />

</html>

```

See that innocent looking slot down at almost the very bottom named "rss-writer"? That's the named slot that allows index.astro to render the WriteFile and RssXml astro components. You might also notice the default `<slot/>`in between the html `<main>` tags. That's where all the content generated by any page that uses Base.astro as its layout gets rendered.

## TLDR; and Summary

There's a lot to digest here. The key takeaways are:

- Accessing MDX content is done through a Content component, which Astro understands, but JavaScript does not.
- As a result, trying to access that content for a full-item-body RSS feed requires using Astro components to generate the feed.
- Astro components only write HTML, not XML or an RSS feed file. Using Astro components to generate XML therefore means writing that to disk yourself.
- This only works in SSG environments. You would not want to use this with an SSR site because it would write rss.xml over and over again. If I were going to use this on an SSR site, I'd want a page with Astro components that isn't public facing, which would get called by a node script executed by a cron job or whenever a post is added to the site.

As always, I'm not a brilliant programmer and I'm sure there are better ways of doing everything I did. I also would never have figured out the syntax and layout requirements for this without the help of Chris in the Astro Discord.

[^1]: Astro currently forces a choice between a fully static site (SSG) or a server-rendered site (SSR). Future support for SSG with SSR routes as needed is on the roadmap (I think).
[^2]: Hint: Nothing. Nothing is what happens.
