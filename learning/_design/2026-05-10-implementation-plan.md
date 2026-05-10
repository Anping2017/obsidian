---
title: Vault 学习辅助系统 v0.1 实施计划
type: topic
tags: [meta, learning-system, plan]
sources: [learning/_design/2026-05-10-system-design.md]
created: 2026-05-10
updated: 2026-05-10
summary: 把 v0.1 设计文档落地为 8 个可执行任务,创建 5 份核心文档 + 2 个空目录 + 修改 vault CLAUDE.md,最后用 Mode A 模拟验证集成是否通畅。
---

# Vault 学习辅助系统 v0.1 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 [设计文档](learning/_design/2026-05-10-system-design.md) 落地为 vault 内可运转的 v0.1 MVP — 5 份核心文档 + 2 个空目录 + 1 处 CLAUDE.md 修改,使 Claude 能识别学习意图、按 PLAYBOOK 执行、产物按代谢规则流入 raw/wiki/output。

**Architecture:** 在 `D:\BaiduNetdiskWorkspace\Obsidian Vault\learning\` 下建立 5 个 markdown 文件作为系统骨架,vault 根 CLAUDE.md 加引导段触发系统。文件全为静态规则文档,执行体是 Claude 本身(读规则后按规则行动)。无代码,无服务,无外部依赖。

**Tech Stack:** Markdown(Obsidian Flavored)+ YAML frontmatter + Claude Code agent runtime

**约束:**
- 不擅自 git commit(用户使用 vault backup 自动提交模式)
- 所有文件遵循 vault SCHEMA frontmatter(title/type/tags/sources/created/updated/summary)
- 不修改 raw/ 或 wiki/ 内容(系统只新增 learning/ 目录,只在 CLAUDE.md 加节)
- 文件路径使用 Windows 反斜杠或正斜杠均可(Obsidian 处理)

---

## Task 1: 创建 CHANGELOG.md

**Files:**
- Create: `learning/CHANGELOG.md`

- [ ] **Step 1: 写文件内容**

```markdown
---
title: 学习系统迭代记录
type: topic
tags: [meta, learning-system, changelog]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 学习辅助系统的版本与修订历史。版本号策略:月复盘改 PLAYBOOK 一项 +0.01,改 RULES 或增减 mode +0.1,架构重构 +1.0。
---

# CHANGELOG

> 版本号策略:月复盘改 PLAYBOOK 一项 → +0.01;改 RULES / 增减 mode → +0.1;架构重构 → +1.0
> 修改触发源:① 月复盘强制(每月 ≥1 处) ② 用户提"剧本不好用"即时重构

## v0.1 — 2026-05-10(初版)

- 创建 `learning/` 目录与 5 份核心文档(SYSTEM / RULES / PLAYBOOK / DASHBOARD / CHANGELOG)
- 在 vault 根 CLAUDE.md 加学习系统引导段
- 6 种 mode 全部启用:A 学科诊断 / B 跨域综合 / C 主题深读 / D 思维模型沙盒 / E stub 升级 / F 自由提问
- DASHBOARD 初始客观指标基于 PROGRESS.md(2026-05-06 快照),主观评分待用户填
- 设计文档:[2026-05-10-system-design.md](_design/2026-05-10-system-design.md)
```

- [ ] **Step 2: 验证文件**

用 Read 工具读 `learning/CHANGELOG.md`,检查:
- frontmatter 7 字段齐全
- 含版本号策略、v0.1 条目
- 引用了设计文档

预期:文件存在,内容完整。

---

## Task 2: 写 SYSTEM.md(系统入口)

**Files:**
- Create: `learning/SYSTEM.md`

- [ ] **Step 1: 写文件内容**

frontmatter + 5 节结构:

1. **是什么** — 一句话定位:vault 上的脚手架式学习辅助系统
2. **何时触发** — 关键词检测列表(学习/总结/复盘/诊断/深入/分析决策/升级 stub/带"?"的问题)
3. **决策树** — 6 步流程:① 识别 mode → ② 读 PLAYBOOK 对应章节 → ③ (可选)读 DASHBOARD 拿历史进度 → ④ 执行剧本 → ⑤ 写 sessions/ 文件 → ⑥ 末尾做"产物归档判定",流向 raw/wiki/output
4. **Session 生命周期** — 起始(确认 mode + 输入)、执行(按 PLAYBOOK)、结束(写 sessions + 更新 DASHBOARD 客观字段 + 询问产物归档 + 温和推荐下一步)
5. **文件地图** — 每个 learning/ 下文件的职责与读取时机

完整内容:

```markdown
---
title: 学习辅助系统总览(入口)
type: topic
tags: [meta, learning-system, entry]
sources: [_design/2026-05-10-system-design.md]
created: 2026-05-10
updated: 2026-05-10
summary: vault 学习辅助系统的入口文档。Claude 在识别到学习意图时先读本文件,按决策树进入对应 mode 的剧本。
---

# 学习辅助系统(v0.1)

## 1. 是什么

vault 上的脚手架式学习辅助系统。**不是教练**——不施压、不主动启动 session;**是工具箱**——提供 6 种 mode 剧本、4 维进度评估、周/月复盘节奏。目标:把 1085+ wiki 从图书馆激活为训练场,同时让知识库在使用中持续生长。

## 2. 何时触发

Claude 检测到下列任一情况,**先读本文件**,按决策树进入系统:

- 关键词:学习 / 总结 / 复盘 / 诊断 / 深入 / 全面理解 / 把 X 和 Y 连起来 / 用模型分析 / 帮我决策 / 升级 stub / 补 [概念]
- 用户主动:"开 session"、"开始学习"、"想学 X"、"我有个困惑"
- 任何带"?"或"如何理解"的问题(默认 Mode F)

如果用户明确说"先不开学习系统,就闲聊",则跳过本系统。

## 3. 决策树

```
1. 识别意图 → 匹配 A-F 哪个 mode(见下表)
2. 读 PLAYBOOK.md 对应章节,严格按步骤
3. (可选)读 DASHBOARD.md,拿该学科/概念的历史进度
4. 执行剧本步骤
5. 写 sessions/YYYY-WW-<mode>-<topic>.md(frontmatter 必含 vault_changes)
6. 末尾做"产物归档判定":本次产生的新素材/概念/综述去 raw/wiki/output 哪里?与用户确认后执行
7. 末尾基于 DASHBOARD 给一句温和建议,可拒绝
```

### Mode 识别速查

| Mode | 触发模式 |
|---|---|
| **A 学科诊断** | "诊断 X"、"看看我 X 到几分"、"扫描 X" |
| **B 跨域综合** | "把 X 和 Y 连起来"、"X 与 Y 的关系" |
| **C 主题深读** | "深入 X"、"全面理解 X" |
| **D 思维模型沙盒** | "用模型分析"、"帮我决策"、"应该不应该 X" |
| **E stub 升级** | "升级 stub"、"补 X" |
| **F 自由提问** | 任何带"?"的问题、"我想问"、"如何理解" |

**冲突时**:不确定属哪个 mode,**主动问用户**,不要猜。

## 4. Session 生命周期

```
[起始]                     [执行]                     [结束]
确认 mode               →  按 PLAYBOOK 步骤        →  写 sessions/<file>
确认输入(学科/概念/决策) 严格遵守                  → 询问产物归档
                                                   → 更新 DASHBOARD 客观字段
                                                   → 一句温和下一步建议
```

## 5. 文件地图

| 文件 | 何时读 | 职责 |
|---|---|---|
| `SYSTEM.md`(本文件) | 检测到学习意图时第一个读 | 入口与决策树 |
| `RULES.md` | 用户挑战边界时 / 不确定能不能做时 | 必做/不能做清单 |
| `PLAYBOOK.md` | 确定 mode 后读对应章节 | 6 种剧本步骤 |
| `DASHBOARD.md` | 需历史进度参考 / 月复盘 | 12 学科 × 4 维度评分 + 全局健康 |
| `CHANGELOG.md` | 月复盘后写入 / 用户问"系统改过什么" | 版本与修订历史 |
| `sessions/` | 每次 session 末尾写入 | 会话日志 |
| `reviews/` | 周/月复盘时写入与读取 | 复盘文档 |
| `_design/` | 设计层面的疑问 | 原始 spec 与 plan |

## 6. 找不到答案怎么办

如果用户的请求不能映射到任何 mode,且不是闲聊:

- **优先 F mode** 兜底(自由提问最轻量)
- 如果 F 也不合适,说明请求超出本系统范围,正常处理(不强行套用学习系统)

不要把所有交互都套进 mode。
```

- [ ] **Step 2: 验证文件**

用 Read 读 `learning/SYSTEM.md`,检查:
- frontmatter 完整
- 6 节结构齐全
- Mode 识别速查表 6 行
- 文件地图覆盖所有 learning/ 文件

预期:文件存在,无截断。

---

## Task 3: 写 RULES.md(规则与边界)

**Files:**
- Create: `learning/RULES.md`

- [ ] **Step 1: 写文件内容**

```markdown
---
title: 学习辅助系统规则与边界
type: topic
tags: [meta, learning-system, rules]
sources: [_design/2026-05-10-system-design.md]
created: 2026-05-10
updated: 2026-05-10
summary: Claude 在学习辅助系统中能做与不能做的明确边界。任何修改需经月复盘并写入 CHANGELOG。
---

# RULES

## Claude 必须做

### 流程层

- ✅ 检测到学习意图时,**第一步读 `SYSTEM.md`**,严格按决策树
- ✅ 进入 mode 后,**完整读 `PLAYBOOK.md` 对应章节**,按步骤,不跳步不混合
- ✅ 每次 session 结束写 `sessions/YYYY-WW-<mode>-<topic>.md`,frontmatter 必含 `vault_changes`
- ✅ session 末尾做**产物归档判定**:列出本次产生的"应入 vault"内容,询问用户确认后执行
- ✅ session 末尾**更新 DASHBOARD 客观字段**(篇数、stub 比、新增 wikilinks 等可机械统计的指标)
- ✅ session 末尾给**一句温和的下一步建议**(基于 DASHBOARD),用户可拒绝
- ✅ 月复盘必须修订 PLAYBOOK 至少一处,并写入 CHANGELOG

### vault 代谢层

- ✅ 学习中遇到**新原始素材**(网页、对话、书摘) → 转 markdown 入 `raw/<对应学科>/`,补完整 frontmatter
- ✅ 学习中产生**新概念**或对已有概念有重大补充 → 在 `wiki/` 建 stub 或升级条目(**用户确认后**写入)
- ✅ 学习中产生**综述、跨域分析、决策报告** → 入 `output/`,frontmatter `type: permanent` `tags` 加 `output`,文末列引用的 wiki 条目
- ✅ 写入 wiki 必须按 `SCHEMA.md` 格式;按 vault CLAUDE.md 的"统一术语"规则用词
- ✅ 写入 raw 时**不修改用户原有 raw/ 文件正文**;只对自己新增的 raw 文件写完整 frontmatter

### 节奏层

- ✅ 周日(或用户说"周复盘")主动**生成本周复盘**(基于 sessions/),写到 `reviews/YYYY-WW-weekly.md`
- ✅ 月末(或用户说"月复盘")**主导对话式月复盘**,产出 `reviews/YYYY-MM-monthly.md`,触发 PLAYBOOK 修订与 CHANGELOG 更新

## Claude 不能做

### 流程层

- ❌ 主动启动 session(必须用户触发)
- ❌ 跳过 SYSTEM.md / PLAYBOOK.md 直接发挥
- ❌ 同一温和建议在被拒绝后 1 周内重复推荐
- ❌ 在 mode 进行中"想到一个更好的 mode"就擅自切换;若需切换,问用户
- ❌ 一次 session 同时跑两个 mode(会合并产物难以归档,需要时拆成两次 session)

### 行为层

- ❌ 主动施压(不催、不打分式批评、不"你应该 X 了")
- ❌ 渲染挫败感("你这领域差太多了"、"你已经停了 N 天没学")
- ❌ 用进度数据制造焦虑;DASHBOARD 是镜子不是鞭子

### vault 写入层

- ❌ 擅自修改 wiki/(任何写入必须用户明确确认)
- ❌ 修改用户原有 raw/ 文件正文(只可对自己新增的 raw 文件补 frontmatter)
- ❌ 删除任何 vault 内已有文件
- ❌ 跨学科混搭命名违反 SCHEMA(中文优先、扁平结构、术语一致)

### 系统自身层

- ❌ 擅自修改 PLAYBOOK / RULES / SYSTEM(必须经月复盘,写入 CHANGELOG)
- ❌ 擅自增加 / 删除 mode(同上)
- ❌ 让有价值产物**只停留在 sessions/** 而不流向 raw/wiki/output

## 模糊地带处理原则

- 不确定 mode 归属 → **问用户**
- 不确定写入位置(raw vs wiki vs output) → **问用户**
- 不确定要不要建 stub → **建议但不擅自创建**
- 不确定要不要触发月复盘 → **看日期**:超过上次月复盘 28 天提议,否则不主动提

## RULES 自身的修改

本文件的任何修改必须:
1. 在月复盘讨论中达成共识
2. 写入 `CHANGELOG.md`
3. 版本号 +0.1(因为改 RULES 不是小调)

用户可以随时口头说"这条规则不好用",但实际修改必须走流程。
```

- [ ] **Step 2: 验证文件**

Read `learning/RULES.md`,检查:
- 必做 / 不能做 / 模糊处理 三段都在
- 流程 / vault 代谢 / 节奏 三个子层全覆盖
- 自身修改流程明确

---

## Task 4: 写 PLAYBOOK.md(六种剧本)

**Files:**
- Create: `learning/PLAYBOOK.md`

文件较长(~500 行)。结构:frontmatter + 全局术语 + 6 节(每个 mode 各一节)+ 冲突处理。

- [ ] **Step 1: 写文件框架与术语**

每个 mode 节统一 8 子节:**触发词 / 输入 / 步骤 / sessions 输出 / vault 产物去向 / 时长 / 不做的事 / 模板**。

- [ ] **Step 2: 写 Mode A 学科诊断章节**

参考 spec 第 4.3 节 Mode A,展开为可执行步骤,含 sessions/ 文件模板。

关键步骤(展开):
1. 用 Glob 列出 `wiki/concepts/` 与 `wiki/topics/` 中该学科相关条目(按学科关键词,例如金融 → 货币/利率/资本/债券/股票/金融/汇率/...)
2. 用 Grep 数 stub 频次:`grep -c "stub" frontmatter`
3. 用 Grep 数 wikilinks 入度:每条目被几处引用
4. 分类:
   - 已掌握:mature 且被引用 ≥3
   - 薄弱:stub 但被引用 ≥2
   - 孤立:mature 但被引用 ≤1
   - 缺失:对照该学科 PROGRESS.md 子主题清单,实际 wiki 没有的子主题
5. 让用户对该学科 4 维度自评 1-5(给参考锚点:"你能给同事讲清楚哪些?")
6. 客观 vs 主观对比,用表格列差距
7. 给 2-3 个下一步建议,优先级排序(每个建议关联具体 mode:"建议下次跑 E mode 升级 [stub 名]")

- [ ] **Step 3: 写 Mode B 跨域综合章节**

关键步骤:
1. 用 Glob/Grep 列出 X、Y(可 Z)三方相关条目
2. 用 Grep `[[X]]` 找已有 X-Y 直接连接
3. 找隐藏连接:① 共享心智模型(读两边引用的心智模型条目)② 相似机制(对比两边核心概念定义)③ 对偶/反例(如金融×心理 → 行为金融,理论×实务 → ...)
4. 写综述 → `output/<X-与-Y>.md`,结构:概述 / 各方理解 / 桥接点 / 综合启示 / wiki 引用清单
5. 综述中提到 vault 没有的概念 → 列出"建议建 stub"清单,询问用户

- [ ] **Step 4: 写 Mode C 主题深读章节**

关键步骤:
1. Read 目标 wiki 条目
2. 用 Grep `[[目标条目]]` 找入度引用,Read 全部
3. 读出度 wikilinks(条目内的 [[X]])
4. 从 raw/ 找原始素材(Glob `raw/**/*<topic>*`)
5. 必要时 web 搜补充(WebSearch / WebFetch)
6. 生成 5 段:定义 / 历史 / 争议 / 应用 / 局限
7. 升级目标条目(如果是 stub)→ Read 现状 → Edit/Write → 用户确认
8. 若引入新原始素材 → 入 raw/

- [ ] **Step 5: 写 Mode D 思维模型沙盒章节**

关键步骤:
1. 让用户描述决策(if 不充分,补问):
   - 决策内容(选项)
   - 利益相关方
   - 时间线 / 不可逆程度
   - 当前倾向
2. 从 110+ 心智模型挑 3-5 个最相关(优先:逆向思维 / 二阶思维 / 概率思维 / 机会成本 / 安全边际 + 决策领域专属)
3. 对每个模型:① 简述模型核心 ② 用模型分析此决策 ③ 得出该模型视角的建议(可能矛盾)
4. 综合多视角,给最终建议
5. 关键产出:**"假设可能错的点"** + **"什么信号会让你反转判断"**(Bayesian 视角)
6. 写到 `output/decisions/<decision-name>.md`
7. 1 个月后可加事后复盘段(留 anchor)

- [ ] **Step 6: 写 Mode E stub 升级章节**

关键步骤:
1. 若用户没指定 stub:从 DASHBOARD 推荐 3 个高引用 stub 让用户选
2. Read 该 stub 现状
3. Grep 入度引用,Read 全部(理解被怎样使用)
4. Glob raw/ 找原始素材
5. 必要时 WebSearch 补
6. 按 SCHEMA 重写为 mature(定义 / 核心要点 / 关系 / 参考源)
7. 加 wikilinks(凡提到的已有 wiki 概念)
8. 用户审阅 → Write 替换

- [ ] **Step 7: 写 Mode F 自由提问章节**

关键步骤:
1. 用 Glob/Grep 在 wiki/ 找直接相关条目
2. 优先用 wiki/ 内容回答,辅以心智模型联想
3. 延伸 2-3 个相关条目链接
4. 引导反问("这让你想到 vault 里的什么?")
5. 简版 sessions/(300-500 字)
6. 若回答中暴露 vault 缺失 → 提议下次开 B/C/E mode

- [ ] **Step 8: 写冲突与歧义处理章节**

```
触发词冲突:
- "深入金融" → 是 C 还是 A?
- "金融与心理学的关系" → 是 B 还是 C(深入"金融与心理学"这个 topic)?

判定原则:
- 单一概念/topic + "深入/全面" → C
- 单一学科 + "诊断/扫描/到几分" → A
- 多个概念/学科 + "关系/连接/综合" → B
- 不确定 → 问用户

不要主动切换 mode:一旦开始,不中途换车;若 mode 错了,正常结束当前 session,下一轮再开新 mode。
```

- [ ] **Step 9: 验证文件**

Read `learning/PLAYBOOK.md`,检查:
- 6 个 mode 各一节,8 子节齐全
- 步骤具体可执行(不只是"分析"、"评估"这种空话)
- sessions/ 模板可直接复用
- 冲突处理章节存在

---

## Task 5: 写 DASHBOARD.md(进度仪表盘)

**Files:**
- Create: `learning/DASHBOARD.md`

- [ ] **Step 1: 收集初始客观数据**

不做精细 per-discipline 统计(留首次月复盘做),用 PROGRESS.md(2026-05-06 快照)作为基线:

| 学科 | 篇数(自 PROGRESS) | Coverage 估算(篇数→1-5) |
|---|---|---|
| 计算机 | 227 | 4 |
| 营销与SEO | 130 | 4 |
| 金融学 | 119 | 4 |
| 商业管理 | 116 | 4 |
| 思维模型 | 110+ | 4 |
| AI与机器学习 | 70 | 3 |
| 哲学 | 67 | 3 |
| 经济学 | 64 | 3 |
| 心理学 | 61 | 3 |
| 英语 | 47 | 2 |
| 工具与生活 | 38 | 2 |
| 会计学 | 35 | 2 |

Coverage 标尺:< 40 → 2 / 40-100 → 3 / 100-200 → 4 / > 200 → 5(粗略,首月复盘细化)

Depth 默认 4(全 vault stub 11.5%,各学科假设接近平均),首月校准。
Connectedness 默认 4(全 vault 平均度 14,高水平),首月校准。
Application 全部 1(output 全空,无应用记录)。

- [ ] **Step 2: 写 DASHBOARD 文件**

```markdown
---
title: 学习进度仪表盘
type: topic
tags: [meta, learning-system, dashboard]
sources: [_design/2026-05-10-system-design.md, ../wiki/PROGRESS.md]
created: 2026-05-10
updated: 2026-05-10
summary: 12 学科 × 4 维度(Coverage/Depth/Connectedness/Application)进度评分,加全局健康指标。客观指标基于 2026-05-06 PROGRESS 快照,主观自评待用户首次填写。
---

# 学习进度仪表盘(v0.1)

> 客观指标:Claude 自动统计;主观评分:用户每月复盘时打分。差距大的格 = 盲点信号。

## 全局健康指标(2026-05-10 初版)

| 指标 | 当前值 | 目标方向 | 上月变化 |
|---|---|---|---|
| Wiki 总篇数 | 1085+ | ↑ 持续生长 | 初版 |
| Stub 比例 | ~11.5%(114/992) | ↓ 月度下降 | 初版 |
| Output 篇数 | 0 | ↑ 月增 ≥ 1 | 初版 |
| Wikilinks 总数 | 13771 | ↑ 自然增长 | 初版 |
| 平均度(链接/篇) | 14 | ↑ 至 18+ | 初版 |
| 跨域桥接对 | 8 | ↑ 月增 ≥ 1 | 初版 |
| Raw 篇数 | 4500+ | 自然增加 | 初版 |

## 12 学科 × 4 维度评分

> Coverage = 覆盖度,Depth = 深度,Connectedness = 连接度,Application = 应用度。
> 每维 1-5,客观(Obj)由 Claude 统计,主观(Self)由你打分。

| 学科 | 篇数 | Cov(Obj/Self) | Dep(Obj/Self) | Con(Obj/Self) | App(Obj/Self) |
|---|---|---|---|---|---|
| 计算机科学 | 227 | 4 / _ | 4 / _ | 4 / _ | 1 / _ |
| 营销与SEO | 130 | 4 / _ | 4 / _ | 4 / _ | 1 / _ |
| 金融学 | 119 | 4 / _ | 4 / _ | 4 / _ | 1 / _ |
| 商业管理 | 116 | 4 / _ | 4 / _ | 4 / _ | 1 / _ |
| 思维模型 | 110+ | 4 / _ | 4 / _ | 4 / _ | 1 / _ |
| AI与机器学习 | 70 | 3 / _ | 4 / _ | 4 / _ | 1 / _ |
| 哲学 | 67 | 3 / _ | 4 / _ | 4 / _ | 1 / _ |
| 经济学 | 64 | 3 / _ | 4 / _ | 4 / _ | 1 / _ |
| 心理学 | 61 | 3 / _ | 4 / _ | 4 / _ | 1 / _ |
| 英语 | 47 | 2 / _ | 4 / _ | 3 / _ | 1 / _ |
| 工具与生活 | 38 | 2 / _ | 3 / _ | 3 / _ | 1 / _ |
| 会计学 | 35 | 2 / _ | 4 / _ | 4 / _ | 1 / _ |

> Self 列首次填写在第一次月复盘(2026-06)。建议你看过几次 mode 之后再打,有手感。

## 评分标尺

### Coverage 覆盖度
- 1:只接触少数核心概念
- 2:覆盖 1-2 个子领域
- 3:覆盖主要子领域之半
- 4:主要子领域大致覆盖
- 5:子领域基本完整,边角也有

### Depth 深度
- 1:多 stub,只是定义
- 2:能复述但无独立见解
- 3:能讲清楚机制
- 4:能识别局限与争议
- 5:能写综述给别人看

### Connectedness 连接度
- 1:孤立成块
- 2:学科内部互通
- 3:有跨域意识
- 4:能跨域联想
- 5:自由跨学科分析

### Application 应用度
- 1:纯阅读,0 应用
- 2:偶尔说起
- 3:用来分析过 1-2 次具体问题
- 4:每月用 1-2 次分析决策
- 5:日常思维默认嵌入

## 更新历史

- 2026-05-10:初版,客观指标据 PROGRESS.md 估算,主观空白等首次月复盘
```

- [ ] **Step 3: 验证文件**

Read `learning/DASHBOARD.md`,检查:
- 全局健康 7 行
- 12 学科表格
- 4 个维度的标尺
- 更新历史段

---

## Task 6: 创建 sessions/ 与 reviews/ 空目录及说明

**Files:**
- Create: `learning/sessions/README.md`
- Create: `learning/reviews/README.md`

- [ ] **Step 1: 写 sessions/README.md**

```markdown
---
title: Sessions 目录说明
type: topic
tags: [meta, learning-system]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 本目录存放每次学习会话(session)的日志文件。命名格式 YYYY-WW-<mode>-<topic>.md。
---

# Sessions

每次学习会话的日志。

## 命名格式

`YYYY-WW-<mode>-<topic>.md`

例:
- `2026-W19-A-finance.md`(2026 年第 19 周,Mode A 诊断金融)
- `2026-W19-D-job-offer-decision.md`(Mode D 工作 offer 决策)

## frontmatter 模板

见 `../PLAYBOOK.md` 各 mode 章节。必含 `vault_changes` 字段,记录本次 session 给 raw/wiki/output 添了什么。

## 不要

- 不在本目录写知识资产(知识应入 raw/wiki/output)
- 不删除历史 session(月复盘归档,但保留)
```

- [ ] **Step 2: 写 reviews/README.md**

```markdown
---
title: Reviews 目录说明
type: topic
tags: [meta, learning-system]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 本目录存放周复盘(weekly)和月复盘(monthly)文档。
---

# Reviews

## 命名格式

- 周复盘:`YYYY-WW-weekly.md`(例 `2026-W19-weekly.md`)
- 月复盘:`YYYY-MM-monthly.md`(例 `2026-05-monthly.md`)

## 周复盘:Claude 主导,你只读

- 本周 session 数与 mode 分布
- 本周 vault 产物清单(raw/wiki/output 增量)
- 涉及学科分布
- 一个亮点 / 一个警惕
- 下周 2-3 个建议

## 月复盘:对话形式,你+Claude 共评

- 本月 session 概览
- 本月 vault 代谢报告
- DASHBOARD 重新打分
- 三个反思问题(最有价值/最无聊/最强烈方向)
- **强制修订 PLAYBOOK 至少一处**
- 写入 CHANGELOG
```

- [ ] **Step 3: 验证目录**

用 Glob `learning/sessions/*` 和 `learning/reviews/*`,确认 README.md 存在。

---

## Task 7: 修改 vault 根 CLAUDE.md 加引导段

**Files:**
- Modify: `CLAUDE.md`(末尾追加新节)

- [ ] **Step 1: Read 现有 CLAUDE.md**

确认末尾位置(避免破坏现有规则)。

- [ ] **Step 2: 在末尾追加学习系统引导段**

```markdown
## 学习辅助系统

vault 内有学习辅助系统位于 `learning/`,v0.1 起。

### 何时进入

Claude 检测到下列任一情况,**先读 `learning/SYSTEM.md`**,按其决策树执行:

- 关键词:学习 / 总结 / 复盘 / 诊断 / 深入 / 全面理解 / 把 X 和 Y 连起来 / 用模型分析 / 帮我决策 / 升级 stub / 补 [概念]
- 用户主动:"开 session"、"开始学习"、"想学 X"、"我有个困惑"
- 任何带"?"或"如何理解"的问题(默认 Mode F)

例外:用户明确说"先不开学习系统,就闲聊",跳过本系统。

### 系统约束(简版)

- Claude 不擅自启动 session,必须由用户触发
- session 产物按代谢规则流入 raw/wiki/output(写 wiki 必须用户确认)
- session 文件本身只是日志,不是知识资产
- 修改 PLAYBOOK / RULES 必须经过月复盘并写入 CHANGELOG

### 如果不进入

正常按 vault CLAUDE.md 现有规则处理。学习系统是叠加层,不替换基础规则。
```

- [ ] **Step 3: 验证 CLAUDE.md**

Read 整个 CLAUDE.md,确认:
- 学习系统节在末尾
- 不与现有"目录结构"、"frontmatter 规范"、"操作规则"等节冲突
- 引用路径 `learning/SYSTEM.md` 准确

---

## Task 8: 验证 — Mode A 模拟集成测试

**Files:** 不创建,只读 + 推演

- [ ] **Step 1: 模拟用户输入**

假设用户在新对话说:"诊断一下我的金融学到几分了"

- [ ] **Step 2: 推演 Claude 行为**

预期顺序:
1. 检测到关键词"诊断" + 学科"金融学" → 进入学习系统
2. Read `learning/SYSTEM.md` → 决策树第 1 步识别 Mode A
3. Read `learning/PLAYBOOK.md` Mode A 章节
4. (可选)Read `learning/DASHBOARD.md` 看金融学历史评分
5. 按 PLAYBOOK Mode A 步骤执行:
   a. Glob/Grep 金融相关 wiki
   b. 数 stub、wikilinks
   c. 分类四类报告
   d. 让用户自评 4 维度
   e. 客观 vs 主观对比
   f. 给 2-3 个下一步建议
6. 写 `learning/sessions/2026-W19-A-finance.md`(frontmatter 含 vault_changes)
7. 末尾产物归档判定:发现的"缺失子主题"→ 提议建 stub
8. 末尾温和建议下一步

- [ ] **Step 3: 检查任何环节会卡壳**

| 检查点 | 通过条件 | 不通过的对策 |
|---|---|---|
| CLAUDE.md 引导被识别 | 关键词"诊断"在引导段列表 | ✅ 已包含 |
| SYSTEM.md 决策树清晰 | Mode A 速查表存在 | ✅ Task 2 |
| PLAYBOOK Mode A 步骤可执行 | 有 Glob/Grep 具体命令模式 | ✅ Task 4 Step 2 |
| DASHBOARD 金融学有初值 | 表格中金融学行存在 | ✅ Task 5 |
| sessions 文件名格式明确 | YYYY-WW-mode-topic | ✅ Task 6 sessions/README |
| 产物归档机制有触发 | RULES 必做项有 | ✅ Task 3 |

- [ ] **Step 4: 记录验证结果**

把推演结果作为口头交付给用户,不写入 vault(不污染 sessions/)。如果发现卡壳,回到对应 Task 修订。

---

## Self-Review

### Spec 覆盖度

| Spec 章节 | 实现 Task |
|---|---|
| 第 3.1 目录结构 | T1-T6 创建所有指定文件 |
| 第 3.2 代谢循环 | T3 RULES.md 必做项 + T4 各 mode "vault 产物去向" |
| 第 3.3 CLAUDE.md 集成 | T7 |
| 第 4.1 SYSTEM.md | T2 |
| 第 4.2 RULES.md | T3 |
| 第 4.3 PLAYBOOK 6 mode | T4 |
| 第 4.4 DASHBOARD | T5 |
| 第 4.5 CHANGELOG | T1 |
| 第 5.1 sessions frontmatter | T4 各 mode 模板 + T6 README |
| 第 5.2 reviews 结构 | T6 README |
| 第 6 复盘节奏 | 不实施(等首周/首月触发) |
| 第 7 实施分阶段 MVP | T1-T8 全覆盖 MVP |
| 第 8 验收 | T8 验证(系统运转层);代谢层等首周/首月 |

未覆盖:复盘自动生成机制(等到 W19 周末或 5 月底自然触发,不在 MVP 范围)。

### Placeholder 扫描

无 TBD/TODO,所有 step 含具体内容或文件名/命令模式。

### 命名一致性

- 文件名:全 learning/ 下 5 文件名一致
- frontmatter 字段名:与 SCHEMA + spec 5.1 一致(`vault_changes` 4 子字段)
- mode 标识:A-F 全文一致

---

## 不在本计划范围(YAGNI)

- 不实现"自动定时周复盘"(等用户主动说"周复盘"或定时 nudge,留 v0.2)
- 不实现"sessions 自动归档"(留 v0.2)
- 不实现"stub 优先级算法"(默认从 DASHBOARD 用户挑,留 v0.2)
- 不做 Obsidian dataview / bases 视图(留 v0.2 可选扩展)
- 不预生成首周/首月模板(等真实数据再生)
