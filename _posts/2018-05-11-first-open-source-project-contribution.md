---
layout: post
title: 'Just Like That I Did My First Open Source Project Contribution'
date: '2018-05-11'
author: rockoder
tags:
- hacking
---

Sometimes, the harder you try, the harder the thing gets. That's the story of your contribution to open source projects so far.

And then all of a sudden, while working in the office on a tight deadline, you find a feature missing in an open source library you are heavily dependent on.

You post on the projects discussion forum and they confirm its missing and welcome you to contribute. You are already overworked and have a tight deadline at the office. There is no way you can do it during office hours. You still can't resist yourself and commit to file a Jira ticket and own it.

Then on Friday night, after all day office fire fighting, you download the source code and look for instructions to build. You trigger the build and go to sleep.

Saturday, you start digging into the code and formulate strategies to fix the issue. You look for relevant unit test which will be affected if the issue is fixed. You run that test and your break point is hit. All set.

Its night by the time you take care of household chores and your 8 months old is finally asleep. You write the first cut. After a couple of hours, you get the unit test working but with lots of TODOs and pending refactoring. You call it a day with confidence to complete in the first half of Sunday.

Sunday morning, your partner reminds you of going out in the afternoon. Meanwhile the refactoring you thought was possible is now somehow not so easy to do. You struggle with one minor issue until afternoon. Finally, post-lunch break, you realise the silly mistake, fix it and clean up the code. You ensure things are building and unit tests passing for the tenth time. You check the PR process for the project one more time. You finally raise the PR.

Next day in office, you constantly check the status of the PR. Are there any review comments? Did I miss something very basic? You wonder how long it will take before this PR is merged. And then in the evening, you get the notification that the PR is merged.

Your first thoughts? That’s it? Just like that? And then you realise just made your first contribution to an open source project. You are happy.

[Here's the PR](https://github.com/apache/camel/pull/2320) you are talking about.
