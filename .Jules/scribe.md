## 2026-02-01 - [Automated Technical Content Extraction from Hacker News]

**Learning:** Automated curation of high-quality technical content from Hacker News requires a multi-layered extraction strategy. `trafilatura` is superior for isolating "clean" article bodies from diverse domains, while internal HN posts (Ask/Show HN) must be treated as first-party content by targeting the `toptext` container. Hierarchical comment extraction is most robust when using the specific `indent` attribute now present in HN's markup, falling back to legacy image-width heuristics only when necessary.
**Implication:** Future curation scripts should prioritize data attributes over structural position to maintain resilience against minor markup changes, and use specialized NLP/scraping libraries like `trafilatura` to ensure expert-level content density without UI clutter.

## 2026-02-17 – The Illusion of Oracle-Driven Correctness

**Learning:** In agentic workflows, passing a test suite (the "oracle") is often mistaken for system maturity. While an oracle provides a feedback loop for functional correctness, it cannot validate architectural integrity, concurrency safety, or performance characteristics that were never encoded in the tests. High-throughput swarm orchestration tends to produce "simulacrums" of architecture—systems that pass the oracle but fail the underlying engineering reality.
**Implication:** Evaluation must move beyond the binary of "tests passed/failed" to include structural audits. Writing should emphasize the risk of "slop patterns" in automated systems that satisfy the surface oracle while introducing deep technical debt.
