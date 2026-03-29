"""
Literature Database Builder (Phase A)
=====================================
Uses OpenAlex API to build the classic literature database.
Strategy:
  1. Author-based search: For each named author, get top-cited works
  2. Keyword-based search: For each topic's keyword queries
  3. Merge, deduplicate, and output JSON

OpenAlex API: https://docs.openalex.org/
- Free, no API key required
- Polite pool: add email to get higher rate limits
- Rate limit: 10 req/s (polite), 1 req/s (anonymous)
"""

import requests
import json
import time
import re
import sys
import os
from datetime import datetime
from pathlib import Path

# --- Configuration ---
EMAIL = "ginger@research.edu"  # For polite pool access
BASE_URL = "https://api.openalex.org"
RATE_LIMIT_DELAY = 0.15  # seconds between requests (polite pool)
OUTPUT_DIR = Path(__file__).parent.parent / "file" / "literature"

# --- Named Authors per Topic ---
# Format: (display_name_query, openalex_hint, topics, description)
NAMED_AUTHORS = [
    # T1: Sanctions & Economic Coercion
    ("Gary Hufbauer", None, [1], "制裁有效性数据库"),
    ("Daniel Drezner", None, [1], "制裁政治学"),
    ("Henry Farrell", None, [1, 5], "weaponized interdependence"),
    ("Abraham Newman", None, [1, 5], "weaponized interdependence"),
    ("Bryan Early", None, [1], "制裁规避"),
    ("Dursun Peksen", None, [1], "制裁经济后果"),
    ("Barry Eichengreen", None, [1], "货币霸权/储备多元化"),
    ("Eswar Prasad", None, [1], "人民币国际化"),
    ("Matteo Maggiori", None, [1], "美元体系/safe assets"),
    ("Javier Bianchi", None, [1], "制裁与美元主导"),
    ("Oleg Itskhoki", None, [1], "制裁与汇率"),
    
    # T2: Trade & Industrial Competition
    ("Pablo Fajgelbaum", None, [2], "贸易战福利分析"),
    ("Mary Amiti", None, [2], "关税传导"),
    ("Robert Staiger", None, [2], "贸易协定理论"),
    ("Kyle Bagwell", None, [2], "WTO经济学"),
    ("Dani Rodrik", None, [2, 5], "产业政策/全球化三难"),
    ("Marc Melitz", None, [2], "异质企业贸易"),
    ("Ralph Ossa", None, [2], "最优关税"),
    
    # T3: Supply Chain & Critical Resources
    ("Pol Antras", None, [3], "全球价值链理论"),
    ("Richard Baldwin", None, [3], "GVC/供应链贸易"),
    ("Laura Alfaro", None, [3], "全球供应链重组"),
    ("Davin Chor", None, [3], "供应链重组"),
    ("Chad Bown", None, [2, 3], "贸易政策+供应链"),
    ("Michael Ross", None, [3], "资源诅咒"),
    ("James Hamilton", "James D. Hamilton", [3], "石油与宏观经济"),
    
    # T4: Tech Competition & Digital Governance
    ("Daron Acemoglu", None, [4, 5], "AI/技术/制度"),
    ("David Autor", None, [4], "技术与劳动力市场"),
    ("Ufuk Akcigit", None, [4], "创新政策"),
    
    # T5: Geopolitical Economics
    ("Branko Milanovic", None, [5], "全球不平等"),
    ("Thomas Piketty", None, [5], "资本/不平等"),
    ("Jeffrey Frankel", None, [1, 5], "国际宏观/汇率"),
    ("Michael Pettis", None, [5], "中国经济/贸易失衡"),
]

# --- Topic Keyword Queries ---
# Each query will be used with OpenAlex search
TOPIC_QUERIES = {
    1: [  # Sanctions
        "economic sanctions effectiveness empirical",
        "weaponized interdependence economic networks coercion",
        "dollar hegemony reserve currency diversification",
        "SWIFT sanctions financial exclusion payment",
        "RMB internationalization yuan renminbi",
        "sanctions evasion circumvention enforcement",
        "secondary sanctions compliance",
        "financial sanctions targeted smart",
        "sanctions regime change policy",
        "economic coercion statecraft",
        "sanctions Russia trade effects",
        "dollar weaponization financial",
    ],
    2: [  # Trade
        "trade war tariff welfare 2018 China",
        "tariff passthrough consumer welfare empirical",
        "Section 301 China tariffs effects",
        "industrial policy subsidies effectiveness",
        "optimal tariff theory",
        "WTO dispute settlement reform",
        "CHIPS Act semiconductor industrial policy",
        "trade agreement welfare gains",
        "infant industry protection empirical",
        "beggar thy neighbor trade policy",
    ],
    3: [  # Supply Chain
        "global value chains fragmentation reshoring",
        "critical minerals supply chain policy",
        "resource curse institutions development",
        "oil price shocks macroeconomic effects",
        "energy transition geopolitics",
        "OPEC market power oil production",
        "supply chain resilience diversification",
        "production networks international trade",
        "friendshoring nearshoring economic effects",
    ],
    4: [  # Tech
        "export controls technology semiconductor",
        "technology decoupling US China",
        "AI regulation governance economic impact",
        "chip war semiconductor geopolitics",
        "digital trade data sovereignty",
        "innovation policy R&D subsidy",
        "technology transfer developing countries",
        "platform regulation antitrust digital",
    ],
    5: [  # Geopolitics
        "geopolitical risk economic impact measurement",
        "geoeconomics theory framework",
        "economic statecraft tools",
        "great power competition economic",
        "institutions colonialism development",
        "global inequality trends",
        "international monetary system reform",
        "economic coercion empirical",
    ],
}

# --- Relevance keywords for filtering ---
TOPIC_RELEVANCE_KEYWORDS = {
    1: r"sanction|embargo|coerci|dollar|reserve.currency|swift|rmb|yuan|renminbi|weaponiz|financial.war|economic.war|dedollar|de-dollar|monetary.hegemony|cips",
    2: r"tariff|trade.war|trade.policy|industrial.policy|wto|subsid|dumping|countervail|free.trade|protectio|chips.act|trade.agreement|import.duty|export.subsid",
    3: r"supply.chain|value.chain|critical.mineral|rare.earth|oil.price|energy|opec|resource.curse|reshoring|friendshor|lng|food.security|commodity",
    4: r"semiconductor|chip|artificial.intelligence|\bai\b|export.control|technology.transfer|digital|cyber|5g|quantum|biotech|innovation.policy|r&d",
    5: r"geopolitic|geoeconom|great.power|institution|inequality|colonial|statecraft|international.order|hegemony|global.south|development",
}


def openalex_get(endpoint, params=None):
    """Make a request to OpenAlex API with rate limiting."""
    if params is None:
        params = {}
    params["mailto"] = EMAIL
    url = f"{BASE_URL}/{endpoint}"
    time.sleep(RATE_LIMIT_DELAY)
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 429:
            print("  [Rate limited, waiting 5s...]")
            time.sleep(5)
            r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  [API Error: {e}]")
        return None


def search_author(name, hint=None):
    """Search for an author on OpenAlex, return author ID."""
    query = hint or name
    data = openalex_get("authors", {"search": query, "per_page": 5})
    if not data or not data.get("results"):
        return None
    
    # Try exact match first
    for author in data["results"]:
        if author["display_name"].lower() == name.lower():
            return author["id"]
    
    # Try partial match
    name_parts = name.lower().split()
    for author in data["results"]:
        dn = author["display_name"].lower()
        if all(p in dn for p in name_parts):
            return author["id"]
    
    # Fall back to first result if works_count is high enough
    if data["results"][0].get("works_count", 0) > 10:
        return data["results"][0]["id"]
    
    return None


def get_author_top_works(author_id, max_papers=20):
    """Get an author's top-cited works from OpenAlex, filtered to econ/polisci."""
    concept_filter = "concepts.id:C162324750|C17744445|C61644048|C556758197|C175444787|C139719470|C118084267"
    data = openalex_get("works", {
        "filter": f"authorships.author.id:{author_id},{concept_filter}",
        "sort": "cited_by_count:desc",
        "per_page": max_papers,
        "select": "id,title,authorships,publication_year,primary_location,cited_by_count,doi,abstract_inverted_index,concepts,topics"
    })
    if not data:
        return []
    return data.get("results", [])


def search_works(query, max_papers=30, min_citations=0):
    """Search for works by keyword query, filtered to economics/political science."""
    # OpenAlex concept IDs for relevant disciplines
    # C162324750 = Economics, C17744445 = Political Science
    # C61644048 = International Economics, C556758197 = International Trade
    concept_filter = "concepts.id:C162324750|C17744445|C61644048|C556758197|C175444787|C139719470|C118084267"
    # C175444787 = Finance, C139719470 = Macroeconomics, C118084267 = Development Economics
    
    data = openalex_get("works", {
        "search": query,
        "sort": "cited_by_count:desc",
        "per_page": max_papers,
        "filter": f"cited_by_count:>{min_citations},type:article|review|book,{concept_filter}",
        "select": "id,title,authorships,publication_year,primary_location,cited_by_count,doi,abstract_inverted_index,concepts,topics"
    })
    if not data:
        return []
    return data.get("results", [])


def reconstruct_abstract(inverted_index):
    """Reconstruct abstract from OpenAlex inverted index format."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)


def extract_paper_info(work):
    """Extract structured paper info from OpenAlex work object."""
    if not work or not work.get("title"):
        return None
    
    # Authors
    authors = []
    for a in work.get("authorships", [])[:10]:
        author = a.get("author", {})
        if author.get("display_name"):
            authors.append(author["display_name"])
    
    # Journal
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    journal = source.get("display_name", "")
    
    # DOI
    doi = work.get("doi", "")
    if doi and doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    
    # Abstract
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    
    return {
        "openalex_id": work.get("id", ""),
        "title": work["title"],
        "authors": authors,
        "year": work.get("publication_year"),
        "journal": journal,
        "doi": doi,
        "url": f"https://doi.org/{doi}" if doi else "",
        "citations": work.get("cited_by_count", 0),
        "abstract": abstract[:500] if abstract else "",
    }


def is_relevant_to_topic(paper_info, topic_num):
    """Check if a paper is relevant to a given topic based on title + abstract keywords."""
    text = f"{paper_info.get('title', '')} {paper_info.get('abstract', '')}".lower()
    pattern = TOPIC_RELEVANCE_KEYWORDS.get(topic_num, "")
    if not pattern:
        return False
    return bool(re.search(pattern, text, re.IGNORECASE))


def generate_paper_id(paper):
    """Generate a readable paper ID from authors + year."""
    authors = paper.get("authors", [])
    year = paper.get("year", "")
    if not authors:
        # Use first word of title
        words = paper.get("title", "unknown").split()[:2]
        base = "_".join(w.lower() for w in words)
    elif len(authors) == 1:
        base = authors[0].split()[-1].lower()
    elif len(authors) == 2:
        base = f"{authors[0].split()[-1].lower()}_{authors[1].split()[-1].lower()}"
    else:
        base = f"{authors[0].split()[-1].lower()}_etal"
    
    # Clean
    base = re.sub(r"[^a-z0-9_]", "", base)
    return f"{base}_{year}" if year else base


def determine_priority(citations):
    """Determine reading priority based on citation count."""
    if citations >= 500:
        return "core"
    elif citations >= 100:
        return "recommended"
    else:
        return "reference"


def determine_journal_tier(journal_name):
    """Determine journal tier from name."""
    if not journal_name:
        return "unknown"
    
    j = journal_name.lower()
    
    # Tier 1
    tier1 = [
        "american economic review", "quarterly journal of economics",
        "journal of political economy", "econometrica",
        "review of economic studies", "journal of finance",
        "journal of financial economics", "review of financial studies"
    ]
    for t in tier1:
        if t in j:
            return "T1"
    
    # Tier 2
    tier2 = [
        "journal of international economics", "review of economics and statistics",
        "american economic journal", "journal of the european economic association",
        "review of international economics", "journal of development economics",
        "journal of monetary economics", "journal of public economics",
        "economic journal", "journal of economic literature",
        "journal of economic perspectives", "brookings papers"
    ]
    for t in tier2:
        if t in j:
            return "T2"
    
    # Tier 3 (political science)
    tier3 = [
        "international organization", "american political science review",
        "journal of peace research", "journal of conflict resolution",
        "world politics", "international security", "foreign affairs"
    ]
    for t in tier3:
        if t in j:
            return "T3"
    
    # Working papers
    wp_indicators = ["nber", "cepr", "ssrn", "working paper", "discussion paper",
                     "world bank", "imf", "policy research"]
    for w in wp_indicators:
        if w in j:
            return "WP"
    
    return "other"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build classic literature database via OpenAlex")
    parser.add_argument("--topic", type=int, choices=[1, 2, 3, 4, 5, 0],
                        default=0, help="Topic to search (0=all)")
    parser.add_argument("--authors-only", action="store_true",
                        help="Only search by named authors")
    parser.add_argument("--keywords-only", action="store_true",
                        help="Only search by keywords")
    parser.add_argument("--min-citations", type=int, default=20,
                        help="Minimum citation count for keyword search (default: 20)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan without executing")
    args = parser.parse_args()
    
    topics_to_search = [args.topic] if args.topic != 0 else [1, 2, 3, 4, 5]
    
    all_papers = {}  # DOI -> paper dict (for dedup)
    paper_topics = {}  # DOI -> set of topic numbers
    
    # ========== Phase 1: Author-based search ==========
    if not args.keywords_only:
        print("\n" + "=" * 60)
        print("PHASE 1: AUTHOR-BASED SEARCH")
        print("=" * 60)
        
        for name, hint, topics, desc in NAMED_AUTHORS:
            # Skip if not in selected topics
            if not any(t in topics_to_search for t in topics):
                continue
            
            if args.dry_run:
                print(f"  [DRY RUN] Would search author: {name} ({desc})")
                continue
            
            print(f"\n>>> Searching author: {name} ({desc})...")
            author_id = search_author(name, hint)
            
            if not author_id:
                print(f"  [NOT FOUND] {name}")
                continue
            
            print(f"  Found: {author_id}")
            works = get_author_top_works(author_id, max_papers=15)
            
            relevant_count = 0
            for w in works:
                info = extract_paper_info(w)
                if not info or not info["doi"]:
                    continue
                
                # Check relevance to any of the author's topics
                relevant_topics = set()
                for t in topics:
                    if is_relevant_to_topic(info, t):
                        relevant_topics.add(t)
                
                # Also check all 5 topics for cross-topic papers
                for t in range(1, 6):
                    if is_relevant_to_topic(info, t):
                        relevant_topics.add(t)
                
                if not relevant_topics:
                    # Author's works without topic match get assigned to author's default topics
                    # but only if high citations
                    if info["citations"] >= 200:
                        relevant_topics = set(topics)
                    else:
                        continue
                
                doi = info["doi"]
                if doi not in all_papers:
                    all_papers[doi] = info
                    paper_topics[doi] = relevant_topics
                    relevant_count += 1
                else:
                    paper_topics[doi].update(relevant_topics)
            
            print(f"  Added {relevant_count} papers (total unique: {len(all_papers)})")
    
    # ========== Phase 2: Keyword-based search ==========
    if not args.authors_only:
        print("\n" + "=" * 60)
        print("PHASE 2: KEYWORD-BASED SEARCH")
        print("=" * 60)
        
        for topic_num in topics_to_search:
            queries = TOPIC_QUERIES.get(topic_num, [])
            print(f"\n--- Topic {topic_num} ({len(queries)} queries) ---")
            
            for query in queries:
                if args.dry_run:
                    print(f"  [DRY RUN] Would search: '{query}'")
                    continue
                
                print(f"  Searching: '{query}'...")
                works = search_works(query, max_papers=20, min_citations=args.min_citations)
                
                new_count = 0
                for w in works:
                    info = extract_paper_info(w)
                    if not info or not info["doi"]:
                        continue
                    
                    # Check relevance
                    relevant_topics = set()
                    for t in range(1, 6):
                        if is_relevant_to_topic(info, t):
                            relevant_topics.add(t)
                    
                    if not relevant_topics:
                        relevant_topics = {topic_num}  # Assign to search topic
                    
                    doi = info["doi"]
                    if doi not in all_papers:
                        all_papers[doi] = info
                        paper_topics[doi] = relevant_topics
                        new_count += 1
                    else:
                        paper_topics[doi].update(relevant_topics)
                
                print(f"    → {new_count} new papers (total: {len(all_papers)})")
    
    if args.dry_run:
        print(f"\n[DRY RUN] Would execute searches. Exiting.")
        return
    
    # ========== Phase 2.5: Post-processing filter ==========
    print("\n" + "=" * 60)
    print(f"POST-PROCESSING: {len(all_papers)} raw papers")
    print("=" * 60)
    
    # Broader list of economics/polisci/IR/policy journals (for 'other' tier recovery)
    econ_polisci_journals = [
        # Additional economics journals not in tier 1-3
        "economic policy", "world economy", "oxford economic papers",
        "journal of international money", "journal of economic growth",
        "journal of law and economics", "rand journal", "journal of labor economics",
        "journal of economic theory", "games and economic behavior",
        "international economic review", "journal of economic behavior",
        "journal of economic dynamics", "european economic review",
        "canadian journal of economics", "scandinavian journal of economics",
        "journal of money, credit", "economic inquiry", "journal of applied economics",
        "journal of economic geography", "world bank economic review",
        "imf economic review", "journal of comparative economics",
        "journal of urban economics", "oxford review of economic",
        "review of international political economy", "annual review of economics",
        "journal of economic history", "explorations in economic history",
        "economic history review", "journal of world trade",
        "world trade review", "journal of international trade",
        "review of world economics", "weltwirtschaftliches archiv",
        "open economies review", "journal of globalization and development",
        "journal of international financial markets",
        # IR / Political Science
        "review of international studies", "european journal of international relations",
        "international studies quarterly", "international affairs",
        "security studies", "journal of strategic studies", "survival",
        "international studies review", "global governance",
        "british journal of political science", "comparative political studies",
        "annual review of political science",  "european journal of political economy",
        "political analysis", "journal of politics",
        # Policy-oriented
        "foreign policy", "national interest", "washington quarterly",
        "chicago journal", "journal of policy", "policy analysis",
        "regulation & governance", "global policy",
        # Area studies with econ focus
        "china economic review", "china quarterly", "journal of asian economics",
        "asian economic", "emerging markets", "post-soviet",
        "journal of african economies", "latin american",
        # Energy/Resource economics
        "energy economics", "energy policy", "energy journal",
        "resource and energy economics", "resources policy",
        "journal of commodity markets", "opec review",
        # Tech/Innovation economics
        "research policy", "technological forecasting", "technovation",
        "information economics", "telecommunications policy",
        "journal of technology transfer",
    ]
    
    # Irrelevant journal patterns (definite exclusion)
    irrelevant_journal_patterns = [
        r"medic|clinic|health|nurs|surg|cardio|oncol|cancer|pathol|pharm|dent|vet",
        r"biolog|biochem|biophys|molec|cell|gene|genom|proteo|immuno|virol|microb",
        r"physic[^a]|chem[^i]|mater|nano|optic|quantum(?!.*econom)",
        r"environ(?!.*econom)|ecolog(?!.*econom)|forest|agric(?!.*trade)|soil|water",
        r"psycholog|psychiatr|behav(?!.*econom)|cognit|neurosci|brain",
        r"math(?!.*econom)|statist(?!.*econom)|comput(?!.*econom)|algorith|machine.learn",
        r"engineer|mechani|electr|robot|aerosp|civil.eng",
        r"educ(?!.*econom)|teach|learn(?!.*econom)|curricul|pedagog",
        r"sport|exercis|athlet|fitness|physical.therap",
        r"management(?!.*econom)|business(?!.*econom)|marketing|logistics|human.resource",
        r"law(?!.*econom)|legal(?!.*econom)|jurisprudence|criminal",
        r"librar|museum|archiv|archaeol|anthropol(?!.*econom)|linguist|sociology(?!.*econom)",
    ]
    
    filtered_papers = {}
    excluded_count = 0
    recovered_count = 0
    
    for doi, info in all_papers.items():
        journal = info.get("journal", "").lower()
        tier = determine_journal_tier(info["journal"])
        
        # T1/T2/T3/WP — always keep
        if tier in ("T1", "T2", "T3", "WP"):
            filtered_papers[doi] = info
            continue
        
        # Check if journal matches broader econ/polisci list
        is_econ_journal = any(ej in journal for ej in econ_polisci_journals)
        
        # Check if journal is definitely irrelevant
        is_irrelevant = any(re.search(pat, journal) for pat in irrelevant_journal_patterns) if journal else False
        
        if is_irrelevant:
            excluded_count += 1
            continue
        
        if is_econ_journal:
            filtered_papers[doi] = info
            recovered_count += 1
            continue
        
        # Unknown journal: require high citations AND relevant title
        title_text = (info.get("title", "") + " " + info.get("abstract", "")).lower()
        all_topic_keywords = "|".join(TOPIC_RELEVANCE_KEYWORDS.values())
        has_relevant_keywords = bool(re.search(all_topic_keywords, title_text))
        
        if has_relevant_keywords and info["citations"] >= 200:
            filtered_papers[doi] = info
            recovered_count += 1
        elif info["citations"] >= 1000 and has_relevant_keywords:
            filtered_papers[doi] = info
            recovered_count += 1
        else:
            excluded_count += 1
    
    print(f"  Excluded: {excluded_count} (irrelevant journals/low relevance)")
    print(f"  Recovered (broader econ/polisci): {recovered_count}")
    print(f"  Kept: {len(filtered_papers)}")
    
    # Replace all_papers with filtered version
    all_papers = filtered_papers
    
    # ========== Phase 3: Build output ==========
    print("\n" + "=" * 60)
    print(f"BUILDING OUTPUT: {len(all_papers)} unique papers")
    print("=" * 60)
    
    papers_list = []
    for doi, info in all_papers.items():
        topics = sorted(paper_topics.get(doi, set()))
        paper_id = generate_paper_id(info)
        
        # Ensure unique ID
        existing_ids = [p["id"] for p in papers_list]
        if paper_id in existing_ids:
            paper_id = f"{paper_id}_b"
        
        # Topic relevance descriptions (placeholder)
        topic_relevance = {}
        for t in topics:
            topic_relevance[str(t)] = ""  # To be filled manually
        
        paper = {
            "id": paper_id,
            "title": info["title"],
            "authors": info["authors"],
            "year": info["year"],
            "journal": info["journal"],
            "journal_tier": determine_journal_tier(info["journal"]),
            "volume": "",
            "issue": "",
            "pages": "",
            "doi": doi,
            "url": info["url"],
            "webvpn_url": None,
            "nber_wp": None,
            "ssrn_id": None,
            "abstract": info["abstract"],
            "jel_codes": [],
            "topics": topics,
            "topic_relevance": topic_relevance,
            "priority": determine_priority(info["citations"]),
            "citations": info["citations"],
            "tags": [],
            "notes_zh": "",
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "read_status": "unread"
        }
        papers_list.append(paper)
    
    # Sort by citations desc
    papers_list.sort(key=lambda p: p["citations"], reverse=True)
    
    # Stats
    topic_counts = {t: 0 for t in range(1, 6)}
    tier_counts = {}
    priority_counts = {"core": 0, "recommended": 0, "reference": 0}
    
    for p in papers_list:
        for t in p["topics"]:
            topic_counts[t] = topic_counts.get(t, 0) + 1
        tier = p["journal_tier"]
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        priority_counts[p["priority"]] = priority_counts.get(p["priority"], 0) + 1
    
    print(f"\nPapers by topic: {dict(topic_counts)}")
    print(f"Papers by tier: {dict(tier_counts)}")
    print(f"Papers by priority: {dict(priority_counts)}")
    
    # Output JSON
    output = {
        "metadata": {
            "library": "classic",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "total_papers": len(papers_list),
            "topic_counts": topic_counts,
            "tier_counts": tier_counts,
            "priority_counts": priority_counts,
            "generated_by": "build_literature.py Phase A"
        },
        "papers": papers_list
    }
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    output_file = OUTPUT_DIR / "literature-classic.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nOutput: {output_file}")
    print(f"Total papers: {len(papers_list)}")
    
    # Also output a quick summary
    summary_file = OUTPUT_DIR / "_build_summary.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"# Literature Build Summary\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Total papers**: {len(papers_list)}\n\n")
        f.write(f"## By Topic\n")
        for t in range(1, 6):
            f.write(f"- T{t}: {topic_counts.get(t, 0)} papers\n")
        f.write(f"\n## By Tier\n")
        for tier, count in sorted(tier_counts.items()):
            f.write(f"- {tier}: {count}\n")
        f.write(f"\n## By Priority\n")
        for pri, count in priority_counts.items():
            f.write(f"- {pri}: {count}\n")
        f.write(f"\n## Top 20 by Citations\n\n")
        for i, p in enumerate(papers_list[:20], 1):
            authors_str = ", ".join(p["authors"][:3])
            if len(p["authors"]) > 3:
                authors_str += " et al."
            f.write(f"{i}. **{p['title']}** ({p['year']})\n")
            f.write(f"   - {authors_str}\n")
            f.write(f"   - {p['journal']} | {p['citations']} citations | {p['priority']}\n")
            f.write(f"   - Topics: {', '.join(f'T{t}' for t in p['topics'])}\n\n")
    
    print(f"Summary: {summary_file}")


if __name__ == "__main__":
    main()
