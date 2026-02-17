---
title: "The Noise of Throughput"
date: 2026-02-17
description: "How AI-accelerated development creates a DDoS attack on organizational review systems and renders traditional velocity metrics obsolete."
author: "Ganesh Pagade"
draft: false
---

In a Quarterly Business Review (QBR), a VP of Engineering stands before the leadership team and presents a slide titled "Efficiency Gains." The chart shows a 40% increase in pull request volume over the last six months. The narrative is clear: AI has unlocked the engineers. The organization is moving faster.

However, in the engineering pods, the mood is different. Engineering Managers (EMs) are struggling with a review queue that has tripled. Staff Engineers are finding that while code is written faster, it takes twice as long to debug because the author has a "disconnected" relationship with the logic. The organization hasn't actually speed up; it has just increased the volume of its noise.

This is the phenomenon of Velocity Inflation.

## The DDoS of Internal Systems

We are seeing a structural mismatch between the cost of generation and the cost of verification. AI has reduced the cost of generating code, text, and documentation to near-zero. But the cost of verifying that output—ensuring it is secure, maintainable, and correct—remains a human-intensive process.

In many ways, this looks like a distributed denial-of-service (DDoS) attack on the organization's own quality systems. When every individual contributor becomes "5x more productive" at shipping code, the central review systems (code review, security scanning, CI/CD pipelines) are overwhelmed.

The rational response for an individual engineer is to use AI to ship more. They are rewarded for "output" in their performance reviews. But for the system, this individual "productivity" acts like a tax. The Engineering Manager who used to spend two hours a day reviewing code now spends six. The Senior Engineer who used to mentor juniors now spends all their time untangling AI-generated "slop" that technically works but violates architectural principles.

## The Statistical Illusion

The fundamental problem is that we are still using metrics designed for a scarcity-based environment in an abundance-based environment. Traditional velocity metrics—story points, PR counts, deployment frequency—assume that every unit of output represents a proportional unit of human effort and intention.

Under AI, that proportionality collapses. A PR with 500 lines of code might represent thirty minutes of prompting rather than three days of deep work. If management continues to use these numbers to measure "progress," they are effectively measuring noise.

As noted in discussions of Statistical Process Control (SPC), a process that is "out of control" cannot be measured by its averages. When the variance of output increases—because some PRs are hand-crafted and others are machine-spewed—the "average velocity" becomes a useless number. It is a veneer of scientific management applied to a chaotic system.

## The Accumulation of Quality Debt

When the review system is overwhelmed, the organization begins to make trade-offs. To keep the velocity charts looking "healthy" for the QBR, managers may subconsciously lower the bar for what gets merged. "It passes the tests" becomes the new standard, replacing "It is the right way to solve the problem."

This creates a silent accumulation of Quality Debt. This is not traditional technical debt, where you knowingly make a shortcut to ship faster. This is structural debt: code that is in the system but which no human fully understands or feels ownership over.

The long-term consequence is Engineering Immaturity. A mature organization understands the relationship between its inputs and its outputs. An immature one celebrates the volume of its outputs while losing visibility into the health of its systems.

## The Invisible Constraint

The "efficiency gains" touted by executives are often just a transfer of burden. The individual is faster, but the collective is more brittle. The Director captures the credit for the 40% throughput gain, while the EM absorbs the risk of the impending maintenance crisis.

The true constraint on organizational speed is not the rate at which code can be written. It is the rate at which an organization can absorb change without breaking. AI has removed the first constraint, but it has done nothing for the second. In fact, by flooding the system with noise, it has made the second constraint even tighter.

The organizations that survive this shift will not be the ones that ship the most code. They will be the ones that recognize that throughput is a vanity metric in an age of automated generation. They will stop asking "how much did we ship?" and start asking "how much noise did we prevent?"
