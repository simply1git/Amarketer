import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Post workflow state mirrors CLAUDE.md gates: only the owner sets `published`.
// The build only renders `published` posts, so a draft merged by mistake
// stays invisible in production.
const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string().max(70),
    description: z.string().max(160),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    status: z.enum(['draft', 'approved', 'published']).default('draft'),
    targetKeyword: z.string(),
    cluster: z.string(),
    offers: z.array(z.string()).default([]), // kb offer/program entry ids used in this post
    hasAffiliateLinks: z.boolean().default(true),
    amazon: z.boolean().default(false), // adds the Amazon-mandated disclosure sentence
  }),
});

export const collections = { posts };
