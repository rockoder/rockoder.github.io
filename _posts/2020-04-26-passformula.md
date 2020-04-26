---
layout: post
title: 'Passformula: Simple Idea to Remember All Your Passwords'
date: '2020-04-26'
author: rockoder
tags:
- hacking, productivity
---

![](https://imgs.xkcd.com/comics/password_strength.png =900x640)

<br/>

---

<img src="https://imgs.xkcd.com/comics/password_strength.png" alt="drawing" height="640" width="900"/>

In this post, I would like to share a simple but highly effective strategy to come up with a strong, unique password each time a new account is created on some website which and which is easy to recall at a later point in time. I call it Passformula, based on the existing [Passphrase](https://en.wikipedia.org/wiki/Passphrase) strategy.

I came up with Passformula around 5 years back when one of my email accounts reported login attempts using my 'favorite' password from a country I had never visited. Luckily the email provider's security check saved my account. But it was a wake-up call for me. It was no longer a bad thing you read in the news but happened to me.

The idea is to create a one time, well-defined formula to derive a password from the name for the service/website domain you're trying to log in. You would apply this formula each time you create an account on any new website. And later use the same formula to get the password at the time of the login.

For example, let's say for any service/website you would apply the following formula to come up with the password:
- The second letter of the website in the upper case
- Last letter of the website in lower case
- Convert the first vowel in the website name to a digit (assign digit like a is 1, e is 2, i is 3, o is 4, and u is 5)
- Find the total number of characters in the website name. Calculate the sum of the digits of this number until sum becomes a single digit. Use the special character on your keyboard at this digit key.
- Your favorite word. This remains the same in all passwords. Try to choose, non-dictionary word. Ex: Taleb, Pani (Water in Hindi/Marathi). Convert to LEET code. So Taleb would become T@l3b. This part is mainly to get the total length of the password greater than 8 chars.

If we apply this formula say while signing up on grammarly.com, our password would be: Ry1(T@l3b

This is a strong password, high probability of being unique and you don't have to remember it. Just remember the formula and next time when you have to log in to this website you will be able to 'recall' the password easily.

Let's take one more example. Say you use service like zenkit.com. Based on the above formula your password will be: Ei2^T@l3b

As you can see, there are many ways you could create your formula. In the above example, I have shown how to create a password with the first 4 characters unique. But you can go to any extent, as long as you could remember the formula.

Before I wrap up, here are some special cases I encountered while using the pass formula:
1. The website that does not support all special characters, and we have to pick from the list provided by them. You might want to avoid an uncommon special character or keep a fall back formula for such a scenario.

2. Some websites need a periodic password update. Usually the period in 1 to 3 months. In such cases, instead of using your favorite word at the end of the password (Taleb, in the above example), use the month in which you are setting the password. Ex: April could become @pri1. Hopefully, your frequency to visit such websites in higher than the rotation period and you could guess the correct password in a few attempts worst case.

3. If you are using the special character formula mentioned in the above example, you would have to know the QWERTY keyboard layout for special characters. This may not be the case when say you are using mobile. Keeping the QWERTY keyboard image handy on mobile could be a solution to solve this problem.

Hope you find this useful. Let me know what you think.

Disclaimer - Needless to say, this is just a strategy to create a password and does not automatically make your account full proof.