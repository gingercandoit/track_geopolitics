---
description: LiteratureSOP - 地缘政治经济学文献搜集与管理标准操作流程
---

# 地缘政治经济学文献 SOP（Prompt 3）

> 项目级 SOP。规范"经典文献建库 + 新文献追踪"的完整工作流。

---

## 一、双库架构

### Library A：经典文献库

- **定位**：该领域已成立的核心文献，理论基础+实证经典
- **建设方式**：一次性建库 → 偶尔补充（发现遗漏经典时）
- **质量线**：field top journal 发表 或 NBER Working Paper 级别
- **规模**：每 topic 5-40 篇，总计 ~75-100 篇（严格地缘政治相关性筛选后的精选规模）
- **相关性标准**：每篇论文必须**直接研究**地缘政治现象（制裁、贸易战、技术竞争、供应链重组、大国博弈等），纯背景经济学理论不收录
- **产出**：`literature/classic/` 下（classic.json + classic.csv + references.bib + views/）

### Library B：新文献追踪库

- **定位**：近12个月内发表的最新论文 + 工作论文
- **时间窗口**：以当前月份为基准，`pub_ym >= (当前年月 - 12个月)`，含当月（共13个月窗口）。例：当前2026-03，则 `pub_ym >= 2025-03` 的论文留在 Library B
- **生命周期**：论文首次进入 Library B → 超过12个月窗口后迁入 Library A 长期保存
- **月度维护**：每月初检查 Library B 中 `pub_ym` 超期的论文，迁移到 Library A
- **更新频率**：月度扫描（随 Prompt 1 信息抓取一起做）
- **质量线**：
  - Top journal 新发表（必收）
  - NBER/CEPR/SSRN 新工作论文（按相关性筛选）
  - 知名领域内作者的最新挂网论文（即使非 top venue）
- **规模**：每月新增 5-20 篇
- **产出**：`literature/new/` 下（new.json + new.csv + references.bib + views/）

### 库间迁移规则

> 核心原则：Library B 是**滑动窗口**，Library A 是**永久存档**。

- **B→A 迁移**（每月执行）：`pub_ym < cutoff` 的论文从 `new.json` 移入 `classic.json`
- **A→B 迁移**（极少见）：仅在建库阶段发现错误归属时执行（如经典库误收了近期论文）
- **迁移后处理**：
  - B→A：保留 `data_zh`/`method_zh` 字段（虽然 Library A 不强制要求）
  - A→B：补充 `data_zh`/`method_zh`（Library B 必填字段）
  - 重建站点 `site/build.py --clean`
  - 更新 `metadata.total_papers` 计数

---

## 二、质量标准

### 期刊白名单

#### Tier 1：General Top 5 + Finance Top（必收，任何相关论文）

| 期刊 | 缩写 |
|------|------|
| American Economic Review | AER |
| Quarterly Journal of Economics | QJE |
| Journal of Political Economy | JPE |
| Econometrica | ECMA |
| Review of Economic Studies | REStud |
| Journal of Finance | JF |
| Journal of Financial Economics | JFE |
| Review of Financial Studies | RFS |

#### Tier 2：Field Top（与 T1-T5 议题相关时必收）

| 期刊 | 缩写 | 覆盖议题 |
|------|------|---------|
| Journal of International Economics | JIE | T1-T3 |
| Review of Economics and Statistics | REStat | 全部 |
| American Economic Journal: Applied | AEJ-App | 全部 |
| American Economic Journal: Economic Policy | AEJ-Pol | T1-T2 |
| American Economic Journal: Macroeconomics | AEJ-Macro | T1-T3 |
| Journal of the European Economic Association | JEEA | T1-T3 |
| Review of International Economics | RIE | T1-T3 |
| Journal of Development Economics | JDE | T3, T5 |
| Journal of Monetary Economics | JME | T1 |
| Journal of Public Economics | JPubE | T2 |
| Economic Journal | EJ | 全部 |
| Journal of Economic Literature | JEL | 全部（综述） |
| Journal of Economic Perspectives | JEP | 全部（综述） |
| Brookings Papers on Economic Activity | BPEA | 全部 |

#### Tier 3：政治学/国际关系 Top（跨学科，选择性收录）

| 期刊 | 缩写 | 覆盖议题 |
|------|------|---------|
| International Organization | IO | T1, T5 |
| American Political Science Review | APSR | T5 |
| Journal of Peace Research | JPR | T1, T5 |
| Journal of Conflict Resolution | JCR | T1, T5 |
| World Politics | WP | T5 |
| International Security | IS | T4, T5 |
| Foreign Affairs | FA | T5（政策论文） |

#### Working Paper 系列（与期刊发表同等重视）

| 系列 | 质量信号 |
|------|---------|
| NBER Working Papers | 最高质量 WP 平台，经济学标准 |
| CEPR Discussion Papers | 欧洲最高质量 WP |
| SSRN（有选择） | 看作者声誉 + 下载量 |
| World Bank Policy Research WP | B层机构背书 |
| IMF Working Papers | B层机构背书 |
| BIS Working Papers | T1 制裁/金融相关 |
| PIIE Working Papers/Policy Briefs | T1-T2 政策导向 |

### 知名作者清单（即使非 top venue 也追踪）

> 以下作者的新工作论文挂网即收，不需要等 top journal 发表。
> 此清单随项目推进持续更新。

#### T1 制裁与经济管制
- Gary Hufbauer (PIIE) — 制裁有效性数据库
- Daniel Drezner (Tufts) — 制裁政治学
- Henry Farrell & Abraham Newman — weaponized interdependence
- Bryan Early (SUNY Albany) — 制裁规避
- Dursun Peksen — 制裁经济后果
- Barry Eichengreen — 货币霸权/储备多元化
- Eswar Prasad — 人民币国际化
- Matteo Maggiore (Stanford) — 美元体系

#### T2 贸易与产业政策
- Pablo Fajgelbaum (Princeton) — 贸易战福利分析
- Mary Amiti (NY Fed) — 关税传导
- Robert Staiger (Dartmouth) — 贸易协定理论
- Kyle Bagwell (Stanford) — WTO 经济学
- Dani Rodrik (Harvard) — 产业政策/全球化三难
- Marc Melitz (Harvard) — 异质企业贸易
- Ralph Ossa (Zurich) — 最优关税
- Pol Antras (Harvard) — 全球价值链理论
- Richard Baldwin (Graduate Institute) — GVC/供应链贸易
- Laura Alfaro (Harvard) & Davin Chor (Dartmouth) — 全球供应链重组/Looming Great Reallocation
- Luosha Du / Chad Bown — 贸易政策+供应链

#### T3 能源安全与资源角力
- Michael Ross — 资源诅咒
- Jim Hamilton — 石油与宏观经济

#### T4 技术竞争与规则制定
- Daron Acemoglu (MIT) — AI/技术/制度
- David Autor (MIT) — 技术与劳动力市场
- Ufuk Akcigit — 创新政策
- Chris Miller — 芯片战争（非典型学术但领域核心）

#### T5 地缘政治经济学（广义）
- Daron Acemoglu & James Robinson — 制度与国家
- Branko Milanovic — 全球不平等
- Thomas Piketty — 资本/不平等
- Jeffrey Frankel — 国际宏观/汇率
- Michael Pettis — 中国经济/贸易失衡

---

## 三、搜索渠道

### 自动化渠道（AI 直接可用）

| 渠道 | 工具 | 用途 | 限制 |
|------|------|------|------|
| **OpenAlex API** | `api.openalex.org/works?search=...` | 主力建库：metadata+abstract+引用 | 免费，无key，polite pool需邮箱 |
| **Semantic Scholar API** | `api.semanticscholar.org/graph/v1/paper/...` | 补充搜索+引用追踪 | 免费但严格限流(429) |
| **NBER WP RSS** | `back.nber.org/rss/new.xml` + 分领域RSS | 最新工作论文（标题+完整摘要） | 见下方分领域代码表 |
| **SSRN** | Exa 搜索 `site:ssrn.com` | 工作论文 | metadata 免费 |
| **RePEc/IDEAS** | Exa 搜索 `site:ideas.repec.org` | 文献数据库 | metadata 免费 |
| **VoxEU/CEPR** | Exa 搜索 `site:cepr.org OR site:voxeu.org` | 政策短文+WP发现 | 免费 |
| **期刊 RSS** | feedparser | 新发表追踪 | 仅标题+摘要，见下方RSS速查表 |

### NBER WP 分领域 RSS 代码

> URL 格式：`https://back.nber.org/rss/new{code}.xml`

| 代码 | 领域 | 对应 Topic |
|------|------|----------|
| `iti` | 国际贸易 | T2 |
| `ifm` | 国际金融与宏观 | T1, T3 |
| `dev` | 发展经济学 | T3, T5 |
| `efg` | 经济波动与增长 | T5 |
| `eee` | 环境与能源 | T3 |
| `io` | 产业组织 | T2, T4 |
| (全部) | 所有新 WP | `new.xml`（每周~28篇） |

### 期刊 RSS 速查表

**Top 5 期刊**：

| 期刊 | RSS / 获取方式 | 注意事项 |
|------|---------------|----------|
| JPE | `journals.uchicago.edu/action/showFeed?type=etoc&feed=rss&jc=jpe` | 含 Ahead of Print |
| QJE | `academic.oup.com/rss/site_5504/3365.xml` | ⚠️ OUP Cloudflare 封 AI IP |
| REStud | `www.restud.com/feed/?post_type=paper` | WordPress RSS，Accepted Papers |
| Econometrica | `onlinelibrary.wiley.com/feed/14680262/most-recent` | Wiley RSS |
| AER | 无可用 RSS，用 OpenAlex Source ID `S23254222` 查询 | AEA 官网可 HTML 抓取 |

**Field-Top 期刊**：

| 期刊 | RSS URL |
|------|--------|
| JIE | `rss.sciencedirect.com/publication/science/00221996` |
| REStat | `direct.mit.edu/rss/site_1000065/1000035.xml` |
| JME | `rss.sciencedirect.com/publication/science/03043932` |
| JDE | `rss.sciencedirect.com/publication/science/03043878` |
| JFE | `rss.sciencedirect.com/publication/science/0304405X` |
| JF | `onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1540-6261` |

### 出版商 RSS URL 拼接模板

> 知道 ISSN 和出版商即可拼出 RSS URL：

| 出版商 | URL 模板 |
|--------|--------|
| Elsevier | `rss.sciencedirect.com/publication/science/{ISSN去横线}` |
| Wiley | `onlinelibrary.wiley.com/feed/{eISSN}/most-recent` |
| UChicago | `journals.uchicago.edu/action/showFeed?type=etoc&feed=rss&jc={code}` |
| MIT Press | `direct.mit.edu/rss/site_{ID}/{feed}.xml` |
| OUP | `academic.oup.com/rss/site_{ID}/{feed}.xml`（⚠️ Cloudflare） |

### 万能 RSS 发现方法

找不到某期刊的 RSS？用 Feedly API 反查：
```
https://cloud.feedly.com/v3/search/feeds?query=期刊名&count=5
```
返回 JSON 含真实 feedId，OUP 旧域名 `oxfordjournals.org` 也能找到。

### 半自动渠道（需用户协助）

| 渠道 | AI 做什么 | 用户做什么 |
|------|---------|-----------|
| **付费全文** | 生成 WebVPN 链接 | 点击链接下载 PDF |
| **Zotero** | 提供导入格式（BibTeX/RIS） | 导入到 Zotero 管理 |
| **PDF 解析** | 读取并提取关键信息 | 将 PDF 放入指定目录 |

### WebVPN 链接格式（待配置）

> **状态**：尚未配置。用户为复旦大学，WebVPN 地址 `https://webvpn.fudan.edu.cn/`，使用 CAS 统一认证。
> 
> **启用方式**：用户首次通过 WebVPN 打开某个付费期刊页面后，将浏览器地址栏的完整 URL 发给 AI，AI 从中推导编码规则，之后即可自动生成 WebVPN 链接。
>
> **在启用前**：阅读清单中的 DOI 链接已足够——用户可通过学校 VPN 客户端或 WebVPN 手动访问。WebVPN 自动链接是锦上添花，不是必需。

---

## 四、搜索关键词矩阵

### Library A 建库搜索（一次性）

#### T1 制裁与经济管制
```
"economic sanctions" effectiveness empirical
sanctions AND (GDP OR trade OR welfare)
"weaponized interdependence" Farrell Newman
"dollar weaponization" OR "dollar hegemony" OR "reserve currency diversification"
SWIFT sanctions financial exclusion
"RMB internationalization" OR "yuan internationalization" OR CIPS
sanctions evasion circumvention
"secondary sanctions" compliance
Hufbauer sanctions "economic sanctions reconsidered"
financial sanctions targeted smart
sanctions AND "regime change" OR "policy change"
```

#### T2 贸易与产业政策
```
"trade war" welfare tariff 2018
tariff passthrough consumer welfare
"Section 301" China tariffs
"industrial policy" subsidies effectiveness
"optimal tariff" theory
WTO dispute settlement reform
CHIPS Act semiconductor industrial policy
"trade agreement" welfare gains
infant industry protection
"beggar thy neighbor" trade policy
"global value chains" fragmentation reshoring
"supply chain resilience" diversification
"production networks" international trade
friendshoring nearshoring economic effects
```

#### T3 能源安全与资源角力
```
"critical minerals" supply chain policy
"resource curse" institutions development
oil price shocks macroeconomic effects
energy transition geopolitics
OPEC market power oil
food security trade policy
```

#### T4 技术竞争与规则制定
```
"export controls" technology semiconductor
"technology decoupling" US China
AI regulation governance economic
"chip war" semiconductor geopolitics
"digital trade" data sovereignty
innovation policy R&D subsidy
technology transfer developing countries
"digital economy" regulation
platform regulation antitrust digital
5G infrastructure geopolitics
```

#### T5 地缘政治经济学
```
"geopolitical risk" economic impact
"geoeconomics" theory framework
"weaponized interdependence" international relations
"economic statecraft" tools
geopolitics trade investment
"great power competition" economic
institutions colonialism development Acemoglu
global inequality Milanovic
international monetary system reform
"economic coercion" statecraft
```

### Library B 追踪搜索（月度）

每月执行：
1. 拉取 NBER WP RSS 最新条目，按 T1-T5 关键词过滤
2. 搜索 Semantic Scholar / SSRN 最近 30 天发表，限定作者清单或关键词
3. 搜索 top journal RSS/网站最近 30 天新发表
4. 合并去重 → 筛选 → 标注 → 输出

---

## 五、文献条目格式

### JSON 数据库结构

```json
{
  "metadata": {
    "library": "classic|new",
    "last_updated": "2026-03-29",
    "total_papers": 0
  },
  "papers": [
    {
      "id": "farrell_newman_2019",
      "title": "Weaponized Interdependence: How Global Economic Networks Shape State Coercion",
      "authors": ["Henry Farrell", "Abraham Newman"],
      "year": 2019,
      "journal": "International Security",
      "journal_tier": "T3",
      "volume": "44",
      "issue": "1",
      "pages": "42-79",
      "doi": "10.1162/isec_a_00351",
      "url": "https://doi.org/10.1162/isec_a_00351",
      "webvpn_url": null,
      "nber_wp": null,
      "ssrn_id": null,
      "abstract": "...",
      "jel_codes": ["F51", "F52"],
      "topics": [1, 5],
      "topic_relevance": {
        "1": "直接相关：全球经济网络作为制裁工具的理论框架",
        "5": "地缘政治经济学核心理论"
      },
      "priority": "core",
      "citations": 850,
      "tags": ["theory", "weaponized-interdependence", "network-effects"],
      "notes_zh": "制裁经济学必读。提出'武器化相互依赖'概念框架，解释如何利用全球网络节点实施经济胁迫。",
      "data_zh": "（Library B 新增字段）数据来源中文描述，如"NBER-CPS就业数据+企业面板"",
      "method_zh": "（Library B 新增字段）方法论中文描述，如"DiD/RDD + LLM文本分析"",
      "added_date": "2026-03-29",
      "read_status": "unread"
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `id` | 唯一标识，格式 `author_year` 或 `author_keyword_year` |
| `journal_tier` | T1/T2/T3（对应期刊白名单分层）或 WP（工作论文） |
| `topics` | 关联的 T1-T5 议题编号 |
| `topic_relevance` | 每个议题的关联说明（中文） |
| `priority` | `core`（必读） / `recommended`（推荐） / `reference`（参考） |
| `tags` | 自由标签，用于交叉检索 |
| `notes_zh` | 中文简评（1-2句），说明为什么收录 |
| `data_zh` | 数据来源中文说明（Library B 专属），描述论文使用的核心数据集 |
| `method_zh` | 方法论中文说明（Library B 专属），描述识别策略或计量方法 |
| `read_status` | `unread` / `reading` / `read` / `noted`（已做笔记） |
| `webvpn_url` | 复旦 WebVPN 代理链接（付费论文用） |

### Markdown 阅读清单格式

```markdown
# T1 制裁与经济管制 — 阅读清单

## 核心必读 (Core)

### Farrell & Newman (2019) — Weaponized Interdependence
- **期刊**：International Security, 44(1), 42-79
- **议题**：T1 制裁, T5 地缘政治
- **摘要**：提出"武器化相互依赖"理论，解释全球网络节点如何成为经济胁迫工具。
- **为什么读**：制裁经济学必读，理论框架论文。
- **DOI**：[10.1162/isec_a_00351](https://doi.org/10.1162/isec_a_00351)
- **WebVPN**：[复旦全文](https://webvpn.fudan.edu.cn/...)

---

## 推荐阅读 (Recommended)

...

## 参考文献 (Reference)

...
```

---

## 六、执行流程

### Phase A：建库（一次性执行）

```
1. 按 T1-T5 × 搜索关键词矩阵，执行 Exa 搜索
   - 每组关键词搜 Semantic Scholar + SSRN + NBER + RePEc
   - 每个 topic 至少搜 8-12 组关键词
   ↓
2. 按知名作者清单，搜索每位作者最高引用论文
   - Semantic Scholar author search
   ↓
3. 合并去重（以 DOI 为 key）
   ↓
4. 质量筛选
   - 必须满足：期刊白名单 OR NBER WP OR 知名作者
   - 优先级排序：citations > 500 → core, > 100 → recommended, else → reference
   ↓
5. 生成 metadata + abstract
   ↓
6. 按 topic 分类，标注 topic_relevance
   ↓
7. 生成 WebVPN 链接（付费论文）
   ↓
8. 输出 JSON + Markdown 阅读清单
   ↓
9. **地缘政治相关性审核**
   - 对每篇论文判断："这篇论文直接研究地缘政治现象吗？"
   - 移除纯背景经济学理论（如一般增长理论、纯资产定价、通用方法论）
   - 移除边界案例（家庭经济学、纯国内政策评估、与地缘政治无关的气候经济学）
   ↓
10. **notes_zh 手写验证**
    - 每篇论文的 notes_zh 必须准确描述其实际内容
    - 禁止用关键词桶匹配自动生成（如把 NAFTA 论文标注为"中美贸易战"）
   ↓
11. Git 提交
```

### Phase B：月度追踪（定期执行）

```
1. 拉取 NBER WP RSS（按分领域代码过滤：iti/ifm/dev/eee）
   ↓
2. 拉取 Field-Top 期刊 RSS（JIE/REStat/JME/JDE 等，见速查表）
   ↓
3. OpenAlex API 搜索作者清单最近 30 天新作
   ↓
4. 按 T1-T5 关键词过滤 + 地缘政治相关性判断
   ↓
5. 滚雪球检查：对高引种子论文做前向引用追踪（谁引了它？）
   ↓
6. 综述探测：搜索 Annual Review of Econ / JEL / JEP 近期相关综述
   ↓
7. 质量筛选（期刊白名单 + 作者清单 + 地缘政治直接相关性）
   ↓
8. 去重（与经典库 + 已有追踪条目对比，以 DOI 为 key）
   ↓
9. 为每篇新论文填写 `data_zh`（数据来源）和 `method_zh`（方法论），基于摘要手写；无摘要者标"待读全文确认"
   ↓
10. **WP 发表状态复查**：用 OpenAlex API 批量检查库中所有 `journal_tier: "WP"` 的论文
    - 是否已被期刊接收/发表？（检查 locations 中是否新增 journal source）
    - 是否有新版本？（SocArXiv → NBER → journal 的升级路径）
    - 无摘要论文（"待读全文确认"）是否现在有摘要可用？
    - 发现更新后：更新 journal/doi/journal_tier 字段，重新生成视图
   ↓
11. 输出 new-papers-YYYY-MM.md + 更新 JSON
    ↓
12. 运行 `scripts/generate_views_new.py` 刷新 Markdown 视图 + CSV
    ↓
13. Git 提交
```

---

## 七、文件结构

> **设计原则**：经典库（Library A）和新文献追踪库（Library B）完全独立，各自有自己的 JSON/CSV/BibTeX/视图。学术文献天然跨议题，因此采用**单一主数据库 + 多视图**架构（而非按 topic 分文件夹）。

```
literature/                             # 与 reports/ 同级
├── classic/                        # Library A: 经典文献（一次性建库）
│   ├── classic.json                # 主数据库（所有论文，单一文件）
│   ├── classic.csv                 # CSV 结构化索引（可在 Excel 中浏览）
│   ├── references.bib              # BibTeX 引用文件（可导入 Zotero）
│   ├── reading-roadmap.md          # 阅读路线图（议题→子主题→优先级）
│   ├── _build_summary.md           # 构建摘要
│   └── views/                      # 自动生成的阅读视图（按需刷新）
│       ├── by-topic-t1.md          # T1 相关论文视图
│       ├── by-topic-t2.md          # T2 相关论文视图
│       ├── by-topic-t3.md          # T3 相关论文视图
│       ├── by-topic-t4.md          # T4 相关论文视图
│       ├── by-topic-t5.md          # T5 相关论文视图
│       ├── by-priority.md          # 按阅读优先级排列
│       └── by-author.md            # 按作者索引
├── new/                            # Library B: 新文献追踪（月度更新）
│   ├── new.json                    # 主数据库（月度新论文）
│   ├── new.csv                     # CSV 索引
│   ├── references.bib              # BibTeX
│   └── views/                      # 视图
│       └── new-papers-YYYY-MM.md   # 按月新论文速览
└── pdf/                            # 用户手动下载的 PDF（.gitignore 排除）
```

**关键点**：
- classic/ 和 new/ 完全独立，各有自己的 JSON/CSV/BibTeX/views
- 每篇论文只在对应库的 JSON 中存一次，通过 `topics` 数组关联多个议题
- `views/` 下的 Markdown 文件是从 JSON 自动生成的**只读视图**，不手动编辑
- 更新 JSON 后运行视图生成脚本即可刷新所有视图
- `pdf/` 目录加入 `.gitignore`（PDF 体积大，不入版本库）

**自动化脚本**：
- `scripts/build_literature.py` — OpenAlex API 建库（Phase A）
- `scripts/build_phase2.py` — 从 JSON 生成 CSV/BibTeX/阅读路线图（Phase 2）
- `scripts/generate_views.py` — 从 JSON 生成 Markdown 视图

---

## 八、与 Prompt 1 的协同

- Prompt 1 发现的重大政策事件 → 触发 Prompt 3 搜索相关学术文献
  - 例：Prompt 1 记录 "OFAC 3/12 新制裁" → Prompt 3 搜索制裁有效性最新研究
- Prompt 3 发现的新论文 → 可为 Prompt 1 的月度总览提供理论注释
- 两者共享 T1-T5 议题框架，确保对齐

---

## 九、质量检查清单

每次文献搜集完成后自检：

- [ ] 每篇论文**直接研究**地缘政治现象（制裁、贸易战、技术竞争、大国博弈等），纯背景经济学理论不收录
- [ ] 每个 topic 至少有 5 篇经典文献（Phase A）
- [ ] 核心必读（core）论文每 topic 不少于 3 篇
- [ ] 每篇论文有 abstract（91%+覆盖率）和 notes_zh
- [ ] **notes_zh 必须准确描述论文实际内容**——禁止用关键词桶匹配生成（如把 NAFTA 论文标注为"中美贸易战"）
- [ ] Library B 每篇必须有 `data_zh` 和 `method_zh`（无摘要者标注"待读全文确认"）
- [ ] DOI 链接有效
- [ ] JSON 数据库无重复条目（以 DOI 去重）
- [ ] 阅读清单按 tier desc → year desc 排列
- [ ] 已 Git 提交

---

## 十、常见陷阱

| 陷阱 | 对策 |
|------|------|
| AI 编造论文（幻觉） | 抽查 5 篇，用 DOI 验证。OpenAlex API 数据最可靠 |
| 搜索词太宽，大量无关论文混入 | 必须人工审核关键词匹配结果，约 20-30% 需删除 |
| notes_zh 用关键词桶匹配生成 | 必须基于每篇论文的实际 title+abstract 撰写，手写或分篇生成 |
| data_zh/method_zh 写得太泛 | 必须写具体数据集名称（如"earnings call transcripts + LLM"），不能写"面板数据"、"回归分析"等通用描述 |
| 只搜到一般经济学，无地缘政治角色 | 判断标准："这篇论文直接研究地缘政治现象吗？"背景理论不收 |
| OpenAlex 日期 ≠ 期刊期号 | OpenAlex 用 online first 日期，查具体某期内容请看期刊官网 |
| OpenAlex 收录延迟 | 刚发表几天的论文可能未被收录，搭配期刊 RSS 补充 |
| OUP Cloudflare 封锁 AI IP | QJE/REStud/RFS 等 OUP 期刊 RSS 对 Agent 封锁，用 OpenAlex 或 Feedly |
| Semantic Scholar 严格限流 (429) | 改用 OpenAlex 为主力，S2 做补充 |
| 同一篇有 WP 版和正式版 | 以 DOI 去重，保留正式发表版，WP 版仅当未正式发表时保留 |
| 找不到某期刊 RSS | 用 Feedly API: `cloud.feedly.com/v3/search/feeds?query=期刊名&count=5` |

---

## 十一、Zotero 集成（可选）

如果用户使用 Zotero：
- 可从 JSON 数据库生成 BibTeX 文件，用户一键导入 Zotero
- BibTeX 输出路径：`literature/classic/references.bib`（经典库）、`literature/new/references.bib`（新文献）
- 生成命令：由 AI 在输出阶段自动附加

---

## 附录：JEL 代码参考

与本项目相关的主要 JEL 分类：

| JEL | 含义 | 对应 Topic |
|-----|------|-----------|
| F10-F19 | 国际贸易 | T2 |
| F20-F29 | 国际要素流动 | T2, T3 |
| F30-F39 | 国际金融 | T1 |
| F40-F49 | 国际宏观 | T1, T3 |
| F50-F59 | 国际关系/国际政治经济学 | T1, T5 |
| F60-F69 | 全球化 | 全部 |
| H56 | 国家安全与战争 | T5 |
| L50-L59 | 产业政策/管制 | T2, T4 |
| O30-O39 | 技术变革 | T4 |
| Q40-Q49 | 能源 | T3 |
