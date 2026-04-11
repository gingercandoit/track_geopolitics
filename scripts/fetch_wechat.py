"""微信公众号地缘政治信息搜索脚本

自动搜索中方 A/C 层微信公众号，补充 T1-T5 议题的中文来源。
API 来源：wechat-article-exporter (https://down.mptext.top)

用法:
    .\.venv\Scripts\python.exe scripts/fetch_wechat.py [选项]

选项:
    --topic 1|2|3|4|5|all   按议题过滤搜索（默认 all）
    --days N                 只保留最近 N 天的文章（默认 30）
    --output DIR             输出目录（默认 data/raw/）
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests

# ─────────────────────────────────────────────────────
# WeChat Article API (self-contained, from ccc_bom)
# ─────────────────────────────────────────────────────

BASE_URL = os.environ.get("WECHAT_ARTICLE_EXPORTER_BASE_URL", "https://down.mptext.top")
AUTH_KEY = "3e0037adcad742ef8560d4d325bcc3d8"
TAG_RE = re.compile(r"<[^>]+>")


def build_session() -> requests.Session:
    """Create a session that ignores broken proxy env vars."""
    session = requests.Session()
    session.trust_env = False
    session.headers.update({
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "track-geopolitics-wechat/1.0",
    })
    return session


def _request_json(path, params, *, session=None, timeout=30):
    owns = session is None
    session = session or build_session()
    try:
        r = session.get(
            f"{BASE_URL}{path}",
            params=params,
            headers={"X-Auth-Key": AUTH_KEY},
            timeout=timeout,
        )
        r.raise_for_status()
        data = r.json()
    finally:
        if owns:
            session.close()
    base_resp = data.get("base_resp", {})
    if base_resp.get("ret") not in (None, 0):
        raise RuntimeError(f"API error: {base_resp.get('err_msg', 'unknown')}")
    return data


def search_accounts(keyword, size=3, *, session=None):
    """搜索公众号，返回 [{fakeid, nickname, alias, ...}]"""
    data = _request_json("/api/public/v1/account", {"keyword": keyword, "size": min(size, 20)}, session=session)
    return data.get("list", [])


def search_articles(fakeid, keyword="", *, begin=0, size=5, session=None):
    """在指定公众号内搜索文章"""
    return _request_json("/api/public/v1/article", {
        "fakeid": fakeid, "keyword": keyword, "begin": begin, "size": min(size, 20)
    }, session=session)


def parse_articles(payload):
    """解析文章搜索结果"""
    results = []
    for item in payload.get("articles", []) or []:
        results.append({
            "title": TAG_RE.sub("", item.get("title", "")).strip(),
            "link": item.get("link", ""),
            "digest": item.get("digest", ""),
            "update_time": item.get("update_time", 0),
        })
    return results


# ─────────────────────────────────────────────────────
# 地缘政治搜索配置
# ─────────────────────────────────────────────────────

# 公众号层级：A=官方政府/党媒, C=智库/市场化媒体
ACCOUNTS = {
    "新华社":      {"tier": "A", "alias": "xinhuashefabu1"},
    "商务部":      {"tier": "A", "search_name": "商务微新闻"},
    "外交部发言人办公室": {"tier": "A", "alias": "xws4_fmprc"},
    "环球时报":    {"tier": "C", "alias": "hqsbwx"},
    "财新":        {"tier": "C"},
    "观察者网":    {"tier": "C", "alias": "guanchacn"},
}

# 搜索计划: (账号名, 关键词, 议题)
SEARCH_PLAN = [
    # T1 制裁与经济管制
    ("新华社", "制裁", "T1"),
    ("新华社", "SWIFT", "T1"),
    ("商务部", "制裁", "T1"),
    ("外交部发言人办公室", "制裁", "T1"),
    ("环球时报", "美元", "T1"),

    # T2 贸易与产业政策
    ("新华社", "关税", "T2"),
    ("商务部", "232", "T2"),
    ("商务部", "反倾销", "T2"),
    ("财新", "贸易战", "T2"),
    ("环球时报", "关税", "T2"),

    # T3 能源安全与资源角力
    ("新华社", "霍尔木兹", "T3"),
    ("新华社", "石油", "T3"),
    ("新华社", "稀土", "T3"),
    ("环球时报", "霍尔木兹", "T3"),
    ("财新", "能源", "T3"),

    # T4 技术竞争与规则制定
    ("新华社", "芯片", "T4"),
    ("新华社", "出口管制", "T4"),
    ("环球时报", "芯片", "T4"),
    ("财新", "半导体", "T4"),
    ("观察者网", "芯片", "T4"),

    # T5 地缘政治信息池
    ("新华社", "伊朗", "T5"),
    ("外交部发言人办公室", "伊朗", "T5"),
    ("环球时报", "伊朗", "T5"),
    ("新华社", "乌克兰", "T5"),
    ("新华社", "北约", "T5"),
]


def main():
    parser = argparse.ArgumentParser(description="微信公众号地缘政治搜索")
    parser.add_argument("--topic", default="all", help="议题过滤 (1-5 或 all)")
    parser.add_argument("--days", type=int, default=30, help="保留最近N天的文章")
    parser.add_argument("--output", default="data/raw", help="输出目录")
    args = parser.parse_args()

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    cutoff = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    topic_filter = f"T{args.topic}" if args.topic != "all" else None

    # 过滤搜索计划
    plan = SEARCH_PLAN
    if topic_filter:
        plan = [(a, k, t) for a, k, t in plan if t == topic_filter]

    session = build_session()
    account_cache = {}
    all_results = []

    for acct_name, keyword, topic in plan:
        print(f"[{topic}] {acct_name} → '{keyword}'", end=" ... ")
        try:
            # 查找账号 fakeid（带缓存）
            search_name = ACCOUNTS.get(acct_name, {}).get("search_name", acct_name)
            if search_name in account_cache:
                fakeid = account_cache[search_name]
            else:
                accounts = search_accounts(search_name, size=3, session=session)
                if not accounts:
                    print("账号未找到")
                    time.sleep(0.5)
                    continue
                fakeid = accounts[0]["fakeid"]
                account_cache[search_name] = fakeid
                time.sleep(0.3)

            # 搜索文章
            payload = search_articles(fakeid, keyword=keyword, size=5, session=session)
            articles = parse_articles(payload)

            recent = []
            for art in articles:
                ts = art.get("update_time", 0)
                if ts > 0:
                    date = time.strftime("%Y-%m-%d", time.localtime(ts))
                    if date >= cutoff:
                        art["date"] = date
                        art["account"] = acct_name
                        art["tier"] = ACCOUNTS.get(acct_name, {}).get("tier", "?")
                        art["topic"] = topic
                        recent.append(art)

            if recent:
                print(f"{len(recent)} 条")
                for art in recent:
                    print(f"    [{art['date']}] {art['title'][:70]}")
            else:
                print(f"{len(articles)} 条（均超出{args.days}天窗口）")

            all_results.extend(recent)
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(0.5)

    session.close()

    # 汇总
    print(f"\n{'='*60}")
    print(f"=== 近{args.days}天文章汇总：{len(all_results)} 条 ===")
    print(f"{'='*60}")

    for art in sorted(all_results, key=lambda x: x["date"], reverse=True):
        tier = art.get("tier", "?")
        print(f"[{art['topic']}|{tier}] {art['date']} | {art['account']} | {art['title'][:60]}")
        if art.get("link"):
            print(f"    {art['link'][:100]}")

    # 保存
    os.makedirs(args.output, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    topic_tag = args.topic if args.topic != "all" else "all"
    out_file = Path(args.output) / f"wechat_{topic_tag}_{ts}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n保存至 {out_file}")

    # 按议题统计
    topics = {}
    for art in all_results:
        t = art["topic"]
        topics[t] = topics.get(t, 0) + 1
    print("\n议题分布:", " | ".join(f"{k}:{v}" for k, v in sorted(topics.items())))


if __name__ == "__main__":
    main()
