---
title: "Astro-Pagefind"
description: "Pagefind is a great find for static site search (thanks to Bryce Wray for that line) and Astro-Pagefind integrates it beautifully into Astro."
date: "2023-06-12T09:00:00-08:00"
keywords: ["search", "pagefind", "astro", "hugo", "eleventy"]
series: "Astro"
slug: "astro-pagefind"
---
I thought I'd talked about [Pagefind](https://pagefind.app) and [Astro-Pagefind](https://github.com/shishkin/astro-pagefind) here before, but [my very own site search](https://scottwillsey.com/search/) which itself is built using Astro-Pagefind says otherwise.

[Pagefind](https://pagefind.app) is a static search library that you install locally to your project, that runs and builds its index locally after your static site is compiled, and that provides both a JavaScript search tool and an HTML UI. It's also [open source and free to download and use](https://cloudcannon.com/blog/introducing-pagefind/) on your site.

You can [watch Liam Bigelow of CloudCannon presenting how Pagefind works](https://www.youtube.com/watch?v=74lsEXqRQys) and how it's scaleable on YouTube in his video from HugoConf 2022. That name "HugoConf" may give you pause if you don't use [Hugo](https://gohugo.io) as your static site generator (I don't – I use [Astro](https://astro.build)), but it's actually a hint to the fact that Pagefind is completely static platform agnostic and will work regardless of you static site builder.

I recommend you watch the video and see for yourself how lean Pagefind runs and then marvel over the fact that it's free and ready to use on your static site. In the words of [Bryce Wray](https://www.brycewray.com), [Pagefind is quite a find for site search](https://www.brycewray.com/posts/2022/07/pagefind-quite-find-site-search/). Bryce also has a really good article on integrating Pagefind called [Sweeter searches with Pagefind](https://www.brycewray.com/posts/2022/12/sweeter-searches-pagefind/).

Initially when I started using Pagefind on my websites, I used it as per the Pagefind docs. In terms of adding Pagefind search to a page, you drop in the following to your HTML template:

```html
<link href="/_pagefind/pagefind-ui.css" rel="stylesheet">
<script src="/_pagefind/pagefind-ui.js" type="text/javascript"></script>
<div id="search"></div> 
<script> 
 window.addEventListener('DOMContentLoaded', (event) => { 
  new PagefindUI({ element: "#search" }); 
 }); 
</script>
```

That actually works quite well as is, but there's even better news for you if you use [Astro](https://astro.build) to build your static sites: [Sergey Shishkin's Astro-Pagefind](https://github.com/shishkin/astro-pagefind) Astro integration.

Astro-Pagefind lets you make life easy for yourself when adding Pagefind to your astro site by integrating it so that you can drop it into your Astro templates as a component.

```astro
---
import Search from "astro-pagefind/components/Search";
---
<Search />
```

It really is that easy. Here's the entirety of my search page Astro template, and it's almost completely CSS to make the Pagefind UI look how I want:

```astro title="src/pages/search.astro"
---
import config from "config";
import Search from "astro-pagefind/components/Search";
import Base from "../layouts/Base.astro";

const title = "Search " + config.get("title");
---

<Base title={title} description={title}>
<h1>Search</h1>

<Search id="search" className="pagefind-ui" />
</Base>

<style is:global>
:root {
 --pagefind-ui-scale: 0.8;
 --pagefind-ui-primary: var(--menu-surface);
 --pagefind-ui-text: #fff;
 --pagefind-ui-message-text: #000;
 --pagefind-ui-result-title-text: var(--brand);
 --pagefind-ui-result-text: #000;
 --pagefind-ui-background: var(--surface1)
 --pagefind-input-background: var(--brand);
 --pagefind-ui-border: var(--accent1);
 --pagefind-ui-tag: #0d0a01;
 --pagefind-ui-border-width: 2px;
 --pagefind-ui-border-radius: 8px;
 --pagefind-ui-image-border-radius: 8px;
 --pagefind-ui-image-box-ratio: 3 / 2;
 --pagefind-ui-font: sans-serif;
 --pagefind-button-background: var(--pagefind-input-background);
 --pagefind-button-color: var(--pagefind-ui-message-text);
}
[data-theme="light"] {
 --pagefind-ui-primary: var(--menu-surface);
 --pagefind-ui-text: #fff;
 --pagefind-ui-message-text: #000;
 --pagefind-ui-result-title-text: var(--brand);
 --pagefind-ui-result-text: #000;
 --pagefind-ui-background: var(--surface1);
 --pagefind-input-background: var(--brand);
 --pagefind-ui-border: var(--accent1);
 --pagefind-ui-tag: #0d0a01;
 --pagefind-button-color: var(--pagefind-ui-text);
 }
[data-theme="dark"] {
 --pagefind-ui-primary: var(--menu-surface);
 --pagefind-ui-text: #fff;
 --pagefind-ui-message-text: var(--pagefind-ui-text);
 --pagefind-ui-result-title-text: var(--accent1);
 --pagefind-ui-result-text: #fff;
 --pagefind-ui-background: #83645a;
 --pagefind-input-background: var(--brand);
 --pagefind-ui-border: var(--brand);
 --pagefind-ui-tag: #b59c94;
 }
#search .pagefind-ui__search-input, #search .pagefind-ui__search-clear {
 background-color: var(--pagefind-input-background);
 color: var(--pagefind-ui-text);
 }
#search .pagefind-ui__result-title, #search .pagefind-ui__result-link {
 display: inline-block;
 font-weight: 700;
 font-size: calc(40px * var(--pagefind-ui-scale));
 color: var(--pagefind-ui-result-title-text);
 }
#search .pagefind-ui__result-excerpt {
 color: var(--pagefind-ui-result-text);
 font-weight: 400;
 font-size: calc(1.5rem * var(--pagefind-ui-scale));
 }
#search .pagefind-ui__message {
 color: var(--pagefind-ui-message-text);
 margin: calc(0.5rem * var(--pagefind-ui-scale)) 0 calc(1.5rem * var(--pagefind-ui-scale)) calc(0.5rem * var(--pagefind-ui-scale));
 }
#search .pagefind-ui__button {
 color: var(--pagefind-button-color);
 background: var(--pagefind-button-background);
 }
#search .pagefind-ui__result-thumb {
 display: none;
 }
</style>
```

As I said, almost all CSS. Everything in the `<style></style>` block overrides Pagefind's default UI appearance. Basically I just used Chrome's inspector tools to look at different elements and figure out which ones applied to me and needed to be overwritten (as well as seeing what the names of the elements were as written to the page).

A nice quality of life enhancement using Astro-Pagefind over directly integrating Pagefind is that your build scripts don't have to include anything about Pagefind at all. Astro-Pagefind takes care of that for you. Before Astro-Pagefind, I had to make sure to include Pagefind commands in my build scripts.

Site build script when using direct Pagefind integration:

```javascript title="package.json"

"scripts" : {
    "build" : "export NODE_ENV=production && astro build && minify public/styles/pagefind-ui.css > public/styles/pagefind-ui.min.css && ./pagefind --source dist && cp -r dist/_pagefind/ public/_pagefind",
    "dev" : "export NODE_ENV=development && astro dev",
    "preview" : "astro preview",
    "start" : "npm run dev",
  }

```

Site build script when using Astro-Pagefind:

```javascript title="package.json"

"scripts" : {
    "build" : "export NODE_ENV=production && astro build",
    "dev" : "export NODE_ENV=development && astro dev",
    "preview" : "astro preview",
    "start" : "npm run dev",
  }

```

To be fair to Pagefind, I think the build script could actually be slightly simpler. I think the reason I'm copying the output to `public/_pagefind` is because I was trying to trick Pagefind into working in dev mode before I discovered Astro-Pagefind.

The BEST part about using Astro-Pagefind instead of just integrating Pagefind the original way though is the ability to have search work even when running in Astro dev server mode (ie, while working on the site). Normally in order to see search working and see what effect your CSS or other changes have had on your Pagefind integration, you'd have to recompile and run a preview server with every change. With Astro-Pagefind, you just run in dev mode as you'd normally do when working on your site, and any changes you make that affect your Pagefind UI appearance will be available instantaneously when you make them.

The trick Astro-Pagefind uses to do this is to use your last compiled site in your dist folder (or whatever you call yours) and pulls the already-built Pagefind index from there. It's super slick and it's really changed how I work whenever I am adding search to an Astro site.

Considering Pagefind's speed, scalability, and ease of integration, I don't know of any better options for static site search. And if you're using Astro, install Astro-Pagefind to your project and be amazed at how something that once was a big downside to static site builds is now an advantage.

Give [Astro-Pagefind](https://github.com/shishkin/astro-pagefind) a try, or download [Pagefind](https://pagefind.app) directly if you're not on Astro.
