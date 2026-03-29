"""
Generate Markdown view files and CSV from literature/new/new.json.

Outputs to literature/new/views/:
  - new-papers-overview.md (full overview grouped by topic)
  - by-topic-t1.md through by-topic-t5.md

Also regenerates:
  - literature/new/new.csv (with data_zh and method_zh columns)
"""
import json
import csv
import os
import sys
import io
from collections import defaultdict
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = 'literature/new/new.json'
VIEWS_DIR = 'literature/new/views'

TOPIC_NAMES = {
    1: "制裁与经济管制",
    2: "贸易与产业政策",
    3: "能源安全与资源角力",
    4: "技术竞争与规则制定",
    5: "地缘政治经济学",
}

TIER_ORDER = {'T1': 0, 'T2': 1, 'T3': 2, 'WP': 3, 'other': 4}


def load_db():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def sort_papers(papers):
    """Sort by tier asc (best first) then year desc (newest first) then citations desc."""
    return sorted(papers, key=lambda p: (
        TIER_ORDER.get(p.get('journal_tier', 'other'), 4),
        -(p.get('year', 0)),
        -(p.get('citations', 0)),
    ))


def format_paper(p, show_topics=False):
    """Format a single paper entry with data_zh and method_zh."""
    authors = p.get('authors', ['Unknown'])
    if len(authors) > 4:
        author_str = ', '.join(authors[:3]) + ' et al.'
    else:
        author_str = ', '.join(authors)

    year = p.get('year', '?')
    title = p.get('title', 'Untitled')
    journal = p.get('journal', '')
    tier = p.get('journal_tier', '?')
    cites = p.get('citations', 0)
    doi = p.get('doi', '')
    priority = p.get('priority', 'reference')
    notes = p.get('notes_zh', '')
    data_zh = p.get('data_zh', '')
    method_zh = p.get('method_zh', '')
    topics = p.get('topics', [])

    lines = []
    lines.append(f"### {p['id']} — {title}")
    lines.append(f"- **Authors**: {author_str}")
    meta = f"- **Year**: {year} | **Tier**: {tier} | **Cites**: {cites}"
    lines.append(meta)
    if journal:
        lines.append(f"- **Journal**: {journal}")
    lines.append(f"- **Priority**: {priority}")
    if show_topics:
        topic_strs = [f"T{t}" for t in sorted(topics)]
        lines.append(f"- **议题**: {', '.join(topic_strs)}")
    if data_zh:
        lines.append(f"- **数据**: {data_zh}")
    if method_zh:
        lines.append(f"- **方法**: {method_zh}")
    if notes:
        lines.append(f"- **简评**: {notes}")
    if doi:
        lines.append(f"- **DOI**: [{doi}](https://doi.org/{doi})")
    lines.append("")
    return '\n'.join(lines)


def gen_overview(data):
    """Generate new-papers-overview.md grouped by topic."""
    papers = data['papers']
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    period = data.get('metadata', {}).get('period', '?')

    # Stats
    topic_counts = defaultdict(int)
    tier_counts = defaultdict(int)
    pri_counts = defaultdict(int)
    for p in papers:
        for t in p.get('topics', []):
            topic_counts[t] += 1
        tier_counts[p.get('journal_tier', 'other')] += 1
        pri_counts[p.get('priority', 'reference')] += 1

    topic_str = ', '.join(f"T{k}:{v}" for k, v in sorted(topic_counts.items()))
    tier_str = ', '.join(f"{k}:{v}" for k, v in sorted(tier_counts.items(), key=lambda x: TIER_ORDER.get(x[0], 4)))
    pri_str = ', '.join(f"{k}:{v}" for k, v in sorted(pri_counts.items(), key=lambda x: ['core','recommended','reference'].index(x[0]) if x[0] in ['core','recommended','reference'] else 9))

    lines = [
        "# Library B — 新文献追踪总览",
        "",
        f"> 生成时间: {now}",
        f"> 论文数量: {len(papers)}",
        f"> 覆盖期间: {period}",
        "",
        "## 统计概览",
        "",
        "| 维度 | 分布 |",
        "|------|------|",
        f"| 议题 | {topic_str} |",
        f"| 期刊层级 | {tier_str} |",
        f"| 优先级 | {pri_str} |",
        "",
        "---",
        "",
    ]

    # Group by topic
    for tid in range(1, 6):
        topic_papers = [p for p in papers if tid in p.get('topics', [])]
        if not topic_papers:
            continue

        lines.append(f"## T{tid}: {TOPIC_NAMES[tid]} ({len(topic_papers)} papers)")
        lines.append("")

        # Group by priority within topic
        for pri in ['core', 'recommended', 'reference']:
            group = [p for p in topic_papers if p.get('priority') == pri]
            if not group:
                continue
            group = sort_papers(group)
            label = {'core': '核心必读', 'recommended': '推荐阅读', 'reference': '参考文献'}[pri]
            lines.append(f"#### {label}")
            lines.append("")
            for p in group:
                lines.append(format_paper(p, show_topics=False))
                lines.append("---")
                lines.append("")

    return '\n'.join(lines)


def gen_topic_view(data, topic_id):
    """Generate by-topic-tN.md — detailed view for one topic."""
    papers = [p for p in data['papers'] if topic_id in p.get('topics', [])]
    papers = sort_papers(papers)
    now = datetime.now().strftime('%Y-%m-%d')

    lines = [
        f"# T{topic_id} {TOPIC_NAMES[topic_id]} — 新文献阅读清单",
        "",
        f"> 自动生成于 {now}，共 {len(papers)} 篇",
        f"> 数据来源：`literature/new/new.json`",
        "",
        "---",
        "",
    ]

    for pri in ['core', 'recommended', 'reference']:
        group = [p for p in papers if p.get('priority') == pri]
        if not group:
            continue
        group = sort_papers(group)
        label = {'core': '核心必读 (Core)', 'recommended': '推荐阅读 (Recommended)', 'reference': '参考文献 (Reference)'}[pri]
        lines.append(f"## {label} ({len(group)} 篇)")
        lines.append("")
        for p in group:
            lines.append(format_paper(p, show_topics=True))
            lines.append("---")
            lines.append("")

    return '\n'.join(lines)


def gen_csv(data):
    """Regenerate new.csv with all fields including data_zh and method_zh."""
    csv_path = 'literature/new/new.csv'
    fieldnames = ['id','title','authors','year','journal','journal_tier','doi',
                  'citations','topics','priority','notes_zh','data_zh','method_zh',
                  'nber_wp','read_status','added_date']
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for p in data['papers']:
            writer.writerow([
                p.get('id',''),
                p.get('title',''),
                '; '.join(p.get('authors',[])),
                p.get('year',''),
                p.get('journal',''),
                p.get('journal_tier',''),
                p.get('doi',''),
                p.get('citations',''),
                ', '.join(f'T{t}' for t in p.get('topics',[])),
                p.get('priority',''),
                p.get('notes_zh',''),
                p.get('data_zh',''),
                p.get('method_zh',''),
                p.get('nber_wp',''),
                p.get('read_status',''),
                p.get('added_date',''),
            ])
    return csv_path


def main():
    os.makedirs(VIEWS_DIR, exist_ok=True)
    data = load_db()

    print(f"Loaded {len(data['papers'])} papers from {DB_PATH}")

    # Regenerate CSV
    csv_path = gen_csv(data)
    print(f"  Regenerated {csv_path} (16 columns)")

    # Overview
    content = gen_overview(data)
    path = os.path.join(VIEWS_DIR, 'new-papers-overview.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Generated {path}")

    # Topic views
    for tid in range(1, 6):
        content = gen_topic_view(data, tid)
        path = os.path.join(VIEWS_DIR, f'by-topic-t{tid}.md')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        count = len([p for p in data['papers'] if tid in p.get('topics', [])])
        print(f"  Generated {path} ({count} papers)")

    print("\nDone! All Library B views generated.")


if __name__ == '__main__':
    main()
