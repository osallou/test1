---
# You don't need to edit this file, it's empty on purpose.
# Edit theme's home layout instead if you wanna make some changes
# See: https://jekyllrb.com/docs/themes/#overriding-theme-defaults
layout: home
---
<h1>Containers</h1>
<table class="table tbale-striped">
<thead class="thead-inverse">
<th>Container</th>
</thead>
<tbody>




{% for page in site.pages %}
  {% if page.title %}
    {% if page.title contains "404" %}
    {% else %}
      <tr><th scope="row"><a title="{{ page.title }}" href="{{ page.url | prepend: site.baseurl }}">{{ page.title }}</a></th></tr>
    {% endif %}
  {% endif %}
{% endfor %}

</tbody>
</table>

<h1>Recent uploads</h1>
<ul>
{% for post in site.categories.container limit:10%}
    <li><a title="{{ post.title }}" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a></li>
{% endfor %}

</ul>
