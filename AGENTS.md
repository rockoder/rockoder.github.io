# rockoder.com Technical Guide

Technical reference for AI assistants and contributors working on rockoder.com.

## Tech Stack

- **Framework**: Astro 5.17.1
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Hosting**: GitHub Pages
- **Domain**: www.rockoder.com
- **Build**: GitHub Actions (`.github/workflows/deploy.yml`)

## Content Architecture

### Content Collections

All content uses Astro's Content Collections API. Schemas defined in `src/content/config.ts`.

| Collection | Path | Schema Fields |
|------------|------|---------------|
| `blog` | `src/content/blog/` | title, date, author, tags, description, draft |
| `beyondthecode` | `src/content/beyondthecode/` | title, date, description, draft |
| `notes` | `src/content/notes/` | title, date, tweet_url, tweet_id, screenshot |
| `case-studies` | `src/content/case-studies/` | title, company, role, period, technologies, summary, impact, draft |

### Static Data

Non-collection content in `src/data/`:
- `books.ts` - Reading list entries
- `writing.ts` - External publications
- `videos.ts` - Conference talks

## Layouts

| Layout | Used By | Features |
|--------|---------|----------|
| `BaseLayout.astro` | Most pages | Header, footer, SEO |
| `PostLayout.astro` | Blog posts | Reading progress, TOC, tags, share buttons |
| `BeyondTheCodeLayout.astro` | Editorial essays | Reading progress, TOC, share buttons (no tags) |
| `CaseStudyLayout.astro` | Case studies | Company/role header, technologies |

## Navigation

Navigation links defined in `src/components/Header.astro`:

```typescript
const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/blog/', label: 'Blog' },
  { href: '/beyondthecode/', label: 'Beyond the Code' },
  { href: '/notes/', label: 'Notes' },
  { href: '/writing/', label: 'Writing' },
  { href: '/reading-list/', label: 'Reading' },
  { href: '/videos/', label: 'Videos' },
  { href: '/about/', label: 'About' },
];
```

## Styling Conventions

- Use CSS variables: `var(--background)`, `var(--foreground)`, `var(--accent)`, etc.
- Responsive breakpoints: `sm:`, `md:`, `lg:`
- Dark mode via `prefers-color-scheme` media query
- Transitions on interactive elements

## Development Commands

```bash
npm install          # Install dependencies
npm run dev          # Dev server at localhost:4321
npm run build        # Production build to ./dist/
npm run preview      # Preview production build
```

## Adding Content

### New Blog Post

```bash
# Create src/content/blog/your-slug.md
---
title: "Title"
date: 2025-02-16
tags: ["tag"]
draft: false
---
```

### New Beyond the Code Essay

```bash
# Create src/content/beyondthecode/your-slug.md
---
title: "Title"
date: 2025-02-16
description: "Brief description"
draft: false
---
```

## Key Files

- `src/content/config.ts` - Content collection schemas
- `src/components/Header.astro` - Site navigation
- `src/styles/global.css` - Design tokens and global styles
- `astro.config.mjs` - Astro configuration
- `tailwind.config.mjs` - Tailwind configuration
