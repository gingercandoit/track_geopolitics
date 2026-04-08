"""
地缘政治增量搜索脚本 — DDG + Exa 双引擎
用法:
    .\.venv\Scripts\python.exe scripts/search_geopolitics.py --days 5
    .\.venv\Scripts\python.exe scripts/search_geopolitics.py --days 5 --topic 1
    .\.venv\Scripts\python.exe scripts/search_geopolitics.py --days 5 --engine exa
    .\.venv\Scripts\python.exe scripts/search_geopolitics.py --days 5 --engine both

管道:
    关键词矩阵 → DDG/Exa 搜索 → trafilatura 提取 → 去重 → 输出 JSON+MD

输出:
    data/raw/YYYY-MM/search_{topic|all}_{engine}_{timestamp}.json
    data/raw/YYYY-MM/search_{topic|all}_{engine}_{timestamp}.md
"""

import json
import os
import re
import sys
import time
import subprocess
from datetime import datetime, timedelta
from urllib.parse import quote, unquote

import requests
import trafilatura

# ── 配置 ──

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
}

SKIP_DOMAINS = [
    'zhihu.com', 'bilibili.com', 'youtube.com', 'tiktok.com',
    'douyin.com', 'facebook.com', 'instagram.com', 'pinterest.com',
]

# 关键词矩阵 — 直接从 02_GeopoliticsWebfetchSOP 提取
TOPIC_QUERIES = {
    1: {
        'name': 'topic1-sanctions',
        'name_zh': '制裁与经济管制',
        'queries': [
            'OFAC sanctions designation SDN list April 2026',
            'EU sanctions package Russia Iran Belarus 2026',
            'secondary sanctions compliance enforcement 2026',
            'SWIFT ban exclusion alternative payment April 2026',
            'dollar weaponization reserve currency diversification 2026',
            'RMB yuan internationalization CIPS cross-border 2026',
            'sanctions evasion circumvention enforcement April 2026',
            'Russia sanctions oil price cap energy 2026',
            'Iran sanctions oil nuclear JCPOA April 2026',
            'financial sanctions de-risking April 2026',
        ],
    },
    2: {
        'name': 'topic2-trade-industrial',
        'name_zh': '贸易与产业政策',
        'queries': [
            'Trump tariff trade war retaliation April 2026',
            'anti-dumping countervailing duty trade investigation 2026',
            'USTR trade policy investigation Section 301 2026',
            'industrial policy CHIPS Act IRA subsidies overcapacity 2026',
            'WTO dispute settlement ruling reform April 2026',
            'carbon border adjustment CBAM EU trade 2026',
            'supply chain reshoring friendshoring nearshoring 2026',
            'tariff pharmaceutical drugs executive order April 2026',
            'Section 232 steel aluminum copper tariff April 2026',
            'trade agreement RCEP CPTPP bilateral FTA 2026',
        ],
    },
    3: {
        'name': 'topic3-supply-resources',
        'name_zh': '能源安全与资源角力',
        'queries': [
            'critical minerals lithium cobalt rare earth policy 2026',
            'OPEC production cut quota oil price April 2026',
            'IEA oil LNG energy outlook critical minerals 2026',
            'energy security Europe Asia pipeline LNG April 2026',
            'natural gas LNG price supply geopolitics 2026',
            'nuclear energy uranium enrichment geopolitics SMR 2026',
            'renewable energy trade tariffs subsidy solar wind 2026',
            'food security grain wheat rice export ban 2026',
            'resource nationalism export restriction mineral 2026',
        ],
    },
    4: {
        'name': 'topic4-tech-digital',
        'name_zh': '技术竞争与规则制定',
        'queries': [
            'BIS entity list export controls semiconductor chip AI 2026',
            'technology restriction China Huawei SMIC NVIDIA April 2026',
            'semiconductor export restriction licensing advanced chip 2026',
            'AI regulation governance US EU China April 2026',
            'technology decoupling tech war chip war 2026',
            'data sovereignty cross-border data digital governance 2026',
            'quantum computing biotech national security restriction 2026',
            'technology standards competition interoperability 2026',
        ],
    },
    5: {
        'name': 'topic5-geopolitics',
        'name_zh': '地缘政治信息池',
        'queries': [
            'summit state visit bilateral multilateral G7 G20 BRICS April 2026',
            'diplomatic alliance partnership geopolitical April 2026',
            'military defense security conflict ceasefire April 2026',
            'NATO AUKUS Quad SCO ASEAN geopolitics April 2026',
            'Ukraine Russia peace negotiations ceasefire April 2026',
            'Global South non-aligned developing countries 2026',
            'Middle East Iran Israel geopolitics April 2026',
            'Arctic space cyber geopolitics sovereignty 2026',
            'election foreign policy political transition 2026',
            'Hormuz strait shipping Red Sea Houthi April 2026',
        ],
    },
}

# ── 搜索引擎 ──

def search_ddg(query, num=8):
    """DuckDuckGo search via ddgs library."""
    try:
        from ddgs import DDGS
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=num))
        urls = []
        for r in results:
            url = r.get('href', '')
            title = r.get('title', '')
            snippet = r.get('body', '')
            if url and not any(d in url for d in SKIP_DOMAINS):
                urls.append({'url': url, 'title': title, 'snippet': snippet})
        return urls[:num]
    except Exception as e:
        print(f"  [DDG] Error: {e}")
        return search_ddg_html(query, num)


def search_ddg_html(query, num=8):
    """DuckDuckGo HTML fallback."""
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return []
        raw_links = re.findall(r'uddg=(https?[^&"]+)', r.text)
        results = []
        for link in raw_links:
            decoded = unquote(link)
            if not any(d in decoded for d in SKIP_DOMAINS) and decoded not in [x['url'] for x in results]:
                results.append({'url': decoded, 'title': '', 'snippet': ''})
        return results[:num]
    except Exception as e:
        print(f"  [DDG-HTML] Error: {e}")
        return []


def search_exa(query, num=5):
    """Search via Exa MCP (mcporter CLI)."""
    try:
        result = subprocess.run(
            ['mcporter', 'call', f'exa.web_search_exa(query: "{query}", numResults: {num})'],
            capture_output=True, text=True, timeout=45, encoding='utf-8',
            shell=True,
        )
        # Parse mcporter output — extract titles, URLs, snippets
        lines = result.stdout.split('\n')
        results = []
        current = {}
        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                current['title'] = line[6:].strip()
            elif line.startswith('URL:'):
                current['url'] = line[4:].strip()
            elif line.startswith('Text:') or line.startswith('Highlights:'):
                current['snippet'] = line.split(':', 1)[1].strip()[:500]
            elif not line and current.get('url'):
                if not any(d in current['url'] for d in SKIP_DOMAINS):
                    results.append(current)
                current = {}
        if current.get('url') and not any(d in current['url'] for d in SKIP_DOMAINS):
            results.append(current)
        return results[:num]
    except subprocess.TimeoutExpired:
        print(f"  [EXA] Timeout (45s)")
        return []
    except Exception as e:
        print(f"  [EXA] Error: {e}")
        return []


def search_urls(query, num=8, engine='ddg'):
    """Dispatch to search engine."""
    if engine == 'exa':
        return search_exa(query, num=min(num, 8))
    else:
        return search_ddg(query, num=num)


# ── 正文提取 ──

def fetch_extract(url, max_chars=5000):
    """Fetch URL and extract text via trafilatura."""
    if any(d in url for d in SKIP_DOMAINS):
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            text = trafilatura.extract(r.text, include_comments=False, include_tables=True)
            if text:
                return text[:max_chars]
    except Exception as e:
        pass
    # Fallback: trafilatura's own downloader
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            if text:
                return text[:max_chars]
    except Exception:
        pass
    return None


# ── 主流程 ──

def run_search(topics_to_search, engine='ddg', days=7, extract_text=False):
    """Execute search for specified topics, return structured results."""
    all_results = {}
    seen_urls = set()
    
    for topic_id in topics_to_search:
        topic = TOPIC_QUERIES[topic_id]
        topic_results = []
        print(f"\n{'='*60}")
        print(f"Topic {topic_id}: {topic['name_zh']} ({topic['name']})")
        print(f"{'='*60}")
        
        for i, query in enumerate(topic['queries'], 1):
            print(f"\n  [{i}/{len(topic['queries'])}] {query}")
            results = search_urls(query, num=8, engine=engine)
            new_count = 0
            
            for r in results:
                url = r.get('url', '')
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                new_count += 1
                
                entry = {
                    'url': url,
                    'title': r.get('title', ''),
                    'snippet': r.get('snippet', ''),
                    'query': query,
                    'topic': topic_id,
                    'engine': engine,
                    'extracted_at': datetime.now().isoformat(),
                }
                
                # Optional: extract full text for top results
                if extract_text:
                    print(f"    Fetching: {url[:80]}...")
                    text = fetch_extract(url)
                    if text:
                        entry['full_text'] = text[:3000]
                        entry['text_length'] = len(text)
                
                topic_results.append(entry)
            
            print(f"    → {len(results)} results, {new_count} new (after dedup)")
            time.sleep(1.5)  # Rate limiting
        
        all_results[topic_id] = {
            'topic_name': topic['name'],
            'topic_name_zh': topic['name_zh'],
            'query_count': len(topic['queries']),
            'result_count': len(topic_results),
            'results': topic_results,
        }
        print(f"\n  Total for T{topic_id}: {len(topic_results)} unique results")
    
    return all_results


def save_results(results, engine, topic_label):
    """Save results as JSON + Markdown summary."""
    now = datetime.now()
    month_dir = f"data/raw/{now.strftime('%Y-%m')}"
    os.makedirs(month_dir, exist_ok=True)
    
    timestamp = now.strftime('%Y%m%d_%H%M')
    base = f"search_{topic_label}_{engine}_{timestamp}"
    json_path = os.path.join(month_dir, f"{base}.json")
    md_path = os.path.join(month_dir, f"{base}.md")
    
    # Save JSON
    output = {
        'metadata': {
            'engine': engine,
            'timestamp': now.isoformat(),
            'topics_searched': list(results.keys()),
        },
        'topics': {},
    }
    for tid, data in results.items():
        output['topics'][f'topic{tid}'] = data
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Save Markdown summary
    lines = [
        f"# 地缘政治搜索结果 — {engine.upper()}",
        f"",
        f"**搜索时间**: {now.strftime('%Y-%m-%d %H:%M')}",
        f"**引擎**: {engine}",
        f"**议题**: {', '.join(f'T{t}' for t in results.keys())}",
        f"",
        f"---",
        f"",
    ]
    
    for tid, data in sorted(results.items()):
        lines.append(f"## T{tid}: {data['topic_name_zh']}")
        lines.append(f"")
        lines.append(f"共 {data['result_count']} 条结果 ({data['query_count']} 组搜索)")
        lines.append(f"")
        
        for r in data['results']:
            title = r.get('title', '(no title)')
            url = r.get('url', '')
            snippet = r.get('snippet', '')[:200]
            lines.append(f"### {title}")
            lines.append(f"- **URL**: {url}")
            lines.append(f"- **Query**: {r.get('query', '')}")
            if snippet:
                lines.append(f"- **Snippet**: {snippet}")
            lines.append(f"")
        
        lines.append(f"---")
        lines.append(f"")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\n[OK] Saved: {json_path}")
    print(f"[OK] Saved: {md_path}")
    return json_path, md_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Geopolitics search pipeline (DDG + Exa)')
    parser.add_argument('--topic', type=int, choices=[1,2,3,4,5], help='Only search this topic')
    parser.add_argument('--engine', default='ddg', choices=['ddg', 'exa', 'both'], help='Search engine')
    parser.add_argument('--days', type=int, default=7, help='Time window in days')
    parser.add_argument('--extract', action='store_true', help='Extract full text (slower)')
    parser.add_argument('--num', type=int, default=8, help='Results per query')
    args = parser.parse_args()
    
    topics = [args.topic] if args.topic else [1, 2, 3, 4, 5]
    topic_label = f't{args.topic}' if args.topic else 'all'
    
    engines = ['ddg', 'exa'] if args.engine == 'both' else [args.engine]
    
    for engine in engines:
        print(f"\n{'#'*60}")
        print(f"# Engine: {engine.upper()}")
        print(f"# Topics: {', '.join(f'T{t}' for t in topics)}")
        print(f"# Time window: {args.days} days")
        print(f"{'#'*60}")
        
        results = run_search(topics, engine=engine, days=args.days, extract_text=args.extract)
        save_results(results, engine, topic_label)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for engine in engines:
        total = sum(len(r.get('results', [])) for r in results.values()) if results else 0
        print(f"  {engine.upper()}: {total} total unique results")


if __name__ == '__main__':
    main()
