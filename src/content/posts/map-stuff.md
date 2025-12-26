---
title: Map Your Stuff
description: JavaScript array maps are a common pattern in Astro, and very useful ones at that.
date: "2022-09-26T05:00:00-08:00"
keywords: ["astro", "javascript", "programming"]
slug: "map-stuff"
---

One of the patterns you'll see frequently in [Astro](https://astro.build) is using the JavaScript [array map function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map). Array.map() creates a new array that holds the results of performing whatever function you provide on each element of the original array.

Ok, that's clear as mud.

But let's say you have a podcast. Let's say this podcast is called [Friends with Beer](https://friendswithbeer.com), and let's say you have a json file full of information about the beer you drink on your podcast. Let's say it looks like this, repeated n number of times where n is the number of beers you've had on the podcast.

```json title="beer.json"

[
  {
    "id": "OShp7ovkwb6F14mpRqFbw",
    "name": "Hell or High Watermelon",
    "brewery": "21st Amendment Brewery",
    "image": "21stAmendmentBreweryHellOrHighWatermelon-EA669A2C-D404-422C-8495-AA268674CAA5",
    "sortOrder": "0",
    "episodes": ["14"],
    "url": "https://www.21st-amendment.com/beers/hell-or-high-watermelon",
    "rating": [
      {
        "host": "Scott",
        "vote": "thumbs-up",
        "description": "I wish it had more watermelon flavor, but it is a nice light wheat beer that's very pleasant."
      }
    ]
  },

...

]

```

Presumably you'd like to show the latest episode on your site's home page with a little view featuring the beer that was consumed on that episode, like this:

[![Latest episode beer list view](../../assets/images/posts/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.png)](/images/posts/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.jpg)

First thing you need to do is grab the json file and find all beer associated with whatever episode is the latest. I have a file named beerlist.mjs that exports a beerList function this because I want to be able to get a beer list in other places on the site too.

```javascript title="beerList.mjs"
import beer from "../../data/beer.json";

export function beerList(episode) {
  const ep = episode ?? 0;
  let beers = Array.from(beer);

  return ep === 0
    ? beers
    : beers.filter((beer) => beer.episodes.includes(String(episode)));
}
```

I can optionally pass in an episode number to filter the list by. If I do, I return an array of the episode-filtered beers. If no episode number is provided, I just return an array of the full list of beers.

Now I can create that view from the image above by importing my function and using it like this:

```astro title="BeerList.astro"
---
import { Icon } from "astro-icon/components";
import { Image } from "@astrojs/image/components";
import { beerList } from "./utilities/beerlist.mjs";

const { episode } = Astro.props;

const beers = beerList(episode);
---

<div class="beer-container">
  {
    beers.map((beer) => (
      <div class="beer">
        <div class="beer-image">
          <a href={`/images/beer/${beer.image}.png`}>
            <Image
              src={`/images/beer/${beer.image}.png`}
              width="300"
              aspectRatio="1:1"
              format="webp"
              alt={`${beer.brewery} ${beer.name}`}
            />
          </a>
        </div>
        <div class="beer-name">
          <div class="brewery">{beer.brewery}</div>
          <div>
            <a href={`/bottle/${beer.id}`}>{beer.name}</a>
          </div>
          <div class="beer-details">
            <span>
              <Icon name="fluent:info-24-filled" />
            </span>
            <span>
              <a href={`/bottle/${beer.id}`}>View Details</a>
            </span>
          </div>
        </div>
      </div>
    ))
  }
</div>
```

The fun part is everything inside the map function. As you can see, my beerList function returns an array of beers. I map that so that for each beer in the array, I output the HTML inside the map function. This consists of an image of the beer, the brewery name, the beer name, and a link to view the page for that beer.

You can also make your maps more legible by creating a component to use inside the map. Here's an example from the code for the paginated blog posts on this site that uses a Post component to do all the rendering of each post, just passing the individual mapped post to the component. It looks neater and is easier to understand, but it means creating another component. It just depends how much you want to break things down into separate components. If you need to show posts in a similar manner elsewhere besides the paginated list, you may want to do it by mapping your array items as props to a separate component, like below.

```astro title="[page].astro"
<Base title="test">
  <section aria-label="Post list">
    {
      posts &&
        posts.map((post) => {
          return (
            <Post content={post}>
              <post.content />
            </Post>
          );
        })
    }
    <Pager page={page} , pageSize={pageSize} />
  </section>
</Base>
```

The Astro docs have a good example of using the map function in the ["Converting markdown to MDX" guide](https://docs.astro.build/en/migrate/#converting-existing-md-files-to-mdx) and (more usefully for most people) the [Astro.glob function documentation](https://docs.astro.build/en/reference/api-reference/#astroglob).

By the way, if you're wondering why I treat episode number as a number sometimes and treat it like a string other times (inside beer.json, for example), rest assured you aren't the only one wondering. I took that json file from my existing Eleventy site for Friends with Beer and didn't think much about it. Refinements are certainly a valid consideration.
