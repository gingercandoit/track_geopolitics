"""
Generate Markdown view files from literature-classic.json.

Outputs to file/literature/views/:
  - by-topic-t1.md through by-topic-t5.md
  - by-priority.md
  - by-author.md
"""
import json
import os
from collections import defaultdict
from datetime import datetime

DB_PATH = 'literature/literature-classic.json'
VIEWS_DIR = 'literature/views'

TOPIC_NAMES = {
    1: "制裁与经济管制 (Sanctions & Economic Coercion)",
    2: "贸易与产业竞争 (Trade & Industrial Policy)",
    3: "供应链与关键资源 (Supply Chains & Resources)",
    4: "技术竞争与数字治理 (Tech Competition & Digital Governance)",
    5: "地缘政治经济学 (Geopolitical Economy)",
}

TIER_NAMES = {
    'T1': 'General Top 5 + Finance Top',
    'T2': 'Field Top Journals',
    'T3': 'Political Science / IR Top',
    'WP': 'Working Papers (NBER/CEPR/IMF/WB)',
    'other': 'Other Venues',
}

PRIORITY_ORDER = ['core', 'recommended', 'reference']
PRIORITY_LABELS = {
    'core': '核心必读 (Core)',
    'recommended': '推荐阅读 (Recommended)',
    'reference': '参考文献 (Reference)',
}


def load_db():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_paper(p, show_topics=False):
    """Format a single paper entry as Markdown."""
    authors = p.get('authors', ['Unknown'])
    if len(authors) > 3:
        author_str = ', '.join(authors[:3]) + ' et al.'
    else:
        author_str = ', '.join(authors)
    
    year = p.get('year', '?')
    title = p.get('title', 'Untitled')
    journal = p.get('journal', 'N/A')
    tier = p.get('journal_tier', '?')
    cites = p.get('citations', 0)
    doi = p.get('doi', '')
    priority = p.get('priority', 'reference')
    notes = p.get('notes_zh', '')
    topics = p.get('topics', [])
    
    lines = []
    lines.append(f"### {author_str} ({year}) — {title}")
    lines.append(f"- **期刊**：{journal} [{tier}]")
    lines.append(f"- **引用**：{cites}")
    lines.append(f"- **优先级**：{priority}")
    if show_topics:
        topic_strs = [f"T{t}" for t in sorted(topics)]
        lines.append(f"- **议题**：{', '.join(topic_strs)}")
    if doi:
        lines.append(f"- **DOI**：[{doi}](https://doi.org/{doi})")
    if notes:
        lines.append(f"- **简评**：{notes}")
    lines.append("")
    return '\n'.join(lines)


def gen_topic_view(data, topic_id):
    """Generate by-topic-tN.md"""
    papers = [p for p in data['papers'] if topic_id in p.get('topics', [])]
    papers.sort(key=lambda x: (-PRIORITY_ORDER.index(x.get('priority', 'reference')),
                                -x.get('citations', 0)))
    
    lines = []
    lines.append(f"# T{topic_id} {TOPIC_NAMES[topic_id]} — 阅读清单")
    lines.append("")
    lines.append(f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d')}，共 {len(papers)} 篇")
    lines.append(f"> 数据来源：`literature-classic.json`")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for priority in PRIORITY_ORDER:
        group = [p for p in papers if p.get('priority') == priority]
        if not group:
            continue
        lines.append(f"## {PRIORITY_LABELS[priority]} ({len(group)} 篇)")
        lines.append("")
        for p in group:
            lines.append(format_paper(p, show_topics=True))
            lines.append("---")
            lines.append("")
    
    return '\n'.join(lines)


def gen_priority_view(data):
    """Generate by-priority.md"""
    papers = data['papers']
    
    lines = []
    lines.append("# 文献库 — 按优先级排列")
    lines.append("")
    lines.append(f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d')}，共 {len(papers)} 篇")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for priority in PRIORITY_ORDER:
        group = [p for p in papers if p.get('priority') == priority]
        if not group:
            continue
        group.sort(key=lambda x: -x.get('citations', 0))
        
        lines.append(f"## {PRIORITY_LABELS[priority]} ({len(group)} 篇)")
        lines.append("")
        
        # For core/recommended, show full entries; for reference, compact table
        if priority == 'reference':
            lines.append("| 作者 | 年份 | 标题 | 期刊 | 引用 | 议题 |")
            lines.append("|------|------|------|------|------|------|")
            for p in group:
                authors = p.get('authors', ['?'])
                a = authors[0].split()[-1] if authors else '?'
                if len(authors) > 1:
                    a += ' et al.'
                yr = p.get('year', '?')
                t = p.get('title', '')[:50]
                j = p.get('journal', '')[:30]
                c = p.get('citations', 0)
                topics = ','.join(f"T{x}" for x in p.get('topics', []))
                lines.append(f"| {a} | {yr} | {t} | {j} | {c} | {topics} |")
            lines.append("")
        else:
            for p in group:
                lines.append(format_paper(p, show_topics=True))
                lines.append("---")
                lines.append("")
    
    return '\n'.join(lines)


def gen_author_view(data):
    """Generate by-author.md"""
    # Group papers by first author last name
    author_papers = defaultdict(list)
    for p in data['papers']:
        authors = p.get('authors', [])
        for author in authors:
            author_papers[author].append(p)
    
    # Sort authors by total citations (descending)
    author_cites = {}
    for author, plist in author_papers.items():
        author_cites[author] = sum(p.get('citations', 0) for p in plist)
    
    sorted_authors = sorted(author_cites.keys(), key=lambda a: -author_cites[a])
    
    # Only show authors with 2+ papers
    multi_authors = [a for a in sorted_authors if len(author_papers[a]) >= 2]
    
    lines = []
    lines.append("# 文献库 — 按作者索引")
    lines.append("")
    lines.append(f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"> 仅显示有 2 篇及以上论文的作者，共 {len(multi_authors)} 位")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for author in multi_authors[:80]:  # Cap at 80 authors
        plist = author_papers[author]
        plist.sort(key=lambda x: -x.get('citations', 0))
        total_cites = author_cites[author]
        
        lines.append(f"## {author} ({len(plist)} 篇, {total_cites} 总引用)")
        lines.append("")
        
        for p in plist:
            year = p.get('year', '?')
            title = p.get('title', '')[:80]
            journal = p.get('journal', '')[:40]
            cites = p.get('citations', 0)
            tier = p.get('journal_tier', '?')
            topics = ','.join(f"T{x}" for x in p.get('topics', []))
            lines.append(f"- [{cites} cites] ({year}) {title} — *{journal}* [{tier}] {topics}")
        
        lines.append("")
    
    return '\n'.join(lines)


def main():
    os.makedirs(VIEWS_DIR, exist_ok=True)
    data = load_db()
    
    print(f"Loaded {len(data['papers'])} papers")
    
    # Generate topic views
    for topic_id in range(1, 6):
        content = gen_topic_view(data, topic_id)
        path = os.path.join(VIEWS_DIR, f'by-topic-t{topic_id}.md')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        count = len([p for p in data['papers'] if topic_id in p.get('topics', [])])
        print(f"  Generated {path} ({count} papers)")
    
    # Generate priority view
    content = gen_priority_view(data)
    path = os.path.join(VIEWS_DIR, 'by-priority.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Generated {path}")
    
    # Generate author view
    content = gen_author_view(data)
    path = os.path.join(VIEWS_DIR, 'by-author.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Generated {path}")
    
    print("\nDone! All views generated.")


if __name__ == '__main__':
    main()
