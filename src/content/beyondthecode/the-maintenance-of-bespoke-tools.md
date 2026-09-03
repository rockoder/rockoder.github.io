---
title: "The Maintenance of Bespoke Tools"
date: 2026-02-24
description: "Why AI-enabled 'vibe-coding' is reviving Shadow IT and creating a long-term maintenance cliff for engineering organizations."
author: "Ganesh Pagade"
draft: false
---

<p class="drop-cap">The manager was tired of waiting for the platform team to prioritize a new deployment dashboard. He asked a Senior Engineer to spend an afternoon with an AI agent. By the end of the day, they had a custom React app that visualized the entire CI/CD pipeline. It worked perfectly. The team stopped complaining. The platform team's backlog remained untouched.</p>

On paper, this is a productivity win. The team unblocked themselves without consuming centralized resources.

**But in a political organization, every bespoke solution is a future maintenance liability disguised as a present-day efficiency.**

## The Revival of Shadow IT

For decades, IT departments fought "Shadow IT"—the practice of departments buying their own SaaS tools or building their own Excel-macros-turned-databases outside the purview of central governance. Governance won because building software was hard. You needed a budget, a server, and a developer.

AI-enabled "vibe-coding" has lowered the barrier to entry so far that Shadow IT is no longer a budgetary line item; it is a Tuesday afternoon activity.

**We are entering the era of Disposable Software.** If an engineer can build a custom CRM bridge or an incident-response bot in three hours, the hurdle for "build vs. buy" collapses. Why wait six months for a vendor review when you can prompt a solution into existence before the next standup?

## The Spatial Locality of Value

The value of these bespoke tools is spatially local. They solve a specific problem for a specific group of people at a specific point in time.

The Platform Team optimizes for "Organizational Legibility." They want every team to use the same deployment pipeline, the same monitoring stack, and the same architectural patterns. This makes the organization manageable at scale.

The individual Engineer optimizes for "Task Velocity." They want the dashboard *now* so they can finish their feature.

When an engineer vibe-codes a bespoke solution, they are trading Organizational Legibility for Task Velocity. The individual wins, but the organization loses a piece of its shared infrastructure. Multiply this by a hundred teams, and the organization becomes a thicket of incompatible, unmonitored, and undocumented "helper apps."

## The Maintenance Cliff

The "disposable" nature of AI-generated software is an illusion. Software is only disposable if it can be turned off without consequence.

In practice, these bespoke tools often become critical path. The "quick script" that syncs Jira to a custom Slack bot becomes the primary way the Director tracks project status. The "temporary" dashboard becomes the only way the team knows if a deployment failed.

**The debt is deferred, not avoided.**

The maintenance cliff appears when the original author leaves the company or rotates to a new project. The Staff Engineer who inherits the team finds themselves responsible for a suite of apps they didn't build, written in a "vibe-coded" style that prioritizes immediate function over long-term maintainability.

They cannot easily modify these tools because the "intent" of the code was often undocumented—it lived in the context window of the AI agent for three hours and then vanished. To change a feature, they must effectively re-prompt the entire app, hoping the AI doesn't introduce a regression that the author didn't have tests for.

## The VP's Dilemma

From the perspective of a VP of Engineering or a CFO, this looks like a cost-saving miracle. "We didn't need to spend $50k on a vendor license because our engineers built it themselves."

But the balance sheet only captures the *purchase* cost. It does not capture the "Latent Maintenance Cost"—the hours spent by high-salaried Staff Engineers three years from now trying to secure a legacy AI-generated app that has become a critical vulnerability.

The VP sees the immediate headcount efficiency. They do not see the "Complexity Tax" being levied on the organization's future.

## Surface Rationality

This is not a story of "lazy" engineers or "incompetent" managers. Both actors are behaving rationally within their incentive structures.

The Engineer is rewarded for unblocking their team. "Vibe-coding" a solution is the fastest way to earn that reward.
The Manager is rewarded for hitting deadlines. Skipping the vendor review process is a rational way to accelerate.

The conflict is structural. The organization needs standard, legible systems to survive at scale. The individual needs fast, bespoke systems to survive the current sprint. AI has simply given the individual a more powerful weapon in this tug-of-war.

## The Prediction

As vibe-coding becomes the default mode for internal tooling, the emergence of a new organizational layer becomes likely: the **Complexity Auditor**.

Their job will not be to write code, but to hunt down and "de-commission" bespoke AI-generated tools that have outlived their usefulness but refused to die. They will be the organizational antibodies, fighting the spread of Shadow AI to preserve the legibility of the system.

Organizations that fail to develop these antibodies will eventually find their "Core Business" work slowed to a crawl by the sheer friction of maintaining a thousand "simple" bespoke tools.

## Where the Model Fails

The "Bespoke Tool" model might succeed if AI agents become sophisticated enough to maintain *any* codebase, regardless of how it was originally written. If an agent can "understand" a legacy React app as easily as a human can, the maintenance cliff might not materialize.

However, this assumes that AI capability will stay ahead of the complexity generated by AI. It is a race between the speed of entropy and the speed of the agent. History suggests that software entropy is a remarkably resilient force.

## Closing the Idea

The tension between local productivity and global legibility is as old as engineering itself. AI hasn't changed the tension; it has merely increased the frequency of the trade-off.

We are currently in the "honeymoon phase" where the productivity gains are visible and the maintenance costs are still latent. The success of an engineering organization in the next five years will be determined not by how many tools they can prompt into existence, but by how many they can afford to keep.
