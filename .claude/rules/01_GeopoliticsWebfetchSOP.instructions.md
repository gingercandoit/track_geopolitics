---
description: GeopoliticsWebfetchSOP - 地缘政治信息抓取与简报生成标准操作流程
---

# 地缘政治 Webfetch SOP

> 项目级 SOP。规范"信息侦察 → 筛选 → 简报生成"的完整工作流。

---

## 一、固定事件类型词表

报告中的每条事件必须从以下8个类型中选一个，不可自造类型。

| 类型代码 | 含义 | 典型示例 |
|----------|------|----------|
| **政策发布** | 官方政策公告、法规、行政规则、总统行政令、立法行动 | BIS 出口管制最终规则、Executive Order、国会法案通过 |
| **贸易调查** | 301调查、反倾销、反补贴、贸易壁垒调查 | USTR 301调查、中国商务部贸易壁垒调查 |
| **制裁与管制** | OFAC制裁指定/撤销、实体清单更新、出口管制规则、技术限制 | OFAC 制裁、BIS Entity List、芯片出口许可审查 |
| **外交动态** | 峰会、双边会晤、外交信号、声明 | 特朗普-习近平峰会、外交部发言人回应 |
| **国际机构** | IMF/WTO/IEA/OECD 的行动或报告 | WTO 争端裁决、IEA 月度报告 |
| **智库分析** | 智库、学术机构或媒体深度调查的分析性内容 | CFR 评论、PIIE 政策简报、Reuters 独家获取内部文件 |
| **企业动态** | 企业回应、行业影响、供应链调整 | 企业供应链多元化、行业合规应对 |
| **数据发布** | 统计数据发布、经济指标、量化报告 | 贸易数据、FDI 统计、能源产量 |

**规则**：
- 如果一条事件横跨多个类型，选最核心的那个
- 不确定时优先选「政策发布」（因为本项目以官方信息为主）
- 行政命令（Executive Order）归入「政策发布」；出口管制/实体清单归入「制裁与管制」
- 媒体调查性报道归入「智库分析」（当其内容为分析/揭露性质）或「政策发布」（当其揭露的是具体政策文件）

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

**A层中国政府 RSS / 信息源**（英文版优先，中文版补充）：
```
https://english.news.cn/rss/world.xml                 # 新华社英文版World
https://english.news.cn/rss/china.xml                 # 新华社英文版China  
http://www.news.cn/english/rss/worldrss.xml           # 新华社英文备用
http://english.mofcom.gov.cn/article/newsrelease/rss  # 商务部英文版（如可用）
```
> **中国A层现状**：新华社英文版有RSS且质量高（含全文），外交部/商务部/发改委无可用RSS，需用Exa搜索覆盖。建议搜索关键词：`site:english.news.cn`、`site:english.mofcom.gov.cn`、`site:www.fmprc.gov.cn/eng`。
> 
> **注意**：中方官方来源是SOP要求的A层"必须覆盖"，不可用西方媒体转述替代。至少在每条涉及中方行动/反应的事件中，应有一条中方官方来源（新华社/商务部/外交部）作为直接引用。

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

#### Exa 搜索（主力——适合回溯和历史发现）
- 每个议题至少执行 5-8 组关键词搜索
- 搜索语言以英文为主，中文来源用英文关键词也能覆盖
- **最适合**：回溯抓取（7天/30天/任意日期范围）、查找特定事件的权威来源、覆盖无RSS的A/B层来源（IMF/World Bank/IEA/OECD等）

#### RSS Feed 拉取（补充——适合实时和近期事件）
- **关键限制**：绝大多数RSS只缓存最近 1-3 天内容，不保存完整历史。30天拉取实际只返回近几天的条目。
- **因此 RSS ≠ 替代 Exa**：RSS用于发现最新24-72小时的事件，Exa用于回溯和填补历史空白。两者互补。
- 使用 `scripts/fetch_sources.py` 自动化拉取（详见下方脚本说明）

#### Bloomberg/WSJ RSS（C层实时事件流）
- 用 `feedparser` 解析，按关键词过滤与五大议题相关的条目
- Bloomberg 摘要够长，可直接做事件识别
- WSJ 摘要短，主要用于发现标题中的事件线索，然后用 fetch_webpage 深度抓取

#### Reddit（D层事件发现+重要性信号）
- r/geopolitics：高质量策展，帖子链向 Foreign Policy、Reuters、CEPA 等，投票+评论数 = 重要性权重
- r/worldnews：覆盖广，周热帖（top/week）可快速识别当周最重大事件
- 使用 `url_overridden_by_dest` 字段获取原始文章 URL，然后用 fetch_webpage 抓原文
- **Reddit 帖子本身不作为来源引用**——引用其链接到的原始来源

#### Exa site:x.com（按需）
- 仅用于追踪特定政策人物声明或突发新闻
- 命令：`mcporter call exa web_search_exa "<query> site:x.com"`
- 不作为常规搜索渠道

### fetch_sources.py 脚本使用

```bash
# 激活虚拟环境
.\.venv\Scripts\python.exe scripts/fetch_sources.py [选项]

# 常用命令
--days N          # 时间范围（天数），默认7
--topic 1|2|3|4|5 # 按议题过滤输出（不影响拉取，仅影响输出文件）
--source rss|reddit|all  # 信息源选择，默认all
--output DIR      # 输出目录，默认data/raw/

# 示例
python scripts/fetch_sources.py --days 3 --topic 1    # 近3天，Topic 1
python scripts/fetch_sources.py --days 30              # 近30天，全部议题
python scripts/fetch_sources.py --source rss           # 仅RSS
```

**输出文件**：自动生成 `data/fetch_{topic|all}_{timestamp}.json` 和 `.md`

**注意事项**：
- 脚本内置39个RSS feed + 3个Reddit端点
- 自动处理 State Dept 需要 User-Agent 的情况
- 关键词过滤使用正则表达式匹配五大议题
- 未匹配议题的条目也会保存在"未匹配"部分——可能包含跨议题事件

### RSS Feed 去重说明

部分RSS源内容有重叠：
- `State Dept Press Releases` 是 `State Dept All Releases` 的子集——取 All Releases 即可
- Bloomberg三个频道（Politics/Economics/Technology）有时同一篇文章出现在多个频道
- 去重策略：以URL为key去重，保留最早出现的那条

### 关键词矩阵

> 2026-03-29 重组：从3个议题扩展为5个议题，按经济政策工具/渠道分类。

#### Topic 1：制裁与经济管制 (topic1-sanctions)
```
OFAC + sanctions / designation / SDN list / delisting
EU sanctions + package / Russia / Iran / Belarus
"secondary sanctions" + compliance / enforcement
SWIFT + ban / exclusion / weaponization / alternative
"dollar hegemony" OR "dollar weaponization" OR "reserve currency"
RMB internationalization / CIPS / yuan / renminbi + cross-border
sanctions evasion / circumvention / enforcement
"anti-sanctions law" / counter-sanctions / retaliatory measures
asset freeze + central bank / sovereign wealth fund
Russia sanctions + oil price cap / energy / circumvention
Iran sanctions + oil / nuclear / JCPOA
North Korea + sanctions / enforcement / evasion
"financial sanctions" + SWIFT / correspondent banking / de-risking
```
**中方视角补充搜索**（Exa）：
```
site:english.news.cn + sanctions / countermeasure / anti-sanctions
"China Ministry of Commerce" + unreliable entity list / export control
"Xinhua" + SWIFT / yuan / RMB internationalization
```

#### Topic 2：贸易与产业竞争 (topic2-trade-industrial)
```
tariff + trade war / retaliation / Section 301
anti-dumping / countervailing duty / trade investigation
USTR + trade policy / agenda / investigation
industrial policy + CHIPS Act / IRA / subsidies / overcapacity
WTO dispute + settlement / ruling / reform / Appellate Body
trade agreement + RCEP / CPTPP / bilateral / FTA
carbon border adjustment / CBAM / EU + trade / climate
"trade barrier" + investigation / countermeasure
Section 301 / anti-dumping / countervailing duty
```
**中方视角补充搜索**（Exa）：
```
site:english.news.cn + trade / tariff / industrial policy
site:english.mofcom.gov.cn + trade barrier / investigation / countermeasure
"China Ministry of Commerce" + investigation / response / retaliation
```

#### Topic 3：供应链与关键资源 (topic3-supply-resources)
```
supply chain + reshoring / friendshoring / nearshoring / resilience
critical minerals + lithium / cobalt / rare earth / policy / supply
OPEC + production / cut / quota / oil price
IEA + oil / LNG / energy outlook / critical minerals
energy security + Europe / Asia / pipeline / LNG
natural gas / LNG + price / supply / geopolitics / terminal
nuclear energy + uranium / enrichment / geopolitics / SMR
renewable energy + trade / tariffs / subsidy / solar / wind
food security + grain / wheat / rice / export ban / supply
agricultural trade + geopolitics / sanctions / fertilizer
resource nationalism + export restriction / mineral / processing
"global value chains" + disruption / restructuring / diversification
```

#### Topic 4：技术竞争与数字治理 (topic4-tech-digital)
```
BIS entity list / export controls + semiconductor / chip / AI
technology restriction + China / Huawei / SMIC / NVIDIA
semiconductor + export / restriction / licensing / advanced chip
AI regulation / governance + US / EU / China
"technology decoupling" OR "tech war" OR "chip war"
data sovereignty / cross-border data / digital governance
5G / submarine cable / digital infrastructure + geopolitics
technology standards + competition / interoperability / ISO
quantum computing / biotech + national security / restriction
```
**中方视角补充搜索**（Exa）：
```
site:english.news.cn + technology / chip / semiconductor / AI
"Xinhua" + export control / technology restriction / chip
```

#### Topic 5：地缘政治信息池 (topic5-geopolitics)

> **定位**：T5 是不设门槛的信息漏斗入口（catch-all inbox）。所有 A-D 层的地缘政治/外交/安全事件，只要不明确属于 T1-T4 的某一个议题，都收入 T5。用户浏览 T5 时发现感兴趣的条目，可以讨论后升级（promote）到 T1-T4 对应议题。

**关键词**：T5 不使用关键词过滤。采集流程中所有未被 T1-T4 关键词匹配的地缘政治相关条目，自动归入 T5。此外，以下关键词主动搜索以确保覆盖：
```
summit / state visit / bilateral / multilateral / G7 / G20 / BRICS
diplomatic / alliance / partnership / geopolitical
military / defense / security / conflict / ceasefire
UN / NATO / AUKUS / Quad / SCO / ASEAN
sanctions (未被T1捕获的边缘案例)
trade (未被T2捕获的边缘案例)
Global South / non-aligned / developing countries
election + foreign policy / regime change / political transition
refugee / migration / humanitarian + geopolitics
Arctic / space / cyber + geopolitics / sovereignty
```
**中方视角补充搜索**（Exa）：
```
site:english.news.cn + diplomacy / visit / bilateral / security
site:www.fmprc.gov.cn/eng + spokesperson / press conference
```

> **T5 收录原则**：宁多勿漏。T1-T4 执行严格筛选，T5 执行宽松收录。低持久性条目排除规则（第四节）对 T5 **不适用**——口头警告、例行访问、安理会投票姿态等在 T1-T4 中被排除的事件，T5 照收。唯一排除标准：与地缘政治完全无关的内容（娱乐、体育、纯国内社会新闻）。
>
> **排列优先级**：T5 月度总览和条目排列中，最重要的外交/地缘事件（如峰会、联盟变化、军事冲突转折点）放在最前面，低持久性事件排在后面。信息池虽不设门槛，但不等于不分轻重。
>
> **升级机制**：用户在浏览 T5 时发现有价值的条目，可指示 AI 将其「升级」到 T1-T4。升级时：(1) 按目标议题的严格标准重新撰写条目，(2) 从 T5 报告中标注「已升级至 TX」但保留原条目，(3) 更新目标议题的报告和 JSON。

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

### ❌ 排除——低持久性条目（重要原则）

以下类型的事件**即使来自 A/B 层来源也不收录**，因为它们缺乏对该板块的长久、实质性影响：

| 类型 | 示例 | 为什么排除 |
|------|------|-----------|
| **外交威慑/口头警告** | "北京警告将采取反制"、IRGC宣布"后果严重" | 口头姿态，无实际动作跟进 |
| **召见/抗议照会** | 召见大使、外交部发言人抗议、领馆预警争议 | 例行外交摩擦，不改变格局 |
| **安理会投票姿态** | 弃权票、谴责声明 | 外交信号，无执行力 |
| **例行代表团访问** | 国会议员访台、部长级例行会见 | 常规操作，非政策突破 |
| **当日战况/油价波动** | "今日布伦特涨/跌$X"、"轰炸了某处" | 24-48小时内失去信息价值 |
| **纯经济数据** | GDP/工业利润/PMI（除非直接触发政策变化） | 宏观数据≠地缘政治事件 |
| **推测性分析** | "是否会导致..."、"可能增加...风险" | 无实质动作，无可验证结论 |
| **国内政治作秀** | "总统向选民推销贸易胜利" | 国内PR，非政策实质 |

**判断标准**：问自己——"这件事在 30 天后还重要吗？它改变了什么结构性的东西？"如果答案是否，不收录。

**例外**：如果以上类型的事件**首次**标志某种结构性转变（如：首次制裁、首次封锁、首次军事行动），仍然收录——因为"第一次"具有标杆意义。后续的重复/延续则不再记录。

**T5 豁免**：以上低持久性排除规则仅适用于 T1-T4。T5（地缘政治信息池）作为 catch-all inbox，不受此规则约束——所有地缘政治相关事件均可收入 T5，无论持久性高低。

---

## 五、报告格式规范

### 文件命名

- Markdown：`reports/topicN-<slug>/YYYY-MM.md`（如 `reports/topic1-sanctions/2026-03.md`）
- JSON：`data/topicN-<slug>/YYYY-MM.json`（如 `data/topic1-sanctions/2026-03.json`）
- 原始拉取：`data/raw/YYYY-MM/fetch_{topic|all}_{timestamp}.{json,md}`
- slug 用英文 kebab-case
- 新增议题时：先在 `reports/` 和 `data/` 下建同名目录

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
   - 类型从固定词表8选1
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
    "topic": "topic1-sanctions",
    "topic_name_zh": "制裁与经济管制",
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

**type 字段**必须使用固定词表中的8个类型之一。

---

## 七、执行流程（Step by Step）

```
1. 确定议题和时间窗口
   ↓
2. 拉取 RSS/Reddit 信息流（事件发现层）
   - 运行 fetch_sources.py --days N [--topic T]
   - 检查输出 Markdown 摘要：按议题和来源层级浏览
   - 高票 Reddit 帖子标记为深度抓取候选
   ↓
3. 按关键词矩阵执行 Exa 搜索（5-8 组）
   - RSS 已发现的事件可跳过重复搜索
   - 重点搜索 RSS 覆盖不到的源（IMF/World Bank/IEA/OECD/智库）
   - 回溯抓取时 Exa 是主力（RSS 只有近 1-3 天）
   ↓
4. 合并 RSS/Reddit/Exa 结果 → 去重（以URL为key）→ 按来源层级排序（A > B > C > D）
   ↓
5. 对 A 层来源和独家报道执行 fetch_webpage 深度抓取（3-5 篇）
   - Reddit 高票帖的原始文章 URL 也纳入深度抓取候选
   - Bloomberg RSS 摘要已够长，通常不需要深度抓取
   ↓
6. 筛选：应用纳入/排除标准
   - 注意关键词匹配可能有误匹配（如 SCMP 社会新闻因含"China"被匹配到多个议题）
   - 人工审核匹配结果，剔除无地缘政治意义的条目
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

**工作流模式选择**：
- **新月度报告**：Step 2（RSS近期）+ Step 3（Exa回溯全月）→ 合并 → 报告
- **补充更新**：Step 2（RSS最新事件）→ 与现有报告对比 → 仅添加缺失事件

---

## 八、质量检查清单

每份报告完成后自检：

- [ ] 所有事件类型均来自固定词表8选1
- [ ] 每条事件有日期、类型、概括三要素标题
- [ ] 每条事件有 bullet 核心点（3-8条）
- [ ] 每条事件有来源标注
- [ ] A 层来源至少占总事件的 30%（注：RSS补充后C层比例自然上升，但A层绝对数量不应减少）
- [ ] 月度总览是自然语言叙述，不是条目罗列
- [ ] 有「背景参考」部分收录前置事件
- [ ] 有「关键数字一览」表格
- [ ] JSON 的 type 字段与 Markdown 一致
- [ ] 文件命名符合 `reports/topicN-<slug>/YYYY-MM.md` 和 `data/topicN-<slug>/YYYY-MM.json` 格式
- [ ] 已运行 `fetch_sources.py` 并检查相关条目
- [ ] 已人工审核关键词匹配结果，剔除误匹配（SCMP社会新闻、体育等）
- [ ] Reddit/X 帖子不作为来源引用，仅用于事件发现（引用其链接到的原始来源）
- [ ] RSS 重复条目已去重（特别是 State Dept 两个 feed、Bloomberg 三个频道）
- [ ] **中方官方来源检查**：涉及中方行动/反应的事件，至少有一条中方A层来源（新华社英文版/商务部/外交部）直接引用，不可仅依赖西方媒体转述
- [ ] **叙事视角平衡**：月度总览中同时呈现"美方行动逻辑"和"中方行动逻辑"，避免单一主体叙事
- [ ] **T5 信息池检查**：T5 条目数量应显著多于 T1-T4（宁多勿漏）；确认无地缘政治相关事件被遗漏；已标注升级条目（如有）
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

---

## 附录：实践经验记录

> 基于2026年3月报告实际执行过程中积累的经验教训。

### A. RSS 局限性

| 问题 | 描述 | 应对 |
|------|------|------|
| 时间窗口短 | 绝大多数RSS仅缓存1-3天，`--days 30`实际只返回近期内容 | 历史回溯必须用Exa，RSS仅用于补充最新事件 |
| B层几乎无RSS | IMF/World Bank/IEA/OECD均无有效RSS，RSSHub公共实例全部403 | 必须用Exa搜索 |
| 智库全部403 | PIIE/Brookings/CFR/CSIS/Chatham House的RSS全部被防火墙封锁 | 用Exa或fetch_webpage |
| State Dept需UA | 不加User-Agent返回0条 | 脚本已自动处理 |

### B. 关键词匹配精度

- 议题1(制裁)和议题2(贸易)因含"sanctions"/"tariff"/"trade"等高频词，可能有误匹配
- 议题3(供应链)因含"oil"/"energy"/"nuclear"/"mineral"等词，匹配量可能远超其他议题
- 议题4(技术)和议题1(制裁)可能有重叠——出口管制同时涉及制裁工具和技术限制，以主要动机判断归属
- **建议**：拉取后必须人工审核匹配结果，20-30%的匹配条目可能无地缘政治价值

### C. 最佳实践

1. **先RSS再Exa**：RSS发现近期事件 → Exa补充历史和B层来源 → 合并去重
2. **Reddit价值**：r/geopolitics高票帖（>50↑）几乎都是重大事件，且链接原始来源（Reuters/Bloomberg/FP等），是优秀的事件发现引擎
3. **补充更新流程**：运行`fetch_sources.py` → 与现有报告对比 → 仅添加现有报告未覆盖的重大事件 → 更新月度总览和关键数字
4. **去重策略**：State Dept两个feed有大量重复，Bloomberg三频道偶有重复，以URL为key统一去重

