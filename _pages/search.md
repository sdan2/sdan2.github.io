---
layout: archive
title: "Search"
permalink: /search/
author_profile: false
excerpt: "Full-text search across publications, posts, and pages."
---

<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<script src="/pagefind/pagefind-ui.js"></script>

<div class="archive-intro">
  <p class="archive-intro__lead">Full-text search across publications, posts, and pages.</p>
  <p class="archive-intro__note">Indexed by Pagefind. Try a paper title, venue, or co-author.</p>
</div>

<div id="search" class="site-search"></div>

<script>
  window.addEventListener('DOMContentLoaded', function () {
    if (typeof PagefindUI === 'undefined') return;
    new PagefindUI({
      element: '#search',
      showImages: false,
      showSubResults: true,
      resetStyles: false,
      autofocus: true,
      excerptLength: 32,
    });
  });
</script>
