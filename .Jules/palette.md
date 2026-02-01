## 2025-05-15 - [Enhancing Form Accessibility and Feedback]
**Learning:** Legacy forms often lack programmatic association between labels and inputs, and use "naive" JavaScript to hide/show success messages, leading to a "flash of content" (FOUC) and poor screen reader support. Using `display: none` by default in CSS and properly associating labels with `for`/`id` significantly improves the experience.
**Action:** Always check form labels and success message implementations for accessibility and visual stability.

## 2026-01-26 - [Standardizing Keyboard Navigation and Skip Links]
**Learning:** For sites with a significant sidebar, a "Skip to Content" link is a critical but often overlooked micro-UX win. Additionally, relying on global focus states can be insufficient for specialized components like social icons or custom-styled buttons; explicit `:focus-visible` styling ensures accessibility without degrading the visual experience for mouse users.
**Action:** Always include a skip-to-content link in layouts with sidebars and audit interactive elements for high-contrast focus indicators using `:focus-visible`.

## 2026-01-28 - [Accessible Media and Interactive Code Blocks]
**Learning:** Using `div` with `background-image` for profile photos is a common anti-pattern that hides content from screen readers and prevents standard browser image interactions (like "open image in new tab"). Furthermore, technical readers highly value "Copy" utilities on code blocks, which can be implemented as a progressive enhancement using a small, accessible button injected via JavaScript.
**Action:** Prefer semantic `img` tags over background images for content-carrying visuals. Implement utility features like "Copy to Clipboard" with focus-visible states and clear success feedback.

## 2026-01-28 - [Clarifying Pagination Affordance and Directionality]
**Learning:** Generic "Older" and "Newer" buttons without visual cues or distinct states lead to user confusion, especially when one is disabled but looks identical to the other. Using directional arrows (affordance), swapping placement to match chronological intuition (Newer on the left), and significantly reducing opacity with a `not-allowed` cursor for disabled states provides an immediate, unambiguous mental model for site navigation.
**Action:** Always differentiate active vs. disabled pagination items using both visual (opacity, color) and behavioral (cursor, pointer-events) cues. Ensure button placement aligns with standard user expectations for "Previous/Next" chronological flow.

## 2026-01-30 - [Improving Content Consumption with Scroll Enhancements]
**Learning:** For content-heavy blogs, a reading progress bar provides immediate visual feedback of remaining content, reducing cognitive load. Additionally, smooth scrolling enhances navigation between sections but MUST respect user preferences for reduced motion to ensure accessibility.
**Action:** Implement reading progress indicators as subtle, non-intrusive elements (e.g., at the viewport top). Always wrap `scroll-behavior: smooth` in a `(prefers-reduced-motion: no-preference)` media query.

## 2026-02-05 - [Enhancing Developer Experience with Copy Utilities]
**Learning:** For technical blogs, friction in copying code snippets is a significant UX hurdle. Injecting a "Copy" button directly into `<pre>` elements provides a clear utility. Ensuring the button is visible on hover/focus and provides immediate visual feedback (e.g., icon change to a checkmark) makes the interaction feel responsive and satisfying.
**Action:** Prefer injecting copy utilities via client-side scripts to avoid polluting content source files, and use ARIA labels and focus-visible states for accessibility.
