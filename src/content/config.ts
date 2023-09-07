import { z, defineCollection } from "astro:content";

const postCollection = defineCollection({
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      link: z.string().optional(),
      date: z.string().transform((str) => new Date(str)),
      keywords: z.string().array(),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      series: z.string().optional(),
    }),
});

export const collections = {
  posts: postCollection,
};
