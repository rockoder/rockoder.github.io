---
title: "The Inflation of Legibility"
date: 2026-02-17
description: "How AI-driven output volume breaks traditional engineering performance metrics and creates a hidden quality tax."
draft: false
---

In many engineering organizations, the primary friction in management is not the speed of code production, but the cost of verifying its intent. The hierarchy requires legibility—a way for those who do not write the code to measure the value of those who do. For decades, this legibility has been built on proxies: pull request counts, story points, and lines of code.

The introduction of high-velocity generative tools has not merely shifted the speed of production; it has inflated the currency of these proxies. When the cost of generating a three-hundred-line function drops to near zero, the line of code ceases to be a unit of value and becomes a unit of noise. Yet, the organizational systems that govern promotions and performance reviews are often the last to recalibrate.

The incentive mismatch is structural. A manager under pressure to demonstrate efficiency gains is naturally inclined to celebrate an increase in throughput. The senior engineer, tasked with reviewing this output, often experiences this not as a productivity gain but as a quality tax. They find themselves in the role of a permanent auditor, sifting through blocks of repetitive code that appear functional but fail on closer examination of edge cases or long-term maintainability.

This creates a veneer of control. The dashboards show velocity trending upward, while the underlying system becomes increasingly brittle. The soft unknowns of software craft—the knowledge of why a specific abstraction was chosen—are often discarded because they are not legible to automated tracking systems. In this environment, the engineer who optimizes for the metric by shipping high volumes of superficially functional code is rewarded, while the engineer who spends time consolidating abstractions or identifying risks is seen as a bottleneck.

The mental model shifts from Output Capital—the ability to produce artifacts—to Judgment Capital—the ability to discern which artifacts are worth keeping. However, judgment is harder to measure than volume. It requires more management bandwidth and a deeper technical understanding from leadership than standard objective-based management allows.

When an organization fails to differentiate between these two types of capital, it enters a feedback loop of velocity inflation. The more the system prioritizes legible output, the more quality debt it accumulates. Eventually, the cost of auditing the generated noise exceeds the value of the speed gains, leading to a state where the organization moves faster while achieving less. The pervasive sense that a system is being built by dozens of uncoordinated agents is the primary signal that the legibility system has decoupled from reality.
