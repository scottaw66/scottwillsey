import { z, defineCollection } from "astro:content";

const postCollection = defineCollection({
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      link: z.string().optional(),
      date: z.string().transform((str) => new Date(str)).optional().nullable(),
      keywords: z.string().array(),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      series: z.string().optional(),
    }),
});

const changeCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)).optional().nullable(),
  }),
});

const nowCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)).optional().nullable(),
  }),
});

const linksCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)).optional().nullable(),
  }),
});

const pinsCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)).optional().nullable(),
  }),
});

const usesCollection = defineCollection({
  type: 'content', // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string().transform((str) => new Date(str)).optional().nullable(),
  }),
});

export const collections = {
  posts: postCollection,
  changelog: changeCollection,
  links: linksCollection,
  now: nowCollection,
  pins: pinsCollection,
  uses: usesCollection,
};
