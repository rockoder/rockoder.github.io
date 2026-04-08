## 2026-02-01 - [Automated Technical Content Extraction from Hacker News]
**Learning:** Automated curation of high-quality technical content from Hacker News requires a multi-layered extraction strategy. `trafilatura` is superior for isolating "clean" article bodies from diverse domains, while internal HN posts (Ask/Show HN) must be treated as first-party content by targeting the `toptext` container. Hierarchical comment extraction is most robust when using the specific `indent` attribute now present in HN's markup, falling back to legacy image-width heuristics only when necessary.
**Implication:** Future curation scripts should prioritize data attributes over structural position to maintain resilience against minor markup changes, and use specialized NLP/scraping libraries like `trafilatura` to ensure expert-level content density without UI clutter.

## 2026-02-24 – Defensibility as a Systemic Divergence
Learning: Organizations often diverge from their stated goals (e.g., privacy) not because of failure or malice, but because of a "defensibility mandate." When the proof of effort becomes more valuable than the outcome, the system naturally optimizes for maximalist data collection. This creates a "trap" where less data is seen as more risk.
Implication: When analyzing organizational behavior, look for the "legibility requirements" imposed by external observers. The tension is often between what is effective and what is defensible.

## 2026-02-24 – The Pragmatism of Parity
Learning: The traditional engineering goal of "improvement" during a migration is a trap that introduces non-linear risk. "Byte-for-byte identical output" is a superior goal because it provides an objective verification signal. AI enables this by handling the tedious translation work that humans naturally resist in favor of refactoring.
Implication: Future writing should highlight where "unidiomatic" but "verifiable" paths are strategically superior to "best practice" paths that introduce behavioral risk.

## 2026-02-24 – Heuristic Collisions
Learning: AI "reasoning" failures are often not a lack of knowledge but a "heuristic collision." A model's linguistic training (e.g., "walking is better for short distances") can override its world-model grounding (e.g., "a car needs to be at a car wash"). The failure is a statistical priority problem, not a semantic one.
Implication: Avoid judging AI capability by instruction-following alone. The real test is the ability to override a plausible linguistic heuristic when it violates a physical or logical constraint.
