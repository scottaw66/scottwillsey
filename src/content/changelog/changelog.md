---
title: "Changelog"
description: Site changelog.
date: "2024-03-04T20:00:41-08:00"
slug: "changelog"
---
### 2024-03-04

Added a site changelog at /changelog! (Hint: you're reading it right now) Originally I had this auto-update using the pre-commit git hook, but this created a couple annoying issues:

1. The pre-commit hook would run every time I committed, even if I didn't want to update the changelog with some mundane item that makes sense for a git commit (and corresponding commit message), but not for a site changelog of new features or site additions.

2. The automatically created commit message was always one commit message behind.

Also added Articles Worth Reading and Newsletters sections to Links page and updates Cool Site Spotlight.
