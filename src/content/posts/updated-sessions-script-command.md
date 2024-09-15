---
title: "Updated Sessions Raycast Script Command"
description: A version of my Sessions Raycast script command using Moom layouts instead of Raycast Window Management layouts.
date: "2024-09-15T05:00:00-08:00"
keywords: ["apps", "mac", "automation", "programming", "raycast"]
cover: "../../assets/images/covers/RaycastHeader.png"
coverAlt: "Raycast"
series: "Raycast"
slug: "updated-sessions-script-command"
---
As you may know, [I created a Raycast script command to trigger what I call “sessions”](https://scottwillsey.com/sessions-script-command/), which are really just setting up the Mac to perform different tasks, such as podcasting or “normal” general use. At the time, I was using Raycast for window management, so my script command referenced Raycast window management layouts. Now [I’m using Moom](https://scottwillsey.com/moom4/) for window management, so I needed to update it to call my Moom layouts instead.

In the process, I decided to steal even more from [Robb Knight](https://rknight.me)’s [App Mode Raycast script command](https://github.com/rknightuk/raycast-script-commands/blob/main/app-mode.sh) and use his method of killing all apps before activating a session and having an array of default apps that I always want open. It’s almost the same exact script now.

The updated version looks like this:

```bash

#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Session
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon /Users/scott/Scripts/Raycast/icons/app-mode.png
# @raycast.argument1 { "type": "dropdown", "placeholder": "Session", "data": [ { "title": "Home", "value": "home" }, { "title": "IT", "value": "it" }, { "title": "Podcast", "value": "podcast" }, { "title": "Podcast Edit", "value": "podcastedit" } ] }
# @raycast.packageName Utils

# Documentation:
# @raycast.description Set up a workflow session
# @raycast.author scott_willsey
# @raycast.authorURL https://raycast.com/scott_willsey

open raycast://extensions/raycast/system/quit-all-applications

sleep 3

CORE=(1Password Messages Mail Safari)

TYPE=$1

for value in "${CORE[@]}"
do
    open -a "$value"
done

if [ "$TYPE" = 'home' ]; then
    open 'raycast://script-commands/set-default-browser-safari'
    sleep 2
    open -a Warp
    /opt/homebrew/bin/SwitchAudioSource -s "Studio Display Speakers"
    /opt/homebrew/bin/SwitchAudioSource -s "Studio Display Microphone" -t "input"
    osascript ~/Scripts/applescript/apply_moom_layout.scpt "Home"
        exit
fi

if [ "$TYPE" = 'it' ]; then
    open 'raycast://script-commands/set-default-browser-chrome'
    sleep 2
    open -a "Google Chrome"
    open -a Warp
    open -a Slack
    /opt/homebrew/bin/SwitchAudioSource -s "Studio Display Speakers"
    /opt/homebrew/bin/SwitchAudioSource -s "Studio Display Microphone" -t "input"
    osascript ~/Scripts/applescript/apply_moom_layout.scpt "IT"
        exit
fi

if [ "$TYPE" = 'podcast' ]; then
    open 'raycast://script-commands/set-default-browser-safari'
    sleep 2
    open -a "Audio Hijack"
    open -a Farrago
    open -a Bear
    open -a FaceTime
    /opt/homebrew/bin/SwitchAudioSource -s "Elgato Wave XLR"
    /opt/homebrew/bin/SwitchAudioSource -s "Elgato Wave XLR" -t "input"
    osascript ~/Scripts/applescript/apply_moom_layout.scpt "Podcast"
        exit
fi

if [ "$TYPE" = 'podcastedit' ]; then
    open 'raycast://script-commands/set-default-browser-safari'
    sleep 2
    open -a "Logic Pro X"
    open -a Finder ~/Documents/Podcasts/FwB
    /opt/homebrew/bin/SwitchAudioSource -s "Elgato Wave XLR"
    osascript ~/Scripts/applescript/apply_moom_layout.scpt "PodcastEdit"
        exit
fi


```

You can see that because my so-called “IT” session sets Chrome as the default browser, I’m compelled to set Safari as my default browser for every other session type. I supposed I could just move that out to the top and have it called no matter what, and then immediately reversed if the session type is “IT”. You can [read about my default browser script commands here](https://scottwillsey.com/default-browser/).

The reason for the sleep commands is that without them, running the Session script command would result in some timing issue in which only some of the apps would open, but not all of them. I was able to solve the problem by putting in a sleep after killing all applications and after setting the default browser.

Calling Moom layouts using AppleScript commands (osascript) is possible because the author of Moom supports AppleScript calls to the program. I wish more programmers would think of their apps as potential links in a workflow chain like this.
