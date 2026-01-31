# rockoder.com Blog

This is the source code for rockoder.com, a personal blog built with Astro 5.x, Tailwind CSS v4, and TypeScript.

## 🚀 Project Overview

- **Framework**: Astro 5.17.1
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Deployment**: GitHub Actions to GitHub Pages
- **Content**: 43 blog posts and 79 notes
- **Features**:
  - Homepage, blog archive with tag filters, and all static pages
  - Command palette, reading progress bar, TOC with active highlighting
  - Tag cloud sidebar on homepage and individual posts
  - GitHub Actions deployment workflow

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 📁 Project Structure

```text
/
├── .github/workflows/deploy.yml    # GitHub Actions deployment workflow
├── src/                            # Main source code
│   ├── components/                 # Reusable components
│   ├── content/                    # Blog posts and notes
│   ├── data/                       # Data files
│   ├── layouts/                    # Page layouts
│   ├── pages/                      # Page routes
│   └── styles/                     # Global styles
├── _posts/                         # Legacy Jekyll posts (if any)
├── public/                         # Static assets
├── package.json                    # Dependencies and scripts
└── README.md                       # This file
```

## 🧑‍💻 Development

To start the development server:
```bash
npm run dev
```

To build for production:
```bash
npm run build
```

To preview the production build:
```bash
npm run preview
```

## 🚀 Deployment

The site is automatically deployed to GitHub Pages using the workflow defined in `.github/workflows/deploy.yml`.

## 📝 Content Management

Blog posts are stored in `_posts/` directory with markdown files. Notes are managed through Astro's content collections.

## 👀 Want to learn more?

Feel free to check [Astro documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).
