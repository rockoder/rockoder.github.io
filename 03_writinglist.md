---
layout: page
title: Writing List
permalink: /writing-list/
---

Apart from my personal website, I have been writing on few websites. Following is list of articles I have written so far. Have you read any?

|     Date    |                                                    Title                                                    |
|-------------|-------------------------------------------------------------------------------------------------------------|
{% for article in site.data.writing -%}
| {{ article.date }} | [{{ article.title }}]({{ article.link }}) |
{% endfor %}
