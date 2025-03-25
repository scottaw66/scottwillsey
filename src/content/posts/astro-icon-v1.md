---
title: "Astro Icon 1.x Upgrade"
description: "Upgrading to Astro Icon 1.x from older versions."
date: "2024-01-14T05:00:00-08:00"
keywords: ["blog", "astro", "component"]
cover: "../../assets/images/covers/AstroHeader.png"
coverAlt: "Astro"
series: "Astro"
slug: "astro-icon-v1"
---

If you started using Nate More’s [Astro Icon](https://www.astroicon.dev) with Astro early on and are using a version lower than 1.0, you will be in for a surprise when you upgrade to the latest version of Astro Icon and suddenly find a lot of breaking errors related to it.

Migrating from 0.x to 1.x is simple but can be a little tedious depending on how many icons you’re using. A couple key things to understand are that you have to import packages for each icon set that you use now, and that this is now an Astro integration. Don’t worry if you’re not sure how that affects you. You’ll handle adjusting to those changes in the upgrade steps below.

By the way, Nate has a great upgrade guide already at [Upgrade to Astro Icon v1 | Astro Icon](https://www.astroicon.dev/guides/upgrade/v1/). I just thought I’d write about it too, since I’ve done this on a couple different sites now and I still have a couple to go.

## Contents

## Upgrading to Astro Icon 1.x from 0.x

1. Upgrade to the latest version packages of astro and astro-icon (astro-icon >= 1.0)
2. Import and integrate astro-icon in your astro.config.mjs
3. Install @iconify-json/icon-family for every icon package you use
4. On every page you import astro-icons, change `import { Icon } from "astro-icon";` to `import { Icon } from "astro-icon/components";`
5. Find and replace [astro-icon] tags with [data-icon] in your css
6. Find and replace any CSS width or height properties on [data-icon] entries and replace with font-size
7. Now go through every single instance of [data-icon] in your CSS and tweak the font-size that you just added.

## 1. Upgrade to the latest Astro and Astro Icon versions

```bash {10}
scott@Songoku:friendswithbrews astro-icon ✗ 4h31m △ ⍉ ➜
ncu
Checking /Users/scott/Sites/friendswithbrews/package.json
[====================] 21/21 100%

 @astrojs/rss            ^4.0.1  →   ^4.0.2
 @astrojs/sitemap        ^3.0.3  →   ^3.0.4
 astro                   ^4.0.7  →   ^4.1.2
 astro-eslint-parser    ^0.16.0  →  ^0.16.1
 astro-icon              ^0.8.2  →   ^1.0.2
 astro-pagefind          ^1.3.0  →   ^1.4.0
 date-fns                ^3.0.6  →   ^3.2.0
 prettier                ^3.1.1  →   ^3.2.2
 prettier-plugin-astro  ^0.12.2  →  ^0.12.3
 sharp                  ^0.33.1  →  ^0.33.2

Run ncu -u to upgrade package.json
```

I use [npm-check-updates](https://www.npmjs.com/package/npm-check-updates) to update npm packages, but you can do it the standard way.  The key thing to note is that in this instance I’m upgrading from astro-icon 0.8.2 to 1.0.2.

## 2. Import and integrate astro-icon in your astro.config.mjs

No explanation needed here – import astro-icon and add to the list of integrations.

```js title="astro.config.mjs" {2, 9}

import { defineConfig } from "astro/config";
import icon from "astro-icon";
import pagefind from "astro-pagefind";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://friendswithbeer.com/",
  integrations: [ icon(), pagefind(), sitemap(),],
});

```

## 3. Install @iconify-json/icon-family for every icon package you use

This one requires you to scour through every place you specify an icon package name. Search for `[astro-icon` in your project and look for instances of things like `<Icon name="simple-icons:mastodon" />` or CSS instances like `[astro-icon="bi:hand-thumbs-up-fill"]` and take note of the package names (in these examples, **simple-icons** and **bi**).

Now install these by installing `@iconify-json/package-name` for each. E.g,

```bash

npm install @iconify-json/simple-icons @iconify-json/bi
```

That will install the two packages in my example above.

## 4. Change your astro-icon import statements on Astro pages

The old way to import astro-icons in your .astro files is

```astro
import { Icon } from "astro-icon";
```

Change all instances of this in your astro files to

```astro
import { Icon } from "astro-icon/components";
```

## 5. Change all references to [astro-icon] in your CSS to [data-icon]

Another search and replace activity – `[astro-icon]` references have been replaced with `[data-icon]` references.

Old:

```astro {2}
<style>
  [astro-icon="simple-icons:mastodon"] {
    color: var(--color-five);
    width: 2.2rem;
  }
</style>
```

New:

```astro {2}
<style>
  [data-icon="simple-icons:mastodon"] {
    color: var(--color-five);
    font-size: 2.2rem;
  }
</style>
```

## 6. Use font-size instead of width or height to set the icon sizes

You may have noticed in the previous section that I not only changed `[astro-icon]` to `[data-icon]` in my CSS reference to it, but I also removed the `width` property and replaced it with a `font-size` property instead.

After performing the first 5 steps, you’ll see wildly sized icons all over the place until you do this.

## 7. Tweak font-size on all CSS for your icons

Step 6 will get you in the ballpark, but you’ll now find that some of your sizes, while closer, are still off. Just play with font-size values until you get what you like. CSS specificity is key here – be specific about which icons you’re setting your CSS for and use scoped CSS by putting them in `<style>` tags in specific astro pages.

The first example below affects all icons, the second one affects the `bi:hand-thumbs-up-fill` icon specifically.

```astro {1}
[data-icon] {
 font-size: 1em;
}
```

```astro {1}
[data-icon="bi:hand-thumbs-up-fill"] {
 margin-bottom: 0.1rem;
}
```

## Summarium

That’s pretty much it. Once change you will notice when running the dev server is that the first time you try to load the site in the browser, Astro Icon has to load all the icon sets and it takes a little bit. Don’t worry. It will work. 🙂
