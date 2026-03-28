---
description: GeopoliticsWebfetchSOP - 地缘政治信息抓取与简报生成标准操作流程
---

# 地缘政治 Webfetch SOP

> 项目级 SOP。规范"信息侦察 → 筛选 → 简报生成"的完整工作流。

---

## 一、固定事件类型词表

报告中的每条事件必须从以下12个类型中选一个，不可自造类型。

| 类型代码 | 含义 | 典型示例 |
|----------|------|----------|
| **政策发布** | 官方政策公告、法规、行政规则 | BIS 出口管制最终规则、USTR 贸易政策议程 |
| **行政命令** | 总统行政令、公告、签署命令 | Proclamation 11002、Executive Order |
| **贸易调查** | 301调查、反倾销、反补贴、贸易壁垒调查 | USTR 301调查、中国商务部贸易壁垒调查 |
| **制裁行动** | OFAC制裁指定/撤销、资产冻结 | OFAC 反恐制裁、实体清单新增 |
| **出口管制** | 出口管制规则、实体清单更新、技术限制 | BIS Entity List、芯片出口许可审查 |
| **外交动态** | 峰会、双边会晤、外交信号、声明 | 特朗普-习近平峰会、外交部发言人回应 |
| **立法动态** | 立法行动、法案、听证会 | 国会听证、法案提交 |
| **国际机构** | IMF/WTO/IEA/OECD 的行动或报告 | WTO 争端裁决、IEA 月度报告 |
| **智库分析** | 智库或学术机构的深度分析 | CFR 评论、PIIE 政策简报 |
| **媒体深度** | 媒体独家报道、调查性报道 | Reuters 独家获取内部文件 |
| **企业动态** | 企业回应、行业影响、供应链调整 | 企业供应链多元化、行业合规应对 |
| **数据发布** | 统计数据发布、经济指标、量化报告 | 贸易数据、FDI 统计、能源产量 |

**规则**：
- 如果一条事件横跨多个类型，选最核心的那个
- 不确定时优先选「政策发布」（因为本项目以官方信息为主）
- 「智库分析」和「媒体深度」的区别：前者有明确机构署名和研究框架，后者是新闻调查

---

## 二、信息来源层级

### A层：官方政府/监管机构（最高权威，必须覆盖）

| 国家/地区 | 来源 |
|-----------|------|
| 美国 | 白宫 whitehouse.gov、USTR、商务部 BIS、财政部 OFAC、国务院 |
| 中国 | 外交部、商务部、国家发改委、新华社官方英文版 |
| 欧盟 | European Commission、欧洲理事会 |
| 其他 | G7 轮值主席国、东盟秘书处（如有重大声明） |

### B层：国际机构（权威数据与框架，必须覆盖）

IMF（含 Article IV、WEO 更新）、World Bank、WTO（含争端解决 DSB 动态，有官方 RSS）、BIS（Bank for International Settlements）、IEA（能源地缘必查）、OECD

> **B层 RSS 现状**：仅 WTO（`http://www.wto.org/library/rss/latest_news_e.xml`）和 UN News（`https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml`）有可用 RSS。IMF/World Bank/IEA/OECD 均无 RSS 且封锁 RSSHub，必须用 Exa 搜索。

### C层：智库与话语权媒体（分析视角，重点覆盖）

- **媒体**：Financial Times、The Economist、Reuters、Bloomberg（地缘政治专栏）、CNBC、BBC、NPR、Wall Street Journal
- **智库**：PIIE、Brookings、CFR、CSIS、Chatham House、RAND、East Asia Forum、Carnegie
- **学术快评**：VoxEU、NBER Working Papers（如有相关新文）

### D层：社区策展与社交媒体（事件发现与重要性信号）

- **Reddit**：r/geopolitics（高质量策展，链向 Foreign Policy、Reuters、CEPA 等，投票数提供重要性权重）、r/worldnews（覆盖广，热帖=重大事件信号）、r/economics
- **X/Twitter**：通过 Exa `site:x.com` 搜索访问，仅用于突发新闻发现和政策人物声明追踪
- **角色说明**：D层不作为事实来源引用，而是作为**事件发现线索**——在 D 层发现线索后，回溯到 A/B/C 层来源获取权威信息

---

## 三、信息采集渠道与搜索策略

### 渠道一览

| 渠道 | 工具/方法 | 覆盖源 | 角色 | 依赖 |
|------|-----------|--------|------|------|
| **Exa 搜索** | `mcporter call exa web_search_exa "<query>"` | 全网 A/B/C 层 | 主力发现 | mcporter + Exa MCP |
| **fetch_webpage** | VS Code Copilot 内置 | 指定 URL | 深度抓取 | 无 |
| **Bloomberg RSS** | `feedparser.parse(url)` | Bloomberg Politics/Economics/Markets | 实时事件流 | feedparser |
| **WSJ RSS** | `feedparser.parse(url)` | WSJ World News/Business/Markets/Opinion | 事件补充 | feedparser |
| **Reddit JSON** | `requests.get(url, headers=...)` | r/geopolitics, r/worldnews, r/economics | 事件发现+重要性信号 | requests |
| **Exa site:x.com** | `mcporter call exa web_search_exa "<query> site:x.com"` | X/Twitter | 突发新闻（按需） | mcporter + Exa MCP |

### RSS Feed URLs（已验证可用）

**Bloomberg**（每频道约30条，含标题+2-3句摘要）：
```
https://feeds.bloomberg.com/politics/news.rss
https://feeds.bloomberg.com/economics/news.rss
https://feeds.bloomberg.com/markets/news.rss
```

**WSJ**（World News 约75条，摘要较短1-2句）：
```
https://feeds.content.dowjones.io/public/rss/RSSWorldNews
https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness
https://feeds.content.dowjones.io/public/rss/RSSMarketsMain
https://feeds.content.dowjones.io/public/rss/RSSOpinion
```

**Reddit JSON API**（无需认证，需自定义 User-Agent，≤10请求/分钟）：
```
https://www.reddit.com/r/geopolitics/hot.json?limit=25
https://www.reddit.com/r/worldnews/top.json?t=week&limit=25
https://www.reddit.com/r/economics/hot.json?limit=10
```

**B层国际机构 RSS**（仅此二者有效，其余需 Exa）：
```
http://www.wto.org/library/rss/latest_news_e.xml
https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml
```

**A层美国政府 RSS**（需 User-Agent 的标注 UA）：
```
https://www.whitehouse.gov/news/feed/
https://www.whitehouse.gov/presidential-actions/feed/
https://www.state.gov/rss-feed/press-releases/feed/          # 需UA
https://www.state.gov/rss-feed/collected-department-releases/feed/  # 需UA
https://www.federalreserve.gov/feeds/press_all.xml
https://www.eia.gov/rss/press_rss.xml
```

**补充 C 层 RSS**（高价值，上面未列的）：
```
https://feeds.npr.org/1004/rss.xml                  # NPR World（全文）
https://foreignpolicy.com/feed/                       # Foreign Policy（全文）
https://www.foreignaffairs.com/rss.xml               # Foreign Affairs（摘要）
https://www.scmp.com/rss/91/feed                     # SCMP（亚洲/中国）
https://thediplomat.com/feed/                         # The Diplomat（亚太）
https://warontherocks.com/feed/                       # War on the Rocks（安全）
https://www.economist.com/international/rss.xml       # Economist（300条）
http://feeds.bbci.co.uk/news/world/rss.xml           # BBC World
https://www.theguardian.com/world/rss                 # Guardian World
https://www.ft.com/world?format=rss                   # FT World
```

### 各渠道使用方式

#### Exa 搜索（主力）
- 每个议题至少执行 5-8 组关键词搜索
- 搜索语言以英文为主，中文来源用英文关键词也能覆盖

#### Bloomberg/WSJ RSS（补充事件流）
- 用 `feedparser` 解析，按关键词过滤与三大议题相关的条目
- Bloomberg 摘要够长，可直接做事件识别
- WSJ 摘要短，主要用于发现标题中的事件线索，然后用 fetch_webpage 深度抓取
- RSS 只返回最近内容（通常 1-3 天），不用于回溯抓取

#### Reddit（事件发现+重要性信号）
- r/geopolitics：高质量策展，帖子链向 Foreign Policy、Reuters、CEPA 等，投票+评论数 = 重要性权重
- r/worldnews：覆盖广，周热帖（top/week）可快速识别当周最重大事件
- 使用 `url_overridden_by_dest` 字段获取原始文章 URL，然后用 fetch_webpage 抓原文
- **Reddit 帖子本身不作为来源引用**——引用其链接到的原始来源

#### Exa site:x.com（按需）
- 仅用于追踪特定政策人物声明或突发新闻
- 命令：`mcporter call exa web_search_exa "<query> site:x.com"`
- 不作为常规搜索渠道

### 关键词矩阵

#### 议题1：中美关系/大国博弈
```
"US China" + tariffs / sanctions / export controls / technology
"decoupling" OR "de-risking"
OFAC designation / BIS entity list
Trump + China + trade / visit / summit
whitehouse.gov / USTR + China + trade policy
China Ministry of Commerce + response / tariffs / investigation
semiconductor / chip + export / restriction / AI
```

#### 议题2：供应链/贸易政策
```
supply chain + reshoring / friendshoring / nearshoring
critical minerals + policy / restriction / supply
WTO dispute + settlement / ruling
trade policy + semiconductor / EV / steel / pharma / battery
CHIPS Act / IRA + implementation / investment
industrial policy + subsidies / overcapacity
Section 301 / anti-dumping / countervailing duty
```

#### 议题3：能源/资源地缘
```
IEA + oil / LNG / critical minerals / energy outlook
energy security + Europe / Asia / sanctions / Russia
lithium / cobalt / rare earth + policy / export ban / supply
OPEC + production / cut / quota
natural gas / LNG + price / supply / geopolitics
renewable energy + trade / tariffs / subsidy
nuclear energy + uranium / enrichment / geopolitics
```

### 搜索节奏

- 每组关键词独立执行一次 Exa 搜索
- 如结果不足（< 3 条高质量），变换关键词再搜一轮
- 搜索结果去重后，按来源层级排序（A > B > C）

---

## 四、筛选标准

### ✅ 纳入

- 来自 A/B 层来源的**任何**官方声明或政策文件
- C 层来源中具有明确政策含义的深度分析
- 包含可量化指标（关税率、制裁名单数量、投资限额等）
- 涉及多国博弈的多边事件
- 独家报道或首发消息

### ❌ 排除

- 纯市场行情报道（无政策背景）
- 重复事件的不同媒体转载（保留最权威来源即可）
- 超出时间窗口的旧闻（除非作为「背景参考」收录）
- 评论员个人专栏（非机构背书）
- 社交媒体未经证实的信息

---

## 五、报告格式规范

### 文件命名

- Markdown：`reports/YYYY-MM-topicN-<slug>.md`
- JSON：`data/YYYY-MM-topicN-<slug>.json`
- slug 用英文 kebab-case

### 报告结构

```markdown
# 地缘政治月度简报：议题 N — {议题名称}

**报告期间**：YYYY年M月D日至M月D日
**生成日期**：YYYY年M月D日
**来源覆盖**：{列出主要来源}

---

## 月度总览

{2-4段自然语言叙述，概括本月的主线和关键转折。这部分要有分析深度，不是简单罗列。}

---

## 第N周：M月D日至D日

### M月D日 | {类型} | {一句话概括}

- {核心点1}
- {核心点2}
- {核心点N}

**来源**：[来源名](URL); [来源名](URL)

---

## 背景参考

{按同样的条目格式收录时间窗口前的关键事件}

---

## 关键数字一览

| 指标 | 数值 |
|------|------|
| ... | ... |
```

### 条目格式规则

1. **标题行**：`### M月D日 | {类型} | {概括}`
   - 日期用中文格式（M月D日）
   - 类型从固定词表12选1
   - 概括不超过30字
   - 如事件跨多天，用 `M月D日–D日`

2. **核心点**：
   - 用无序列表（`-`）
   - 每条一个独立信息点
   - 事实在前，分析/意义在后
   - 有数字的优先列（量化信息 > 定性描述）
   - 3-8 条为宜，不超过 10 条

3. **来源**：
   - 格式：`**来源**：[显示名](URL); [显示名](URL)`
   - 无 URL 的来源直接写名称
   - A 层来源列在最前

4. **月度总览**：
   - 保留自然语言叙述体
   - 提炼 2-4 条主线
   - 每条主线用 `**粗体开头句。**` 引导
   - 有分析深度，不是事件罗列

---

## 六、JSON 数据规范

```json
{
  "report_metadata": {
    "topic": "topic1-us-china",
    "topic_name_zh": "中美关系与大国博弈",
    "period_start": "2026-03-01",
    "period_end": "2026-03-28",
    "generated_at": "2026-03-28T22:00:00+08:00",
    "version": "1.0"
  },
  "events": [
    {
      "date": "2026-03-11",
      "type": "贸易调查",
      "title_zh": "USTR 发起第一轮 301 调查",
      "summary_zh": "...",
      "source_tier": "A",
      "sources": [
        {"name": "USTR", "url": "https://..."},
        {"name": "Pillsbury", "url": "https://..."}
      ],
      "metrics": {"economies_investigated": 16},
      "week": 2
    }
  ],
  "analysis_articles": [...],
  "background_context": [...],
  "key_metrics": {...}
}
```

**type 字段**必须使用固定词表中的12个类型之一。

---

## 七、执行流程（Step by Step）

```
1. 确定议题和时间窗口
   ↓
2. 拉取 RSS/Reddit 信息流（事件发现层）
   - Bloomberg RSS（politics + economics）→ 关键词过滤
   - WSJ RSS（world news）→ 关键词过滤
   - Reddit r/geopolitics hot + r/worldnews top/week → 筛选高票帖
   ↓
3. 按关键词矩阵执行 Exa 搜索（5-8 组）
   ↓
4. 合并 RSS/Reddit/Exa 结果 → 去重 → 按来源层级排序（A > B > C > D）
   ↓
5. 对 A 层来源和独家报道执行 fetch_webpage 深度抓取（3-5 篇）
   - Reddit 高票帖的原始文章 URL 也纳入深度抓取候选
   ↓
6. 筛选：应用纳入/排除标准
   ↓
7. 分类：给每条事件指定「类型」（从固定词表选）
   ↓
8. 排列：按周→日时间线排列
   ↓
9. 撰写月度总览（自然语言，提炼主线）
   ↓
10. 生成 Markdown 报告 + JSON 数据
    ↓
11. Git 提交
```

> **脚本辅助**：Step 2 可使用 `scripts/fetch_sources.py` 自动化拉取和关键词过滤（如已创建）。

---

## 八、质量检查清单

每份报告完成后自检：

- [ ] 所有事件类型均来自固定词表12选1
- [ ] 每条事件有日期、类型、概括三要素标题
- [ ] 每条事件有 bullet 核心点（3-8条）
- [ ] 每条事件有来源标注
- [ ] A 层来源至少占总事件的 40%
- [ ] 月度总览是自然语言叙述，不是条目罗列
- [ ] 有「背景参考」部分收录前置事件
- [ ] 有「关键数字一览」表格
- [ ] JSON 的 type 字段与 Markdown 一致
- [ ] 文件命名符合 `YYYY-MM-topicN-<slug>` 格式
- [ ] 已拉取 Bloomberg/WSJ RSS 并检查相关条目（如可用）
- [ ] 已检查 Reddit r/geopolitics 高票帖（如可用）
- [ ] Reddit/X 帖子不作为来源引用，仅用于事件发现
- [ ] 已 Git 提交

---

## 九、写作风格

- **月度总览**：自然语言叙述，有分析深度，读者是经济学研究者
- **条目核心点**：bullet 式，简洁精准，每条一个信息点
- **禁止**：符号速记（✅❌📌等 emoji 不用于正文）、电报式缩写、无主语句子
- **数字**：阿拉伯数字 + 单位，如「25%」「16个经济体」「50%算力上限」
- **人名**：首次出现全名+职位，后续可用姓氏
- **来源引用**：以事实归因为主（"Reuters 报道"、"新华社称"），不用"据报道"等模糊表述

---

## 十、更新与维护

- 月度报告在当月内可追加（新事件追加到对应周）
- 跨月不修改旧报告，出新月报
- Prompt 模板更新时同步更新本 SOP
- 类型词表如需扩展，先在本文件讨论后再新增

