---
layout: page
title: Video List
permalink: /video-list/
---

List of some of my favourite videos/courses that I watch/re-watch.

|  #  |                                           Title                                           	|                                                                                  Comment                                                                                  	|
|---- |-----------------------------------------------------------------------------------------  	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
{% for video in site.data.videos -%}
| {{ forloop.index }}. | [{{ video.title }}]({{ video.link }}) | {{ video.comment }} |
{% endfor %}
