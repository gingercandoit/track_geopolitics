"""
Site configuration for track_geopolitics static website.
All paths, colors, fonts, and topic definitions are centralized here.
"""
from pathlib import Path

# ── Paths (relative to site/ directory) ──────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent  # track_geopolitics/
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
LITERATURE_DIR = PROJECT_ROOT / "literature"
TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"
OUTPUT_DIR = Path(__file__).parent / "dist"

# ── Site metadata ────────────────────────────────────────────────────
SITE_TITLE = "Geopolitical Economics Monthly"
SITE_SUBTITLE = "地缘政治经济月度追踪"
SITE_LANG = "zh-CN"

# ── Topics ───────────────────────────────────────────────────────────
TOPICS = {
    "topic1-sanctions": {
        "id": 1,
        "name_zh": "制裁与经济管制",
        "name_short": "制裁",
        "name_en": "Sanctions & Economic Controls",
        "slug": "topic1-sanctions",
        "color": "#8B0000",
        "icon": "shield",
        "compact": False,
    },
    "topic2-trade-industrial": {
        "id": 2,
        "name_zh": "贸易与产业政策",
        "name_short": "贸易",
        "name_en": "Trade & Industrial Policy",
        "slug": "topic2-trade-industrial",
        "color": "#1B4965",
        "icon": "scale",
        "compact": False,
    },
    "topic3-supply-resources": {
        "id": 3,
        "name_zh": "能源安全与资源角力",
        "name_short": "能源",
        "name_en": "Energy Security & Resource Contest",
        "slug": "topic3-supply-resources",
        "color": "#2E7D32",
        "icon": "link",
        "compact": False,
    },
    "topic4-tech-digital": {
        "id": 4,
        "name_zh": "技术竞争与规则制定",
        "name_short": "科技",
        "name_en": "Tech Competition & Rule-Making",
        "slug": "topic4-tech-digital",
        "color": "#5C6BC0",
        "icon": "cpu",
        "compact": False,
    },
    "topic5-geopolitics": {
        "id": 5,
        "name_zh": "更多社媒资讯",
        "name_short": "社媒",
        "name_en": "More from Social Media",
        "slug": "topic5-geopolitics",
        "color": "#455A64",
        "icon": "globe",
        "compact": True,
    },
}

# ── Event type colors ────────────────────────────────────────────────
EVENT_TYPE_COLORS = {
    "政策发布": "#1B4965",
    "贸易调查": "#D4A574",
    "制裁管制": "#8B0000",
    "外交动态": "#2E7D32",
    "国际机构": "#5C6BC0",
    "智库分析": "#6D4C41",
    "企业动态": "#F57C00",
    "数据发布": "#455A64",
}

# ── Visual design tokens ─────────────────────────────────────────────
COLORS = {
    "bg": "#FAFAF7",
    "text": "#1A1A1A",
    "text_secondary": "#555555",
    "accent": "#8B0000",
    "link": "#2C5F7C",
    "link_hover": "#1A3F5C",
    "card_bg": "#FFFFFF",
    "card_border": "#E8E5E0",
    "card_shadow": "0 1px 3px rgba(0,0,0,0.08)",
    "divider": "#E0DDD8",
    "tag_bg": "#F0EDE8",
    "nav_bg": "#FFFFFF",
    "footer_bg": "#F5F3EE",
}

FONTS = {
    "heading": "'Playfair Display', 'Noto Serif SC', serif",
    "body": "'Source Serif Pro', 'Noto Serif SC', serif",
    "label": "'DM Sans', 'Noto Sans SC', sans-serif",
    "mono": "'JetBrains Mono', 'Fira Code', monospace",
}

# ── Source tier labels ────────────────────────────────────────────────
SOURCE_TIERS = {
    "A": {"label": "官方", "color": "#8B0000"},
    "B": {"label": "国际机构", "color": "#1B4965"},
    "C": {"label": "智库/媒体", "color": "#6D4C41"},
    "D": {"label": "社区", "color": "#999999"},
}

# ── Literature priority labels ────────────────────────────────────────
PRIORITY_LABELS = {
    "core": {"label": "核心必读", "color": "#8B0000"},
    "recommended": {"label": "推荐阅读", "color": "#1B4965"},
    "reference": {"label": "参考文献", "color": "#6D4C41"},
}

# ── Journal tier labels ──────────────────────────────────────────────
JOURNAL_TIERS = {
    "T1": {"label": "Top 5 + Finance Top", "color": "#8B0000"},
    "T2": {"label": "Field Top", "color": "#1B4965"},
    "T3": {"label": "政治学/IR Top", "color": "#2E7D32"},
    "WP": {"label": "Working Paper", "color": "#F57C00"},
}

# ── Journal abbreviations ─────────────────────────────────────────────
JOURNAL_ABBREV = {
    # T1
    "American Economic Review": "AER",
    "Econometrica": "Econometrica",
    "Journal of Political Economy": "JPE",
    "The Quarterly Journal of Economics": "QJE",
    "The Review of Economic Studies": "RES",
    # T2
    "American Economic Review Insights": "AER Insights",
    "AEA Papers and Proceedings": "AEA P&P",
    "American Economic Journal Applied Economics": "AEJ: Applied",
    "Annual Review of Economics": "Ann.Rev.Econ",
    "Brookings Papers on Economic Activity": "Brookings Papers",
    "China & World Economy": "China World Econ",
    "International Economic Review": "Int'l Econ Rev",
    "Journal of Development Economics": "J Dev Econ",
    "Journal of Economic Growth": "J Econ Growth",
    "Journal of Economic Literature": "JEL",
    "Journal of Economic Surveys": "J Econ Surveys",
    "Journal of International Economics": "JIE",
    "Journal of Monetary Economics": "J Mon Econ",
    "Journal of the European Economic Association": "JEEA",
    "Review of International Political Economy": "RIPE",
    "The Journal of Economic Perspectives": "JEP",
    "World Economy": "World Economy",
    # T3
    "Asia policy": "Asia Policy",
    "Industrial and Corporate Change": "Ind Corp Change",
    "International Affairs": "Int'l Affairs",
    "International Organization": "IO",
    "International Security": "Int'l Security",
    "International Studies Quarterly": "ISQ",
    "Journal of Conflict Resolution": "JCR",
    "Journal of European Public Policy": "JEPP",
    "Journal of Global Security Studies": "JGSS",
    "Journal of International Economic Law": "JIEL",
    "Journal of Peace Research": "J Peace Res",
    "The Journal of Politics": "J Politics",
    "The Review of International Organizations": "Rev Int'l Org",
    "World Politics": "World Politics",
    # WP
    "IMF Working Paper": "IMF WP",
    "IMF staff discussion note": "IMF Note",
    "National Bureau of Economic Research": "NBER",
    # other
    "AI & Society": "AI & Society",
    "Development and Change": "Dev Change",
    "Geopolitics": "Geopolitics",
    "Graduate Institute Geneva Institutional Repository (Graduate Institute of International and Development Studies)": "Geneva Inst",
    "Journal of International Business Policy": "JIBP",
    "Journal of International Business Studies": "JIBS",
    "Lecture notes in energy": "Energy Book",
    "World Development": "World Dev",
}
