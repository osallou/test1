---
layout: home
title: subdir
---
# subdir
 blabla 
site.categories: container subdir
<ul>{% for post in site.categories.subdir %}{% if post.url %}<li><a href="{{ post.url }}">{{ post.title }}</a></li>{% endif %}{% endfor %}</ul>