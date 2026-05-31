---
title: "The Cost of Universality"
date: 2026-02-16
author: "Ganesh Pagade"
tags: ["engineering", "tooling", "scm", "abstraction"]
description: "Why our reliance on text-based source control has become the primary bottleneck for software intelligence."
draft: false
---

We have long accepted text as the natural state of software. It is the common denominator that allows a developer in 2026 to use tools designed in the 1970s. This universality is a triumph of the Unix philosophy: everything is a file, and files are just bytes that humans can read.

However, this reliance on text is a lossy compression of intent. When we write code, we are thinking in graphs—relationships between functions, types, and modules. We then flatten that multidimensional graph into a linear sequence of characters to save it to disk. Every tool that interacts with that code—the compiler, the IDE, the static analyzer—must then spend significant energy re-constituting the graph from the flattened text.

This re-parsing is often viewed as a minor technical tax, a necessary cost of portability. But in an environment where we increasingly expect machines to reason about code, the cost of universality is becoming a ceiling on intelligence.

The current model of source control treats code as a series of line-based diffs. This works exceptionally well for merging human contributions, where "what changed" can be visually inspected. But for an agent trying to understand the "blast radius" of a change, line-based diffs are almost useless. The agent must parse the entire repository into a temporary structural representation just to answer a simple question about a dependency.

We tend to assume that text is the "golden source" because it is human-readable. But human-readability is a specific constraint, not an inherent property of logic. By insisting that the storage format matches the input format, we force our tools to operate in a state of constant, shallow amnesia. They "forget" the structure of the code the moment the file is saved, only to struggle to remember it the next time a query is made.

The transition to a structural storage model—where code is stored as a queryable graph rather than a flat file—is often resisted on the grounds of interoperability. If the code isn't text, how do we use Git? How do we use GitHub? These are valid concerns, but they highlight a deeper tension: we are preserving the ability to use old tools at the cost of enabling new ones.

The bottleneck in modern engineering is no longer the speed of typing or the cost of storage. It is the latency of understanding. As long as we treat the flattening of logic into text as a default step, we will continue to build increasingly complex layers of "magic" to hide the fact that our tools are working with a degraded representation of our thoughts.
