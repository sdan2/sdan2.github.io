---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

<div class="archive-intro">
  <p class="archive-intro__lead">Publications across natural language processing, robustness, reasoning, planning, multimodal learning, and LLM evaluation.</p>
  {% if author.googlescholar %}
    <p>For a complete and regularly updated list, see <a href="{{author.googlescholar}}">Google Scholar</a>.</p>
  {% endif %}
</div>

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
