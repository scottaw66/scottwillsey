---
title: "Astro Remark Eleventy Image"
description: "Christian Ohanaja's Astro Remark Eleventy Image plugin."
date: "2023-02-07T05:00:00-07:00"
keywords: ["blog", "images", "responsive", "astro"]
series: "Responsive Images"
slug: "astro-remark-eleventy-image"
---

So there I was, playing with [eleventy-img](https://www.11ty.dev/docs/plugins/image/) to find a way to [generate responsive images for image links in markdown files](https://scottwillsey.com/episode-image-script/), when [Christian Ohanaja](https://cjohanaja.com) did the work for me and created the [Astro Remark Eleventy Image](https://github.com/ChrisOh431/astro-remark-eleventy-image) plugin.

I'm glad he did too, because looking at the remark part of the code, I feel confusion more than anything. I guess I have another rabbit hole to pop down to learn about THAT.

Anyway, being the true jerk that I am, instead of just being grateful and using his plugin, I forked it to add some additional options (such as the ability for the inline image to link to the high resolution version) and to add an Astro component for image optimization. That way I can have one plugin that provides image optimization in both markdown files and inside Astro components.

I'm assuming that I can technically combine a plugin and an Astro component in one project. I actually have no idea, but I'll find out.
