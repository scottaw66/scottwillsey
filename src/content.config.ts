import { z, defineCollection } from "astro:content";
import { glob } from "astro/loaders";

const postCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/posts" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      link: z.string().optional(),
      date: z
        .string()
        .transform((str) => new Date(str))
        .optional()
        .nullable(),
      keywords: z.string().array(),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      series: z.string().optional(),
      draft: z.boolean().optional(),
    }),
});

const changeCollection = defineCollection({
  loader: glob({
    pattern: "**/[^_]*.{md,mdx}",
    base: "./src/content/changelog",
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z
      .string()
      .transform((str) => new Date(str))
      .optional()
      .nullable(),
  }),
});

const nowCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/now" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z
      .string()
      .transform((str) => new Date(str))
      .optional()
      .nullable(),
  }),
});

const linksCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/links" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z
      .string()
      .transform((str) => new Date(str))
      .optional()
      .nullable(),
  }),
});

const reviewsCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/reviews" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z
      .string()
      .transform((str) => new Date(str))
      .optional()
      .nullable(),
  }),
});

const usesCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/uses" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z
      .string()
      .transform((str) => new Date(str))
      .optional()
      .nullable(),
  }),
});

const readsCollection = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/reads" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z
      .string()
      .transform((str) => new Date(str))
      .optional()
      .nullable(),
    keywords: z.string().array(),
  }),
});

export const collections = {
  posts: postCollection,
  changelog: changeCollection,
  links: linksCollection,
  reviews: reviewsCollection,
  now: nowCollection,
  reads: readsCollection,
  uses: usesCollection,
};
