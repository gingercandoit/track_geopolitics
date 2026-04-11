---
description: MasterWorkflowSOP - T1-T5资讯更新主控流程（采集→撰写→上线）
---

# 资讯更新主控 SOP

> 项目级主控流程。定义"从用户下达更新指令到网站上线新内容"的完整步骤、人机分工和检查点。
> 本文件只管 T1-T5 资讯更新，不涉及文献库。

---

## 一、角色定位

本 SOP 是**总调度**——告诉 AI "走哪条路、在哪里停下来问人"。每一步的具体操作细节由子 SOP 承载：

| 步骤 | 引用 | 文件 |
|------|------|------|
| 信息采集 | 02_GeopoliticsWebfetchSOP §二-三 | 来源层级、搜索渠道、关键词矩阵 |
| 筛选标准 | 02_GeopoliticsWebfetchSOP §四 | 纳入/排除、低持久性排除规则 |
| 报告格式 | 02_GeopoliticsWebfetchSOP §五-六 | Markdown 格式 + JSON 数据规范 |
| 写作风格 | 05_WritingStyle | 禁用词、新闻体准则、bullet 格式 |
| 网站构建 | 04_FrontendSOP §六-七 | build.py 使用、月份维护 |

**规则**：本 SOP 不重复子 SOP 的内容，只注明"在这一步参照哪个 SOP 的哪一节"。

---

## 二、触发场景

用户下达更新指令时，AI 先识别属于哪种场景，走对应的流程：

| 场景 | 用户可能说的话 | AI 做什么 |
|------|---------------|-----------|
| **A. 新月份初始化** | "4月了"、"新月份上线"、"创建4月页面" | 创建空框架 → 采集 → 撰写 → 构建 |
| **B. 增量更新** | "3/20到4/1没搜"、"补一下T1最近的"、"搜一下T3能源最近7天" | 在现有月份 JSON 上追加事件 → 更新总览 → 重建 |
| **C. 月度收尾** | "3月的报告收尾"、"3月定稿" | 质量检查 → 补漏 → 冻结 → 重建 |

> 单议题搜索（如"搜一下T3"）归入场景 B。增量更新天然支持"全部议题"和"指定议题"两种粒度，在 Step 1 确认范围时区分。

识别不了场景时，用 AskQuestions 问用户。

### 跨月事件归属规则

事件日期在哪个自然月，就归入哪个月的 JSON 文件。

- 3月31日的事件 → `data/topicN/2026-03.json`
- 4月1日的事件 → `data/topicN/2026-04.json`
- 采集时间窗口跨月（如 3/25-4/5）时，AI 自动拆分到对应月份的文件
- 如果目标月份的 JSON 尚不存在，先走场景 A Step 2 创建框架

---

## 三、场景 A：新月份初始化

> 适用于月初，从零创建新月份页面。

### Step 1｜确认范围 `🧑 → 🤖`

AI 用 AskQuestions 确认：
- 时间窗口：月初至今？还是自指定日期起？
- 议题范围：全部 T1-T5，还是只做部分？
- 上月是否有未收尾的缺口需要一并补？

### Step 2｜创建月份框架 `🤖`

为每个议题创建空数据文件和报告文件：

```
data/topicN-slug/YYYY-MM.json    （空事件数组 + metadata）
reports/topicN-slug/YYYY-MM.md   （标题 + 空月度总览）
```

运行一次 `site/build.py --clean`，确认网站月份选择器出现新月份。

> **检查点**：告知用户"框架已建好，月份可切换，开始采集？"

### Step 3｜信息采集 `🤖`

按 02_GeopoliticsWebfetchSOP §三 执行，节奏如下：

1. **RSS/Reddit 拉取**：`python scripts/fetch_sources.py --days N`
2. **微信公众号搜索**：`python scripts/fetch_wechat.py --days N`（中方A/C层信源，含新华社/商务部/外交部等6个账号）
3. **Exa 搜索**：按 §三 关键词矩阵，每议题 5-8 组搜索
4. **深度抓取**：A 层来源和 Reddit 高票帖原始链接用 fetch_webpage
5. **合并去重**：以 URL 为 key。补缺更新时还需与现有 JSON 中的事件去重——以 `date + title_zh` 或 `sources[0].url` 匹配，已存在的事件不重复添加

**每个议题采集完成后**，汇报发现条数和来源层级分布（如"T1: 12条，A层4/C层6/D层2"）。

> **检查点**：展示各议题采集概览，请用户确认"继续筛选和撰写？"

### Step 4｜筛选 + 撰写 `🤖 → 🧑`

分两层工作：

**a) 筛选**（参照 02_WebfetchSOP §四）
- 应用纳入/排除标准
- 应用低持久性条目排除规则（T5 豁免）
- 给每条事件指定事件类型（8 选 1 词表）

**b) 撰写**（参照 05_WritingStyle 全文 + 02_WebfetchSOP §五-六）
- 撰写 JSON 事件条目：date / type / title_zh / summary_zh / sources / week
- **summary_zh 首句必须点明板块归属**（详见 05_WritingStyle §二「首句点明板块归属」）
- 撰写 Markdown 月度总览（bullet 格式，按日期升序）
- 同步更新 `digest_zh`（主页摘要卡片）

**关键规则**：
- JSON 和 Markdown 内容必须一致（同一批事件，不可 JSON 有而 MD 无，或反之）
- 先写 JSON（结构化，方便增删），再从 JSON 生成 Markdown 对应部分
- 事件的 `week` 字段按 05_WritingStyle §三「周分组规则」计算：第1周=1-7日，第2周=8-14日，第3周=15-21日，第4周=22日-月末（JSON中29-31日可写week=5，前端自动合并入第4周）

**JSON → Markdown 同步规则**：
- `build.py` 优先读 JSON 的 `report_metadata.overview`，JSON 直接对网页负责
- **MD 不自动更新**——仅在用户主动要求（如"更新 MD"、"同步 MD"）时才更新 reports/ 下的 Markdown 文件
- 日常工作流中 AI 只需维护 JSON，不需要同时写两份
- 如发现 JSON 和 MD 不一致，以 JSON 为准

> **检查点**：逐议题展示撰写结果摘要。用户审阅后确认"写入文件"或"修改后重写"。

### Step 5｜写入文件 + 构建 `🤖`

1. 将确认后的内容写入 `data/topicN/YYYY-MM.json` 和 `reports/topicN/YYYY-MM.md`
2. 运行 `python site/build.py --clean`
3. 告知用户打开 `site/dist/index.html` 本地预览

> **检查点**：用户确认页面正确后，AI 执行 git commit + push。

### Step 6｜部署 `🤖`

```bash
git add -A
git commit -m "feat: add YYYY-MM content for T1-T5"
git push
```

Cloudflare Pages 自动触发部署。告知用户等候 1-2 分钟后检查线上版本。

---

## 四、场景 B：补缺更新

> 适用于月中追加内容，如"3/20 到 4/1 之间的事件没搜"。

### Step 1｜确认范围 `🧑 → 🤖`

AI 用 AskQuestions 确认：
- 补哪个月的数据？（修改哪个 JSON 文件）
- 补哪些议题？全部还是指定？
- 时间窗口？（从 X 日到 Y 日）

### Step 2｜增量采集 `🤖`

与场景 A Step 3 相同，但 Exa 搜索的时间范围限定为用户指定的缺口期。

> **检查点**：汇报发现条数。

### Step 3｜筛选 + 撰写 `🤖 → 🧑`

与场景 A Step 4 相同，但：
- 新事件**追加**到现有 JSON 的 events 数组中（按日期插入正确位置）
- 月度总览 bullet **追加**新条目（保持日期升序）
- `digest_zh` 视需要更新

> **检查点**：展示新增事件清单，用户确认后写入。

### Step 4｜写入 + 构建 + 部署 `🤖`

同场景 A Step 5-6。Git commit message 用 `update: add MM/DD-DD events to topicN`。

---

## 五、场景 C：月度收尾

> 适用于月末定稿，冻结当月报告。

### Step 1｜质量检查 `🤖`

对照 02_WebfetchSOP §八 质量检查清单逐条过：
- 事件类型全部来自8选1词表
- 每条有日期+类型+来源
- A 层来源占比 ≥ 30%
- 中方来源检查（涉中事件有中方 A 层直接引用）
- 月度总览国别标注
- 叙事视角平衡
- T5 条目数量检查

### Step 2｜补漏 `🤖 → 🧑`

质量检查发现的问题，AI 列出修复建议，用户确认后执行。

### Step 3｜定稿 + 部署 `🤖`

Git commit message 用 `finalize: YYYY-MM reports`。

---

## 六、文件产出对照表

每次更新涉及的文件：

| 文件 | 作用 | 何时创建/更新 |
|------|------|--------------|
| `data/topicN/YYYY-MM.json` | 结构化事件数据，网站直接消费 | Step 4 写入 |
| `reports/topicN/YYYY-MM.md` | Markdown 报告（月度总览+事件条目） | Step 4 写入 |
| `site/dist/*` | 静态 HTML 产出 | Step 5 build.py 生成 |

**一致性规则**：JSON 是 single source of truth。Markdown 报告的事件列表必须与 JSON 一一对应。如有冲突以 JSON 为准。

---

## 七、人机分工速查

| 符号 | 含义 |
|------|------|
| `🤖` | AI 自主执行 |
| `🧑` | 用户决策 |
| `🧑 → 🤖` | 用户下指令，AI 执行 |
| `🤖 → 🧑` | AI 做完初稿，用户审阅确认 |

**AI 行为约束**：
- 每个标注为 `检查点` 的位置必须用 AskQuestions 请示用户
- 不跳过检查点自行推进到下一步
- 不在用户未确认的情况下写入文件或 git push

---

## 八、常见问题

| 问题 | 答案 |
|------|------|
| 新月份页面怎么出现？ | build.py 自动发现 `data/topicN/YYYY-MM.json`，rebuild 后月份选择器自动包含 |
| JSON 和 MD 不一致怎么办？ | 以 JSON 为准，从 JSON 重新生成 MD 对应部分 |
| 上月报告还能改吗？ | 可以，直接编辑上月 JSON+MD → rebuild 即可。但月度收尾后尽量不改 |
| 采集结果太多怎么筛？ | 严格按 02_WebfetchSOP §四 筛选标准，宁缺毋滥 |
| T5 收多少算够？ | T5 不设上限，宁多勿漏（02_WebfetchSOP §四 T5 豁免条款） |
