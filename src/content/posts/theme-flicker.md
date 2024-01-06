---
title: "Get Rid of Theme Flicker"
description: Avoiding theme flicker on Astro sites with multiple themes.
date: "2023-08-11T09:00:00-07:00"
keywords: ["blog", "astro", "design", "programming", "css"]
series: "Astro"
slug: "theme-flicker"
---

As I wrote yesterday, I celebrated [John Siracusa's every-five-year Hypercritical t-shirt sale](https://hypercritical.co/2023/07/12/hypercritical-t-shirts-return) with a [new Hypercritical Gold Theme](https://scottwillsey.com/hypercritical-theme/) for this site. As with my previous dark/light mode configuration, toggling themes is done with a little icon button at the bottom of the menu that can look like a sun (when in light mode), a moon (when in dark mode), and now a 128k Mac (when in Hypercritical Gold mode).

Theme toggling can cause flickering issues when pages load. The symptom is that when you click a link to go to another page on the site, you see a flash of the wrong colors and then the page quickly switches to your chosen theme colors. This is because when the default colors load first, and then the browser realizes you've set the theme to something else and loads the correct colors. I had this issue myself, but I didn't really notice it when I just had light/dark modes, probably because I was almost always in dark mode. I did notice it right away when I added Hypercritical Gold.

I found two articles addressing this issue, one of which was even written from an Astro perspective.

[Prevent dark mode from flickering on page load in Astrojs](https://axellarsson.com/blog/astrojs-prevent-dark-mode-flicker/)

```html
<head>
  <script is:inline>
    // The configured mode is stored in local storage
    const isDarkMode = localStorage.getItem("darkMode");

    // Set theme to 'dark' if darkMode = 'true'
    const theme = isDarkMode === "true" ? "dark" : "";

    // Put dark class on html tag to enable dark mode
    document.querySelector("html").className = theme;
  </script>
  ...
</head>
```

[Light/dark mode: avoid flickering on reload - DEV Community](https://dev.to/ayc0/light-dark-mode-avoid-flickering-on-reload-1567)

```html
<body>
  <script>
    const theme = localStorage.getItem("theme") || "light";
    document.documentElement.dataset.theme = theme;
  </script>

  <!-- rest of your html -->
</body>
```

They both basically use exactly the same technique – early on in the page, either in the `<head>` section or early in the `<body>` section, have an inline JavaScript that checks your preferred theme setting by seeing what your `localStorage` setting for your theme choice is.

As it happens, I was already doing this. But I was doing it in my menu component, which in turn is called by my Base.astro base layout. Also my script was declared as `<script>` instead of `<script is:inline>`, which in Astro means it was getting bundled by Vite instead of loading directly inline where it was declared. The result of these two factors meant the timing of the script checking the visitor's theme preference was off, and theme flicker was the result.

My first attempt at getting rid of theme flicker was changing the script to use the `is:inline` directive, but this caused a problem. Now the script couldn't find the elements it referred to by ID, namely the theme toggle icons. My assumption is this is because Astro was modifying the element names as part of how it bundled up and rendered the component, but with the JavaScript now being unmodified and unprocessed by Astro, it no longer knew what those were now called.

Because of this, I decided to nuke the menu component and move everything in it into Base.astro. I moved it as is, with the JavaScript above the html for the menu elements, and the script using the `is:inline` directive. Now I had a new variation of the JavaScript can't find html elements issue. For fun, I tried moving the JavaScript down below the menu html, hoping it was still high enough in the page to load the theme quick enough to avoid theme flicker. It seems to have worked – I don't see theme flicker now while using Hypercritical Gold or Light themes. These are the two themes that would show flicker, because Dark theme is the default.

To recap, I no longer have a `Menu.astro` component. My menu is now in my `Base.astro` template. The highlighted part is the JavaScript dealing with loading the correct theme based on the user's preference, and changing themes when the toggle icon is clicked or tapped.

```astro title="src/layouts/Base.astro" {113-189}
---
import { Icon } from "astro-icon/components";
import config from "config";
import Header from "../components/Header.astro";
import Footer from "../components/Footer.astro";
import "../styles/sw2.css";

export interface Props {
  title: string;
  description: string;
  url: string;
}

const { title, description } = Astro.props;
---

<html lang="en" data-theme="dark">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="title" content={title} />
    <meta name="description" content={description} />
    <meta name="view-transition" content="same-origin" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <link
      rel="preload"
      href="/fonts/BlinkMacSystemFont-Medium.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
  </head>
  <body>
    <div id="wrapper-grid">
      <aside>
        <nav id="main-nav">
          <div class="menu">
            <a href="/">
              <div class="menu-item">
                <div class="menu-icon"><Icon name="ri:home-7-fill" /></div>
                <div class="menu-text">HOME</div>
              </div>
            </a>
            <a href="/1">
              <div class="menu-item">
                <div class="menu-icon">
                  <Icon name="ep:copy-document" />
                </div>
                <div class="menu-text">POSTS</div>
              </div>
            </a>
            <a href="/about">
              <div class="menu-item">
                <div class="menu-icon">
                  <Icon name="fluent:info-28-filled" />
                </div>
                <div class="menu-text">ABOUT</div>
              </div>
            </a>
            <a href="/search">
              <div class="menu-item">
                <div class="menu-icon"><Icon name="bi:search" /></div>
                <div class="menu-text">SEARCH</div>
              </div>
            </a>
            <a href={config.social.threads}>
              <div class="menu-item">
                <div class="menu-icon"><Icon name="noto:sewing-needle" /></div>
                <div class="menu-text">THREADS</div>
              </div>
            </a>
            <a href={config.social.mastodon}>
              <div class="menu-item">
                <div class="menu-icon">
                  <Icon name="simple-icons:mastodon" />
                </div>
                <div class="menu-text">MASTO</div>
              </div>
            </a>
            <a href={config.social.github}>
              <div class="menu-item">
                <div class="menu-icon"><Icon name="simple-icons:github" /></div>
                <div class="menu-text">GITHUB</div>
              </div>
            </a>
            <a href="/rss.xml">
              <div class="menu-item">
                <div class="menu-icon"><Icon name="ion:logo-rss" /></div>
                <div class="menu-text">RSS</div>
              </div>
            </a>
            <div class="theme">
              <button id="theme-toggle" aria-label="Switch to dark theme">
                <Icon id="sun-icon" name="octicon:sun-24" />
                <Icon id="moon-icon" name="octicon:moon-24" />
                <svg
                  id="hypercritical-icon"
                  width="24"
                  height="24"
                  viewBox="0 0 48 64"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M44 2H4V0H44.5V2H46V4H44V2ZM46 54V4H48V54H46ZM2 54L46 54V64H2L2 54ZM2 4L2 54H2.14577e-06L0 4H2ZM2 4H4V2H2V4ZM40 8H8V6H40V8ZM40 34V8H42V34H40ZM8 34H40V36H8V34ZM8 34H6V8H8V34ZM15 18V14H17V18H15ZM23 23V14H25V25H21V23H23ZM29 18V14H31V18H29ZM17 29V27H19V29H17ZM27 29V31H19V29H27ZM27 29H29V27H27V29ZM40 46H28V44H40V46ZM10 46V48H6V46H10ZM4 56V62H44V56H4Z"
                  ></path>
                </svg>
              </button>
            </div>
            <script is:inline>
              const themeToggle = document.getElementById("theme-toggle");
              let currentTheme = localStorage.getItem("theme");
              switch (currentTheme) {
                case "light":
                  enableLightTheme();
                  break;
                case "hypercritical":
                  enableHypercriticalTheme();
                  break;
                case "dark":
                  enableDarkTheme();
                  break;
                default:
                  enableDarkTheme();
                  break;
              }

              themeToggle.addEventListener("click", () => {
                if (document.documentElement.hasAttribute("data-theme")) {
                  currentTheme =
                    document.documentElement.getAttribute("data-theme");
                }
                toggleTheme(currentTheme);
              });

              function enableDarkTheme() {
                document.documentElement.setAttribute("data-theme", "dark");
                localStorage.setItem("theme", "dark");
                document.getElementById("sun-icon").style.display = "none";
                document.getElementById("moon-icon").style.display = "inline";
                document.getElementById("hypercritical-icon").style.display =
                  "none";
              }

              function enableLightTheme() {
                document.documentElement.setAttribute("data-theme", "light");
                localStorage.setItem("theme", "light");
                document.getElementById("moon-icon").style.display = "none";
                document.getElementById("sun-icon").style.display = "inline";
                document.getElementById("hypercritical-icon").style.display =
                  "none";
              }

              function enableHypercriticalTheme() {
                document.documentElement.setAttribute(
                  "data-theme",
                  "hypercritical",
                );
                localStorage.setItem("theme", "hypercritical");
                document.getElementById("moon-icon").style.display = "none";
                document.getElementById("sun-icon").style.display = "none";
                document.getElementById("hypercritical-icon").style.display =
                  "inline";
              }

              function toggleTheme(currentTheme) {
                if (currentTheme) {
                  switch (currentTheme) {
                    case "light":
                      enableDarkTheme();
                      break;
                    case "hypercritical":
                      enableLightTheme();
                      break;
                    case "dark":
                      enableHypercriticalTheme();
                      break;
                    default:
                      enableDarkTheme();
                      break;
                  }
                } else {
                  enableDarkTheme();
                }
              }
            </script>
          </div>
        </nav>
      </aside>
      <main>
        <Header />
        <slot />
        <Footer />
      </main>
    </div>
    <script is:inline src="/scripts/barefoot.min.js"></script>
    <script is:inline>
      lf = new BareFoot();
      lf.init();
    </script>
  </body>
</html>
<style>
  nav {
    margin-top: 14rem;
    padding: 2rem;
    background-color: var(--surface-menu);
    border-radius: 10px;
    position: sticky;
    top: 3rem;
  }
  nav div.menu {
    justify-self: center;
    display: grid;
    grid-template-rows: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    row-gap: 1rem;
    justify-items: start;
    width: fit-content;
    padding: 0;
  }

  nav div.menu a {
    color: var(--accent1);
    text-decoration: none;
  }

  nav div.menu a:hover {
    text-decoration: underline;
  }

  .menu-item {
    display: flex;
    flex-direction: row;
    column-gap: 0.5rem;
    justify-content: flex-start;
    align-items: center;
    color: var(--accent1);
    font-size: 0.75rem;
    margin: 0;
    padding: 0;
  }

  .menu-item [data-icon] {
    width: 1.5rem;
  }

  .theme {
    justify-self: center;
  }

  #theme-toggle {
    cursor: pointer;
    background: 0;
    border: 0;
    border-radius: 50%;
  }

  .theme [data-icon] {
    width: 1.25rem;
    color: var(--accent1);
  }

  .theme [data-icon]:hover,
  .theme [data-icon]:focus {
    color: var(--brand);
  }

  .theme #hypercritical-icon {
    width: 1.25rem;
    height: 1.25rem;
    fill: var(--accent1);
  }

  .theme #hypercritical-icon:hover,
  .theme #hypercritical-icon:focus {
    fill: var(--brand);
  }

  .theme [data-icon="octicon:sun-24"],
  .theme svg {
    display: none;
  }

  @media only screen and (max-width: 899px) {
    nav {
      margin-top: 2rem;
    }
    .menu-item {
      column-gap: 1rem;
      font-size: 1.25rem;
    }
    .menu-item [data-icon] {
      width: 1.5rem;
    }
    .theme [data-icon] {
      width: 1rem;
    }
  }
</style>
```

The moral of the story is, grab the user theme preference and set the theme early in the page load lifecycle. With Astro, that means understanding how Astro is optimizing your layouts, components, CSS, and scripts.

In my case, because the JavaScript is loaded above the part of the base template that loads the page content, it seems to work timing-wise to load the theme quickly enough to avoid theme flicker.
