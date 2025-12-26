---
title: "title case"
description: "A good system should never make you remember its implementation details in order to use."
date: "2022-11-10T05:00:00-08:00"
keywords: ["astro","blog", "writing", "regex", "javascript"]
slug: "title-case"
---

A good system should never make you remember its implementation details in order to use. That extends to blogging platforms. Since my blogging platform is a self-created, self-hosted website built on [Astro](https://astro.build), the onus of making myself not have to remember how it works just to use it rests solely on me.

Today I started writing a post about Mastodon and the Fediverse and why it's not the solution to all your problems that you might think it is, and I realized I couldn't remember if I write my blog post titles in Title Case or Just the first word capitalized or in camelCase.[^1] It's not the first time I've had to ask myself this question, and that means it's a problem I don't want to think about anymore. So here's a very simple Title Case generator:

```javascript
export function titleCase(str) {
  return str.replace(/\b[A-Za-z]/g, (x) => x.toUpperCase());
}
```

Running the first paragraph of this blog post through it results in this:

```
A Good System Should Never Make You Remember Its Implementation Details In Order To Use. That Extends To Blogging Platforms. Since My Blogging Platform Is A Self-Created, Self-Hosted Website Built On Astro, The Onus Of Making Myself Not Have To Remember How It Works Just To Use It Rests Solely On Me.

```

So now my blog post titles are generated like this:

```astro
<h1>
  <a
    href={new URL(
      path.join(config.get("posts.path"), content.frontmatter.slug),
      config.get("url"),
    )}
    >{titleCase(content.frontmatter.title)}
  </a>
</h1>
```

Speaking of camelCase, I also took the opportunity to add a camelCase function that outputs what we called camelCase when I was a juvenile programmer-wannabe.

```javascript
export function camelize(str) {
  return str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
}
```

I'll be back next time with some reasons why Mastodon and the Fediverse aren't suitable for most people in their current incarnations.[^2]

[^1]: You modern whippersnappers probably think ThisIsCamelCase, but when I was a boy, thisWasCamelCase. So put that in your programming pipe and smoke it.
[^2]: Hint: it's not a technical problem, it's a people problem.
