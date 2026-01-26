## 2025-05-15 - [Enhancing Form Accessibility and Feedback]
**Learning:** Legacy forms often lack programmatic association between labels and inputs, and use "naive" JavaScript to hide/show success messages, leading to a "flash of content" (FOUC) and poor screen reader support. Using `display: none` by default in CSS and properly associating labels with `for`/`id` significantly improves the experience.
**Action:** Always check form labels and success message implementations for accessibility and visual stability.

## 2026-01-26 - [Standardizing Keyboard Navigation and Skip Links]
**Learning:** For sites with a significant sidebar, a "Skip to Content" link is a critical but often overlooked micro-UX win. Additionally, relying on global focus states can be insufficient for specialized components like social icons or custom-styled buttons; explicit `:focus-visible` styling ensures accessibility without degrading the visual experience for mouse users.
**Action:** Always include a skip-to-content link in layouts with sidebars and audit interactive elements for high-contrast focus indicators using `:focus-visible`.
