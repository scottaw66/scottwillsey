import { defineConfig } from "astro/config";
import expressiveCode from "astro-expressive-code";
import pagefind from "astro-pagefind";

// https://astro.build/config
export default defineConfig({
    site: "https://scottwillsey.com/",
    integrations: [expressiveCode(), pagefind()],
});
