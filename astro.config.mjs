import { defineConfig } from "astro/config";
import expressiveCode from "astro-expressive-code";
import pagefind from "astro-pagefind";
import { rehypeAccessibleEmojis } from "rehype-accessible-emojis";
import remarkToc from "remark-toc";
import { remarkYouTubeLinks } from "./src/components/utilities/remark-social-links.mjs";
import { remarkMastodonLinks } from "./src/components/utilities/remark-social-links.mjs";
import { remarkThreadsLinks } from "./src/components/utilities/remark-social-links.mjs";

/** @type {import('astro-expressive-code').AstroExpressiveCodeOptions} */
const astroExpressiveCodeOptions = {
  // Example: Change the themes
  themes: ["material-theme-ocean", "light-plus", "github-dark-dimmed"],
  themeCssSelector: (theme) => `[data-theme='${theme.name}']`,
};

// https://astro.build/config
export default defineConfig({
  site: "https://scottwillsey.com/",
  integrations: [expressiveCode(astroExpressiveCodeOptions), pagefind()],
  markdown: {
    remarkPlugins: [
      [remarkToc, { heading: "contents" }],
      remarkYouTubeLinks,
      remarkMastodonLinks,
      remarkThreadsLinks,
    ],
    rehypePlugins: [rehypeAccessibleEmojis],
  },
});
