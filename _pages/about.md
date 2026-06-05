---
permalink: /
title: 
excerpt: "Machine Learning researcher focused on LLM agents, robustness, and efficient reasoning systems."
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<section id="about" class="page-section">
  <header class="page-section__head">
    <p class="eyebrow">Bio</p>
  </header>
  <p class="bio__lead">I build reliable language and agentic systems with an emphasis on reasoning, robustness, memory, and efficient learning.</p>
  <p class="bio__summary">I am a Machine Learning Researcher at Scale AI working on LLM agents. Previously, I was a Senior Research Scientist at Microsoft working on Copilot and a Research Scientist at IBM Research. I completed my Ph.D. in Computer and Information Science at the University of Pennsylvania, where I was advised by Prof. <a href="https://www.cis.upenn.edu/~danroth/">Dan Roth</a> in the <a href="https://cogcomp.seas.upenn.edu/">Cognitive Computation Group</a>. Before that, I earned my undergraduate degree in Computer Science from IIT Kharagpur, where I was awarded the President of India Gold Medal.</p>
</section>

<section id="publications" class="page-section">
  <header class="page-section__head">
    <p class="eyebrow">Publications</p>
    <h2 class="page-section__title">Selected and recent work</h2>
  </header>
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
<h3 class="bibliography-year" id="y{{ post_year }}">{{ post_year }}</h3>
<ol class="bibliography">
{%- assign current_year = post_year -%}
{%- endif -%}
{% include publication-card.html post=post %}
{%- endfor -%}
{%- unless papers.size == 0 %}</ol>{% endunless -%}
</div>
</section>

<section id="cv" class="page-section" markdown="1">

<header class="page-section__head">
  <p class="eyebrow">Curriculum Vitae</p>
  <h2 class="page-section__title">Education, experience, and awards</h2>
</header>

### Education

- B.Tech. in Computer Science and Engineering, Indian Institute of Technology (IIT) Kharagpur
- Graduate study in Computer Science, University of Illinois Urbana-Champaign
- Ph.D. in Computer and Information Science, University of Pennsylvania

### Work experience

- **February 2026 – Present** &middot; Machine Learning Research Scientist, **Scale AI**, New York City
- **September 2024 – January 2026** &middot; Senior Research Scientist, **Microsoft**, New York City
- **September 2022 – 2024** &middot; Research Scientist, **IBM Research**, Yorktown Heights
- **Summer 2019** &middot; Research Intern, **RIKEN AIP**, Tokyo (Prof. Masashi Sugiyama)
- **Summer 2017** &middot; Research Intern, **IBM Thomas J. Watson Research Center**, Yorktown Heights (Prof. Michael Witbrock, Jie Chen, Ryan Musa)
- **Summer 2015** &middot; Research Intern, **Big Data Experience Lab, Adobe Research**, Bangalore (Prof. Kokil Jaidka)
- **Summer 2014** &middot; Research Intern, **R.C. Bose Center for Cryptology and Security, Indian Statistical Institute**, Kolkata (Prof. Sourav Sen Gupta)

### Teaching experience

- Teaching Assistant, **CIS 419/519 (Spring 2018) — Applied Machine Learning**. Instructor: Prof. Dan Roth.
- Teaching Assistant, **CIS 620 (Spring 2021) — Learning in Few-Labels Settings**. Instructor: Prof. Dan Roth.

### Awards and honours

- Andrew and Shana Laursen Fellowship, University of Illinois at Urbana–Champaign, 2016.
- President of India Gold Medal, Indian Institute of Technology Kharagpur, 2016.
- Goralal Syngal Scholarship and Bigyan Sinha Memorial Prize, IIT Kharagpur, 2016.
- Kishore Vaigyanik Protsahana Yojana (KVPY) fellowship, National Rank 16.

</section>
