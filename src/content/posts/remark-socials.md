---
title: "Remarking the Socials"
description: How I learned to paste links into my blog and have them magically converted into amazing embeds.
date: "2024-07-04T05:00:00-08:00"
keywords: ["blog", "astro", "markdown","remark"]
series: "Astro"
slug: "remark-socials"
---

## Contents

## Astro Remark Support

One of the cool things about [Astro](https://astro.build) is how it supports Markdown using [remark](https://github.com/remarkjs/remark). This means it also supports remark plugins, and THAT means you can write your own custom remark plugins to modify the markdown in your posts however you like.

Astro’s documentation has [many examples of modifying front matter with remark](https://docs.astro.build/en/guides/content-collections/#modifying-frontmatter-with-remark). Actually modifying things in the markdown content itself is a slightly different matter, but it’s still pretty simple, all things considered. Astro has a recipes and guides section on their Community Educational Comment page (basically links to external articles), and in that recipes and guides section is a section on Markdown, with a link to this example:

[Remove runts from your Markdown with ~15 lines of code · John Eatmon](https://eatmon.co/blog/remove-runts-markdown)

I don’t care about runts because I’m neither a pig farmer nor a person who notices them on my own blog. But I’m glad John cares, because he basically outlined a strategy for looking for and transforming specific things in my blog posts.

## Social Links in Blog Posts

If you read a lot of blogs, you’ll notice that most times you see social media or YouTube videos linked to, they’re basically a fancy little mini-view of the content called an embed – the content is actually embedded into the post rather than just being a link.

Naturally I want that look for any social media or YouTube links I post here, but one constant with me is that I never like to know implementation details to write a post. That includes things like embedding links from YouTube, Mastodon, Threads, or whatever. I want to be able to just paste the link in and have my site handle it for me. There is an astro integration called [Astro Embed](https://astro-embed.netlify.app/) that will worry about this for you, but it doesn’t support Mastodon or Threads links. So I created my own remark plugin that does, primarily because I found it easier than modifying the Astro Embed extension.

Mastodon links are weird compared to other social network links in that they don’t have a known common domain for every link. There are all sorts of Mastodon URLs out there. My profile link, for example, is <https://social.lol/@scottwillsey>. Take that, X. YouTube links are easy, and Threads links are easy. It’s trivial to use regular expressions to find these links, assuming they exist on a line all by themselves, unadorned and glaringly obvious, like a hanging chad desperately waiting to be peered at and analyzed within an inch of its life.[^1]

## Transforming Social Media Links in Astro Markdown files

Step 1 in transforming the social links is creating aforementioned regular expressions and testing them.

### Regular Expressions for YouTube, Threads, and Mastodon Links

If you have a Mac and you do any scripting or text file management or log analysis, I highly suggest [BBEdit](https://www.barebones.com/products/bbedit/index.html) from Bare Bones Software. It’s not cheap, it’s

[^1]: Remember when [hanging chads](https://www.history.com/news/2000-election-bush-gore-votes-supreme-court) were the biggest of our political problems? It can definitely be argued, however, that there’s a direct line from those hanging chads to where we are today with people storming the capitol to protest a “stolen election”.
