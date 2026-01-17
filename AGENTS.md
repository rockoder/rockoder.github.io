# Blog Status Assessment - Jan 2026

This document provides a technical assessment of the rockoder.com blog to assist with future upgrades and maintenance.

## Tech Stack (Modernized)
- **Framework**: [Jekyll](https://jekyllrb.com/) 4.3.4
- **Language**: Ruby 3.3.x
- **Build System**: GitHub Actions
- **Styles**: SCSS with System Font Stack & Dark Mode support
- **Hosting**: GitHub Pages
- **Domain**: www.rockoder.com

## Key Changes in 2026 Upgrade
1.  **Framework Upgrade**: Moved from Jekyll 3.4.1 to 4.3.4.
2.  **Ruby Upgrade**: Moved from EOL Ruby 2.4.2 to Ruby 3.3.
3.  **Deployment**: Switched to GitHub Actions for automated builds and deployments.
4.  **Theme Modernization**:
    *   Converted CSS to SCSS in `assets/css/style.scss`.
    *   Implemented a modern system font stack.
    *   Added automatic Dark Mode support.
    *   Migrated assets from `public/` to `assets/`.
    *   Switched sidebar and contact socials to high-quality SVG icons.
5.  **Analytics**: Migrated to `gtag.js` to support GA4.
6.  **Configuration**: Modernized `_config.yml`.

## Current Configuration (`_config.yml`)
- **URL**: `https://www.rockoder.com`
- **Markdown**: `kramdown`
- **Highlighter**: `rouge`

## Maintenance Notes
- The site is built via the `.github/workflows/jekyll.yml` workflow.
- Styles are managed in `assets/css/style.scss`.
- To update tracking, change `google_analytics` ID in `_config.yml`.

## Resolved Issues
- **Fixed Post Extension**: Renamed `_posts/2026-01-17-website-migration` to `_posts/2026-01-17-website-migration.md`.
- **Legacy Tech Stack**: Upgraded Ruby, Jekyll, and Build system.
- **Legacy Theme**: Modernized typography, icons, and asset organization.
