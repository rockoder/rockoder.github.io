---
title: "The Comfortable Chair Fallacy: Why Your CI/CD is Killing Your Velocity"
date: 2026-02-07
author: "Ganesh Pagade"
tags: ["engineering", "devops", "cicd", "productivity"]
description: "Why treating GitHub Actions as a production runtime for builds instead of a verification step leads to the decay of engineering feedback loops."
draft: true
---

There is a specific kind of developer misery that only exists in the modern era: the `git commit -m "try fix 4"` loop. You wait ten minutes for a CI runner to spin up, pull a Docker image, and fail at the same step. You change one line of YAML and repeat.

We have optimized our CI/CD systems to be "comfortable chairs"—full of helpful UI, ANSI colors, and integrated secrets—while ignoring the fact that the chair is in the middle of a freeway, and we are being hit by the truck of slow feedback loops.

### The Real Problem: Programming in Configuration

The fundamental issue is that we have moved the **Build Logic** out of the repository and into the **Orchestrator**.

GitHub Actions (GHA) is an incredible event dispatcher and execution engine, but it is a terrible place to store your build graph. When you "program in YAML," you are creating a proprietary, unobservable, and non-local runtime for your software. You have created a dependency on a cloud-native black box just to compile your code.

### Why This Exists: The Convenience Trap

The shift happened because GHA made it *too easy* to avoid the hard work of local environment management.

1.  **Secret Management:** It’s easier to put a secret in GHA than to manage a local `.env` or vault.
2.  **Resource Asymmetry:** Your laptop is M1/ARM; your prod is x86. It’s easier to just run it "where it works" (in the cloud) than to fix the cross-compilation mess.
3.  **The "Ops" Hand-off:** Devs want to write code; they don't want to maintain a Makefile. GHA plugins (Actions) feel like a high-level abstraction that makes CI "someone else's problem."

### The Missing Model: Local-First CI

The missing model is **Local-First CI**. In this model, the CI system is strictly a **Verification Step**, not a **Production Runtime** for your builds.

The "Golden Rule" of CI should be: **Any command run in the cloud must be runnable locally with identical results.**

```text
The Local-First Architecture:

[ Local Dev ] --( make test )--> [ SUCCESS ]
      |
[ git push ]
      |
[ GHA Runner ] --( make test )--> [ SUCCESS ]
```

If your CI involves a `step` that isn't just an invocation of a local script (Makefile, Taskfile, etc.), you have introduced a "Verification Gap."

### Tradeoffs and Failure Modes

Maintaining local-equivalency isn't free. It requires **Architectural Discipline**.

*   **The Docker Tax:** You often have to run everything inside Docker locally to match the CI environment, which is slower and eats battery life.
*   **The "Heavy" Laptop:** You can't use $800 "thin-and-light" laptops if you expect every dev to run a 1/50th scale facsimile of the production environment locally.
*   **The Knowledge Barrier:** Devs have to understand `make`, `bash`, or `docker-compose` instead of just copy-pasting YAML from the GHA Marketplace.

### Second-Order Effects: The Velocity Compounder

The second-order effect of fixing this is the **Restoration of Focus**.

When a developer can run the full test suite in 30 seconds on their machine, they stay in "the flow." When they have to wait for GHA, they switch to Slack, then to HN, then to a meeting. The "try fix 4" loop isn't just slow; it's a context-switching engine that destroys senior-level productivity.

Teams that embrace Local-First CI don't just have faster builds; they have better developers because those developers are actually forced to understand how their software is built, rather than treating the build process as a series of magical incantations in a `.github/workflows` folder.

---
*Inspired by the discussion on HN: [GitHub Actions is slowly killing engineering teams](https://news.ycombinator.com/item?id=46892484) and [Things Unix can do atomically](https://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html)*
