+++
title = "The Great npm Purge of 2026"
description = "No more node_modules: moving my sites from Astro to Zola, and letting Claude do the heavy lifting."
date = 2026-10-07T00:10:00-08:00
slug = "the-great-npm-purge-of-2026"
[taxonomies]
tags = ["mac", "astro", "zola", "automation", "website"]
[extra]
display_title = "The Great Npm Purge of 2026"
display_date = "Wednesday, 07 Oct 2026"
rfc2822_date = "Wed, 07 Oct 2026 08:10:00 GMT"
+++

I don't think it's any secret that npm and the whole node supply chain are a mess. It seems like every week a new p0wnage comes out in the news, and I have to scramble to audit all the packages on all my [Astro](https://astro.build/) sites.

This gets old. And frankly, it's not worth the risk.

So in early August, I fired up Claude Fable 5 and threw the problem at it. I asked for options, migration strategies, and detailed reasoning behind each option. Its top choice was [Zola](https://www.getzola.org/) – a Rust-based single executable with no giant dependency chain.

I know a little bit about Rust, but I wouldn't say I know Rust. But it doesn't matter for 2 reasons:

1. The templates are written in [Tera](https://keats.github.io/tera/), not Rust.
2. I'll never look at them anyway, because I have a python dashboard app that I run scripts from to create posts and update the various pages automatically (YouTube and Overcast histories, Cool Site Spotlight, etc).

All I really needed was something that could match the customizations I'd made to the site and display everything identically. And making that happen was Fable 5's job, not mine.

Every site conversion or major update previous to this one, I've done myself. And it took many days and lots of effort. I'm a ponderous programmer, to put it mildly.

But guess what? I didn't miss doing all that a single bit. What matters to me is the result. The content, the stuff ON the site, that's the contribution I care about, because that's what you will read, assuming you're here reading this now. I know what I want in a web site, and I'm the one dictating the features, the look, and the result (for better or worse). I don't care about writing every if statement or file timestamp comparison.

It took about an hour for Claude to do a complete conversion and then another hour or so to fix a couple issues and make sure that all my site update scripts worked perfectly with the new framework. Even assuming my memory is bad and it really took a total of 3 hours worth of work, that's nothing compared to a normal full site conversion from one framework to another. It's even less time than it took for me to write my site update and maintenance scripts, and those are small and targeted.

The site before Zola:

[{{<img src="posts/20260205-HomeDark-8a79dbf5-145c-428d-b8ba-f6031b2d0877.png" alt="20260205-HomeDark" />}}](/images/posts/20260205-HomeDark-8a79dbf5-145c-428d-b8ba-f6031b2d0877.jpg)

The site after Zola:

[{{<img src="posts/20261007-Home-8a79dbf5-145c-428d-b8ba-f6031b2d0877.png" alt="20261007-Home" />}}](/images/posts/20261007-Home-8a79dbf5-145c-428d-b8ba-f6031b2d0877.jpg)

I'm sure some readers will be mad that I didn't do all this by hand and that I don't care about the actual coding as much as the features and functionality and thought behind the system design. Be angry all you like, but I have spent many hours in the past learning CSS in great depth, learning how image optimization works in modern HTML, learning various programming languages for the build automation part of the system, and learning how to construct all of it completely by hand. Having done it and understood it, I don't feel like I need to keep doing it to understand it or to benefit from that knowledge.

The beauty of automation is the time savings it can provide, not to mention making sure things happen the same way time after time. The beauty of LLMs is that I can focus on how I want things to work, what design decisions are important, and then go do something that makes me money while the LLM writes and tests the code.

Having said all the above, I'd not be surprised if I was horrified by some of the CSS construction and other things if I looked too deeply at it.

After all this, I now have all my websites running on Zola and not running anything npm related anymore. This is a relief and it's a much simpler system to maintain. But I still have utilities and scripts on my site that do require node and npm, and I have Claude audit those updates every time so I can at least *try* to mitigate the possibility of getting p0wned by a supply chain attack. I do the same for Python packages and any other 3rd party libraries and packages I use, locally or on any of my servers.

Oh, and also related to LLMs, they *love* to download packages to solve programming problems or generate reports or whatever task you throw at them, so keep on eye on it and create standing rules that don't allow them to do this. Sandbox them if needed, just don't let your LLMs yank packages off the internet, even temporarily, without informing you first, and doing audits on the packages and their dependencies.

And whatever you do, quit filling up your file system with node packages.
