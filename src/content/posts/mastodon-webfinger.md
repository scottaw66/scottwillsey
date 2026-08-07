---
title: "The Mastodon Webfinger Domain Search Super Trick"
description: You can help people find you on Mastodon by letting them search for your own domain name, regardless of what Mastodon instance you're on.
date: "2022-11-23T05:00:00-08:00"
keywords: ["mastodon", "search"]
slug: "mastodon-webfinger"
---

I promised an article about whether or not Mastodon and the Fediverse were going to solve all our problems and make us happy humans with a long species survival probability, but work and other tech projects have intervened. More on that later.

In the meantime, if you ARE on Mastodon and don't want to run your own instance but would like people to be able to search for you there using your own domain name instead of the domain name of the instance you're on, [Maarten Balliauw](https://mastodon.online/@maartenballiauw) has a [really cool trick for this](https://blog.maartenballiauw.be/post/2022/11/05/mastodon-own-donain-without-hosting-server.html):

> In other words, if you want to be discovered on Mastodon using your own domain, you can do so by copying the contents of `https://<your mastodon server>/.well-known/webfinger?resource=acct:<your account>@<your mastodon server>` to `https://<your domain>/.well-known/webfinger`.

You can read Maarten's [post on the webfinger method](https://blog.maartenballiauw.be/post/2022/11/05/mastodon-own-donain-without-hosting-server.html) on [his blog](https://blog.maartenballiauw.be).
