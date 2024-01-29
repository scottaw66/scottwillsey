---
title: "Reponsive Image Rabbit Hole – Part 2"
description: Using automation, specifically Astro Image, to give the browser image options.
date: "2022-09-30T05:00:00-08:00"
keywords: ["blog", "images", "responsive", "astro"]
series: "Responsive Images"
slug: "image-rabbit-hole-2"
---

[In installment 1 of this responsive image topic](https://scottwillsey.com/image-rabbit-hole-1/), I talked about how the modern approach to giving site visitors the best combination of image file size and image quality comes down to generating a bunch of versions of the image and letting the browser choose. Further, the browser chooses by being given a choice of sources and/or srcset elements using the HTML [picture](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) or [img](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img). So the two step process for making image optimization possible for site visitors is: 1) Make a bunch of image files for each image you will display, 2) Create the HTML that allows the browser to know about and choose from the available options.

This sounds like a lot of work to do whenever you want to drop an image in a blog post. Who wants to do all this every time? The correct answer is no one. Anyone who does this manually for every image they want to inflict on their visitors doesn't understand that the computer is there to work for them instead of the other way around. Fortunately, all modern web frameworks understand this and have solutions in place to tackle image optimization.

## Astro Image plugin

In the case of [Astro](https://astro.build), the official answer to this is the [@astrojs/image plugin](https://www.npmjs.com/package/@astrojs/image). For simplicity I'll just call it Astro Image from now on. To understand what image optimization plugins do, the Astro Image documentation says this:

> Images play a big role in overall site performance and usability. Serving properly sized images makes all the difference but is often tricky to automate.
>
> This integration provides `<Image />` and `<Picture>` components as well as a basic image transformer, with full support for static sites and server-side rendering. The built-in image transformer is also replaceable, opening the door for future integrations that work with your favorite hosted image service.

There are a couple key points here. One is providing Image and Picture Astro components. That means you can generate all the html you need with a component like this:

```astro
<Picture
  src={beerlatest}
  widths={[800, 1200, 1800]}
  sizes="(max-width: 800px) 95vw, 90vw"
  formats={["webp"]}
  alt="Latest episode beer list view"
/>
```

The resulting HTML will be the fully conceived HTML picture element with all the sources and srcsets you need. I added judicious use of carriage returns and tabs to make each of the elements more readable.

```html
<picture class="astro-EI35XRNH">
  <source
    type="image/webp"
    srcset="
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_1mD09L.webp   800w,
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_Z1gGQwg.webp 1200w,
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_Z22UqRY.webp 1800w
    "
    class="astro-EI35XRNH"
    sizes="(max-width: 800px) 95vw, 90vw"
  />
  <source
    type="image/png"
    srcset="
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_wgsuf.png    800w,
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_Z2b2h6I.png 1200w,
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_1yzNhO.png  1800w
    "
    class="astro-EI35XRNH"
    sizes="(max-width: 800px) 95vw, 90vw"
  />
  <img
    src="/assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_Z8LQlw.png"
    class="astro-EI35XRNH"
    loading="lazy"
    decoding="async"
    alt="Latest episode beer list view"
  />
</picture>
```

You may notice the different file names for each image resolution in the srcset for each of the two sources. If you guessed that the second part of what Astro Image does is generate the different image files for the browser to choose from, you win a virtual round of applause. For each of the widths you specify in the widths attribute of the Astro Image Picture component, Astro Image will generate an image of that width for that source's file type. For local images, all heights will be calculated to keep the original aspect ratio, while for remote images, an aspect ratio must be provided for Picture to know what height to use.

Astro Image also has an Image component which you can use to create resized images in whatever format you desire. However, there are some limitations to the Image component in Astro Image. You can only generate one size (it does not make use of the HTML img srcset attribute) and one format. This means you need to remember my warning about high resolution screens at the bottom of [part 1](https://scottwillsey.com/image-rabbit-hole-1/). This means if you use the Image component, you are going to certainly want to specify a width of 2-3x the pixel width you plan to display the image at.

I use this for my [About page](https://scottwillsey.com/about/) selfie image. Below is the Astro component code followed by the resultant HTML.

```astro
<Image
  class="about-av"
  src={av}
  width={600}
  format={"webp"}
  alt="Scott Willsey"
  quality={85}
/>

<img
  class="about-av astro-AT6AUSG4 astro-UXNKDZ4E"
  alt="Scott Willsey"
  width="600"
  height="600"
  src="/assets/ScottLatest.cbf6b2e6_1ymKwq.webp"
  loading="lazy"
  decoding="async"
/>
```

I actually display the image at 300x300 (which I control in css) and it looks ok on high resolution screens because the image is 600x600.

## The Retina wrinkle (again)

Remember last time when I said retina or high resolution displays throw a monkey in the wrench of displaying images? I fooled myself for a long time into thinking Astro Image wasn't working correctly because I kept forgetting about it, even though I know very well about retina displays and their need for higher resolution images.

But now, because apparently I can't quit using words, I'll have to save that for part 3. I want to explain what I did on my Eleventy sites and what I was doing with my Astro sites, and how converting Friends with Beer from one to the other helped me understand my incredible ignorance about how all this works in the first place.

Stay tuned.
