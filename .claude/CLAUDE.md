# Track Geopolitics — 地缘政治追踪项目

> 项目创建日期：2026-03-28

## 项目概述

可持续跟踪并更新的"地缘政治"研究项目。核心工作流分两个阶段：
- **Prompt 1**：官方信息抓取与分类（自动化信息侦察）
- **Prompt 2**：月度每日地缘政治经济简报生成（待讨论）

## 用户画像

- 用户：ginger
- 背景：经济学研究方向，关注地缘政治经济学
- 工具环境：VS Code Copilot（Windows）

## 项目结构

```
track_geopolitics/
├── .claude/                    # AI 记忆与规则
│   ├── CLAUDE.md
│   └── rules/
├── data/                       # 结构化数据
│   ├── topic1-sanctions/       # T1 制裁与经济管制
│   ├── topic2-trade-industrial/ # T2 贸易与产业竞争
│   ├── topic3-supply-resources/ # T3 供应链与关键资源
│   ├── topic4-tech-digital/    # T4 技术竞争与数字治理
│   ├── topic5-geopolitics/     # T5 地缘政治信息池（catch-all inbox）
│   └── raw/                    # fetch_sources.py 原始拉取
│       └── 2026-03/            # 按月归档
├── reports/                    # 生成的简报产出
│   ├── topic1-sanctions/       # T1 报告（按月：2026-03.md）
│   ├── topic2-trade-industrial/ # T2 报告
│   ├── topic3-supply-resources/ # T3 报告
│   ├── topic4-tech-digital/    # T4 报告
│   └── topic5-geopolitics/     # T5 报告
├── file/                       # 文档与参考资料
├── literature/                 # Prompt 3 文献库（与 reports 同级）
│   ├── classic/                # Library A: 经典文献（一次性建库）
│   │   ├── classic.json        # 主数据库（92篇）
│   │   ├── classic.csv         # CSV 结构化索引
│   │   ├── references.bib      # BibTeX 引用文件
│   │   ├── reading-roadmap.md  # 阅读路线图
│   │   └── views/              # 自动生成的阅读视图
│   ├── new/                    # Library B: 新文献追踪（月度更新）
│   │   ├── new.json            # 主数据库
│   │   ├── new.csv             # CSV 索引
│   │   ├── references.bib      # BibTeX
│   │   └── views/              # 视图
│   └── pdf/                    # 用户下载的PDF（.gitignore排除）
├── prompts/                    # Prompt 模板存档
├── scripts/                    # 自动化脚本（fetch_sources.py）
├── config/                     # 工具配置（mcporter.json）
├── chat-history/               # 对话历史（.gitignore 排除）
└── _tmp/                       # 临时文件（.gitignore 排除）
```

### 五大议题

| # | Slug | 中文名 | 覆盖范围 |
|---|------|--------|---------|
| T1 | topic1-sanctions | 制裁与经济管制 | OFAC/EU制裁, SWIFT, 美元武器化, 储备多元化, 人民币/CIPS, 反制裁 |
| T2 | topic2-trade-industrial | 贸易与产业竞争 | 关税/贸易战, 301/反倾销, 产业政策(CHIPS/IRA), WTO, CBAM |
| T3 | topic3-supply-resources | 供应链与关键资源 | 供应链重组, 关键矿产, 能源安全, OPEC, 粮食安全 |
| T4 | topic4-tech-digital | 技术竞争与数字治理 | BIS出口管制, 半导体/AI限制, AI治理, 数据主权 |
| T5 | topic5-geopolitics | 地缘政治信息池 | 不设门槛的 catch-all inbox，收录 T1-T4 未覆盖的所有地缘政治事件，供浏览发现后升级 |

### 文件命名规范

- 目录名：按议题 `topicN-<slug>` (kebab-case)
- 报告/数据文件名：按月 `YYYY-MM.md` / `YYYY-MM.json`
- 原始拉取：`data/raw/YYYY-MM/fetch_{topic|all}_{timestamp}.{json,md}`
- 新增议题时：先在 reports/ 和 data/ 下建同名目录

## 核心工作流

### Prompt 1：信息侦察
- 时间窗口：滚动 7 天
- 来源分层：A层（官方政府）> B层（国际机构）> C层（智库/媒体）> D层（社区策展）
- 五大议题：制裁与经济管制、贸易与产业竞争、供应链与关键资源、技术竞争与数字治理、地缘政治信息池（catch-all）
- 产出格式：结构化 JSON + Markdown 简报
- SOP：`.claude/rules/01_GeopoliticsWebfetchSOP.instructions.md`

### Prompt 2：月度简报（待定义）

### Prompt 3：文献搜集
- 双库架构：Library A（经典文献一次性建库 ~75-100篇）+ Library B（月度新论文追踪 5-20篇/月）
- 质量线：Tier 1-3 期刊白名单 + NBER/CEPR WP + 知名作者追踪
- 文件结构：`literature/` 目录（与 reports 同级），classic/ + new/ 完全独立子目录
- 产出：`literature/classic/` (classic.json + CSV + BibTeX + roadmap + views) + `literature/new/` (new.json + CSV + BibTeX + views)
- SOP：`.claude/rules/02_LiteratureSOP.instructions.md`
- **Library A 当前状态**（2026-03-29）：
  - 92 篇论文（76篇基础 + 18篇滚雪球 - 5篇WP重复 + 3篇缺失经典补充），经严格地缘政治相关性筛选
  - notes_zh 全部手工撰写，逐篇验证准确性
  - Topic 分布：T1:19, T2:49, T3:18, T4:9, T5:38
  - Tier 分布：T1:19, T2:33, T3:20, WP:7, other:13
  - 81/92 有摘要（88%），11篇摘要 OpenAlex/S2 均无数据
- **Library B 当前状态**（2026-07-18）：
  - 45 篇新文献（2024-mid 至 2026-present），聚焦经济学界最热门地缘政治研究
  - 搜索覆盖：OpenAlex（知名作者+NBER WP+Top Journal）、Exa（SSRN+JMP）
  - Topic 分布：T1:14, T2:24, T3:6, T4:3, T5:16
  - Tier 分布：WP:38, T1:2, T2:1, T3:4
  - Priority：core:23, recommended:21, reference:1
  - 42/45 有摘要（93%）
  - 每篇均含 `data_zh`（数据来源）和 `method_zh`（方法论）字段，基于摘要逐篇手写（无摘要者标注"待读全文确认"）
  - 核心论文：Clayton/Maggiori 地缘经济三部曲、Auclert 关税宏观冲击(16引)、Ossa/Redding 关税经济学综述、Gopinath/Neiman 关税负担、CHIPS法案就业影响

## 自动化脚本

| 脚本 | 用途 | 调用方式 |
|------|------|---------|
| `scripts/build_literature.py` | OpenAlex API 建库（Phase A） | `.\.venv\Scripts\python.exe scripts/build_literature.py` |
| `scripts/build_phase2.py` | 从 JSON 生成 CSV/BibTeX/阅读路线图 | `.\.venv\Scripts\python.exe scripts/build_phase2.py` |
| `scripts/generate_views.py` | 从 JSON 生成 7 个 Markdown 视图 | `.\.venv\Scripts\python.exe scripts/generate_views.py` |
| `scripts/fetch_sources.py` | Prompt 1 信息侦察：RSS+Reddit 拉取 | `.\.venv\Scripts\python.exe scripts/fetch_sources.py [--days N] [--topic T]` |
| `scripts/generate_views_new.py` | Library B 视图 + CSV 同步生成 | `.\.venv\Scripts\python.exe scripts/generate_views_new.py` |

## 技术约定

- Python 虚拟环境：`.venv/`（已安装 requests, feedparser）
- 数据文件统一 UTF-8 编码
- 日期格式：YYYY-MM-DD
- 文件命名：kebab-case
- 抓取结果按日期归档
