---
title: AppleScript GPT
description: ChatGPT doesn't always get programming right.
date: "2023-04-06T09:00:00-08:00"
keywords:
  ["mac", "automation", "applescript", "images", "programming", "chatgpt"]
cover: "../../assets/images/covers/MacHeader.png"
coverAlt: "Mac"
series: "Mac"
slug: "applescript-gpt"
---

I've been playing with using ChatGPT (via [MacGPT](https://www.macgpt.com)) with the gpt-3.5-turbo model to help script things. Today I wanted an AppleScript to rename some files by sticking a UUID in between the base file name and the file extension (e.g., rename MyImage.png to MyImage-FFE9D8C8-8AEE-42E2-8A48-F0C328A9E5F2.png). I asked MacGPT to write the script and this is what it came up with:

```applescript

-- Prompt user to select input directory
set inputFolder to (choose folder with prompt "Please select the input directory")

-- Prompt user to select output directory
set outputFolderAlias to (choose folder with prompt "Please select the output directory")
set outputFolder to (outputFolderAlias as string)

-- Generate a UUID
set uuid to (do shell script "uuidgen")

tell application "Finder"
 -- Get a list of all files in the input directory
 set fileList to every file of folder inputFolder

 -- Loop through each file and copy it to the output directory with a new name
 repeat with aFile in fileList
  set fileName to name of aFile
  set fileExtension to name extension of aFile
  set baseName to text 1 thru ((length of fileName) - (length of fileExtension) - 1) of fileName
  set newName to baseName & "-" & uuid & "." & fileExtension
  set newFile to outputFolder & newName
  duplicate aFile to folder outputFolder with replacing
  delay 3
  set name of (file newFile) to newName
 end repeat
end tell


```

It actually had `delay 1` but I set it to 3.

But this script is wrong. Running this script generates an error about not being able to rename the apparently already renamed file, complete with UUID, to the desired (same) name, complete with UUID.

```sh frame="none"
Finder got an error: Can’t set file "Macintosh HD:Users:scott:Documents:Podcasts:FwB:BrewsImages:OUT:Cup_Shots_Kagoshima_800x-559DCE44-3B60-4CE9-8AEE-1A862C6498FA-CBC0F756-F7E3-4368-ACFB-98F4DC50E1BB.png" to "Cup_Shots_Kagoshima_800x-559DCE44-3B60-4CE9-8AEE-1A862C6498FA-CBC0F756-F7E3-4368-ACFB-98F4DC50E1BB.png".
```

The reason is simple: ChatGPT set the `newFile` variable to `outputFolder & newName` and then tries to set the name of `file newFile` to `newName` later.

The correct code for the repeat loop section is:

```applescript
repeat with aFile in fileList
 set fileName to name of aFile
 set fileExtension to name extension of aFile
 set baseName to text 1 thru ((length of fileName) - (length of fileExtension) - 1) of fileName
 set newName to baseName & "-" & uuid & "." & fileExtension
 set newFile to outputFolder & fileName
 duplicate aFile to folder outputFolder with replacing
 delay 3
 set name of (file newFile) to newName
end repeat
```

The only difference here is that now when the newFile variable is created, it's set to `outputFolder & fileName` (the original filename) so that when it looks for the file to rename, it correctly looks for the original file name.

I told MacGPT about its mistake and it claims to be glad that I did, but I wonder if it learns that way. I don't think its model changes based on user feedback, but I don't really know what all goes into improving its learning.

By the way, in case you're wondering why I'm using AppleScript in 2023 for a new task, it's because I can use AppleScript very simply to tell [Retrobatch](https://flyingmeat.com/retrobatch/) to run a saved workflow that crops images to a square ratio and save them as png. Since I'm already running the AppleScript, I'm also using it to stick the UUID into the file names, something I was using a shell script for. I would have just had my Retrobatch workflow run the script, but I couldn't get it to work correctly and I'm not sure why. The documentation on how the shell script action in Retrobatch works isn't super comprehensive, and I didn't find anything in the Flying Meat forum that helped either.

And to answer what might now be another question of yours, in general I stick a UUID in image file names because I don't ever want to have to worry about image file name collisions when I shove them in the site images folder. I just want to upload them and be done with it. If I have the UUID in the file name when I start writing my post, all I have to do is make sure none of the images in that particular post have the same name (I use one UUID for all images in a post).
