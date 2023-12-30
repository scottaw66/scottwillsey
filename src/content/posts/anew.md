---
title: Anew
description: My website has begun anew, and here's why.
date: "2022-08-21T09:00:00-07:00"
keywords: ["blog", "hugo", "eleventy", "javascript", "astro"]
slug: "anew"
---

The last time I posted to my site was on February 24th. That's 6 months between posts.

Far from being dead, the site was just undergoing a metamorphosis that was invisible to you. And to me, very honestly. I've been working on other projects, like [Friends with Beer](https://friendswithbeer.com) and [Siracusa Says](https://siracusasays.com), so this site was pushed to the back of the queue for its inevitable and much needed refactoring.

When I built this site, I was new to modern static site generators. I used [Hugo](https://gohugo.io), which was super popular at the time (and maybe still is) because of its performance and because the web store was one of two wildly divergent camps: single-page web applications, built in React or similar, and completely static sites with little to no interactivity. Hugo is great for fully static websites because it's FAST and because it's a very well thought out framework with many of the features people want included by default. But it uses the horrific Go templating language which was apparently created by [Yoda](https://lingojam.com/EnglishtoYoda) and which broke my brain every time I tried to make an even semi-complicated query or logic statement.

Even worse than Go templating language when I built this site with Hugo was my understanding of how to structure it. I didn't fully grasp how Hugo built pages and directories based on template names and types, and so I came up with a very convoluted scheme in which all of my different categories had their own folders. Not great. And I should never have had so many categories to begin with, which was another failure of my imagination. The end result was a site that was way too complicated for a guy who just wanted to babble about things most people will never read.

I thought I'd build the next iteration with [Eleventy](https://www.11ty.dev). It's what I used for [Friends with Beer](https://friendswithbeer.com), and I learned a lot from that. The beauty of Eleventy is that it's [Node.js](https://nodejs.dev/en/) based and allows for templates and layouts that use good old Javascript instead of terrible templating languages, although I primarily used Nunjucks for the templating, because that's what a lot of the best examples I could find at the time used. Also, since you can just import modules that you or other people write, I was able to just write a lot of straight code in modules and use those in my layouts.

But then as I was getting my head wrapped around THAT mode of working, along came a new framework: [Astro](https://astro.build). On the surface, Astro is a lot like Eleventy. It's Node.js based, it allows for a lot of Javascript (actually its default is Typescript) modules, and it has a great static site story. But it's more than just that, and there are a list of things that make it more attactive to me than Eleventy:

- It doesn't use templating languages. It used HTML and Javascript and Components.
- It was built to allow for flexibility in terms of interactivity. Zero Javascript to the client by default, but an [Islands Architecture](https://jasonformat.com/islands-architecture/) approach allows adding what you need as you need it. An example is my [search page](/search), powered a [Solidjs](https://www.solidjs.com) component that executes everything on the client in Javascript.
- It has an [SSR](https://medium.com/kongcepts-hq/server-side-rendering-bc6a979b3a7c) story as well, and you can deploy it to several different platforms including hosting your own with a [Node adapter](https://docs.astro.build/en/guides/integrations-guide/node/).
- Finally, it's just very easy to build with. It's more reminiscient of the old days of Asp.NET or PHP but with modern frameworks and platform functionality. It's user friendly for both programmers and site visitors, and it remembers what the web actually is and works with those strengths instead of pretending the web is something it's not.

Astro had a very tumultous beta period, but the developers were purposefully working towards getting a stable 1.0 that could be used and built upon, and I think they've succeeded. There are some weirdnesses and omissions that most of us who've used other frameworks notice immediately, but mostly there aren't, and mostly it's just very easy and fun to work with. Just as importantly, the team and community behind it is overwhelmingly positive.

This site runs on Astro. It makes use of things like [@astrojs/image](https://www.npmjs.com/package/@astrojs/image), [@astrojs/mdx](https://www.npmjs.com/package/@astrojs/mdx), [@astrojs/rss](https://www.npmjs.com/package/@astrojs/rss), [data-icon](https://www.npmjs.com/package/astro-icon), [SolidJs](https://www.solidjs.com), and a few other tools, as well as the standard use of layouts and components that are the backbone of building an Astro site.

I will absolutely write about Astro and some of the things I've had to learn on this site. As always, I'm not a professional programmer and I'm certainly not the quickest or smartest. I do it because I enjoy it, and I think that's ok. More people should feel good about doing things they enjoy but probably wouldn't be considered authorities on. Life will be better if we get back to allowing each other that more often again.

There's also the matter of my ever-evolving computer platform approach, and I have made some decisions in that regard lately. I can't wait to get started on them, but that will take some money I don't have just yet, and it will be something I write about quite a lot.

For now... let's begin anew, friend.
