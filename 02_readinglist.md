---
layout: page
title: Reading List
description: Books I have read and found worth sharing.
permalink: /reading-list/
---

| Year | Book | Review |
|:-----|:-----|:-------|
{% for book in site.data.books -%}
| {{ book.year }} | [{{ book.title }}]({{ book.link }}) | {% if book.review %}[Review]({{ book.review | relative_url }}){% endif %} |
{% endfor %}
