"""
fetch_sources.py — 地缘政治信息源自动拉取脚本

功能：
  1. 拉取 A/B/C 层 RSS feeds（43个已验证 feed）
  2. 拉取 Reddit JSON API（r/geopolitics, r/worldnews, r/economics）
  3. 按五大议题关键词过滤（T5为catch-all信息池）
  4. 输出结构化 JSON + 可读 Markdown 摘要

五大议题：
  T1 制裁与经济管制    T2 贸易与产业政策    T3 能源安全与资源角力
  T4 技术竞争与规则制定  T5 地缘政治信息池（catch-all）

使用方式：
  python scripts/fetch_sources.py                    # 拉取全部
  python scripts/fetch_sources.py --topic 1          # 只看议题1
  python scripts/fetch_sources.py --topic 5          # 只看议题5 (catch-all)
  python scripts/fetch_sources.py --source rss       # 只拉RSS
  python scripts/fetch_sources.py --source reddit    # 只拉Reddit
  python scripts/fetch_sources.py --days 3           # 只看最近3天

依赖：pip install feedparser requests
"""

import feedparser
import requests
import json
import re
import time
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from html import unescape

# =============================================================================
# 配置：RSS Feed 清单
# =============================================================================

RSS_FEEDS = {
    # ---- A层：美国政府 ----
    "A|White House News": "https://www.whitehouse.gov/news/feed/",
    "A|White House Presidential Actions": "https://www.whitehouse.gov/presidential-actions/feed/",
    "A|State Dept Press Releases": "https://www.state.gov/rss-feed/press-releases/feed/",
    "A|State Dept All Releases": "https://www.state.gov/rss-feed/collected-department-releases/feed/",
    "A|Federal Reserve Press": "https://www.federalreserve.gov/feeds/press_all.xml",
    "A|Federal Reserve Speeches": "https://www.federalreserve.gov/feeds/speeches.xml",
    "A|EIA Press": "https://www.eia.gov/rss/press_rss.xml",
    "A|GAO Reports": "https://www.gao.gov/rss/reports.xml",

    # ---- A层：其他政府 ----
    "A|UK FCDO": "https://www.gov.uk/government/organisations/foreign-commonwealth-development-office.atom",

    # ---- B层：国际机构 ----
    "B|WTO News": "http://www.wto.org/library/rss/latest_news_e.xml",
    "B|UN Peace & Security": "https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml",
    "B|WHO News": "https://www.who.int/rss-feeds/news-english.xml",
    "B|NBER Papers": "https://www.nber.org/rss/new.xml",

    # ---- C层：主流媒体 ----
    "C|Bloomberg Politics": "https://feeds.bloomberg.com/politics/news.rss",
    "C|Bloomberg Economics": "https://feeds.bloomberg.com/economics/news.rss",
    "C|Bloomberg Technology": "https://feeds.bloomberg.com/technology/news.rss",
    "C|WSJ World News": "https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
    "C|WSJ Markets": "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain",
    "C|WSJ Opinion": "https://feeds.content.dowjones.io/public/rss/RSSOpinion",
    "C|FT World": "https://www.ft.com/world?format=rss",
    "C|Economist International": "https://www.economist.com/international/rss.xml",
    "C|Economist Finance": "https://www.economist.com/finance-and-economics/rss.xml",
    "C|Economist Asia": "https://www.economist.com/asia/rss.xml",
    "C|Economist China": "https://www.economist.com/china/rss.xml",
    "C|Economist US": "https://www.economist.com/united-states/rss.xml",
    "C|NPR World": "https://feeds.npr.org/1004/rss.xml",
    "C|NPR Politics": "https://feeds.npr.org/1014/rss.xml",
    "C|BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "C|BBC Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "C|CNBC World": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362",
    "C|CNBC Economy": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
    "C|Guardian World": "https://www.theguardian.com/world/rss",
    "C|Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "C|Foreign Policy": "https://foreignpolicy.com/feed/",
    "C|Foreign Affairs": "https://www.foreignaffairs.com/rss.xml",
    "C|SCMP": "https://www.scmp.com/rss/91/feed",
    "C|The Diplomat": "https://thediplomat.com/feed/",

    # ---- C层：智库/安全 ----
    "C|War on the Rocks": "https://warontherocks.com/feed/",
    "C|Bruegel": "https://www.bruegel.org/rss.xml",
}

# 需要 User-Agent 的 feeds
FEEDS_NEEDING_UA = {
    "A|State Dept Press Releases",
    "A|State Dept All Releases",
}

# =============================================================================
# 配置：Reddit 端点
# =============================================================================

REDDIT_ENDPOINTS = [
    {
        "name": "r/geopolitics (hot)",
        "url": "https://www.reddit.com/r/geopolitics/hot.json?limit=25",
    },
    {
        "name": "r/worldnews (top/week)",
        "url": "https://www.reddit.com/r/worldnews/top.json?t=week&limit=25",
    },
    {
        "name": "r/economics (hot)",
        "url": "https://www.reddit.com/r/economics/hot.json?limit=15",
    },
]

# =============================================================================
# 配置：五大议题关键词
# =============================================================================

TOPIC_KEYWORDS = {
    1: {
        "name": "制裁与经济管制",
        "name_en": "Sanctions & Economic Coercion",
        "slug": "topic1-sanctions",
        "keywords": [
            r"ofac|sanctions?\b|designation|sdn.list|delisting",
            r"eu.sanction|package.+sanction|sanction.+russia|sanction.+iran|sanction.+belarus",
            r"secondary.sanction|compliance.+sanction|enforcement.+sanction",
            r"swift.+ban|swift.+exclu|swift.+weapon|swift.+alternative",
            r"dollar.hegemony|dollar.weapon|reserve.currency",
            r"rmb.international|cips\b|yuan.+cross|renminbi",
            r"sanction.+evasion|sanction.+circumvent|sanction.+enforce",
            r"anti.sanction|counter.sanction|retaliatory.measure",
            r"asset.freeze|sovereign.wealth.+sanction|central.bank.+sanction",
            r"oil.price.cap|sanction.+oil|sanction.+energy",
            r"jcpoa|iran.+nuclear.+deal",
            r"north.korea.+sanction|dprk.+sanction",
            r"financial.sanction|de.risk|correspondent.bank",
            r"unreliable.entity|entity.list.+sanction",
        ],
    },
    2: {
        "name": "贸易与产业政策",
        "name_en": "Trade & Industrial Competition",
        "slug": "topic2-trade-industrial",
        "keywords": [
            r"tariff|trade.war|retaliat.+trade|section.301",
            r"anti.dump|countervail|trade.investigat",
            r"ustr\b|trade.policy|trade.agenda",
            r"industrial.policy|chips.act|inflation.reduction.act|ira\b.+subsid|overcapacity",
            r"wto.+dispute|wto.+settle|wto.+rul|wto.+reform|appellate.body",
            r"trade.agreement|rcep|cptpp|bilateral.+trade|fta\b",
            r"carbon.border|cbam\b|eu.+trade.+climate",
            r"trade.barrier|trade.+countermeasure",
            r"301.+investigat|anti.dumping|countervailing.dut",
        ],
    },
    3: {
        "name": "能源安全与资源角力",
        "name_en": "Supply Chains & Critical Resources",
        "slug": "topic3-supply-resources",
        "keywords": [
            r"supply.chain|reshoring|nearshoring|friendshoring|supply.+resilien",
            r"critical.mineral|lithium|cobalt|rare.earth",
            r"opec\b|oil.produc|oil.cut|oil.quota|oil.price",
            r"iea\b|energy.agency|energy.outlook",
            r"energy.security|pipeline|lng\b|natural.gas",
            r"nuclear.energy|uranium|enrichment|smr\b",
            r"renewable.+trade|solar.+tariff|wind.+subsid",
            r"food.security|grain|wheat|rice.+export|export.ban.+food",
            r"agricultur.+trade|agricultur.+geopolit|fertilizer",
            r"resource.national|export.restrict.+mineral",
            r"global.value.chain|supply.+disrupt|supply.+divers",
            r"oil|petroleum|crude|brent|wti",
            r"saudi.+oil|hormuz|gas.price|energy.crisis",
            r"spr\b|strategic.+reserve",
            r"mining|mineral.+export",
        ],
    },
    4: {
        "name": "技术竞争与规则制定",
        "name_en": "Tech Competition & Digital Governance",
        "slug": "topic4-tech-digital",
        "keywords": [
            r"bis\b.+entity|export.control.+semicon|export.control.+chip|export.control.+ai\b",
            r"tech.+restrict.+china|huawei|smic|nvidia.+restrict|nvidia.+ban",
            r"semiconductor.+export|semiconductor.+restrict|semiconductor.+licens|advanced.chip",
            r"ai.regulat|ai.governance|ai.+rule|ai.+framework",
            r"tech.+decoupl|tech.war|chip.war",
            r"data.sovereign|cross.border.data|digital.governance",
            r"5g.+geopoli|submarine.cable|digital.infrastr",
            r"tech.+standard.+compet|interoperab",
            r"quantum.comput|biotech.+national.secur|biotech.+restrict",
            r"tiktok|bytedance|tech.+ban",
            r"entity.list|bis\b.+rule|chip.+export",
        ],
    },
    5: {
        "name": "地缘政治信息池",
        "name_en": "Geopolitics Catch-All",
        "slug": "topic5-geopolitics",
        "keywords": [
            # T5 actively matches broad geopolitics keywords
            r"summit|state.visit|bilateral|multilateral|g7\b|g20\b|brics\b",
            r"diplomat|alliance|partnership|geopolit",
            r"military|defense|defence|security.+conflict|ceasefire",
            r"un\b.+security|nato\b|aukus\b|quad\b|sco\b|asean\b",
            r"global.south|non.aligned|developing.countr",
            r"election.+foreign|regime.change|political.transit",
            r"refugee|migration.+geopoli|humanitarian.+crisis",
            r"arctic.+geopoli|space.+geopoli|cyber.+geopoli|cyber.+sovereign",
            r"foreign.policy|national.security|strategic",
            r"war\b|invasion|conflict|peace.talk|negotiat.+peace",
            r"china|russia|iran|ukraine|north.korea|taiwan",
        ],
        "is_catchall": True,  # T5 also gets all unmatched items
    },
}

# =============================================================================
# 辅助函数
# =============================================================================

def clean_html(text):
    """Remove HTML tags and decode entities."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_date(entry):
    """Extract datetime from feed entry."""
    for field in ["published_parsed", "updated_parsed"]:
        t = entry.get(field)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    # Try string parsing
    for field in ["published", "updated"]:
        s = entry.get(field, "")
        if s:
            for fmt in [
                "%a, %d %b %Y %H:%M:%S %Z",
                "%a, %d %b %Y %H:%M:%S %z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%S",
            ]:
                try:
                    return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
    return None


def match_topic(text, topic_num):
    """Check if text matches a topic's keywords."""
    if not text:
        return False
    text_lower = text.lower()
    keywords = TOPIC_KEYWORDS[topic_num]["keywords"]
    for pattern in keywords:
        if re.search(pattern, text_lower):
            return True
    return False


def get_matching_topics(text):
    """Return list of matching topic numbers. T5 is catch-all: gets all unmatched items."""
    topics = []
    for t in [1, 2, 3, 4]:
        if match_topic(text, t):
            topics.append(t)
    # T5 catch-all: items matched by T5 keywords OR not matched by T1-T4
    if match_topic(text, 5) or not topics:
        topics.append(5)
    return topics


# =============================================================================
# RSS 拉取
# =============================================================================

def fetch_rss_feeds(days_back=7):
    """Fetch all RSS feeds and return structured items."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    items = []
    errors = []

    for feed_name, feed_url in RSS_FEEDS.items():
        tier = feed_name.split("|")[0]
        source = feed_name.split("|")[1]

        try:
            if feed_name in FEEDS_NEEDING_UA:
                req = Request(feed_url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeopoliticsTracker/1.0"
                })
                resp = urlopen(req, timeout=15)
                data = resp.read()
                feed = feedparser.parse(data)
            else:
                feed = feedparser.parse(feed_url)

            status = feed.get("status", 0)
            if status >= 400 or len(feed.entries) == 0:
                errors.append(f"  SKIP {source}: status={status}, entries=0")
                continue

            count = 0
            for entry in feed.entries:
                title = clean_html(entry.get("title", ""))
                description = clean_html(entry.get("description", ""))
                link = entry.get("link", "")
                pub_date = parse_date(entry)

                # Date filter
                if pub_date and pub_date < cutoff:
                    continue

                # Combine text for keyword matching
                full_text = f"{title} {description}"
                topics = get_matching_topics(full_text)

                items.append({
                    "source": source,
                    "tier": tier,
                    "title": title,
                    "description": description[:500],
                    "url": link,
                    "published": pub_date.isoformat() if pub_date else None,
                    "topics": topics,
                    "channel": "rss",
                })
                count += 1

            if count > 0:
                print(f"  OK  {source}: {count} items")
            else:
                print(f"  --  {source}: 0 items in date range")

        except Exception as e:
            errors.append(f"  ERR {source}: {str(e)[:80]}")

    if errors:
        print("\n  Errors/Skips:")
        for e in errors:
            print(e)

    return items


# =============================================================================
# Reddit 拉取
# =============================================================================

def fetch_reddit(days_back=7):
    """Fetch Reddit posts and return structured items."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    items = []
    headers = {"User-Agent": "GeopoliticsTracker/1.0 (academic research)"}

    for endpoint in REDDIT_ENDPOINTS:
        try:
            r = requests.get(endpoint["url"], headers=headers, timeout=15)
            if r.status_code != 200:
                print(f"  ERR {endpoint['name']}: status={r.status_code}")
                continue

            data = r.json()
            children = data.get("data", {}).get("children", [])
            count = 0

            for post in children:
                d = post.get("data", {})

                # Skip stickied/pinned
                if d.get("stickied"):
                    continue

                title = d.get("title", "")
                selftext = d.get("selftext", "")[:500]
                score = d.get("score", 0)
                num_comments = d.get("num_comments", 0)
                domain = d.get("domain", "")
                url = d.get("url_overridden_by_dest", d.get("url", ""))
                created = d.get("created_utc", 0)

                pub_date = datetime.fromtimestamp(created, tz=timezone.utc) if created else None

                # Date filter
                if pub_date and pub_date < cutoff:
                    continue

                full_text = f"{title} {selftext}"
                topics = get_matching_topics(full_text)

                items.append({
                    "source": endpoint["name"],
                    "tier": "D",
                    "title": title,
                    "description": selftext[:300] if selftext else "",
                    "url": url,
                    "published": pub_date.isoformat() if pub_date else None,
                    "topics": topics,
                    "channel": "reddit",
                    "reddit_score": score,
                    "reddit_comments": num_comments,
                    "reddit_domain": domain,
                })
                count += 1

            print(f"  OK  {endpoint['name']}: {count} posts")
            time.sleep(1)  # Rate limit

        except Exception as e:
            print(f"  ERR {endpoint['name']}: {str(e)[:80]}")

    return items


# =============================================================================
# 输出
# =============================================================================

def generate_output(items, topic_filter=None, output_dir=None):
    """Generate JSON data file and Markdown summary."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data" / "raw"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Filter by topic if specified
    if topic_filter:
        relevant = [i for i in items if topic_filter in i["topics"]]
        unmatched = [i for i in items if not i["topics"]]
        label = f"topic{topic_filter}"
    else:
        relevant = items
        unmatched = []
        label = "all"

    # Sort by date (newest first), then by tier
    tier_order = {"A": 0, "B": 1, "C": 2, "D": 3}
    relevant.sort(key=lambda x: (
        x.get("published") or "0000",
    ), reverse=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # --- JSON output ---
    json_path = output_dir / f"fetch_{label}_{timestamp}.json"
    output_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "topic_filter": topic_filter,
            "total_items": len(relevant),
            "by_tier": {
                tier: len([i for i in relevant if i["tier"] == tier])
                for tier in ["A", "B", "C", "D"]
            },
            "by_channel": {
                ch: len([i for i in relevant if i["channel"] == ch])
                for ch in ["rss", "reddit"]
            },
        },
        "items": relevant,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # --- Markdown summary ---
    md_path = output_dir / f"fetch_{label}_{timestamp}.md"
    lines = []
    topic_name = TOPIC_KEYWORDS[topic_filter]["name"] if topic_filter else "全部议题"
    lines.append(f"# 信息源拉取摘要 — {topic_name}")
    lines.append(f"")
    lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**总条目**：{len(relevant)}")
    lines.append(f"**来源分布**：A层 {output_data['metadata']['by_tier']['A']} | "
                 f"B层 {output_data['metadata']['by_tier']['B']} | "
                 f"C层 {output_data['metadata']['by_tier']['C']} | "
                 f"D层 {output_data['metadata']['by_tier']['D']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by tier
    for tier, tier_label in [("A", "A层：政府/监管"), ("B", "B层：国际机构"),
                              ("C", "C层：媒体/智库"), ("D", "D层：Reddit")]:
        tier_items = [i for i in relevant if i["tier"] == tier]
        if not tier_items:
            continue

        lines.append(f"## {tier_label}（{len(tier_items)}条）")
        lines.append("")

        for item in tier_items:
            pub = item.get("published", "")[:10] if item.get("published") else "?"
            source = item["source"]
            title = item["title"]
            url = item["url"]
            desc = item.get("description", "")[:200]
            topics_str = ",".join([str(t) for t in item.get("topics", [])])

            # Reddit items show score
            if item["channel"] == "reddit":
                score = item.get("reddit_score", 0)
                comments = item.get("reddit_comments", 0)
                lines.append(f"### [{pub}] {title}")
                lines.append(f"- **来源**：{source} | ↑{score} | {comments}评论 | 域名：{item.get('reddit_domain','')}")
            else:
                lines.append(f"### [{pub}] {title}")
                lines.append(f"- **来源**：{source}")

            if desc:
                lines.append(f"- **摘要**：{desc}")
            if topics_str:
                lines.append(f"- **匹配议题**：{topics_str}")
            lines.append(f"- **链接**：[原文]({url})")
            lines.append("")

    # Unmatched items (if filtering)
    if topic_filter and unmatched:
        lines.append(f"## 未匹配任何议题（{len(unmatched)}条）")
        lines.append("")
        lines.append("以下条目未匹配五大议题关键词，但可能有相关价值：")
        lines.append("")
        for item in unmatched[:20]:  # Cap at 20 to avoid noise
            pub = item.get("published", "")[:10] if item.get("published") else "?"
            lines.append(f"- [{pub}] **{item['source']}** — {item['title']}")
        if len(unmatched) > 20:
            lines.append(f"- ...及另外 {len(unmatched) - 20} 条")
        lines.append("")

    md_content = "\n".join(lines)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return json_path, md_path


# =============================================================================
# 主函数
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="地缘政治信息源拉取脚本")
    parser.add_argument("--topic", type=int, choices=[1, 2, 3, 4, 5],
                        help="只看特定议题（1=制裁, 2=贸易, 3=供应链, 4=技术, 5=地缘政治池）")
    parser.add_argument("--source", choices=["rss", "reddit", "all"], default="all",
                        help="信息源类型（默认 all）")
    parser.add_argument("--days", type=int, default=7,
                        help="回溯天数（默认 7）")
    parser.add_argument("--output", type=str, default=None,
                        help="输出目录（默认 data/）")
    args = parser.parse_args()

    print(f"=" * 60)
    print(f"  地缘政治信息源拉取")
    print(f"  时间范围：最近 {args.days} 天")
    print(f"  信息源：{args.source}")
    print(f"  议题过滤：{'议题 ' + str(args.topic) if args.topic else '全部'}")
    print(f"=" * 60)

    all_items = []

    # RSS
    if args.source in ("rss", "all"):
        print(f"\n[RSS] 拉取 {len(RSS_FEEDS)} 个 feed...")
        rss_items = fetch_rss_feeds(days_back=args.days)
        all_items.extend(rss_items)
        print(f"[RSS] 完成，获取 {len(rss_items)} 条")

    # Reddit
    if args.source in ("reddit", "all"):
        print(f"\n[Reddit] 拉取 {len(REDDIT_ENDPOINTS)} 个端点...")
        reddit_items = fetch_reddit(days_back=args.days)
        all_items.extend(reddit_items)
        print(f"[Reddit] 完成，获取 {len(reddit_items)} 条")

    # Topic matching stats
    print(f"\n{'=' * 60}")
    print(f"  议题匹配统计")
    print(f"{'=' * 60}")
    for t in [1, 2, 3, 4, 5]:
        matched = len([i for i in all_items if t in i.get("topics", [])])
        catchall = " (catch-all)" if t == 5 else ""
        print(f"  议题 {t} ({TOPIC_KEYWORDS[t]['name']}): {matched} 条{catchall}")
    no_match = len([i for i in all_items if not i.get("topics")])
    print(f"  无议题标记: {no_match} 条")
    print(f"  总计: {len(all_items)} 条")

    # Output
    json_path, md_path = generate_output(
        all_items,
        topic_filter=args.topic,
        output_dir=args.output,
    )

    print(f"\n[输出]")
    print(f"  JSON: {json_path}")
    print(f"  Markdown: {md_path}")
    print(f"\n===== 完成 =====")


if __name__ == "__main__":
    main()
