---
title: "Astro 5 Upgrade"
description: "Astro 5 is out with a number of changes from Astro 4. The good news is I was able to upgrade instantly with no modifications (but there are some to come later)."
date: "2024-12-10T01:00:00-08:00"
keywords: ["blog", "astro", "programming"]
series: "Astro"
slug: "astro5"
---
[Astro 5](https://astro.build/blog/astro-5/) is out, and it has a number of changes from Astro 4. The good news is, I was able to upgrade this site to it without making any changes at all. That doesn’t mean I don’t have any to make – I need to [convert my Content Collections](https://docs.astro.build/en/guides/upgrade-to/v5/#updating-existing-collections) to the new [Content Layer API](https://astro.build/blog/content-layer-deep-dive/) at the very least, for example.

But the fact that it worked as is enabled me to update all my packages to the latest versions and then worry about updating specific implementation details later.

I do want to point out that if you have any sites using the [Astro Starlight documentation site framework](https://starlight.astro.build), you can’t upgrade to Astro 5 yet. It will not compile. [There is a PR in place](https://github.com/withastro/starlight/pull/2612) and the stellar Astro documentation team is all over it!

I’ll make notes about the actual changes I do make to this site to be fully Astro 5 compliant and write a post about it soon.
