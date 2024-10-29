---
title: "Initial SuperDuper Copy"
description: A tip for making your first SuperDuper! drive copy.
date: "2024-10-28T05:00:00-08:00"
keywords: ["apps", "mac", "superduper"]
cover: "../../assets/images/covers/macseries.png"
coverAlt: "Mac"
series: "Mac"
slug: "superduper-initial"
---
Last night I [mentioned](https://scottwillsey.com/superduper-invisible/) setting up [SuperDuper!](https://shirt-pocket.com/SuperDuper/SuperDuperDescription.html) to clone my Mac’s internal SSD to an external SSD daily. One thing about the initial copy you should know that doesn’t pertain to subsequent incremental copies is don’t let your Mac sleep during the initial copy.

I even thought about this when I started the initial backup, but then thought it shouldn’t matter. I came back to a failed copy with the following errors in the SuperDuper! log:

```bash
| Info |       Volume replication failed - Resource busy
| Error | ***ERROR OCCURRED: ****FAILED****: result=256 errno=60 (Operation not permitted)
```

I sent the log to [Shirt Pocket](https://shirt-pocket.com) support, and Dave Nanian quickly replied with the following (I hope he doesn’t mind me posting it here):

> Your Mac has fallen asleep during the copy, even though we asked it not to, or something similar (such as a TRIM operation that takes too long) -- as you can see, Apple's error is vague and unhelpful.  
> 
> But, in our experience, this usually works. Please reformat the backup drive (which, done this way, should reset all the TRIM operations):
>
> - Open Disk Utility
> - Choose "Show All Devices" from the View menu
> - Select the destination drive hardware (above the existing volume)
> - Click Erase
> - Choose the "GUID" partition scheme (2nd pop-up), THEN "APFS" formatting (1st pop-up) and name appropriately
> - Click Erase
>
> Then restart your Mac. Install Coca (free) from the App Store and enable it to keep your Mac awake -- *including* the screen. Ensure it's plugged in if it's a laptop. Turn Time Machine off temporarily. Then try the erase-then-copy backup again.  
> 
> Note that none of this should be necessary for future Smart Updates, which are done with our copy engine, and not Apple's.  
> 
> Hope that helps!  
> —  
> Dave Nanian  
> Shirt Pocket  

In my case, I use the [Raycast Coffee extension](https://www.raycast.com/mooxl/coffee) now when I want to keep my Mac awake, so I used that to make sure the first copy finished.

Anyway, don’t sleep on that first copy, and do back your drive up to more than one destination. Make at least one local and at least one remote (cloud backup is fine). I highly recommend SuperDuper! for its features, price, and always outstanding support from Dave Nanian.
