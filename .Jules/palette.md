## 2025-05-15 - [Enhancing Form Accessibility and Feedback]
**Learning:** Legacy forms often lack programmatic association between labels and inputs, and use "naive" JavaScript to hide/show success messages, leading to a "flash of content" (FOUC) and poor screen reader support. Using `display: none` by default in CSS and properly associating labels with `for`/`id` significantly improves the experience.
**Action:** Always check form labels and success message implementations for accessibility and visual stability.
