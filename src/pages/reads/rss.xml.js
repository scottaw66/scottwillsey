import rss from "@astrojs/rss";
import { experimental_AstroContainer as AstroContainer } from "astro/container";
import { getCollection, render } from "astro:content";
import { transform, walk } from "ultrahtml";
import sanitize from "ultrahtml/transformers/sanitize";
import { rfc2822 } from "../../components/utilities/DateFormat";
import site from "../../data/site.json";

export async function GET(context) {
  let baseUrl = site.url;
  if (baseUrl.at(-1) === "/") baseUrl = baseUrl.slice(0, -1);

  const container = await AstroContainer.create();

  const posts = (await getCollection("reads")).sort(
    (a, b) =>
      new Date(b.data.date).valueOf() - new Date(a.data.date).valueOf(),
  );

  const items = [];
  for (const post of posts) {
    const { Content } = await render(post);
    const rawContent = await container.renderToString(Content);
    const content = await transform(rawContent.replace(/^<!DOCTYPE html>/, ""), [
      async (node) => {
        await walk(node, (node) => {
          if (node.name === "a" && node.attributes.href?.startsWith("/")) {
            node.attributes.href = baseUrl + node.attributes.href;
          }
          if (node.name === "img" && node.attributes.src?.startsWith("/")) {
            node.attributes.src = baseUrl + node.attributes.src;
          }
        });
        return node;
      },
      sanitize({ dropElements: ["script", "style"] }),
    ]);
    items.push({
      title: post.data.title,
      link: `${baseUrl}/reads/${post.id}`,
      pubDate: rfc2822(post.data.date),
      description: post.data.description,
      customData: `<summary>${post.data.description}</summary>`,
      content,
    });
  }

  return rss({
    title: `${site.title} Weekly Reads`,
    description: "Weekly Reads",
    site: context.site,
    xmlns: {
      atom: "http://www.w3.org/2005/Atom/",
      dc: "http://purl.org/dc/elements/1.1/",
      content: "http://purl.org/rss/1.0/modules/content/",
    },
    items,
  });
}
