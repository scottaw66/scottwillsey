import { z, defineCollection } from "astro:content";

export const collections = {
  posts: defineCollection({
    schema: z.object({
      title: z.string(),
      description: z.string(),
      link: z.string().optional(),
      date: z.string().transform((str) => new Date(str)),
      keywords: z.string().array(),
      series: z.string().optional(),
    }),
  }),
};
