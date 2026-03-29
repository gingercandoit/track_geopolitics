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
│   ├── topic1-us-china/        # 议题1 JSON（按月：2026-03.json）
│   ├── topic2-supply-chain/    # 议题2 JSON
│   ├── topic3-energy-resources/ # 议题3 JSON
│   └── raw/                    # fetch_sources.py 原始拉取
│       └── 2026-03/            # 按月归档
├── reports/                    # 生成的简报产出
│   ├── topic1-us-china/        # 议题1 报告（按月：2026-03.md）
│   ├── topic2-supply-chain/    # 议题2 报告
│   └── topic3-energy-resources/ # 议题3 报告
├── prompts/                    # Prompt 模板存档
├── scripts/                    # 自动化脚本（fetch_sources.py）
├── config/                     # 工具配置（mcporter.json）
├── chat-history/               # 对话历史（.gitignore 排除）
└── _tmp/                       # 临时文件（.gitignore 排除）
```

### 文件命名规范

- 目录名：按议题 `topicN-<slug>` (kebab-case)
- 报告/数据文件名：按月 `YYYY-MM.md` / `YYYY-MM.json`
- 原始拉取：`data/raw/YYYY-MM/fetch_{topic|all}_{timestamp}.{json,md}`
- 新增议题时：先在 reports/ 和 data/ 下建同名目录

## 核心工作流

### Prompt 1：信息侦察
- 时间窗口：滚动 7 天
- 来源分层：A层（官方政府）> B层（国际机构）> C层（智库/媒体）
- 三大议题：中美关系、供应链/贸易政策、能源/资源地缘
- 产出格式：结构化 JSON + Markdown 简报

### Prompt 2：月度简报（待定义）

## 技术约定

- 数据文件统一 UTF-8 编码
- 日期格式：YYYY-MM-DD
- 文件命名：kebab-case
- 抓取结果按日期归档
