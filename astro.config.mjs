import { defineConfig } from "astro/config";
import expressiveCode from "astro-expressive-code";
import icon from "astro-icon";
import pagefind from "astro-pagefind";
import { rehypeAccessibleEmojis } from 'rehype-accessible-emojis';
import remarkToc from 'remark-toc';

/** @type {import('astro-expressive-code').AstroExpressiveCodeOptions} */
const astroExpressiveCodeOptions = {
  // Example: Change the themes
  themes: ["material-theme-ocean", "light-plus", "github-dark-dimmed"],
  themeCssSelector: (theme) => `[data-theme='${theme.name}']`,
}

// https://astro.build/config
export default defineConfig({
    site: "https://scottwillsey.com/",
    integrations: [expressiveCode(astroExpressiveCodeOptions), icon(), pagefind()],
    markdown: {
    remarkPlugins: [ [remarkToc, { heading: "contents" } ] ],
    rehypePlugins: [ rehypeAccessibleEmojis ],
  },
});
