---
title: "From $11/Month to $0: How I Used AI to Reclaim My Evening"
date: 2026-01-17
author: "Ganesh Pagade"
tags: ["tools", "tutorial"]
draft: false
---

## The Problem

I had a small web application running on AWS EC2. It was a Spring Boot app with Thymeleaf templates that collected form submissions and sent email notifications. Traffic was minimal. A few hundred requests per month at most.  
Yet the AWS bill was eleven dollars every month.

For a side project with negligible usage, that felt unjustifiable. The EC2 instance sat idle 99.9 percent of the time, costing money simply by existing.

I already knew the right solution: migrate to a static site with serverless functions. Cloudflare Pages and AWS Lambda both offer generous free tiers, enough to bring the cost to zero. The architecture was obvious. The migration path was straightforward.

What I didn’t want was to spend three evenings relearning JavaScript syntax, debugging CORS issues, and stitching together infrastructure glue code. I’ve done that many times before. This time, I wanted the outcome without the friction.

---

## The Migration

The application itself was simple. The Thymeleaf templates were roughly ninety-five percent static HTML. Only a handful of things were dynamic: date dropdowns and flash messages generated server-side. That made it an ideal candidate for static hosting with a thin serverless backend.

I started with a blunt prompt. I shared the codebase and explained the constraint:

> “This costs me $11 per month to run. The load is extremely low. I want the cost to be zero.”

The AI validated the approach and helped outline a concrete plan.

On the frontend, the AI replaced the remaining Thymeleaf logic with plain JavaScript: generating date dropdowns client-side, handling form submissions via `fetch`, and integrating Google reCAPTCHA.

On the backend, it produced a Node.js Lambda handler with infrastructure-as-code configuration, multiple endpoints for different form types, and a `DRY_RUN` mode for local testing without real SMTP credentials.

This is boilerplate I’ve written dozens of times over the years. The difference was that the AI generated it in minutes, not hours, and I didn’t have to context-switch into tooling I rarely touch anymore.

---

## Where AI Actually Added Value

The most interesting part wasn’t code generation. It was problem-solving during integration.

When local form submissions failed due to reCAPTCHA being restricted to the production domain, the AI suggested using Google’s test reCAPTCHA keys for development. These keys always pass validation on localhost. I didn’t know they existed.

Better yet, it updated the code to automatically switch between test and production keys based on hostname. That was a thoughtful solution, not a generic one.

Later, I mentioned that I didn’t want to configure Gmail credentials just to test things locally. I wasn’t asking for a feature. I was stating a constraint.

The AI inferred the missing requirement and implemented a `DRY_RUN` mode that logged email contents to the console instead of sending them. That proactive inference saved real time and friction.

It also suggested using Cloudflare Pages for hosting. That turned out to be simpler than my original plan, with unlimited bandwidth on the free tier, custom domains, and free SSL.

---

## The Results

After deployment, I submitted a test form. An email arrived immediately.

Total time from first prompt to working production deployment was one evening. Most of that time was spent waiting for deployments and reviewing generated code, not writing it.

The monthly cost dropped from roughly eleven dollars to zero. Everything now runs on free tiers: Lambda for compute, API Gateway for routing, Cloudflare Pages for hosting, and CloudWatch for logging.

That’s an annual saving of about one hundred thirty-two dollars. For a low-traffic side project, that effectively means I’m no longer paying anything to keep it alive.

---

## What I Learned

The real lesson here is leverage.

I didn’t need to *learn* JavaScript, Node.js, or Cloudflare Pages. I needed those pieces implemented correctly so I could move on. The AI handled execution. I focused on architecture, constraints, and review. That’s the correct division of labor.

More importantly, the AI was good at inferring intent. When I said I didn’t want to configure Gmail credentials, I wasn’t asking for a feature. I was exposing a constraint. The AI filled in the gap between what I said and what I actually needed.

That’s where these tools become genuinely useful: not as code generators, but as force multipliers that translate intent into implementation.

My final prompt was simple:

> “Write documentation assuming you won’t be here next time.”

The AI produced a comprehensive README with exact commands, configuration values, and troubleshooting steps. Six months from now, I won’t remember any of this. The documentation will.

---

## Conclusion

I completed a full architecture migration in one evening by delegating low-leverage implementation work to an AI while keeping ownership of decisions and constraints.

The AI handled the busywork: JavaScript, infrastructure configuration, CORS issues, deployment scripts, and documentation. I handled judgment.

This is what AI assistants are actually good for. Not replacing engineers, but letting them operate outside their daily stack without paying the cognitive tax of relearning everything from scratch.

I could have done this migration myself. I chose not to. My time is more valuable than eleven dollars a month.

Now, if you’ll excuse me, I have an EC2 instance to terminate.
