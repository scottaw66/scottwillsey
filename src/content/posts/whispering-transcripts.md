---
title: "Whispering Podcast Transcripts"
description: "Whisper.cpp is a C/C++ port of OpenAI's Whisper that might meet your needs for audio transcription."
date: "2023-01-25T05:00:00-07:00"
keywords: ["podcast", "audio", "transcription", "apps"]
slug: "whispering-transcripts"
---

In what feels like a lifetime ago, I had a podcast called Pocket Sized Podcast, talking about iOS apps and devices, mostly. At some point, for reasons I can't even begin to recall, I joined up with a fledgling podcast network called Fiat Lux, which was later rebranded Constellation by the two fairly angry guys running it. The whole thing was a giant fiasco full of insane stories, but it's relevant to me now because podcast transcription is having a moment.

Fiat Lux/Constellation decided that the core feature of the podcast network would be incredibly detailed show notes on all podcasts. Unfortunately they had some really bad ideas about exactly what those show notes should be like.[^1] None of us wanted anything to do with their plan, mainly because of how they presented it and the amount of shouting involved in their attempts to convince us.

If you're going to try to herd cats, you'd better be a cat person is what I'm saying.

But the idea of making podcast episodes available in text **IS** a good idea, and several very popular podcasters I know of are looking at all kinds of options for creating good transcripts without spending hours and hours on them.

There are several paid and soon-to-be-paid options such as [Adobe Podcast](https://podcast.adobe.com) (currently in beta, pricing to be determined), and [Otter](https://otter.ai). But the completely free option that got my attention is a Mac port of OpenAI's [Whisper](https://github.com/openai/whisper), called [Whisper.cpp](https://github.com/ggerganov/whisper.cpp).

Whisper runs locally on your own machine, and Whisper.cpp jettisons the Python runtime for C and C++, which has obvious positive performance implications. Better yet, it's even optimized for Apple Silicon.

I heard about Whisper.cpp while listening to [Rebuild](https://rebuild.fm) from [Tatsuhiko Miyagawa](https://mastodon.social/@miyagawa), a very enjoyable Japanese language tech podcast. It's actually one of my favorite podcasts in any language. Anyway, at the time Miyagawa-san was experimenting with Whisper.cpp on his new Apple Silicon Mac, and I filed that information away in my brain, figuring it would be some time before I got an Apple Silicon Mac of my own. It was, but now I have, and so I recently jumped into performing Whisper.cpp experiments of my own.[^2]

Whisper.cpp has several [models](https://github.com/ggerganov/whisper.cpp/tree/master/models) you can download, depending on what kind of quality vs time tradeoffs you want to make. I've tested Whisper.cpp on [Friends with Brews](https://friendswithbrews.com) episodes using the ggml-base.en.bin, ggml-medium.en.bin, and ggml-large.bin models, with interestingly varying results.

The first thing I found is that the base model is **FAST**. I transcribed a 50 minute podcast episode in about a minute with decent results. I had to fix a few names and technical terms, but otherwise it was quite good.

I couldn't tell a huge difference between the medium and large models with the two particular episodes I experimented with, but the time difference between all three models was noticeable. I tested all three models on [Friends with Brews episode 21](https://friendswithbrews.com/21/), which is 45 minutes and 29 seconds long and roughly 24 MB in size.

**Base.en** – 1.5 minutes  
**Medium.en** – 10 minutes  
**Large** – 19 minutes

Even with the large model, transcribing a podcast at 2x speed is pretty good.

So that's how long it takes, but what about the results? [Compare for yourselves](/whisper-compare/). The headers for each file are links so you can download the markdown files to compare locally if you like.

The end result is that I think it's worth going with the medium or large models. It'll cost you disk space – the base english model is 142MB, the medium english model is 1.5GB, and the large model is 2.9GB. But I think it's worth it in terms of results.

You may have to do some testing to decide between the medium and large though, even if you're convinced that the base model isn't the way to go. Generally I think I like the large model results better, but there are some instances where the medium transcribed something more accurately.

Personally I'm using the large model, but that's because I'm actually using yet another port, which I'll talk about in another post very soon.

By the way, if you want to hear the Fiat Lux/Constellation stories, just slip [@Vichudson1@appdot.net](https://appdot.net/@vichudson1) a nice glass of whiskey.[^3] He has a much better memory than I do about pretty much anything in the past, and especially about the saga of the world's unhappiest podcast network.

[^1]: Including wanting markdown format in Google Docs specifically as opposed to any plaintext document format (like, I don't know, .md?), but whatever.
[^2]: Whisper.cpp actually runs on Intel Silicon too, but I didn't realize it at the time. But my late 2015 iMac probably would have barfed up a lung on it anyway.
[^3]: Fair warning, he'll probably try to get you to buy him more than one.
