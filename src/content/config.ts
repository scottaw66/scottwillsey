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

const nowCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)),
  }),
});

const linksCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)),
  }),
});

const pinsCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)),
  }),
});

const usesCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)),
  }),
});

export const collections = {
  posts: postCollection,
  links: linksCollection,
  now: nowCollection,
  pins: pinsCollection,
  uses: usesCollection,
};
