---
layout: post
title: How to create audio book from any ebook
date: '2013-08-16T20:45:00.000+05:30'
author: rockoder
tags: 
modified_time: '2013-08-24T09:45:23.907+05:30'
blogger_id: tag:blogger.com,1999:blog-101508721195247855.post-1125366516806449009
blogger_orig_url: http://blog.rockoder.com/2013/08/how-to-create-audio-book-from-any-ebook.html
---

English is not my native language. However it was my first language in school. All it means is that I am little slow while reading English. And hence I prefer audio books. There are many other benefits of audio books (like listening while driving etc) but I mainly use them to read out the book in front of me, for me.  

This speeds up the reading and also allows me to highlight important sections in the book (either hard copy or ebook).  

However not all books come with audio book version. I have few ebooks (mainly PDFs) which I really want to read but there is no corresponding audio book available. This was a long pending problem which I solved yesterday.  

I found a generic way to generate audio book for any ebook. Here's how.  

First, you need a good text to speech (TTS) converter software. I have wasted many hours in finding one. The one that would read any text from any application. Finally I found a decent one - [TextAloud](http://www.nextup.com/purchase.html). The default voice is useless and don't judge the software based on that.  

Next, you need a good voice that would sound as natural as possible. And the one that I found most comforting was [Paul from NeoSpeech](http://www.neospeech.com/). A good voice is more critical than the actual TTS software being used. Install this voice and make it your default voice in TextAloud.  

Now open any ebook in TextAloud or simply copy-paste the entire book into the TextAloud. Opening PDF in TextAloud will convert it into plain text. This will insert extra text like page number, page footer etc between each page. You don't want this to be read in your audio book. So copy the plain text generated by TextAloud and paste it in your favor editor (like SublimeText, Notepad++ etc) and find-replace all such text to blank. For page numbers RegEx based find-replace should be done.  

Make sure no garbage text is present. Now copy back this content into the TextAloud and click 'To File'. This will convert the entire book into an audio file. Depending on the size of the text, it will take a while to generate the entire audio file. Be patient.  

For me, a PDF of 3.5 MB had text of around 750 KB. From this text, TextAloud produced audio file of size 1.5 GB.  

While testing the audio book generated, I completed two chapters of the book! Wanna know the name of the book?