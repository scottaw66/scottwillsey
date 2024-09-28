import rss from "@astrojs/rss";
import sanitizeHtml from "sanitize-html";
import { rfc2822 } from "../../components/utilities/DateFormat";
import { globalImageUrls } from "../../components/utilities/StringFormat";
import site from "../../data/site.json";

export function GET(context) {
  const postImportResult = import.meta.glob("../../content/reads/**/*.md", {
    eager: true,
  });
  const posts = Object.values(postImportResult).sort(
    (a, b) =>
      new Date(b.frontmatter.date).valueOf() -
      new Date(a.frontmatter.date).valueOf(),
  );

  return rss({
    title: `${site.title} Weekly Reads`,
    description: "Weekly Reads",
    site: context.site,
    xmlns: {
      atom: "http://www.w3.org/2005/Atom/",
      dc: "http://purl.org/dc/elements/1.1/",
      content: "http://purl.org/rss/1.0/modules/content/",
    },
    items: posts.map((post) => ({
      title: post.frontmatter.title,
      link: `${site.url}${post.frontmatter.slug}`,
      pubDate: rfc2822(post.frontmatter.date),
      description: post.frontmatter.description,
      customData: `<summary>${post.frontmatter.description}</summary>`,
      content: globalImageUrls(site.url, sanitizeHtml(post.compiledContent())),
    })),
  });
}
