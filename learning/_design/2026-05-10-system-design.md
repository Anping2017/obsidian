---
title: Vault 学习辅助系统 v0.1 设计文档
type: topic
tags: [meta, learning-system, design]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 在 vault 之上构建工具箱式学习辅助系统(用户偏好 B 主线 + C 偶尔),含六种学习剧本、四维进度评估、周月复盘节奏、强制迭代机制,以及与 vault raw/wiki/output 三层的代谢循环,目标是把 1085+ wiki 从图书馆激活为训练场,同时让知识库在使用中持续生长。
---

# Vault 学习辅助系统 v0.1 设计文档

## 1. 背景与问题定义

### 1.1 vault 现状

- 1085+ wiki(873 概念 + 50 主题 + 69 实体),12 学科
- wikilinks 13771 条,平均每篇 14 个连接
- 三层流程 raw / wiki / output 已建立,**但 output/ 为空**
- 最近活跃:Round 5(2026-05-06)新增 90+ 心智模型,共 110+ 篇
- vault 现状是"输入与整理"已完成,缺"激活、输出、评估、生长"

### 1.2 教育学诊断

把 vault 状态放进学习科学的几个经典框架:

- **Bloom 认知层级**:已完成"记忆+理解",剩下"应用/分析/评估/创造"四层基本空白
- **学习金字塔**:留存率最高是"教别人(90%)",但用户停在"读(10%)"
- **Kolb 经验学习圈**:卡在"概念化"一步,缺"主动实验"和"反思"
- **元认知缺位**:无"每个领域到几分"的系统评估
- **Argyris 双圈学习**:vault 已有 single-loop(执行已知方法),缺 double-loop(质疑方法本身)

### 1.3 缺口

1. **激活**:把死知识用起来
2. **输出**:费曼技巧式的反向检验
3. **评估**:知道自己每个领域到几分
4. **节奏**:没有定期复盘,学习不形成闭环
5. **代谢**:学习产生的新东西没有标准入库通道,会"散失"

### 1.4 用户偏好

- 主线:**B 有方向但无时间线**(可能加深 AI / 金融 / 哲学 / Odoo 等)
- 偶尔:**C 泛泛提升**(纯探索时段)
- 自驱性强(vault 规模为证)

## 2. 设计原则

1. **不施压时间线** — 不预设"几周完成什么",DASHBOARD 不显示"完成度"
2. **保留探索弹性** — 工具箱模式默认,月度主题可选
3. **节奏由用户掌控** — Claude 不主动启动 session
4. **脚手架而非教练** — 提供框架但不替代用户思考(维果茨基 ZPD)
5. **强制迭代** — 月复盘必须修订系统至少一处
6. **自包含可携带** — 系统文档与 vault 共生(都是 markdown,git 追踪)
7. **vault 内循环(代谢原则)** ⭐ — 学习产生的所有有价值产物必须流入 vault 三层(raw/wiki/output),不滞留 sessions/。学习系统是 vault 的"代谢机制",而不是平行的笔记本
8. **持续生长** ⭐ — 系统的成功标志不是"完成多少 session",而是"vault 在使用中是否长大、连接是否变密、stub 比例是否下降"

## 3. 系统架构

### 3.1 目录结构

```
D:\BaiduNetdiskWorkspace\Obsidian Vault\
├── raw\               # 原始素材(已有,学习系统会持续注入新素材)
├── wiki\              # 知识层(已有,学习系统会新建/升级条目)
├── output\            # 衍生输出(已有,学习系统会持续产出综述/报告)
├── learning\          # 学习辅助系统(新增)
│   ├── SYSTEM.md          # 入口
│   ├── RULES.md           # 规则与边界
│   ├── PLAYBOOK.md        # A-F 六种剧本
│   ├── DASHBOARD.md       # 12 学科 × 4 维度评分
│   ├── CHANGELOG.md       # 系统迭代记录
│   ├── _design\
│   │   └── 2026-05-10-system-design.md   # 本文档
│   ├── sessions\          # 每次会话日志
│   │   └── 2026-W19-A-finance.md
│   └── reviews\           # 周/月复盘
│       ├── 2026-W19-weekly.md
│       └── 2026-05-monthly.md
└── CLAUDE.md          # 加引导段,指向 learning/SYSTEM.md
```

**重要**:`learning/` 不是平行结构,而是 raw/wiki/output 的"调度层"。学习行为产生的产物去 raw/wiki/output,`learning/` 只存元信息(日志、复盘、评分、规则)。

### 3.2 vault 集成与代谢循环

```
        ┌──────────────────────────────────────────┐
        │           learning/(调度与记录)           │
        │  PLAYBOOK 决定怎么做,DASHBOARD 记录到几分 │
        └─────────────┬────────────────────────────┘
                      │ 调用 mode A-F
                      ▼
   ┌──────────────────────────────────────────────┐
   │              session 执行                    │
   │  在过程中产生:新素材/新概念/新综述/新决策    │
   └────────┬───────────┬───────────┬─────────────┘
            │           │           │
            ▼           ▼           ▼
   ┌────────────┐ ┌─────────┐ ┌──────────┐
   │  raw/      │ │  wiki/  │ │ output/  │
   │ 新素材入档  │ │新建/升级 │ │新综述报告 │
   └────────────┘ └─────────┘ └──────────┘
            │           │           │
            └───────────┴───────────┘
                        │ 反向反馈
                        ▼
              更新 DASHBOARD 客观指标
              (篇数 / stub 比 / 连接数 / output 引用)
```

**关键映射**:
- session 中**遇到新原始素材**(新文章、PDF、对话、观点) → 转 markdown 入 `raw/`,补 frontmatter
- session 中**产生新概念**或**对已有概念的更新** → 新建 stub 或升级到 wiki/(用户确认)
- session 中**产生综述、跨域分析、决策报告** → 入 `output/`,frontmatter `type: permanent` `tags` 加 `output`
- session 文件本身只是日志,**不是知识资产**;真正的资产在 raw/wiki/output

### 3.3 vault CLAUDE.md 集成

在 vault 根 CLAUDE.md 末尾加一段引导:Claude 检测到学习意图(关键词触发或用户主动开 session)时,先读 `learning/SYSTEM.md`,按系统流程执行,session 末尾自动判定产物去向。

## 4. 各组件详细设计

### 4.1 SYSTEM.md(入口)

职责:① 系统简介 ② 调用决策树 ③ 指向其他文件

调用决策树:
1. 用户表达学习意图 → 先读本文件
2. 识别意图属于 A-F 哪个 mode → 读 PLAYBOOK.md 对应章节
3. 若需要历史进度 → 读 DASHBOARD.md
4. 若用户问"上周学了什么" → 读 reviews/ 最新文件
5. 若用户说"改规则" → 提示需在月复盘中修订
6. session 末尾自动检查"本次产物清单",流向 raw/wiki/output

### 4.2 RULES.md(规则与边界)

**Claude 必须做**:
- 每次 session 开始前读 SYSTEM.md 和 PLAYBOOK.md 对应 mode
- 每次 session 结束写 sessions/ 文件,frontmatter 中包含 `vault_changes`
- **session 末尾强制做"产物归档判定"**:本次产生了哪些应入 raw/wiki/output 的内容?(新素材?新概念?新综述?)
- 提议归档时与用户确认,然后执行(或留到下次)
- session 末尾基于 DASHBOARD 给一句温和建议(可拒绝)
- 月复盘时强制修订 PLAYBOOK 至少一处

**Claude 不能做**:
- ❌ 主动施压(不催、不批评)
- ❌ 擅自启动 session(必须用户触发)
- ❌ 擅自改 wiki/ 内容(只读;升级/新建条目要用户确认)
- ❌ 擅自修改 raw/(用户原始素材的正文不修改,补 frontmatter 可以)
- ❌ 擅自修改 PLAYBOOK / RULES(必须经过月复盘)
- ❌ 同一建议重复推荐(被拒后 1 周内不再推)
- ❌ Mode 调用时绕过 PLAYBOOK 步骤(任意发挥)
- ❌ 让有价值产物只停在 sessions/ 而不入 vault 三层

### 4.3 PLAYBOOK.md(六种剧本)

每个剧本 6 要素:**触发词 / 输入 / 步骤 / sessions 输出 / vault 产物去向 / 时长**。

#### Mode A — 学科诊断

| 项 | 内容 |
|---|---|
| 触发词 | "诊断 [学科]"、"看看我 [学科] 到几分"、"扫描 [领域]" |
| 输入 | 学科名(12 学科之一或细分领域) |
| 步骤 | ① 统计篇数、stub 比、wikilinks 平均度 ② 找孤立节点(<2 引用)和热点(≥5 引用) ③ 按子主题识别盲区 ④ 生成"已掌握/薄弱/孤立/缺失"四类报告 ⑤ 用户对该学科 4 维度自评 1-5 ⑥ 客观与主观对比标注差距 ⑦ 给 2-3 个下一步建议 |
| sessions 输出 | `sessions/YYYY-WW-A-<学科>.md`(诊断报告 + 雷达评分 + 行动建议) |
| **vault 产物去向** | 发现的"缺失子主题"提议在 wiki/ 建 stub(用户确认);DASHBOARD 该学科 4 维度更新 |
| 时长 | 30-45 分钟 |

#### Mode B — 跨域综合

| 项 | 内容 |
|---|---|
| 触发词 | "把 X 和 Y 连起来"、"X 与 Y 的关系"、"综合 X Y" |
| 输入 | 2-3 个学科 / 概念 |
| 步骤 | ① 检索各方相关 wiki ② 找已有 wikilinks 连接 ③ 找隐藏连接(共享心智模型、相似机制、对偶关系) ④ 写综述 ⑤ 推荐相关 stub 升级 |
| sessions 输出 | `sessions/YYYY-WW-B-<topic>.md`(过程记录) |
| **vault 产物去向** | **综述写到 `output/<跨域主题>.md`**(主要产物);综述中提到的 vault 没有的概念 → wiki/ 建 stub |
| 时长 | 45-60 分钟 |
| 特性 | 产生 output/ 的主要 mode |

#### Mode C — 主题深读

| 项 | 内容 |
|---|---|
| 触发词 | "深入 [主题/概念]"、"全面理解 [X]" |
| 输入 | 1 个 wiki topic 或 concept |
| 步骤 | ① 读目标条目 + 入度/出度全部 wikilinks ② 整合多角度信息(raw/ 原始 + wiki/ 提炼,必要时 web 搜) ③ 生成"定义/历史/争议/应用/局限"五段分析 ④ 升级目标条目(stub→mature 时) ⑤ 用户确认后写入 wiki/ |
| sessions 输出 | `sessions/YYYY-WW-C-<topic>.md` |
| **vault 产物去向** | **升级 wiki/ 该条目**(主要产物);若引入新原始素材(网页/对话提取)→ 入 `raw/`;若派生横向综述 → `output/` |
| 时长 | 30-60 分钟 |

#### Mode D — 思维模型沙盒

| 项 | 内容 |
|---|---|
| 触发词 | "用模型分析"、"帮我决策"、"应该不应该 X" |
| 输入 | 真实决策、问题、情境 |
| 步骤 | ① 让用户描述决策 + 利益相关方 + 时间线 + 当前倾向 ② Claude 从 110+ 心智模型挑 3-5 个最相关 ③ 用每个模型分析此决策 ④ 综合多视角给决策建议 ⑤ 标注假设可能错的点 + 什么信号会反转判断 |
| sessions 输出 | `sessions/YYYY-WW-D-<decision>.md` |
| **vault 产物去向** | **决策分析报告写到 `output/decisions/<decision>.md`**(主要产物,含模型应用记录);决策中暴露的新概念 → wiki/ 建 stub;决策事后(如 1 月后)有反馈 → 更新该 output 文件,沉淀为反思案例库 |
| 时长 | 30-45 分钟 |

#### Mode E — stub 升级

| 项 | 内容 |
|---|---|
| 触发词 | "升级 stub"、"补 [概念]" |
| 输入 | 概念名(可选;默认 Claude 从 DASHBOARD 推荐高引用 stub) |
| 步骤 | ① 读 stub 当前内容 + 引用它的页面 ② 从 raw/ 找原始素材;若不足,web 搜补充 ③ 按 SCHEMA 重写为 mature ④ 加 wikilinks ⑤ 用户审阅后替换 wiki/ |
| sessions 输出 | `sessions/YYYY-WW-E-<concept>.md` |
| **vault 产物去向** | **wiki/ 升级**(主要产物);若 web 搜得到新文章/资料 → 入 `raw/<相应学科>/`;若发现该概念催生新概念 → 顺手建 stub |
| 时长 | 20-40 分钟 |

#### Mode F — 自由提问

| 项 | 内容 |
|---|---|
| 触发词 | 任何带"?"的问题、"我想问"、"如何理解" |
| 输入 | 问题 |
| 步骤 | ① 用 vault 知识回答(优先 wiki/) ② 延伸到 2-3 个相关条目 ③ 引导一个反问 |
| sessions 输出 | `sessions/YYYY-WW-F-<question>.md`(简版,300-500 字) |
| **vault 产物去向** | 如果回答中暴露 vault 缺失概念 → 提议建 stub;如果引出可拓展话题 → 提议下次开 B 或 C mode 跟进 |
| 时长 | 5-15 分钟 |
| 特性 | 日常激活机制,鼓励频繁使用 |

### 4.4 DASHBOARD.md(进度仪表盘)

**12 学科 × 4 维度 = 48 格,每格 1-5 分**

| 维度 | 客观指标(Claude 自动统计) | 主观评分(你打) | 1 分含义 | 5 分含义 |
|---|---|---|---|---|
| **Coverage 覆盖度** | 篇数 / 该学科预期总量 | 主要子领域涵盖几成 | 只接触少数核心 | 主要子领域基本覆盖 |
| **Depth 深度** | mature 占比、平均篇长 | 能讲清楚到几分 | 多 stub | 能写综述给别人看 |
| **Connectedness 连接度** | wikilinks 平均度、跨域桥接数 | 能跳到别的领域吗 | 孤立成块 | 自由跨学科联想 |
| **Application 应用度** | D mode 调用次数、output/ 引用次数 | 最近一月用过几次 | 纯阅读 | 日常应用 |

**全局健康指标**(DASHBOARD 顶部展示):

- vault 总篇数(raw / wiki / output 分别)
- stub 比例(目标:从当前 11.5% 持续下降)
- 月度 wiki 新增/升级数
- 月度 output 新增数
- wikilinks 总数与平均度
- 跨域桥接数

每月在月复盘时更新一次。客观与主观差距大就是盲点信号。

### 4.5 CHANGELOG.md(迭代记录)

格式:

```
## v0.11 — 2026-06-XX
- 修改:mode B 步骤增加"可视化连接图"输出
- 原因:本月 5 次 B mode,纯文字综述读起来吃力
- 触发者:月复盘
```

版本号策略:
- 初版 **v0.1**
- 月复盘修订 PLAYBOOK 一项 → +0.01 = v0.11
- 增减 mode 或重写 RULES → +0.1 = v0.2
- 架构重构 → +1.0 = v1.0

## 5. 文件格式规范

### 5.1 sessions/ 文件 frontmatter

```yaml
---
title: 2026-W19 A 模式 — 金融学诊断
mode: A
date: 2026-05-10
duration_min: 35
topic: 金融学
wikilinks_touched: [行为金融学, 投资组合理论, 资本结构]
self_rating: 4
vault_changes:
  raw_added: []                          # 新增 raw 文件路径
  wiki_added: []                         # 新建 wiki 条目
  wiki_updated: [stub→mature: 资本结构]   # 升级条目
  output_added: []                       # 新增 output 文件
follow_ups: [下次 C mode 深读"行为金融学"]
---
```

`self_rating` 1-5 用户在 session 末尾打。`vault_changes` 是代谢循环的可审计记录,每月汇总。

### 5.2 reviews/ 文件结构

**周复盘**(自动生成,你只读):
- 本周 session 数与 mode 分布
- **本周 vault 产物清单(raw/wiki/output 增量)**
- 涉及学科分布
- 一个亮点(最有创造性的连接/分析)
- 一个警惕(模式僵化、避难所)
- 下周 2-3 个建议

**月复盘**(对话形式):
- 本月 session 概览
- **本月 vault 代谢报告:raw 新增 N 篇 / wiki 新增 N 篇 / wiki 升级 N 篇 / output 新增 N 篇 / stub 比例变化**
- DASHBOARD 更新(用户重打分,Claude 提供客观对照)
- 三个反思问题:最有价值的 mode、最无聊的 mode、最强烈的方向
- **强制修订 PLAYBOOK 至少一处**
- CHANGELOG 写入

## 6. 复盘节奏

| 频率 | 谁主导 | 时长 | 产物 |
|---|---|---|---|
| 周复盘 | Claude(基于 sessions/ 自动汇总) | 15 分钟,你只读 | reviews/YYYY-WW-weekly.md |
| 月复盘 | 对话形式,你 + Claude 共评 | 30-45 分钟 | reviews/YYYY-MM-monthly.md + DASHBOARD 更新 + **PLAYBOOK 必改 ≥1 处** |

## 7. 实施分阶段

| 阶段 | 时间 | 内容 |
|---|---|---|
| **MVP** | 立刻 | 创建 5 个核心文件(SYSTEM/RULES/PLAYBOOK/DASHBOARD/CHANGELOG)+ sessions/ + reviews/ 空目录 + 在 vault CLAUDE.md 加引导 + 跑第一次 A mode 验证 |
| **首周** | 1 周内 | 跑 2-3 种不同 mode,确认剧本与 vault 代谢循环都通畅,第一次周复盘 |
| **首月** | 1 月内 | 第一次月复盘,触发首次迭代,v0.1 → v0.11 |
| **可选扩展** | 之后 | 月度主题、stub 自动推荐、计划任务 nudge 周复盘 |

## 8. 验收标准

**系统运转层面**:
- 系统建立后第一周内,能成功调用至少 3 种不同 mode
- 每次 session 都有 sessions/ 文件留档,frontmatter 完整(含 vault_changes)
- 第一个月内 DASHBOARD 至少更新 1 次
- 第一次月复盘后 CHANGELOG 至少有 1 条迭代记录
- vault 根 CLAUDE.md 引导段生效

**vault 代谢层面(更重要)**:
- 第一周内至少 1 项 vault 资产新增/更新(raw/wiki/output 任一)
- 第一月内 wiki 至少 1 篇升级或新建
- 第一月内 output 至少 1 篇产生(打破 output/ 全空状态)
- stub 比例月度统计可见,不再是黑盒

## 9. 已知风险与对策

| 风险 | 对策 |
|---|---|
| 用户觉得太繁琐放弃 | F mode 极轻(5 分钟);周复盘自动化用户只读 |
| Mode 越来越多失控 | 严格版本号策略,只在月复盘改 |
| sessions/ 堆积 | 每月归档,只保留近一月 active(机制留 v0.2) |
| 评估变成"刷分游戏" | 主观自评为准,客观数据只对照 |
| Claude 过度推荐打扰 | 温和推荐 1 句即可,被拒 1 周内不重推 |
| 系统文档自相矛盾 | CHANGELOG 是 single source of truth |
| **产物滞留 sessions/ 未入 vault** | **session 末尾强制"归档判定"步骤,frontmatter `vault_changes` 必填** |
| **wiki 写入污染** | 任何 wiki/ 写入必须用户明确确认;raw/ 正文不改,只补 frontmatter |
| **output 质量参差** | output/ 文件 frontmatter 加 `quality: draft / reviewed / canonical`,月复盘审视 draft 转化 |

## 10. 后续可扩展点(v0.2+)

1. **月度主题** — 用户可指定本月专注 X,Claude 在每次 session 优先围绕 X
2. **跨域自动推荐** — 基于 wikilinks 图谱主动建议未连接的高价值跨域
3. **stub 优先级算法** — 按 (引用度 × 学科评分弱) 自动排序
4. **学习时长追踪** — 每个 session 自动记录起止时间
5. **错题本 / 反思集** — D mode 决策事后复盘,沉淀为反思条目
6. **Obsidian 视图** — 用 dataview / bases 把 DASHBOARD 渲染为可视化
7. **季度大综述** — 三个月一次,把 output/ 中相关综述合并升级
8. **vault 体检** — 季度统计 stub/mature 比例变化、孤立节点变化、output 引用图

## 11. 设计决策依据

| 决策 | 依据 |
|---|---|
| 工具箱模式而非教练驱动 | 用户自驱性强(vault 规模),教练式会压抑 |
| 6 个 mode 全部保留 | 用户明确"全都想做",并入会损失颗粒度 |
| 系统放 vault 而非 ~/.claude/skills | 自包含 / git 追踪 / 与现有结构自洽 |
| **强制 vault 内循环代谢** | 用户明确要求"新知识/概念/成果加入 raw/wiki/output";否则 sessions/ 会变孤岛 |
| 强制月复盘必改 | Argyris double-loop:不质疑系统就僵化 |
| 4 维度评估 + 全局健康指标 | Bloom 多层 + 元认知细颗粒;全局指标看代谢健康 |
| 主观+客观双评分 | 防止刷分;差距本身是信号 |
| F mode 极轻量 | 留给"C 偶尔泛泛"的入口,不增加心智负担 |
| 不预设月度主题为强制 | 用户 B 偏好"无时间线",月度主题作为可选 |
| sessions/ 是日志,资产在 raw/wiki/output | 学习产物必须长期存活,日志可归档 |

## 12. 不在本设计范围(YAGNI)

- 不做用户认证 / 多用户(单人 vault)
- 不做 web UI(纯 markdown,Obsidian 渲染)
- 不做自动定时(v0.1 全靠用户触发,定时是 v0.2 可选)
- 不做与外部学习平台同步(vault 内闭环)
- 不做 AI 自动出题测验(超出脚手架边界,容易变教练式)
- 不重组现有 raw/ 子目录结构(保持已有路径)
- v0.1 不做自动归档 sessions/(等量积累后再设计)
