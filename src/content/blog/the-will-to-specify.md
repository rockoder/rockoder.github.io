---
title: "The Will to Specify"
date: 2026-02-09
author: "Ganesh Pagade"
tags: ["Engineering", "AI", "Philosophy"]
description: "Why the primary value of an engineer is shifting from the ability to produce code to the discipline of defining system behavior."
draft: false
---

In the traditional model of software development, the act of "building" and the act of "thinking" were inextricably linked. The friction of writing code—managing memory, navigating syntax, and debugging logic—forced a level of deliberate decision-making. To build something, you had to understand it, or at least understand the specific path you were taking through the problem space.

As large language models move implementation costs toward zero, this link is being severed. We are entering a world where we can outsource the "making" entirely, leaving us only with the task of "defining."

This shift is often framed as a liberation. If we no longer need to spend hours debugging a concurrent singleton, we can spend more time on "high-level design." But in practice, the removal of implementation friction often leads to the erosion of functional precision. We are tempted to trade the rigor of a specification for the ease of a "vibe."

The danger of AI-assisted programming is not "hallucination," a technical problem that will likely continue to diminish. The deeper risk is the erosion of the "will to specify." When a model can turn a vague prompt into a running application, it invites us to skip the most difficult part of engineering: the confrontation with irreducible dependencies and edge cases.

A natural language prompt is almost always functionally underspecified. In asking for a "note-taking app," we describe a space of a billion possible programs. Without constraints, the model must guess—making choices about data models and security on our behalf. We become consumers of artifacts rather than producers of systems, reacting to what is generated rather than deliberately constructing what is intended.

This transition changes the role of the engineer from a producer of lines of code to a reviewer of high-density logic.

In this environment, the specification becomes the primary artifact. A well-articulated specification is a compact, high-density definition of behavior—the only moat left when the translation from idea to execution is commoditized. The value of a senior practitioner shifts from speed at the keyboard to the discipline of articulation: exactly how a system behaves under stress, how it handles failure, and what guarantees it must provide.

There is a historical parallel in the move toward higher-level languages and managed runtimes. Each step up the stack required us to relinquish a certain level of control—over memory layout, instruction fetching, or garbage collection—in exchange for reduced mental burden. But in those cases, the loss of control was bounded by the formal semantics of the language. With natural language, the loss of control is unbounded.

"Vibe-based" development produces systems that work on the "happy path" but collapse when they encounter the messy reality of production. Without a rigorous specification, there is no stable ground to stand on when something goes wrong. You cannot verify what you have not defined.

We may see a future where open-source projects revolve entirely around specifications rather than implementations. A community might debate the "idea merge request"—a modular, reusable definition of a business process or a compliance standard—leaving the actual generation of the code to whatever tool is most efficient at the moment.

For the individual engineer, the path forward requires a renewed focus on the foundations of systems thinking. If the implementation is a commodity, then the ability to manage dependencies, to reason about state, and to enforce rigor in the face of "reasonable" guesses becomes the core professional skill. The machines can do the work, but they cannot yet do the thinking.
