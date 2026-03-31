import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blogCollection = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.date().or(z.string()).transform(val => new Date(val)),
    ogImage: z.string().optional(),
    tags: z.array(z.string()).optional(),
    canonicalUrl: z.string().optional(),
    series: z.string().optional(),
    seriesLabel: z.string().optional(),
    part: z.number().optional(),
    heroImage: z.string().optional()
  })
});

export const collections = {
  'blog': blogCollection,
};
