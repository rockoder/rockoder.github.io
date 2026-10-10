---
title: "The Judgment Vacuum: What's Left When Code Is Free"
date: 2026-08-29
description: "AI has collapsed the cost of writing code, but not the cost of deciding what to build. Most engineering organizations still measure the wrong one."
author: "Ganesh Pagade"
draft: true
---

<p class="drop-cap">The staff engineer walked into the H2 planning review with three initiatives already specced, cost-estimated, and half-built. Over the weekend, the AI had generated the scaffolding, the tests, and two working prototypes. What it had not done was tell her which of the three problems was worth solving. The review deck had a column for delivery readiness and none for problem fit; when she raised the question of whether any of the three should be built at all, the VP running the meeting nodded, said "good problem to have," and asked which one could ship first. Standing in front of the roadmap slide, she realized she could not remember the last time someone had asked her to decide something — only to produce something.</p>

**Code got cheap. Judgment didn't. The gap between them is where careers now live or die.**

## The Mechanism

For most of the industry's recent history, seniority in engineering correlated with production. The senior person shipped more, touched more of the codebase, closed more tickets, reviewed more PRs. Velocity was a noisy proxy, but it was a proxy — and it was legible enough to build promotion cycles around.

AI breaks the proxy without breaking the intent behind it. When a model can generate scaffolding, tests, and a working prototype over a weekend, first-draft production stops being scarce — the rough version of a feature that used to take a sprint now takes an afternoon. Production-grade delivery is a different claim. Integration with existing systems, security review, operational readiness, on-call ownership, and the coordination required to ship into a live organization remain exactly as scarce as they were — and in some cases scarcer, since the volume of AI-generated code arriving at that gate has gone up. What's changed is where the bottleneck sits in the pipeline, not whether a bottleneck exists.

The organization still needs the same things it always needed — the right problem solved at the right time, in a way that doesn't create three more problems downstream — but the bottleneck that used to sit at "can this get built" has moved upstream, to problem selection, sequencing, and the tradeoff calls that determine whether the thing that got built cheaply should have been built at all.

Judgment isn't one skill; it's a bundle of specific calls. **Problem selection** — which of ten pursuable ideas actually reduces the constraint that matters. **Sequencing** — what has to happen first so the rest doesn't have to be redone. **Reversibility** — which decisions can be undone next sprint and which one locks in an architecture for three years. **Risk assessment** — what happens if this is wrong, and how the organization would find out. **Architecture** — whether the system this weekend's prototype extends can bear the load a full rollout would put on it. **Stakeholder tradeoffs** — whose timeline, budget, or political capital gets spent, and whether they know it. AI can execute against any of these once a human has made the call. It has no mechanism for making the call itself, because none of them are questions about code — they're questions about the organization's constraints, and AI has no stake in those constraints.

This is the part that doesn't show up in a diff. Judgment shows up in the option that was never pursued, the meeting where a plan got killed before it consumed a quarter, the tradeoff nobody bothered to write down because the alternative was obviously worse. None of that produces an artifact. All of it produces value.

Performance systems haven't caught up, and the lag isn't an oversight — it's structural. Those systems were built to measure what AI now produces faster and cheaper as a first draft. They were never built to measure what remains scarce, because until recently, scarcity and production were the same thing.

## Why Organizations Can't See It

Cycle time. PR count. Story points closed. These metrics measure throughput, and first-draft throughput is exactly what AI has commoditized. The metrics didn't get worse — they got partial, and nobody updated the dashboard to say so.

Calibration sessions and promotion committees run on comparable narratives. "Shipped the migration." "Reduced latency by 40%." "Owned the rollout." These are portable, defensible, and easy to rank against a peer's equally portable narrative. A rejected initiative has no comparable artifact. Nobody writes "prevented the team from spending a quarter on a feature that would have failed" into a promo packet, because there's no ticket, no demo, no before-and-after chart to attach to it.

The managers running these committees were promoted through the same system. They learned to recognize a bad decision in hindsight — the postmortem, the deprecated service, the six-month detour — but they were never trained to recognize a good decision in real time, because good decisions of this kind rarely announce themselves. **A bad decision avoided produces no roadmap slide, no demo, no Slack thread. It produces nothing, and nothing reads as nothing happened.**

<blockquote class="pull-quote">Review that moves at generation speed isn't supervision — it's rubber-stamping with extra steps.</blockquote>

## Named Failure Modes

**The Throughput Trap.** Engineers and their organizations keep optimizing AI-assisted output volume, because it's still the easiest axis to measure — even after it stops correlating with anything the business cares about. The dashboards report record velocity. The roadmap doesn't move any faster toward outcomes that matter, because velocity was never the constraint on outcomes. It just used to look like one, back when producing code and deciding what to produce took roughly the same amount of effort.

**The Judgment Vacuum.** For most of a career, the question senior engineers answered was "can you build X." They got very good at answering it — good enough that "can you build X" started to feel like the whole job. AI removes most of the first-draft building bottleneck, which exposes a second question that was always there and almost never asked out loud: "should we build X." Most engineers were never coached on how to answer it, because for most of their careers, someone else — a PM, a founder, a director three levels up — was implicitly answering it for them by deciding what got prioritized. Now the answer is needed faster and more often, and the muscle for producing it hasn't been trained.

<blockquote class="pull-quote">AI didn't remove the bottleneck from engineering. It moved it upstream, to the question nobody's tracking.</blockquote>

**The Delegation Illusion.** Engineers tell themselves they're supervising the AI — reviewing its output, catching its mistakes, staying in the loop. That's true when the review is slow enough to matter: tracing a change through the systems it touches, asking what breaks under load, checking whether the failure mode is the one that took down a similar service two years ago. That kind of review is judgment, exercised at the point of contact with the code. The illusion shows up when review speed matches generation speed — when PRs get approved not because they were checked against the system's actual failure modes, but because nothing in them pattern-matched to an obvious error. **The problem isn't reviewing AI output. It's reviewing it too fast to catch what only shows up under real conditions.** The engineer who merges three AI-generated PRs before lunch has been productive. Whether judgment was exercised doing it is a separate question, and it's the one that's gone quiet.

## Where This Breaks

This argument has edges, and it's worth being precise about them.

Regulated and safety-critical domains still require rigorous code-level scrutiny. A model generating a payment-processing diff or a flight-control routine doesn't get a pass on review because the org has decided judgment matters more than syntax. In these contexts, judgment doesn't substitute for review — it sits alongside it, and the review itself is where a meaningful share of the judgment lives.

Judgment also doesn't emerge from nowhere. It's built from years of hands-on contact with systems that broke in specific, memorable ways. An engineer who has never personally debugged a race condition at 2 a.m. is not well positioned to smell one in a design doc. Early-career engineers still need that contact — not because writing code is inherently virtuous, but because it's the raw material judgment is made from. Skipping it doesn't produce a faster path to judgment. It produces the absence of it.

Which is also why this isn't an argument for engineers to stop writing code. Direct contact with the system — reading the diff, running the query, feeling where the abstraction leaks — is often what keeps judgment calibrated against reality rather than drifting into abstraction for its own sake. **The goal isn't less code. It's code that stops being the primary signal of value.**

And some organizations already structure for exactly this. Staff-plus tracks that explicitly reward technical direction over output. RFC and design-doc cultures that make the tradeoff conversation a first-class, reviewable artifact. In these places, a killed initiative already has a paper trail, and the judgment behind it is already legible to a promotion committee. The critique here targets the common case — the org still running promo cycles on shipped-feature counts — not the universal one.

## Implications

If a promotion case still rests primarily on volume of code shipped, that case is expiring faster than most people building it have noticed. Not because the code stopped mattering, but because first-draft volume stopped being scarce, and scarcity is what promotion cases have always secretly been about.

The artifact that will carry weight going forward isn't a shipped feature. It's a documented tradeoff. A killed initiative with a clear rationale attached. A "no" that held under pressure from a VP who wanted the feature anyway, and turned out to be right. These are harder to produce on demand than a PR, and much harder to fake.

For managers and promotion committees, this is a process problem before it's an evaluation problem. If the packet template only has fields for shipped work, a killed initiative has nowhere to go — and the engineer who killed it will quietly stop bringing decisions and start bringing demos instead, because demos are what get rewarded. The fix isn't a new rubric line called "judgment"; that just adds another vague axis to score. It's asking, in every calibration conversation, for the option that was rejected and why, with the same rigor applied to the option that was chosen.

Nobody will ever ask an engineer to prove what they correctly chose not to build. That's the whole problem, and it isn't going to fix itself by being named.