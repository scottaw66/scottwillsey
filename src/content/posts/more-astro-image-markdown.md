---
title: "More on Astro, Image Optimization, and Markdown"
description: A continuing journey to get image optimization for markdown files with Astro.
date: "2023-01-07T05:00:00-08:00"
keywords: ["blog", "rss", "astro", "podcast", "images"]
series: "Astro"
slug: "more-astro-image-markdown"
---

I've talked a lot about image optimization and RSS feed handling with [Astro](https://astro.build/). I'm about to talk about it some more. I presume you're like me and obsess endlessly about these topics, so you should enjoy this.[^1] In my case, I don't know how much of it is enjoyment and how much of it is a compulsive search for a better way.

Now that Astro has support for full post content RSS feeds with the [compiledContent property for markdown content](https://docs.astro.build/en/guides/rss/#including-full-post-content), I modified [Friends with Brews](https://friendswithbrews.com) to use standard markdown files (.md) instead of [MDX](https://mdxjs.com) (.mdx). My reasoning was that, since I almost never include images in the show notes for Friends with Brews and since using standard markdown would let me use compiledContent to put full episode show notes in the podcast RSS feed, it was an automatic must-do.

Unfortunately for me, the second I made the switch, I needed to add an image to the show notes of an upcoming episode, which would make it the second time I've had to add an image to FwB show notes. The first time was back on episode 8, [Satan is not normally depicted as being purple](https://friendswithbrews.com/8/), and that was the critical piece of visual information known as the Chonk Chart.

If I have to do anything more than once, it means I will have to do it several times, and that means I have to support it properly. And that means being able to combine image optimization AND standard markdown in Astro, and that's not currently possible - the [Astro Image components are only supported in Astro and MDX files](https://docs.astro.build/en/guides/images/#astros-image-integration), for the obvious reason that they're components, and markdown can't execute components.

I can continue to process the usual images of episode brews (coffee, beer, tea) with Astro image in my layout templates, as well as all the other images used on the site, so that's not a problem. Those brew images are not actually in the show notes. Instead, I have a JSON file of brews that contains a bunch of information about them, including which episode(s) they're associated with. So I only have to concern myself with how to optimize the inline images in the show notes markdown files.

The good news is that manually writing Picture elements complete with sources and srcsets and default images is simple. And if it's simple for a human, it's simple for a script. I can easily assume a certain standard width for images I'm going to put in my show notes, and then generate optimized images for that size plus 2x and 3x resolutions, as well as the original for linking to. Then the html for the Picture element associated with the optimized images can be generated fairly simply. Ben Holmes, who now works for Astro, [has a post about this approach using eleventy-image](https://bholmes.dev/blog/picture-perfect-image-optimization/). Because [eleventy-image](https://www.11ty.dev/docs/plugins/image/) can be manipulated directly in JavaScript, it's a great candidate for this.

So here's the plan:

- Continue to optimize permanent site images and episode brew images using the Astro Image components in my Astro layout files,
- Use [eleventy-image](https://www.11ty.dev/docs/plugins/image/) to optimize inline show notes images to predetermined widths and image formats,
- Figure out how to insert the associated Picture elements for the optimized images into my markdown files. This step might take the most work.

If you noticed that the last step of the plan looks a bit like the Far Side cartoon with scientists drawing out a diagram of the creation of the universe with a "and then a miracle occurs" note tagged onto the end, it's true. The good news is, there are several places in my writing and publishing workflow I can inject the html. I'll write more about that as I start implementing a system.

[^1]: If you aren't endlessly obsessed with these topics, we need to talk about that.
