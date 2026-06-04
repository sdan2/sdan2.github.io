#!/usr/bin/env python3
"""
One-shot migration: parse the legacy combined publication list at
_publications/papers.md (originally _pages/papers.md) and emit one Jekyll
markdown file per paper into _publications/.

Frontmatter fields written:
  title, collection: publications, permalink, excerpt, date, year, venue,
  authors (raw markdown with **Soham Dan** preserved), paperurl, category.

Run from the repo root:
    python3 markdown_generator/split_legacy_publications.py

The legacy file is left in place (rename to .legacy.md after verifying output).
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "_publications" / "papers.md"
OUT_DIR = REPO / "_publications"

YEAR_HEADER = re.compile(r"^###\s+(\d{4}|Patents)\s*$")
ENTRY_START = re.compile(r"^\*\s+\[")

# Within a single entry block, the title can wrap a newline before the closing ]
TITLE_URL = re.compile(r"\[(?P<title>.+?)\]\((?P<url>[^)]*)\)", re.DOTALL)

# Venue + year pattern, anchored near the end of the body line.
#   **Venue** Year[ (qualifier)]
VENUE_YEAR = re.compile(
    r"\*\*(?P<venue>[^*]+?)\*\*\s*(?P<year>\d{4})\s*(?P<qual>\([^)]*\))?\.?\s*$"
)
# Fallback: just **venue** with no year (for the Patents section)
VENUE_NO_YEAR = re.compile(r"\*\*(?P<venue>[^*]+?)\*\*\.?\s*$")


def slugify(text: str, max_words: int = 8) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).lower()
    words = [w for w in text.split() if w][:max_words]
    return "-".join(words) or "untitled"


def split_entries(lines: list[str]) -> list[tuple[str, list[str]]]:
    """Group lines into (section, [entry-lines]) tuples.

    Section is a year string ("2024") or "Patents". An entry is the lines
    starting at `*` up to (but not including) the next entry or section.
    """
    section = None
    entries: list[tuple[str, list[str]]] = []
    current: list[str] | None = None

    def flush():
        nonlocal current
        if current is not None and section is not None:
            text = "\n".join(current).strip()
            if text:
                entries.append((section, current))
        current = None

    for raw in lines:
        line = raw.rstrip("\n")
        if YEAR_HEADER.match(line):
            flush()
            section = YEAR_HEADER.match(line).group(1)
            continue
        if section is None:
            continue
        if ENTRY_START.match(line):
            flush()
            current = [line]
        elif current is not None:
            current.append(line)
    flush()
    return entries


def parse_entry(section: str, entry_lines: list[str]) -> dict | None:
    blob = " ".join(l.strip() for l in entry_lines).lstrip("* ").strip()
    # Title + URL
    m = TITLE_URL.search(blob)
    if not m:
        return None
    title = re.sub(r"\s+", " ", m.group("title")).strip()
    paperurl = m.group("url").strip()
    rest = blob[m.end():].lstrip()
    # Drop leading <br/> separator(s)
    rest = re.sub(r"^\s*(?:<br\s*/?>\s*)+", "", rest).strip()

    # Venue + year
    venue, year, qual = "", "", ""
    vm = VENUE_YEAR.search(rest)
    if vm:
        venue = vm.group("venue").strip()
        year = vm.group("year").strip()
        qual = (vm.group("qual") or "").strip()
        authors_blob = rest[: vm.start()].rstrip().rstrip(".")
    else:
        vm2 = VENUE_NO_YEAR.search(rest)
        if vm2:
            venue = vm2.group("venue").strip()
            authors_blob = rest[: vm2.start()].rstrip().rstrip(".")
        else:
            authors_blob = rest

    # Authors: strip trailing period; keep markdown bolding intact
    authors = re.sub(r"\s+", " ", authors_blob).strip().rstrip(".")
    # Section "Patents" → no year
    if section == "Patents":
        year_for_filename = "patents"
        sort_year = "2017"  # earliest patent in list dates to 2017
        category = "patent"
    else:
        year_for_filename = section
        sort_year = section
        category = "paper"

    if not year:
        year = sort_year if category == "paper" else ""

    venue_slug = slugify(venue.replace(" ", "-")) if venue else "misc"
    title_slug = slugify(title)
    name = f"{year_for_filename}-{venue_slug}-{title_slug}"
    permalink = f"/publication/{name}/"

    return {
        "name": name,
        "title": title,
        "paperurl": paperurl,
        "authors": authors,
        "venue": venue,
        "year": year,
        "qualifier": qual,
        "category": category,
        "sort_year": sort_year,
        "permalink": permalink,
    }


def write_paper(paper: dict) -> Path:
    # Build a stable, sort-friendly date. Use Dec 31 of the year so newer years sort
    # after older ones; per-year ordering within the year is by venue alphabetically.
    sort_year = paper["sort_year"]
    date = f"{sort_year}-12-31"
    # Escape characters in YAML strings
    def yaml_str(s: str) -> str:
        s = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{s}"'

    body_lines = []
    if paper["authors"]:
        body_lines.append(f'**Authors.** {paper["authors"]}')
        body_lines.append("")
    if paper["venue"]:
        venue_line = f'**Venue.** {paper["venue"]}'
        if paper["year"]:
            venue_line += f' {paper["year"]}'
        if paper["qualifier"]:
            venue_line += f' {paper["qualifier"]}'
        body_lines.append(venue_line)
        body_lines.append("")
    if paper["paperurl"]:
        body_lines.append(f'[Paper]({paper["paperurl"]})')

    frontmatter = [
        "---",
        f'title: {yaml_str(paper["title"])}',
        "collection: publications",
        f'permalink: {paper["permalink"]}',
        f'date: {date}',
        f'year: "{paper["year"] or sort_year}"',
        f'venue: {yaml_str(paper["venue"])}',
        f'authors: {yaml_str(paper["authors"])}',
        f'paperurl: {yaml_str(paper["paperurl"])}',
        f'category: {paper["category"]}',
    ]
    if paper["qualifier"]:
        frontmatter.append(f'qualifier: {yaml_str(paper["qualifier"])}')
    # Excerpt = single-sentence summary fallback; here we just use venue/year
    excerpt = paper["venue"] or paper["title"]
    if paper["year"]:
        excerpt = f'{excerpt} {paper["year"]}'
    frontmatter.append(f'excerpt: {yaml_str(excerpt.strip())}')
    frontmatter.append("---")

    out_path = OUT_DIR / f'{paper["name"]}.md'
    out_path.write_text("\n".join(frontmatter) + "\n\n" + "\n".join(body_lines) + "\n")
    return out_path


def main() -> int:
    text = SRC.read_text().splitlines()
    entries = split_entries(text)
    written = 0
    skipped = 0
    print(f"Parsing {len(entries)} entries from {SRC.relative_to(REPO)}")
    for section, lines in entries:
        paper = parse_entry(section, lines)
        if paper is None:
            skipped += 1
            print("  SKIP:", " ".join(l.strip() for l in lines)[:80])
            continue
        path = write_paper(paper)
        written += 1
        print(f"  + {paper['sort_year']}  {paper['venue']:<22}  {paper['title'][:60]}")
    print(f"\nWrote {written} files; skipped {skipped}.")
    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
