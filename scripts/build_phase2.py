"""
Phase 2 整理流程：从 literature-classic.json 生成 CSV、BibTeX、阅读路线图
按 chatmemory LiteratureSearchSOP Phase 2 规范执行
"""
import json
import csv
import re
from pathlib import Path
from collections import defaultdict

LIT_DIR = Path(__file__).parent.parent / "literature" / "classic"
JSON_PATH = LIT_DIR / "classic.json"

TOPIC_NAMES = {
    1: "制裁与经济管制",
    2: "贸易与产业竞争",
    3: "供应链与关键资源",
    4: "技术竞争与数字治理",
    5: "地缘政治经济学",
}

# ============================================================
# Subtopic classification rules (within each topic)
# ============================================================
SUBTOPICS = {
    1: {
        "制裁有效性与设计": r"sanction.*(effective|success|failure|design|targeted|smart|comprehensive)|economic.sanction.*reconsider",
        "金融制裁与SWIFT": r"financial.sanction|swift|correspondent.bank|payment.system|de-?risking",
        "美元霸权与储备多元化": r"dollar.*(hegemon|weapon|dominan)|reserve.currency|dollar.trap|exorbitant.privilege",
        "人民币国际化与替代体系": r"rmb|renminbi|yuan|cips|人民币|internationaliz.*currency",
        "制裁规避与执行": r"sanction.*(evas|circumvent|enforce|comply)|secondary.sanction|illicit.finance",
        "经济胁迫理论": r"economic.coercion|economic.statecraft|weaponized.interdependen|geoeconomic",
        "国际金融体系": r"bretton.woods|international.monetary|capital.flow|financial.globaliz|capital.account|balance.of.payment",
        "金融市场与资产定价": r"asset.pric|stock.return|cross.section|investor|portfolio|financial.market|risk.premi",
    },
    2: {
        "关税与贸易战": r"tariff|trade.war|301|retali|protectionism|trade.conflict",
        "贸易自由化与福利": r"trade.liberal|gains.from.trade|welfare|free.trade|trade.agreement|wto|gatt",
        "产业政策": r"industrial.policy|subsid|chips.act|infant.industry|strategic.trade|picking.winner",
        "贸易与劳动力市场": r"china.*(syndrome|shock)|import.competition|labor.market|employment|wage|offshoring|outsourcing",
        "FDI与跨国企业": r"foreign.direct|fdi|multinational|mne|eclectic.paradigm|international.production|odi",
        "贸易理论与引力模型": r"gravity|comparative.advantage|heckscher|heterogeneous.firm|melitz|new.trade.theory|ricardian",
        "反倾销与贸易救济": r"anti.?dumping|countervailing|trade.remedy|safeguard|trade.defense",
        "区域经济一体化": r"regional.integration|economic.union|common.market|customs.union|rcep|cptpp|eu.*single.market",
    },
    3: {
        "全球价值链与生产网络": r"global.value.chain|gvc|production.network|fragmentation|vertical.specializ|intermediat.*trade",
        "供应链韧性与重组": r"supply.chain.*(resilien|disrupt|restructur|diversif)|reshoring|nearshoring|friendshoring",
        "能源安全与地缘政治": r"energy.*(security|geopolit|transition)|oil.*(price|shock|geopolit)|opec|natural.gas|lng|pipeline",
        "关键矿产与资源": r"critical.mineral|rare.earth|lithium|cobalt|resource.*(curse|national)|mineral.*policy",
        "粮食安全与农业贸易": r"food.*(security|trade|crisis)|agri.*trade|grain|wheat|fertilizer",
        "国际新创企业与知识": r"international.new.venture|born.global|internationali.*process|knowledge.*firm|evolutionary.*multinational",
        "荷兰病与资源经济": r"dutch.disease|booming.sector|de-?industriali|resource.*(boom|abundant|rich)",
    },
    4: {
        "出口管制与技术限制": r"export.control|entity.list|chip.*war|semiconductor.*restrict|technology.*(restrict|ban|decouple)",
        "AI治理与监管": r"artificial.intelligence|ai.*(regulat|govern|ethic|policy)|machine.learning.*policy",
        "技术变革与劳动力": r"skill.*(bias|content|premium)|technological.change.*labor|automation|robot|polariz.*labor",
        "数字经济与数据治理": r"digital.*(econom|trade|govern)|data.*(sovereign|privacy|locali)|platform.*regulat|e-?commerce",
        "创新政策与R&D": r"innovation.*(policy|subsidy)|r&d|patent|intellectual.property|technology.transfer",
        "技术竞争与标准": r"technology.*(compet|race|standard)|5g|digital.infrastructure|tech.*decoupl",
    },
    5: {
        "制度与发展": r"institution.*(coloniali|development|growth|quality)|why.nations|acemoglu.*robinson|extractive|inclusive",
        "全球不平等": r"inequality|gini|income.distribution|piketty|top.*(income|wealth)|milanovic",
        "国际关系与秩序": r"international.*(regime|order|institution)|embedded.liberal|hegemony|great.power|multipolar",
        "地缘政治风险": r"geopolit.*risk|political.risk|policy.uncertainty|conflict.*econom|war.*econom",
        "全球化与治理": r"globaliz|global.govern|multilateral|sovereignty|democratic.deficit",
        "政治经济学方法论": r"econometric|program.evaluation|difference.in.difference|instrumental.variable|regression.discontin|causal",
        "民族分裂与政治": r"fractionali|ethnic|civil.*(war|conflict)|political.*(instability|violence)|state.capacity",
    },
}


def classify_subtopic(paper, topic_id):
    """Classify a paper into subtopic within a given topic."""
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    text = f"{title} {abstract}"

    best_match = None
    best_score = 0
    for subtopic_name, pattern in SUBTOPICS.get(topic_id, {}).items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        score = len(matches)
        # Title matches count double
        title_matches = re.findall(pattern, title, re.IGNORECASE)
        score += len(title_matches)
        if score > best_score:
            best_score = score
            best_match = subtopic_name

    return best_match or "其他"


def generate_csv(papers):
    """Generate CSV index (Phase 2.1)"""
    csv_path = LIT_DIR / "classic.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "authors", "year", "title", "journal", "tier",
            "citations", "doi_url", "topics", "subtopic", "priority", "notes"
        ])
        for p in sorted(papers, key=lambda x: x.get("citations", 0), reverse=True):
            authors = "; ".join(p.get("authors", [])[:3])
            if len(p.get("authors", [])) > 3:
                authors += " et al."
            topics_str = ",".join(f"T{t}" for t in p.get("topics", []))
            # Classify subtopic for primary topic
            primary_topic = p.get("topics", [0])[0] if p.get("topics") else 0
            subtopic = classify_subtopic(p, primary_topic)

            writer.writerow([
                p.get("id", ""),
                authors,
                p.get("year", ""),
                p.get("title", ""),
                p.get("journal", ""),
                p.get("journal_tier", ""),
                p.get("citations", 0),
                p.get("url", ""),
                topics_str,
                subtopic,
                p.get("priority", ""),
                p.get("notes_zh", ""),
            ])
    print(f"  CSV: {csv_path} ({len(papers)} rows)")
    return csv_path


def generate_bibtex(papers):
    """Generate BibTeX file (Phase 2.2)"""
    bib_path = LIT_DIR / "references.bib"

    def clean_key(s):
        """Make a BibTeX-safe citation key"""
        return re.sub(r'[^a-zA-Z0-9_]', '', s)

    entries = []
    for p in papers:
        key = clean_key(p.get("id", "unknown"))
        authors_raw = p.get("authors", [])
        # BibTeX author format: "Last1, First1 and Last2, First2"
        authors_bib = " and ".join(authors_raw)
        title = p.get("title", "")
        journal = p.get("journal", "")
        year = p.get("year", "")
        volume = p.get("volume", "")
        issue = p.get("issue", "")
        pages = p.get("pages", "")
        doi = p.get("doi", "")

        entry_type = "article"
        # Books
        if any(w in journal.lower() for w in ["press ebooks", "university press", "handbook"]):
            entry_type = "book"
        # Working papers
        if p.get("journal_tier") == "WP" or p.get("nber_wp"):
            entry_type = "techreport"

        lines = [f"@{entry_type}{{{key},"]
        lines.append(f'  author = {{{authors_bib}}},')
        lines.append(f'  title = {{{title}}},')
        lines.append(f'  year = {{{year}}},')
        if entry_type == "article":
            lines.append(f'  journal = {{{journal}}},')
            if volume:
                lines.append(f'  volume = {{{volume}}},')
            if issue:
                lines.append(f'  number = {{{issue}}},')
            if pages:
                lines.append(f'  pages = {{{pages}}},')
        elif entry_type == "book":
            lines.append(f'  publisher = {{{journal}}},')
        elif entry_type == "techreport":
            lines.append(f'  institution = {{{journal}}},')
            if p.get("nber_wp"):
                lines.append(f'  number = {{{p["nber_wp"]}}},')
            lines.append(f'  type = {{Working Paper}},')
        if doi:
            lines.append(f'  doi = {{{doi}}},')
        url = p.get("url", "")
        if url:
            lines.append(f'  url = {{{url}}},')
        lines.append("}")
        entries.append("\n".join(lines))

    with open(bib_path, "w", encoding="utf-8") as f:
        f.write("% Auto-generated BibTeX from classic.json\n")
        f.write(f"% {len(entries)} entries | Generated by build_phase2.py\n\n")
        f.write("\n\n".join(entries))
        f.write("\n")
    print(f"  BibTeX: {bib_path} ({len(entries)} entries)")
    return bib_path


def generate_reading_roadmap(papers):
    """Generate reading roadmap (Phase 2.4)"""
    roadmap_path = LIT_DIR / "reading-roadmap.md"

    # Group papers by topic, then subtopic
    topic_papers = defaultdict(list)
    for p in papers:
        for t in p.get("topics", []):
            subtopic = classify_subtopic(p, t)
            topic_papers[t].append((subtopic, p))

    lines = []
    lines.append("# 阅读路线图 (Reading Roadmap)")
    lines.append("")
    lines.append("> 按议题 → 子主题 → 优先级排列。Core 必读，Recommended 推荐，Reference 参考。")
    lines.append(f"> 总计 {len(papers)} 篇论文")
    lines.append("")

    # Priority order
    priority_order = {"core": 0, "recommended": 1, "reference": 2}

    for topic_id in range(1, 6):
        topic_name = TOPIC_NAMES[topic_id]
        tp = topic_papers[topic_id]
        lines.append(f"## T{topic_id}: {topic_name} ({len(tp)} 篇)")
        lines.append("")

        # Group by subtopic
        subtopic_groups = defaultdict(list)
        for subtopic, p in tp:
            subtopic_groups[subtopic].append(p)

        # Sort subtopics by total citations
        sorted_subtopics = sorted(
            subtopic_groups.items(),
            key=lambda x: sum(p.get("citations", 0) for p in x[1]),
            reverse=True,
        )

        for subtopic_name, sub_papers in sorted_subtopics:
            # Sort within subtopic by priority then citations
            sub_papers.sort(
                key=lambda p: (
                    priority_order.get(p.get("priority", "reference"), 9),
                    -p.get("citations", 0),
                )
            )
            lines.append(f"### {subtopic_name}")
            lines.append("")

            for p in sub_papers[:15]:  # Cap at 15 per subtopic
                cites = p.get("citations", 0)
                tier = p.get("journal_tier", "?")
                pri = p.get("priority", "reference")
                pri_icon = {"core": "★", "recommended": "◆", "reference": "○"}.get(pri, "·")
                authors = ", ".join(p.get("authors", [])[:2])
                if len(p.get("authors", [])) > 2:
                    authors += " et al."
                year = p.get("year", "?")
                title = p.get("title", "")
                journal = p.get("journal", "")
                doi_url = p.get("url", "")

                lines.append(f"- {pri_icon} **{authors} ({year})** — {title}")
                lines.append(f"  - {journal} [{tier}] | {cites} citations")
                if doi_url:
                    lines.append(f"  - DOI: [{doi_url}]({doi_url})")
                notes = p.get("notes_zh", "")
                if notes:
                    lines.append(f"  - 📝 {notes}")
                lines.append("")

            if len(sub_papers) > 15:
                lines.append(f"  *(另有 {len(sub_papers)-15} 篇，见 CSV 完整索引)*")
                lines.append("")

        lines.append("---")
        lines.append("")

    with open(roadmap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Roadmap: {roadmap_path}")
    return roadmap_path


def main():
    print("=== Phase 2: 文献整理 ===")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    papers = data["papers"]
    print(f"Loaded {len(papers)} papers from {JSON_PATH}")

    # 2.1 CSV
    print("\n[2.1] 生成 CSV 结构化索引...")
    generate_csv(papers)

    # 2.2 BibTeX
    print("\n[2.2] 生成 BibTeX...")
    generate_bibtex(papers)

    # 2.3 + 2.4 Subtopic classification + Reading roadmap
    print("\n[2.3+2.4] 子主题分类 + 阅读路线图...")
    generate_reading_roadmap(papers)

    # Summary
    print("\n=== Phase 2 完成 ===")
    print(f"产出文件：")
    print(f"  literature/classic/classic.csv      — CSV 结构化索引")
    print(f"  literature/classic/references.bib   — BibTeX 引用文件")
    print(f"  literature/classic/reading-roadmap.md — 阅读路线图")


if __name__ == "__main__":
    main()
