import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    author: z.string().default('Ganesh Pagade'),
    tags: z.array(z.string()).optional().default([]),
    description: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const notesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tweet_url: z.string().url().optional(),
    tweet_id: z.string().optional(),
    screenshot: z.string().optional(),
  }),
});

const caseStudiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    company: z.string(),
    role: z.string(),
    period: z.string(),
    technologies: z.array(z.string()),
    summary: z.string(),
    impact: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const beyondTheCodeCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional(),
    heroImage: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
  notes: notesCollection,
  'case-studies': caseStudiesCollection,
  'beyondthecode': beyondTheCodeCollection,
};
