---
title: Bunch of Amphetamine
description: A hyper addition to my podcast workflow that keeps my Mac awake at all times.
date: "2023-03-19T09:00:00-08:00"
keywords: ["mac", "automation", "applescript", "programming", "podcast", "apps"]
slug: "amphbunch"
---

[Last month I wrote](https://scottwillsey.com/bunch/) about [Bunch](https://bunchapp.co), a wonderful utility for scripting work sessions, complete with sets of apps and the ability to customize various Mac settings. Last night as I was creating transcripts for [Friends with Brews,](https://friendswithbrews.com), I realized that part of my transcription workflow could be handy for podcasting as well – namely, starting an [Amphetamine](https://apps.apple.com/us/app/amphetamine/id937984704?mt=12) session.

Sounds a little extreme, you might be thinking, but it's actually less controversial than that. [Amphetamine](https://apps.apple.com/us/app/amphetamine/id937984704?mt=12) is a Mac utility that can keep your Mac from sleeping for a predetermined period of time, with granularity. Want to let the monitor sleep, but nothing else? Can do. Want to set a trigger so that whenever a specific app is running, Amphetamine is active? Can do!

In my case, since I already set up for podcasting by running my podcast bunch, I decided to see if I could trigger an Amphetamine session on and off with it. The answer is simple – can do! The reason is William Gustafson, creator of Amphetamine, made it possible to trigger sessions with AppleScript, and Brett Simmons, author of Bunch, supports running AppleScript commands in a bunch. Problem solved.

Starting an Amphetamine session with AppleScript in a bunch script:

```applescript
* tell application "Amphetamine" to start new session
```

The asterisk tells Bunch that the following is an AppleScript command. It's not part of the AppleScript syntax.

Stopping an Amphetamine session with AppleScript in a bunch:

```applescript
* tell application "Amphetamine" to end session
```

Just by adding these lines to my podcast bunch, I now have the ability to stand in front of my Mac for long podcast sessions without touching mouse or keyboard and not having to worry about the screensaver kicking on. Perfect.
