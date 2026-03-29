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
SITE_TITLE = "Geopolitical Research Quarterly"
SITE_SUBTITLE = "地缘政治经济学研究简报"
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
        "name_zh": "贸易与产业竞争",
        "name_short": "贸易",
        "name_en": "Trade & Industrial Competition",
        "slug": "topic2-trade-industrial",
        "color": "#1B4965",
        "icon": "scale",
        "compact": False,
    },
    "topic3-supply-resources": {
        "id": 3,
        "name_zh": "供应链与关键资源",
        "name_short": "供应链",
        "name_en": "Supply Chains & Critical Resources",
        "slug": "topic3-supply-resources",
        "color": "#2E7D32",
        "icon": "link",
        "compact": False,
    },
    "topic4-tech-digital": {
        "id": 4,
        "name_zh": "技术竞争与数字治理",
        "name_short": "科技",
        "name_en": "Tech Competition & Digital Governance",
        "slug": "topic4-tech-digital",
        "color": "#5C6BC0",
        "icon": "cpu",
        "compact": False,
    },
    "topic5-geopolitics": {
        "id": 5,
        "name_zh": "地缘政治信息池",
        "name_short": "信息池",
        "name_en": "Geopolitical Intelligence Pool",
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
