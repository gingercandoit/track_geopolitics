#!/usr/bin/env python3
"""
build.py — Static site generator for track_geopolitics.

Reads JSON data from data/ and literature/, renders Jinja2 templates,
and outputs static HTML to site/dist/.

Usage:
    python site/build.py              # Build entire site
    python site/build.py --clean      # Clean dist/ then rebuild
"""

import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# Add site/ to path so we can import config
sys.path.insert(0, str(Path(__file__).parent))
import config


def discover_data_files():
    """Scan data/ for all topicN-*/YYYY-MM.json files.
    Returns: {topic_slug: [month_str, ...]} sorted descending.
    """
    result = defaultdict(list)
    for topic_slug in config.TOPICS:
        topic_dir = config.DATA_DIR / topic_slug
        if not topic_dir.exists():
            continue
        for f in topic_dir.glob("????-??.json"):
            month = f.stem  # e.g., "2026-03"
            result[topic_slug].append(month)
    # Sort months descending (newest first)
    for slug in result:
        result[slug].sort(reverse=True)
    return dict(result)


def load_topic_data(topic_slug, month):
    """Load a single topic-month JSON file."""
    path = config.DATA_DIR / topic_slug / f"{month}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_report_overview(topic_slug, month):
    """Extract the monthly overview text from the report Markdown."""
    path = config.REPORTS_DIR / topic_slug / f"{month}.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    # Extract content between "## 月度总览" and next "## " or "---"
    match = re.search(
        r"## 月度总览\s*\n(.*?)(?=\n## |\n---|\Z)", text, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return ""


def load_literature(library="classic"):
    """Load literature JSON (classic or new)."""
    path = config.LITERATURE_DIR / library / f"{library}.json"
    if not path.exists():
        return {"papers": [], "metadata": {}}
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def group_events_by_week(events):
    """Group events by week number, sorted by date."""
    weeks = defaultdict(list)
    for event in events:
        week = event.get("week", 0)
        weeks[week].append(event)
    # Sort events within each week by date
    for week in weeks:
        weeks[week].sort(key=lambda e: e.get("date", ""))
    return dict(sorted(weeks.items()))


def get_all_months(data_map):
    """Get all unique months across all topics, sorted descending."""
    months = set()
    for topic_months in data_map.values():
        months.update(topic_months)
    return sorted(months, reverse=True)


def format_month_display(month_str):
    """Convert '2026-03' to '2026年3月'."""
    parts = month_str.split("-")
    return f"{parts[0]}年{int(parts[1])}月"


def markdown_to_html(text):
    """Convert simple markdown to HTML (paragraphs + bold)."""
    if not text:
        return ""
    # Convert **bold** to <strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Split into paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{p}</p>" for p in paragraphs)


def extract_first_sentence(text):
    """Extract the first 1–2 sentences from markdown text for digest."""
    if not text:
        return ""
    # Remove **bold** markers for plain text
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Split by 。 to get sentences
    sentences = [s.strip() for s in clean.split('。') if s.strip()]
    if not sentences:
        return clean[:120].strip() + '…'
    first = sentences[0] + '。'
    if len(sentences) > 1:
        combined = first + sentences[1] + '。'
        if len(combined) <= 200:
            return combined
    return first


def compute_relative_path(from_path, to_path):
    """Compute relative path from one HTML file to another.
    Both paths are relative to dist/.
    """
    from_parts = Path(from_path).parent.parts
    to_parts = Path(to_path).parts
    # Go up from from_path's directory
    ups = len(from_parts)
    return "/".join([".."] * ups + list(to_parts))


def build_site(clean=False):
    """Main build function."""
    dist = config.OUTPUT_DIR
    if clean and dist.exists():
        shutil.rmtree(dist)

    dist.mkdir(parents=True, exist_ok=True)

    # ── Setup Jinja2 ─────────────────────────────────────────────
    env = Environment(
        loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
        autoescape=True,
    )
    # Register custom filters
    env.filters["month_display"] = format_month_display

    # ── Discover data ────────────────────────────────────────────
    data_map = discover_data_files()
    all_months = get_all_months(data_map)
    latest_month = all_months[0] if all_months else None

    if not latest_month:
        print("No data files found. Nothing to build.")
        return

    print(f"Found months: {', '.join(all_months)}")
    print(f"Latest month: {latest_month}")

    # ── Shared template context ──────────────────────────────────
    base_context = {
        "site_title": config.SITE_TITLE,
        "site_subtitle": config.SITE_SUBTITLE,
        "topics": config.TOPICS,
        "event_type_colors": config.EVENT_TYPE_COLORS,
        "colors": config.COLORS,
        "fonts": config.FONTS,
        "source_tiers": config.SOURCE_TIERS,
        "priority_labels": config.PRIORITY_LABELS,
        "journal_tiers": config.JOURNAL_TIERS,
        "all_months": all_months,
        "latest_month": latest_month,
    }

    # ── Build topic pages ────────────────────────────────────────
    for topic_slug, topic_info in config.TOPICS.items():
        topic_months = data_map.get(topic_slug, [])
        if not topic_months:
            continue

        # Create topic output directory
        topic_out_dir = dist / topic_slug
        topic_out_dir.mkdir(parents=True, exist_ok=True)

        for month in topic_months:
            data = load_topic_data(topic_slug, month)
            if not data:
                continue

            overview = load_report_overview(topic_slug, month)
            events = data.get("events", [])
            events_by_week = group_events_by_week(events)

            # Choose template based on compact flag
            template_name = (
                "topic5.html" if topic_info.get("compact") else "topic.html"
            )
            template = env.get_template(template_name)

            # Build weeks list for template
            weeks_list = []
            for week_num, week_events in sorted(events_by_week.items()):
                dates = [e.get("date", "") for e in week_events if e.get("date")]
                if dates:
                    date_range = f"{dates[0][5:]} — {dates[-1][5:]}"
                else:
                    date_range = ""
                weeks_list.append({
                    "week_num": week_num,
                    "date_range": date_range,
                    "events": week_events,
                })

            # Convert overview markdown to HTML
            overview_html = markdown_to_html(overview)

            # Compute relative path to root for static assets
            rel_to_root = ".."  # topic-slug/month.html -> dist root

            html = template.render(
                **base_context,
                topic=topic_info,
                topic_id=topic_slug.replace("topic", "t").split("-")[0],
                topic_slug=topic_slug,
                month=month,
                current_month=month,
                month_display=format_month_display(month),
                available_months=topic_months,
                overview_html=overview_html,
                events=events,
                weeks=weeks_list,
                metadata=data.get("report_metadata", {}),
                key_metrics=data.get("key_metrics", {}),
                background_context=data.get("background_context", []),
                rel_to_root=rel_to_root,
                current_page=f"{topic_slug}/{month}.html",
            )

            out_path = topic_out_dir / f"{month}.html"
            out_path.write_text(html, encoding="utf-8")
            print(f"  Built: {topic_slug}/{month}.html ({len(events)} events)")

    # ── Build index page ─────────────────────────────────────────
    # Build topics_data dict and collect per-topic digests
    topics_data = {}
    topic_digests = []  # [{slug, name_zh, name_short, color, digest_text}]
    for topic_slug, topic_info in config.TOPICS.items():
        topic_months = data_map.get(topic_slug, [])
        if not topic_months:
            continue
        data = load_topic_data(topic_slug, topic_months[0])
        if not data:
            continue
        topics_data[topic_slug] = data
        # Extract digest (first 1-2 sentences) for homepage
        overview = load_report_overview(topic_slug, topic_months[0])
        digest = extract_first_sentence(overview)
        topic_digests.append({
            "slug": topic_slug,
            "name_zh": topic_info["name_zh"],
            "name_short": topic_info.get("name_short", ""),
            "color": topic_info["color"],
            "compact": topic_info.get("compact", False),
            "digest": digest,
            "event_count": len(data.get("events", [])),
        })

    # Load latest literature for sidebar
    lit_new = load_literature("new")
    latest_papers = sorted(
        lit_new.get("papers", []),
        key=lambda p: p.get("year", 0),
        reverse=True,
    )[:6]

    index_template = env.get_template("index.html")
    index_html = index_template.render(
        **base_context,
        topics_data=topics_data,
        topic_digests=topic_digests,
        latest_papers=latest_papers,
        latest_month_display=format_month_display(latest_month),
        rel_to_root=".",
        current_page="index.html",
    )
    (dist / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Built: index.html")

    # ── Build literature page ────────────────────────────────────
    lit_classic = load_literature("classic")
    lit_new_data = load_literature("new")

    # Merge papers with _library tag
    classic_papers = lit_classic.get("papers", [])
    new_papers_list = lit_new_data.get("papers", [])
    for p in classic_papers:
        p["_library"] = "classic"
    for p in new_papers_list:
        p["_library"] = "new"
    all_papers = classic_papers + new_papers_list
    # Sort by year descending
    all_papers.sort(key=lambda p: p.get("year", 0), reverse=True)

    lit_template = env.get_template("literature.html")
    lit_html = lit_template.render(
        **base_context,
        papers=all_papers,
        classic_count=len(classic_papers),
        new_count=len(new_papers_list),
        rel_to_root=".",
        current_page="literature.html",
    )
    (dist / "literature.html").write_text(lit_html, encoding="utf-8")
    print(
        f"  Built: literature.html "
        f"({len(classic_papers)} classic, "
        f"{len(new_papers_list)} new)"
    )

    # ── Build archive page ───────────────────────────────────────
    archive_months = []
    for month in all_months:
        topic_counts = {}
        for topic_slug in config.TOPICS:
            if month in data_map.get(topic_slug, []):
                data = load_topic_data(topic_slug, month)
                topic_counts[topic_slug] = len(
                    data.get("events", [])
                ) if data else 0
            else:
                topic_counts[topic_slug] = 0
        archive_months.append({
            "month": month,
            "display": format_month_display(month),
            "topic_counts": topic_counts,
        })

    archive_template = env.get_template("archive.html")
    archive_html = archive_template.render(
        **base_context,
        archive_months=archive_months,
        rel_to_root=".",
        current_page="archive.html",
    )
    (dist / "archive.html").write_text(archive_html, encoding="utf-8")
    print(f"  Built: archive.html ({len(all_months)} months)")

    # ── Copy static assets ───────────────────────────────────────
    static_dest = dist / "static"
    if static_dest.exists():
        shutil.rmtree(static_dest)
    shutil.copytree(config.STATIC_DIR, static_dest)
    print(f"  Copied: static/")

    print(f"\nBuild complete! Output: {dist}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build geopolitics static site")
    parser.add_argument("--clean", action="store_true", help="Clean dist/ before build")
    args = parser.parse_args()

    build_site(clean=args.clean)
