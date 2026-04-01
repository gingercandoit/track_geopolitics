---
description: FrontendSOP - 静态网站构建与维护标准操作流程
---

# 前端静态网站 SOP

> 项目级 SOP。规范"数据 → 构建 → 部署"的完整工作流。

---

## 一、架构概述

### 技术栈

- **构建工具**：Python + Jinja2 模板引擎
- **输出格式**：纯静态 HTML/CSS/JS（零服务端依赖）
- **部署目标**：GitHub Pages（或任何静态托管）
- **设计风格**：学术期刊 / 编辑部风（Academic Editorial）

### 核心原则

1. **数据与呈现完全分离**：JSON 数据不变，模板和配置控制呈现
2. **一键重建**：`python site/build.py` 即可重新生成全站
3. **自动发现**：build.py 自动扫描 `data/` 和 `literature/` 目录，不需要手动注册新月份或新议题
4. **路径依赖极低**：所有路径映射集中在 `site/config.py`，改一处即可

---

## 二、文件结构

```
site/                             # 前端项目根目录
├── build.py                      # 构建入口脚本
├── config.py                     # 配置：颜色、字体、路径映射、议题定义
├── templates/                    # Jinja2 模板
│   ├── base.html                 # 基础模板（HTML head + nav + footer）
│   ├── index.html                # 首页模板
│   ├── topic.html                # T1-T4 议题页模板（带事件卡片流）
│   ├── topic5.html               # T5 紧凑列表模板
│   ├── literature.html           # 文献页模板
│   ├── archive.html              # 往期存档索引
│   └── components/               # 可复用 Jinja2 组件
│       ├── event_card.html       # T1-T4 事件折叠卡片
│       ├── event_row.html        # T5 紧凑事件行
│       ├── paper_card.html       # 文献折叠卡片
│       ├── nav.html              # 导航栏
│       ├── footer.html           # 页脚
│       └── month_selector.html   # 月份选择器
├── static/                       # 静态资源
│   ├── css/
│   │   └── style.css             # 主样式表
│   └── js/
│       └── main.js               # 卡片折叠 / 筛选 / 月份切换
└── dist/                         # 构建输出（.gitignore 排除）
    ├── index.html
    ├── archive.html
    ├── literature.html
    ├── topic1-sanctions/
    │   └── 2026-03.html
    ├── topic2-trade-industrial/
    │   └── 2026-03.html
    ├── topic3-supply-resources/
    │   └── 2026-03.html
    ├── topic4-tech-digital/
    │   └── 2026-03.html
    ├── topic5-geopolitics/
    │   └── 2026-03.html
    └── static/                   # 复制的静态资源
        ├── css/
        └── js/
```

---

## 三、数据流

```
data/topicN-slug/YYYY-MM.json ──┐
                                 ├──→ site/build.py ──→ site/dist/*.html
literature/classic/classic.json ─┤
literature/new/new.json ─────────┘
```

build.py 读取路径由 config.py 定义：

```python
DATA_DIR = Path("../data")
LITERATURE_DIR = Path("../literature")
OUTPUT_DIR = Path("dist")
```

---

## 四、页面架构

### 首页 (index.html)

1. **Hero 区**：当月期数 + 翻页箭头（← →）可切换月份，每月独立生成一个 index（最新月=`index.html`，旧月=`YYYY-MM.html`）
2. **五大议题入口卡片**：每个议题一张卡，显示议题名 + 颜色标识 + 当月事件数 + 最新 3 条事件标题
3. **最新文献速览**：Library B 最近 5 篇论文（标题 + 作者 + 议题标签）
4. **往期存档链接**

### 导航栏月份选择器

- 位于 nav 栏最右侧（存档链接之后），所有页面可见
- 在**主页**：切换跳转到对应月份的 index 页
- 在**议题页**：切换跳转到同一议题的对应月份页
- 在**其他页**（文献/存档）：切换跳转到对应月份的 index 页

### 议题页 T1-T4 (topic.html)

1. **议题标题**（月份切换已移至 nav 栏统一处理）
2. **月度总览叙述**（Markdown → HTML）
3. **事件时间线**：按周分组（4周制：W1=1-7, W2=8-14, W3=15-21, W4=22-月末），每周内按日期倒序
   - JSON `week` 字段 29-31日可写5，`build.py` 渲染时自动合并入W4
   - 每个事件是**折叠卡片**：日期 | 类型彩色标签 | 标题 → 点击展开 → bullets + 来源
4. **关键数字一览表**
5. **背景参考**（如有）

### T5 紧凑列表 (topic5.html)

1. **议题标题**（月份切换已移至 nav 栏统一处理）
2. **紧凑事件列表**：每条一行（日期 + 类型标签 + 标题），点击展开 1-2 行简述 + 来源
3. 条目数远多于 T1-T4，适合快速扫描

### 文献页 (literature.html)

1. **经典库 / 新文献 切换标签**
2. **筛选器**：议题标签（T1-T5） × 优先级（core/recommended/reference） × 年份区间（双输入框 yearFrom/yearTo） × 搜索框
3. **论文卡片列表**：折叠式，展开显示：
   - `abstract_zh`（中文摘要翻译，首选）/ `abstract`（英文摘要，回退）
   - 元信息行：引用数 · 数据来源（`data_zh`）· 方法论（`method_zh`）· DOI 来源链接
   - 所有论文（经典 + 新文献）统一展示结构，不做条件区分
4. **统计摘要**：总数、议题分布、Tier 分布

### 往期存档 (archive.html)

- 按月份倒序列出所有可用月份
- 每月一行：年月 + 各议题事件数 + 链接

---

## 五、视觉规范

### 色彩

| 角色 | 色值 | 说明 |
|------|------|------|
| 背景 | #FAFAF7 | 暖白 |
| 文字 | #1A1A1A | 近黑 |
| 强调/品牌 | #8B0000 | 深红 |
| 链接 | #2C5F7C | 蓝灰 |
| 卡片背景 | #FFFFFF | 纯白（带微阴影） |

### 事件类型标签色

| 类型 | 色值 |
|------|------|
| 政策发布 | #1B4965 |
| 贸易调查 | #D4A574 |
| 制裁与管制 | #8B0000 |
| 外交动态 | #2E7D32 |
| 国际机构 | #5C6BC0 |
| 智库分析 | #6D4C41 |
| 企业动态 | #F57C00 |
| 数据发布 | #455A64 |

### 字体

| 用途 | 字体族 |
|------|--------|
| 标题 | Playfair Display, serif |
| 正文中文 | Noto Serif SC, serif |
| 正文英文 | Source Serif Pro, serif |
| 标签/日期 | DM Sans, sans-serif |

### 卡片交互

- **折叠态**：日期 + 类型标签 + 标题 + ▸ 箭头，单行高度
- **展开态**：显示 summary bullets + 来源链接 + metrics
- **过渡**：max-height CSS transition，200ms ease
- **纯 CSS + 少量 vanilla JS**，不引入框架

### 事件卡片导语样式

- **所有事件卡**都显示导语（summary_zh 首句），格式为左侧竿线 + 加粗文字
- 竿线颜色随议题变化（通过 CSS 变量 `--lead-color` 传递）
- 导语后续句子渲染为 `<ul>` bullets
- CSS 选择器：`.event-summary p.event-lead`（需覆盖父规则 `.event-summary p`）

### CSS 开发注意事项

- **Specificity 陷阱**：修改子元素样式前，先检查父选择器是否有更高优先级的定义（如 `.event-summary p` 会覆盖裸 `.event-lead`）
- **缓存破坏**：CSS 迭代期间必须使用 query string 时间戳（`style.css?v={{ build_ts }}`），否则浏览器缓存旧版本
- **配色一致性**：组件颜色通过 CSS 变量或 inline style 从 config 传入，不硬编码在 CSS 中

---

## 六、月度维护流程

### 新增月份

```
1. 创建新月份 JSON 数据
   data/topic1-sanctions/2026-04.json
   data/topic2-trade-industrial/2026-04.json
   ...

2. 重新构建
   .\.venv\Scripts\python.exe site/build.py

3. 验证
   用浏览器打开 site/dist/index.html 检查

4. Git 提交
```

### 修改现有事件

```
1. 编辑对应 JSON 文件
2. 重新构建: python site/build.py
3. 验证 + Git 提交
```

### 更新文献

```
1. 更新 literature/classic/classic.json 或 literature/new/new.json
2. 重新构建: python site/build.py
3. 验证 + Git 提交
```

---

## 七、构建脚本规范 (build.py)

### 核心功能

1. **自动发现**：扫描 `data/` 下所有 `topicN-*/YYYY-MM.json` 文件
2. **月份排序**：所有发现的月份按倒序排列（最新在前）
3. **模板渲染**：读取 JSON → 传入 Jinja2 模板 → 输出 HTML
4. **静态资源复制**：`static/` → `dist/static/`
5. **相对路径**：所有页面间链接使用相对路径（GitHub Pages 兼容）

### 命令行参数（可选扩展）

```bash
python site/build.py                # 构建全站
python site/build.py --topic 1      # 仅构建 T1
python site/build.py --month 2026-04  # 仅构建指定月份
python site/build.py --clean        # 清理 dist/ 后重建
```

---

## 八、部署 (GitHub Pages)

### 配置

- 使用 `docs/` 目录或 GitHub Actions
- 如用 `docs/`：`build.py --output ../docs`
- 如用 Actions：`.github/workflows/deploy.yml` 自动构建并推送到 `gh-pages` 分支

### 注意事项

- 所有资源使用**相对路径**（不用绝对路径 `/static/...`）
- 如果部署在子目录（如 `username.github.io/track_geopolitics/`），需在 config.py 设置 `BASE_URL`

---

## 九、质量检查

每次构建后确认：

- [ ] 所有议题页面正常渲染，事件卡片可折叠/展开
- [ ] 月份选择器包含所有可用月份
- [ ] T5 紧凑列表条目数正确
- [ ] 文献页筛选功能正常
- [ ] 首页最新月份正确
- [ ] 所有链接可点击（相对路径无断链）
- [ ] 移动端响应式布局正常（如有）
- [ ] 已 Git 提交
