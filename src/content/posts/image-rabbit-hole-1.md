---
title: "Reponsive Image Rabbit Hole – Part 1"
description: I learned about responsive images the hard way, by misunderstanding how they worked.
date: "2022-09-28T05:00:00-08:00"
keywords: ["blog", "images", "responsive", "astro"]
slug: "image-rabbit-hole-1"
---

## Contents

I fell down a deep rabbit hole yesterday thanks to the fact that I'm converting the [Friends with Beer podcast website](https://friendswithbeer.com) from [Eleventy](https://friendswithbeer.com) to [Astro](https://astro.build). The rabbit hole was specifically image optimization, the effort to build responsive and hopefully smaller file size images.

## Why image optimization?

Image optimization and how browsers can handle various methods of optimization is a pretty interesting topic. The basic idea is to give the browser options for any given image so that it can display them as intended by the site or article author, but with as little data transfer and image loading time as possible.

Browser variables that can affect image rendering efficiency are things like platform (mobile vs desktop-class browser), internet connection bandwidth, viewport size, screen resolution, and which image formats the browser supports. [Ben Holmes](https://twitter.com/BHolmesDev) wrote a great article on the topic of [perfect image optimization](https://bholmes.dev/blog/picture-perfect-image-optimization/) that you should read which talks about some of these variables.[^1]

## How image optimization?

Ok, that's not really proper English, but you get the point. Now we know we need to try not to send bigger images to the browser than necessary, but we still want them to look good. How do we do this?

The answer is: _make multiple sizes and formats of each image and let the browser figure it out._

Modern browsers allow you to specify source sets for images. Given these image source sets, the browser can make a choice on which one it wants to request to perform the role of the image specified in the img tag.

Image source sets can be specified using either the [HTML picture element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) or directly in the [HTML img element](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images) itself.

### HTML img element

With an HTML img, you can specify a srcset like this ([example from MDN](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)):

```html
<img
  srcset="elva-fairy-480w.jpg 480w, elva-fairy-800w.jpg 800w"
  sizes="(max-width: 600px) 480px,
         800px"
  src="elva-fairy-800w.jpg"
  alt="Elva dressed as a fairy"
/>
```

In the above example, there are two jpg versions of the same image available, one 480px wide and the other 800px wide. The browser will download the image size that makes sense for it given the viewport size and screen resolution. The value of the sizes attribute specifies that if the viewport is 600px or less, you'll get a 480px wide image, otherwise you'll get an 800px wide one.

### HTML picture element

The Picture element is a little more involved but also more versatile ([again from MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture)):

```html
<picture>
  <source srcset="photo.avif" type="image/avif" />
  <source srcset="photo.webp" type="image/webp" />
  <img src="photo.jpg" alt="photo" />
</picture>
```

As you can see, instead of just one srcset, you can have multiple sources (one source for each image format option available), each with their own srcsets. These srcsets can in turn contain multiple image sizes. Here's an example of this from my last post on this site:

```html
<picture class="astro-EI35XRNH">
  <source
    type="image/webp"
    srcset="
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_ZFUDaL.webp   300w,
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_Z2uWKfV.webp  600w,
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
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_Z1MMor.png   300w,
      /assets/BeerList-FCBA21C9-2F71-4051-B283-51452F68625D.d9a54970_13Es8j.png   600w,
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

This is an admittedly extreme example of generating 10 different images (5 sizes of webp, 5 sizes of png) just for one actual image on the website. I probably shouldn't do this many resolutions in practice, and in fact I probably gain no benefit from doing this many. I probably only need 2 or 3 of those. But it does give you a good idea of the fact that each source in a picture element is a specific format of image, and inside that source, the srcset contains the different image sizes available for that format option.

The Sizes attribute works as it does with img, in this case specifying that up to 800px browser width, the image should be sized to take up 95% of the viewport width, and above 800px wide, only 90% of the viewport width. The context here is that my whole website content section is set to a maximum of 70ch or something like that, so even if you have your browser in fullscreen mode on a 5k iMac, the image will only be 90% of 70ch wide anyway.

## The Retina wrinkle

Speaking of 5k iMac displays, there's a wrinkle in this whole image optimization scheme: high-resolution displays (known as [Retina displays](https://en.wikipedia.org/wiki/Retina_display) in the Apple world). Basically for a given resolution, the screen uses double or triple the pixel density in order to display things sharp enough that the individual pixels can't been seen by the human eye. What this means in terms of images on websites is that if you want to display a nice looking 800px wide image on a Retina display, you actually need a much higher resolution version of the image.

The image resolution issue was something I tripped over when fighting my image optimization strategy for both this site and the work-in-progress Astro version of Friends with Beer. I knew this fact but didn't take it into account when I was looking at which size image was downloading for a given image. I thought the [Astro Image component](https://www.npmjs.com/package/@astrojs/image) I was using was downloading a larger image than it should be given the size I wanted to display, but in fact the only thing that was broken was my understanding of how responsive images work.

I'll tell that story in [Part 2](https://scottwillsey.com/image-rabbit-hole-2/). In the meantime, here are some excellent links on image optimization.

- [A guide to the responsive images syntax in HTML](https://css-tricks.com/a-guide-to-the-responsive-images-syntax-in-html/)
- [Halve the size of images by optimising for high density displays](https://jakearchibald.com/2021/serving-sharp-images-to-high-density-screens/)
- [Image file type and format guide](https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types)
- [Optimizing images with the 11ty image plugin](https://www.aleksandrhovhannisyan.com/blog/eleventy-image-plugin/)
- [Picture perfect image optimization for any framework](https://bholmes.dev/blog/picture-perfect-image-optimization/)
- [Responsive images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- [Using images in HTML](https://developer.mozilla.org/en-US/docs/Web/Media/images)

[^1]: Ben now works for [Astro](https://astro.build), the framework that I use for this website and highly endorse.
