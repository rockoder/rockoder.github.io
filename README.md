# rockoder.com

Personal website and technical publication built with Astro 5.x, Tailwind CSS v4, and TypeScript.

## Project Overview

- **Framework**: Astro 5.17.1
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Deployment**: GitHub Actions to GitHub Pages
- **Domain**: www.rockoder.com

## Content Sections

| Section | Path | Description |
|---------|------|-------------|
| Blog | `/blog/` | Technical articles, tutorials, book reviews |
| Beyond the Code | `/beyondthecode/` | Essays on engineering leadership, promotion mechanics, organizational systems |
| Notes | `/notes/` | Short-form content and observations |
| Writing | `/writing/` | External publications (Baeldung, Stackify) |
| Case Studies | `/case-studies/` | Professional experience deep-dives |
| Reading List | `/reading-list/` | Books read by year |
| Videos | `/videos/` | Conference talks and presentations |

## Features

- Command palette (Cmd+K)
- Reading progress bar
- Table of contents with active highlighting
- Tag filtering and search
- Dark/light mode support
- RSS feed

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# Opens at http://localhost:4321

# Build for production
npm run build

# Preview production build
npm run preview
```

## Commands

| Command | Action |
|---------|--------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build production site to `./dist/` |
| `npm run preview` | Preview production build locally |
| `npm run astro check` | Run TypeScript diagnostics |

## Project Structure

```
src/
├── components/          # Reusable Astro components
├── content/             # Content collections (Astro Content API)
│   ├── blog/            # Blog posts (markdown)
│   ├── beyondthecode/   # Editorial essays (markdown)
│   ├── case-studies/    # Case study content
│   └── notes/           # Short-form notes
├── data/                # Static data (books.ts, writing.ts, videos.ts)
├── layouts/             # Page layout templates
│   ├── BaseLayout.astro
│   ├── PostLayout.astro
│   ├── BeyondTheCodeLayout.astro
│   └── CaseStudyLayout.astro
├── pages/               # File-based routing
└── styles/              # Global CSS and design tokens
```

## Content Collections

Content is managed via Astro's Content Collections API. Schemas are defined in `src/content/config.ts`.

### Adding a Blog Post

Create `src/content/blog/your-post-slug.md`:

```markdown
---
title: "Post Title"
date: 2025-02-16
author: "Ganesh Pagade"
tags: ["tag1", "tag2"]
description: "Optional description"
draft: false
---

Content here...
```

### Adding a Beyond the Code Essay

Create `src/content/beyondthecode/your-essay-slug.md`:

```markdown
---
title: "Essay Title"
date: 2025-02-16
description: "Brief description of the essay"
draft: false
---

Content here...
```

## Styling

- Uses Tailwind CSS v4 with CSS variables for theming
- Design tokens defined in `src/styles/global.css`
- Dark mode supported via `prefers-color-scheme`
- Colors: `var(--background)`, `var(--foreground)`, `var(--accent)`, etc.

## Deployment

Automatic deployment to GitHub Pages via `.github/workflows/deploy.yml` on push to `master`.
