---
layout: post
title: "The Theory Building Debt of AI Agents"
date: 2026-01-26 09:00:00 -0800
categories: engineering leadership
---

The current discourse around AI-assisted coding is obsessed with "velocity"—the speed at which an agent can convert a natural language prompt into a working pull request. But for the senior engineering leader, velocity is a trailing indicator. The real metric of a software organization is not lines of code produced, but the density and accuracy of the "theory" held by its developers.

### The Real Problem

The real problem is not that AI "hallucinates" or produces buggy code. We have always had junior engineers who hallucinate and produce buggy code. The problem is **the severance of the developer from the act of theory building.**

When an AI agent "vibecodes" a 500-line refactor to fix a 10-line bug, the resulting code may pass every test in the suite. However, if the developer cannot articulate *why* that specific structure was chosen over another, the "theory" of the program has not been transferred to a human mind. The software is no longer a living reflection of human intent; it is a fossilized artifact of a statistical average.

### Why This Exists

This state exists because of two misaligned incentives:
1.  **Management's faster-horse fallacy:** Leadership sees AI as a way to increase throughput without understanding that software is a knowledge-capture exercise, not a manufacturing process.
2.  **The "Reverse Centaur" trap:** To maintain the illusion of velocity, developers become passive filters for AI output. They spend their time squinting at diffs rather than constructing mental models. Reviewing is lower-friction than building, but it is also lower-signal for learning.

### The Missing Model: Programming as Theory Building

In 1985, Peter Naur proposed that **"programming is not the production of a program; it is the building of a theory of how the program matches the real-world problem."**

In this model, the source code is merely an incomplete representation of the theory. The *actual* program exists in the shared mental models of the engineering team.

| Act | Traditional Model | AI-Agentic Model |
| :--- | :--- | :--- |
| **Writing** | Building the theory | Prompting a "best guess" |
| **Reading** | Refining the theory | Auditing for "vibes" |
| **Refactoring** | Evolving the theory | Overwriting with new slop |

When we outsource the "writing" to an agent, we skip the cognitively expensive process of building the theory. We are essentially taking out a "knowledge loan" with a compounding interest rate.

### Tradeoffs and Failure Modes

This doesn't mean AI agents are useless. The tradeoff is **Utility vs. Insight.**

*   **Failure Mode 1: The Paper Plane.** The code looks like an airplane and flies like an airplane, but it lacks structural integrity. It fails under the first custom requirement that wasn't in the agent's training data.
*   **Failure Mode 2: The "Failure to Launch" for Juniors.** If entry-level engineers never have to "ride the CPU" or manage memory manually because an agent does it, they never build the foundational theories required for senior-level judgment.

### Second-Order Effects

If we continue to optimize for agentic velocity at the expense of human theory building, we will see:
1.  **Maintenance Inversion:** Organizations will spend more on "incident response" and "slop cleanup" than they ever saved on initial development.
2.  **The Senior Gap:** A generation of developers who can "audit" code but cannot "author" it, leading to a critical shortage of architects who can see the system-level second-order effects.

**This is the crux:** Velocity is the price we pay for a hollowed-out understanding of our own systems. True engineering maturity is the restraint to use AI for the *mechanics* while keeping the *theory* firmly in human hands.
