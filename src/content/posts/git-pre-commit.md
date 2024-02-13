---
title: "Using Git Hooks for Displaying Last Modified Dates" 
description: "Git hooks are pretty cool. I'm using pre-commit to conditionally update the last modified date on certain pages in my blog. Here's how I did it."
date: "2024-02-12T05:00:00-08:00"
keywords: ["blog", "astro", "git"]
series: "Astro"
slug: "git-pre-commit"
---
Not so very long ago, I wrote about using remark and a script called `remark-modified-time.mjs` to update a page’s front matter `Date` value for [Auto-Generated Last Modified Dates in Astro](https://scottwillsey.com/astro-last-modified). This approach worked pretty well until I moved the content for my [/Uses](https://scottwillsey.com/uses/) page out of a markdown file and into a json file. I didn’t want to have to keep modifying essentially an associated empty markdown file to get the last modified date to change.

What I wanted was a way to see if the json file itself had changed, and then enter THAT date into the [/Uses](https://scottwillsey.com/uses/) markdown file front matter. In essence, change one file, and another one gets its updated timestamp. This would give me a self-updating last modified date value for everything and I wouldn’t have to remember to manually change anything to make it happen.

Enter [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

Git hooks let you run a script when some git action occurs. One git related action that occurs all the time is the git commit. Git commit turns out to be a very good time to look at when files were last modified, since git’s entire job is paying attention to when and how files are modified. The git hook to use if you want it to happen when you perform a git commit is called `pre-commit`.

Although it’s called `pre-commit`, it happens during a commit but before you enter the commit message. It can be used to verify commits before allowing them to happen, but instead I use it to modify files and commit those new changes along with the existing ones.

Implementing a pre-commit git hook is simple. Go into your project’s `.git/hooks` directory and create a file called `pre-commit`, with no file extension. There should already be a file in there called `pre-commit.sample` – you can either rename it without the extension and edit it, or just create a new one with the correct name.

 Here are the contents of my `.git/hooks/pre-commit` file:

```bash
#!/bin/sh

git diff --cached --name-status | 
grep -iE '^M.*src/(content/links/links\.md|content/now/now\.md|content/pins/pins\.md|data/uses\.json|data/spotlight\.json)$' |
while read _ file; do
    if [[ "$file" == "src/data/uses.json" ]]; then
       file="src/content/uses/uses.md"
    elif [[ "$file" == "src/data/spotlight.json" ]]; then
        file="src/content/links/links.md"
    fi

    filecontent=$(cat "$file")
    frontmatter=$(echo "$filecontent" | awk -v RS='---' 'NR==2{print}')
    cat $file | sed "/---.*/,/---.*/s/^date:.*$/date: \"$(TZ='America/Los_Angeles' date "+%Y-%m-%dT%H:%M:%S-08:00")\"/" > tmp
    
    mv tmp $file
    git add $file
done

```

Two points if you noticed that it’s just a bash script and that it clearly is running a git command to see what files have changed since the last commit!

The output of that command is piped to grep to look to see if any of the modified files are `src/content/links/links.md`, `src/content/now/now.md`, `src/content/pins/pins.md`, `src/data/uses.json`, or `src/data/spotlight.json`.[^1]

Once it finds any modified files that match my list, it uses awk and sed to find the front matter and change the date value to git’s modified timestamp. I leave learning all about awk and sed as an exercise for the reader – see you in about 10 years.

For the most part, the files that are modified are the files that get their front matter `date` value updated, except in the case of the two json files. If `src/data/spotlight.json` is modified, `src/content/links/links.md` gets its timestamp instead. And if `src/data/uses.json` is changed, `src/content/uses/uses.md` gets that timestamp in its front matter `date` field.

Another way to look at it is that if any of the markdown files I’m looking for are updated, they get their timestamp set accordingly. In addition, `links.md` also gets an updated timestamp if `src/data/spotlight.json` is modified. This is because both `links.md` and `spotlight.json` contain data that shows up on [Links](https://scottwillsey.com/links/).

But in the case of my [/Uses](https://scottwillsey.com/uses/) page, I never look to see if `src/content/uses/uses.md` gets updated. That’s because I’m really only using it for its front matter at this point. All of the data displayed on the page itself comes from `src/data/uses.json`. So I only look to see if `uses.json` was modified, and if so, I update the timestamp in `uses.md`. Then I can use that value to display on the compiled page as the last modified date and time.

That’s it. It really is that simple to implement git hooks. They’re sitting inside `.git/hooks` in your repo just waiting to be used for exciting things like telling people when you added your mouse to the list of computer hardware that you gaze at lovingly on a daily basis.

[^1]: Spotlight.json is used for the Cool Site Spotlight on my [Links](https://scottwillsey.com/links/) page.
