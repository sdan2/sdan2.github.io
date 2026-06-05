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
  <p class="archive-intro__note"><span>*</span> equal contribution &nbsp;·&nbsp; <span>^</span> joint advising</p>
</div>

{% include base_path %}

{%- assign papers = site.publications | sort: "date" | reverse -%}
{%- assign current_year = "" -%}
<div class="publications">
{%- for post in papers -%}
{%- assign post_year = post.date | date: "%Y" -%}
{%- if post.year and post.year != "" -%}{%- assign post_year = post.year -%}{%- endif -%}
{%- if post_year != current_year -%}
{%- unless forloop.first %}</ol>{% endunless %}
<h2 class="bibliography-year" id="y{{ post_year }}">{{ post_year }}</h2>
<ol class="bibliography">
{%- assign current_year = post_year -%}
{%- endif -%}
{% include publication-card.html post=post %}
{%- endfor -%}
{%- unless papers.size == 0 %}</ol>{% endunless -%}
</div>
