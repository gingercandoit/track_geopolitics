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
│   ├── topic5-diplomacy/       # T5 地缘政治信息池（catch-all inbox）
│   └── raw/                    # fetch_sources.py 原始拉取
│       └── 2026-03/            # 按月归档
├── reports/                    # 生成的简报产出
│   ├── topic1-sanctions/       # T1 报告（按月：2026-03.md）
│   ├── topic2-trade-industrial/ # T2 报告
│   ├── topic3-supply-resources/ # T3 报告
│   ├── topic4-tech-digital/    # T4 报告
│   └── topic5-diplomacy/       # T5 报告
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
| T5 | topic5-diplomacy | 地缘政治信息池 | 不设门槛的 catch-all inbox，收录 T1-T4 未覆盖的所有地缘政治事件，供浏览发现后升级 |

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

### Prompt 2：月度简报（待定义）

## 技术约定

- 数据文件统一 UTF-8 编码
- 日期格式：YYYY-MM-DD
- 文件命名：kebab-case
- 抓取结果按日期归档
