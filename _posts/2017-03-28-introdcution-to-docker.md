---
layout: post
title: Introduction to Docker
date: '2017-03-28'
author: rockoder
tags:
- docker
---

Yesterday, I gave a full day training on Docker. It was a introductory level course covering basics of Docker and introducing tools like Docker Compose and Docker Swarm. I also demoed these features and conducted hands-on session.

<iframe src="http://rockoder.com/introduction_to_docker" title="iframe example 1" width="650" height="500"></iframe>

I throughly enjoyed the process of preparation and delivering the training. I think I was able to communicate the material I had planned to deliver and was able to clear the doubts, concepts.

I made my slides as verbose as possible so that the students could follow the steps after the training also.

# Experience with reveal.js

- This time I tried reveal.js based slides. I wanted something text based (preferably Markdown) format for preparing the presentation slides and reveal.js for perfect for it. I was able to prepare all my slides in single Markdown file.
- reveal.js is easy to pick once you have initial setup ready and not expecting something fancy in your presentation slide (see below). I think I spent around 4-5 hours during my preparation in learning, setting up and researching reveal.js. So if you are on tight schedule, it might be a big distraction (its also lots of fun to play around with) and better to stick with tool you are already comfortable with.
- reveal.js and Markdown were does not help you much with diagrams. I explored Typora, however it does not support drawing simple block diagrams (typical high level architectural diagrams) in it. And eventually you end up exporting the image file out of it and embedding it into your md file. I ended up creating/editing images myself.
- Animation of diagrams was another problem I faced. I ended up creating bulk images each showing part of the animation and sliding them one after the other. Need some better way to do this with reveal.js and Markdown.

Anyway, the final output of my slides was satisfying and I would prefer reveal.js instead of using any binary format like PowerPoint etc. In fact, in coming days I plan to convert all my old presentations into reveal.js.

Finally here is the link to my presentation. Press ***s*** key to see the presenter notes:

[http://rockoder.com/introduction_to_docker](http://rockoder.com/introduction_to_docker)

If you want to refer the Markdown code for these slides check out [docker_slides.md](https://github.com/rockoder/introduction_to_docker/blob/master/docker_slides.md) on my github repo.

