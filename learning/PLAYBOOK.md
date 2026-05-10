---
title: 学习辅助系统剧本(Playbook)
type: topic
tags: [meta, learning-system, playbook]
sources: [_design/2026-05-10-system-design.md]
created: 2026-05-10
updated: 2026-05-10
summary: 6 种学习模式(A-F)的详细执行剧本。每种 mode 含触发词、输入、步骤、sessions 输出、vault 产物去向、时长、不做的事、sessions 文件模板。
---

# PLAYBOOK

## 全局术语

| 术语 | 含义 |
|---|---|
| **mode** | A-F 六种学习模式之一 |
| **session** | 一次完整的学习会话(从用户触发到 Claude 写完 sessions 文件) |
| **sessions log** | `sessions/YYYY-WW-<mode>-<topic>.md`,日志,不是知识资产 |
| **vault_changes** | sessions frontmatter 字段,记录本次给 raw/wiki/output 添了什么 |
| **产物归档判定** | session 末尾必做:列出本次产生的内容,确定流向 raw/wiki/output |
| **温和建议** | session 末尾一句话(≤30 字),基于 DASHBOARD,可拒绝 |

## sessions 文件 frontmatter 通用模板

```yaml
---
title: <YYYY-WW> <mode> 模式 — <topic>
mode: <A|B|C|D|E|F>
date: YYYY-MM-DD
duration_min: <实际耗时,整数>
topic: <学科/概念/决策>
wikilinks_touched: [概念1, 概念2, ...]
self_rating: <1-5,session 末尾用户打>
vault_changes:
  raw_added: []                   # 新增 raw 文件路径列表
  wiki_added: []                  # 新建 wiki 条目列表
  wiki_updated: []                # 升级条目(stub→mature)列表
  output_added: []                # 新增 output 文件列表
follow_ups: []                    # 下次想做的延伸
---
```

---

## Mode A — 学科诊断

### 触发词
- "诊断 [学科]"、"看看我 [学科] 到几分"、"扫描 [领域]"、"[学科] 评估"

### 输入
- **学科名**:必须是 12 学科之一(计算机/营销/金融/商业/思维模型/AI/哲学/经济/心理/英语/工具生活/会计)或细分领域

### 步骤

1. **统计该学科 wiki 现状**
   - 用 Glob 列出 `wiki/concepts/<相关名>*.md` 与 `wiki/topics/<相关名>*.md`
   - 学科关键词举例:
     - 金融 → 货币、利率、资本、债券、股票、金融、汇率、银行、保险、投资...
     - AI → AI、人工智能、机器学习、深度学习、LLM、神经网络、Transformer...
     - 哲学 → 哲学、形而上学、认识论、伦理、辩证、本体...
   - Grep frontmatter 中 `(stub)` 或 tag `#stub`,数 stub 频次
   - Grep 该学科条目被多少 [[wikilink]] 引用(入度)

2. **分类四类报告**
   - **已掌握**:mature 且被引用 ≥ 3
   - **薄弱**:stub 但被引用 ≥ 2(高需求未升级)
   - **孤立**:mature 但被引用 ≤ 1(可能命名不规范或主题边缘)
   - **缺失**:对照 `wiki/PROGRESS.md` 该学科子主题清单,wiki 实际没有的

3. **让用户对该学科 4 维度自评 1-5**
   - 给参考锚点而非空打分:
     - "你能给同事讲清楚哪些子领域?(Coverage)"
     - "你能写一篇 1000 字的小综述吗?(Depth)"
     - "这个领域和别的领域的连接你能说几对?(Connectedness)"
     - "最近 1 个月你用这个领域的概念分析过具体问题吗?(Application)"

4. **客观 vs 主观对比**
   - 用表格列差距,标注盲点信号(差距 ≥ 2 分的格)

5. **给 2-3 个下一步建议**
   - 优先级排序,每个建议关联具体 mode
   - 例:"建议下次跑 E mode 升级 [stub 名]"、"或 D mode 用 [概念] 分析最近一个决策"

6. **更新 DASHBOARD**
   - 该学科一行的客观字段(篇数、stub 比、平均度)
   - 主观字段写入用户当次自评

### sessions 输出
- 文件名:`sessions/YYYY-WW-A-<学科>.md`
- 内容含:四类报告、雷达评分(客观+主观)、差距标注、下一步建议清单

### vault 产物去向
- **该学科 DASHBOARD 行更新**(主要)
- 发现的"缺失子主题" → 提议在 `wiki/` 建 stub(用户确认)
- **不擅自升级 stub**,只标识(若要升级,改下次开 E mode)

### 时长
- 30-45 分钟

### 不做
- 不擅自升级 stub
- 不擅自建 wiki 条目
- 不脱离客观数据空打分
- 不在一次诊断中改超过 1 个学科

### sessions 模板示例

```yaml
---
title: 2026-W19 A 模式 — 金融学诊断
mode: A
date: 2026-05-10
duration_min: 35
topic: 金融学
wikilinks_touched: [行为金融学, 投资组合理论, 资本结构, 货币政策]
self_rating: 4
vault_changes:
  raw_added: []
  wiki_added: []
  wiki_updated: []
  output_added: []
follow_ups: [E 模式升级"资本结构"和"货币政策"两个高引用 stub]
---
```

---

## Mode B — 跨域综合

### 触发词
- "把 X 和 Y 连起来"、"X 与 Y 的关系"、"综合 X Y"、"打通 X 和 Y"

### 输入
- **2-3 个学科或概念**(必须明确,模糊则问用户细化)

### 步骤

1. **检索三方相关条目**
   - 对 X、Y(可 Z)分别 Glob `wiki/**/*<关键词>*.md`
   - 列出每方的代表性条目 5-10 个

2. **找已有 X-Y 直接连接**
   - Grep `[[X 概念]]` 在 Y 学科条目中的出现
   - 反向再来一次

3. **找隐藏连接**
   - **共享心智模型**:两边都引用同一心智模型(如 X 用了`激励理论`,Y 也用了)
   - **相似机制**:不同领域的同构机制(经济泡沫 vs 心理传染、热力学熵 vs 信息熵)
   - **对偶/反例**:X 是 Y 的反面或互补(理性 vs 直觉、个体 vs 群体)
   - **历史共享**:同一时代背景影响两个领域(战后 vs 行为经济学诞生)

4. **写综述到 output/**
   - 文件:`output/<X-与-Y>.md`(中文连接符)
   - 结构:
     1. 概述(本文要打通什么)
     2. 各方理解(X 的视角、Y 的视角各 1-2 段)
     3. 桥接点(2-4 个,每个 1 段)
     4. 综合启示
     5. 引用 wiki 清单(用 wikilinks)
   - frontmatter:`type: permanent`、`tags: [output, ...]`

5. **推荐 stub 升级**
   - 综述中提到 vault 没有或太薄的概念 → 列"建议建 stub / 升级"清单
   - 询问用户要不要顺手做(或留下次开 E mode)

6. **更新 DASHBOARD**
   - X、Y 学科 Connectedness 客观值 +1(若有跨域桥接新增)
   - 跨域桥接对总数 +1

### sessions 输出
- 文件:`sessions/YYYY-WW-B-<X-Y>.md`
- 简版,主要内容已在 output/

### vault 产物去向
- **`output/<X-与-Y>.md`**(主要产物)
- 综述中暴露的 stub 缺失 → 提议建立(用户确认)
- 若 web 搜引入新原始素材 → 入 raw/

### 时长
- 45-60 分钟

### 不做
- 不写没有具体桥接点的"水综述"(必须 2-4 个具体桥接)
- 不引用 vault 没有的概念却不建 stub(留 dangling reference)
- 不在一次 session 跨 4 个以上学科(摊薄)

### sessions 模板示例

```yaml
---
title: 2026-W19 B 模式 — 金融与心理学
mode: B
date: 2026-05-11
duration_min: 55
topic: 金融与心理学
wikilinks_touched: [行为金融学, 前景理论, 损失厌恶, 心理账户, 投资组合理论]
self_rating: 5
vault_changes:
  raw_added: []
  wiki_added: [前景理论, 心理账户]
  wiki_updated: []
  output_added: [output/金融与心理学的深度交叉.md]
follow_ups: [C 模式深读"行为金融学"]
---
```

---

## Mode C — 主题深读

### 触发词
- "深入 [主题/概念]"、"全面理解 [X]"、"读透 [X]"

### 输入
- **1 个 wiki topic 或 concept 名**

### 步骤

1. **读目标条目**
   - Read `wiki/concepts/<X>.md` 或 `wiki/topics/<X>.md`
   - 看现状:是 stub 还是 mature?frontmatter 是否完整?

2. **读入度 wikilinks**
   - Grep `[[X]]` 全 vault,Read 每个引用页(理解 X 怎么被使用)

3. **读出度 wikilinks**
   - 列出 X 内含的 [[Y]]、[[Z]],必要时 Read 它们

4. **从 raw/ 找原始素材**
   - Glob `raw/**/*<X>*.md`,列原始素材
   - Read 几个最相关的

5. **必要时 web 搜补充**
   - WebSearch / WebFetch 找权威定义、最新发展、重要争议
   - 新素材转 markdown 入 raw/<对应学科>/<X>-补充.md(补 frontmatter)

6. **生成 5 段分析**
   1. **定义**:X 是什么(2-3 句)
   2. **历史**:谁提出、何时、什么背景
   3. **争议**:不同学派/视角的分歧
   4. **应用**:在哪些场景中起作用、有什么实例
   5. **局限**:边界、失效条件、批评

7. **升级目标条目(若是 stub)**
   - 用 5 段分析重写,符合 SCHEMA.md
   - 加 wikilinks(凡提到的已有 wiki 概念)
   - 用户审阅后 Write 替换;不审阅则只写 sessions/不动 wiki

8. **更新 DASHBOARD**
   - 该学科 Depth 客观值 +1(stub→mature)
   - 全局 stub 比例自动下降

### sessions 输出
- 文件:`sessions/YYYY-WW-C-<X>.md`
- 含:5 段分析草稿、引用源清单、升级前后对比

### vault 产物去向
- **升级后的 wiki/<X>.md**(主要产物,用户确认)
- 若 web 搜引入新原始素材 → 入 raw/
- 若派生横向综述 → 可选写到 output/

### 时长
- 30-60 分钟

### 不做
- 不擅自改 wiki(必须用户确认)
- 不删除目标条目原有内容(只增不减,除非用户明确说删)
- 不脱离 SCHEMA.md(中文优先、扁平结构、术语一致)
- 不无限拉长(超过 60 分钟应停下来,留下次再做)

### sessions 模板示例

```yaml
---
title: 2026-W19 C 模式 — 深读"行为金融学"
mode: C
date: 2026-05-12
duration_min: 50
topic: 行为金融学
wikilinks_touched: [前景理论, 损失厌恶, 心理账户, 锚定效应, 卡尼曼]
self_rating: 4
vault_changes:
  raw_added: [raw/金融学/行为金融学-Kahneman-访谈摘录.md]
  wiki_added: []
  wiki_updated: [行为金融学(stub→mature)]
  output_added: []
follow_ups: [B 模式打通"行为金融学 × 营销心理学"]
---
```

---

## Mode D — 思维模型沙盒

### 触发词
- "用模型分析"、"帮我决策"、"应该不应该 X"、"这个决定怎么办"

### 输入
- **真实决策、问题、情境**(不能是假设性问题)

### 步骤

1. **让用户描述决策**
   - 必要 4 项,缺则补问:
     1. **决策内容**:有哪些选项?
     2. **利益相关方**:决策影响谁?
     3. **时间线 / 不可逆程度**:多久要决定?决定后能改吗?
     4. **当前倾向**:你现在更倾向哪个?为什么?

2. **挑 3-5 个最相关的心智模型**
   - 优先候选(默认从这里挑):
     - **逆向思维** — 反问"什么会保证失败?"
     - **二阶思维** — 后果之后果是什么?
     - **概率思维** — 各选项的成功概率分布?
     - **机会成本** — 为什么不选 B?
     - **安全边际** — 最差情况能承受吗?
     - **能力圈** — 这件事在你理解的圈内吗?
   - 决策领域专属(按需补):
     - 投资 → `投资组合理论`、`基本面分析`、`行为金融学`
     - 职业 → `复利效应`、`生态位`、`马太效应`
     - 产品 → `4P`、`STP`、`价值主张`、`竞争壁垒`
     - 人际 → `互惠原则`、`激励偏差`、`基本归因错误`

3. **对每个模型逐一分析**
   - **A** 简述模型核心(1 句话)
   - **B** 用模型分析此决策
   - **C** 该模型视角下的建议(可能与其他模型矛盾,这是好事)

4. **综合多视角**
   - 列出各模型给出的建议
   - 矛盾处用"权衡"结构:"如果你更看重 X,选 A;如果你更看重 Y,选 B"
   - 给最终建议(用户当下情境最匹配的)

5. **关键产出(强制)**
   - **"假设可能错的点"**:这个建议依赖哪些前提假设?
   - **"什么信号会让你反转判断"**:Bayesian 视角,什么新证据会让你换决定?
   - 这两点是 D mode 的核心价值,缺则不算完成

6. **写到 output/decisions/**
   - 文件:`output/decisions/<decision-name>.md`
   - 文末留"事后复盘"段(空),1 个月后回填实际结果

7. **更新 DASHBOARD**
   - 涉及学科的 Application 客观值 +1
   - output 篇数 +1

### sessions 输出
- 文件:`sessions/YYYY-WW-D-<decision>.md`
- 简版,主要决策报告在 output/

### vault 产物去向
- **`output/decisions/<decision>.md`**(主要产物)
- 决策中暴露的新概念 → wiki/ 建 stub
- 1 月后事后复盘 → 更新该 output 文件,沉淀为反思案例库

### 时长
- 30-45 分钟

### 不做
- 不分析"假设性"决策(用户必须有真实情境)
- 不替用户决定(给视角不给答案)
- 不跳过"假设可能错的点"和"反转信号"两个强制项
- 不混入 D 之外的目的(诊断学科应是 A,综合应是 B)

### sessions 模板示例

```yaml
---
title: 2026-W19 D 模式 — 工作 offer 决策(留 vs 跳)
mode: D
date: 2026-05-13
duration_min: 40
topic: 工作 offer 决策
wikilinks_touched: [机会成本, 二阶思维, 复利效应, 生态位, 安全边际]
self_rating: 5
vault_changes:
  raw_added: []
  wiki_added: []
  wiki_updated: []
  output_added: [output/decisions/2026-05-job-offer-decision.md]
follow_ups: [1 月后事后复盘]
---
```

---

## Mode E — stub 升级

### 触发词
- "升级 stub"、"补 [概念]"、"让 [概念] 变 mature"

### 输入
- **概念名**(可选;不指定则 Claude 推荐)

### 步骤

1. **若用户没指定 stub**
   - 从 DASHBOARD 全 vault 健康指标拉 stub 列表
   - 推荐 3 个高引用 stub(被 [[]] 引用次数最多的)
   - 让用户挑

2. **Read 该 stub 现状**
   - 读 frontmatter + 正文
   - 看 summary 与现有内容是否一致

3. **Grep 入度引用,Read 全部**
   - 找出哪些页面在用这个概念
   - 它们对这个概念的"期待"是什么?(语境暗示了内容方向)

4. **Glob raw/ 找原始素材**
   - `raw/**/*<concept>*.md`
   - Read 最相关的几篇,提炼核心

5. **必要时 web 搜补**
   - 若 raw/ 不够,WebSearch 找权威定义和当代发展
   - 新素材入 raw/

6. **按 SCHEMA 重写**
   - 概念页结构:**定义 → 核心要点 → 和其他概念的关系 → 参考源**
   - 加 wikilinks(凡提到的已有 wiki 概念)
   - frontmatter `tags` 去掉 `stub`,加 `mature`(若有 status tag)
   - summary 重写,30-80 字

7. **用户审阅后 Write 替换**

8. **更新 DASHBOARD**
   - 该学科 Depth 客观值 +1
   - 全局 stub 比例 -0.1%(如有)

### sessions 输出
- 文件:`sessions/YYYY-WW-E-<concept>.md`
- 含:升级前后对比、引用源、wikilinks 改动清单

### vault 产物去向
- **升级后的 `wiki/<concept>.md`**(主要产物)
- 若 web 搜引入新原始素材 → 入 raw/<对应学科>/
- 若该 stub 升级过程中发现新概念 → 顺手建 stub(用户确认)

### 时长
- 20-40 分钟

### 不做
- 不擅自改 wiki(必须用户确认)
- 不仅仅扩字数(必须有"定义、核心、关系、源"四件)
- 不忽略入度引用上下文(否则升级版可能不匹配既有引用)

### sessions 模板示例

```yaml
---
title: 2026-W19 E 模式 — 升级"资本结构"stub
mode: E
date: 2026-05-14
duration_min: 30
topic: 资本结构
wikilinks_touched: [资本成本, 资本结构理论, MM定理, 优序融资理论]
self_rating: 4
vault_changes:
  raw_added: []
  wiki_added: []
  wiki_updated: [资本结构(stub→mature)]
  output_added: []
follow_ups: []
---
```

---

## Mode F — 自由提问

### 触发词
- 任何带"?"或"?"的问题
- "我想问"、"如何理解"、"帮我想想"
- 用户疑惑陈述句:"我搞不懂 X"、"X 怎么那么 Y"

### 输入
- **任何问题**(无格式要求)

### 步骤

1. **用 vault 知识回答**
   - 优先 Glob/Grep 在 `wiki/` 找直接相关条目
   - 若 wiki 没有 → Glob `raw/`
   - 若都没有 → 直接答(标注"vault 暂无相关条目")

2. **延伸 2-3 个相关条目**
   - 用 wikilinks 形式列出,简短解释每个跟问题的关系
   - 鼓励用户继续点进去(下次就近开 C 或 B mode)

3. **引导一个反问**
   - "这让你想到 vault 里的什么?"
   - 或:"如果换个视角(用 [心智模型 X])怎么看?"
   - 反问是为了激活元认知,不是考用户

4. **写 sessions(简版)**
   - 300-500 字,主要记问题 + 答案要点 + 延伸链接
   - 不要写得跟 C mode 一样长

5. **若回答中暴露 vault 缺失**
   - 提议下次开 B/C/E mode 跟进
   - 例:"vault 里'第二大脑方法论'是 stub,要不下次 E mode 升级它?"

### sessions 输出
- 文件:`sessions/YYYY-WW-F-<question-keyword>.md`
- 简版,300-500 字

### vault 产物去向
- 通常 F 不直接产生 vault 资产
- 但常 trigger 下次 B/C/E:**这是 F 的主要价值**——把模糊好奇心引到具体 mode

### 时长
- 5-15 分钟

### 不做
- 不把 F 跑成 C(超过 15 分钟应该升级到 C/E)
- 不无引用空答(必须挂 wikilinks)
- 不省略反问(F 的核心机制)

### sessions 模板示例

```yaml
---
title: 2026-W19 F 模式 — 为什么 LLM 有涌现能力
mode: F
date: 2026-05-10
duration_min: 10
topic: LLM 涌现能力
wikilinks_touched: [涌现能力, Transformer, 大语言模型, 临界质量]
self_rating: 3
vault_changes:
  raw_added: []
  wiki_added: []
  wiki_updated: []
  output_added: []
follow_ups: [C 模式深读"涌现能力"]
---
```

---

## 冲突与歧义处理

### 触发词冲突

常见模糊场景:

| 用户说 | 可能的 mode | 判定 |
|---|---|---|
| "深入金融学" | A 还是 C? | "金融学"是学科 → A;若改"深入金融衍生品"(单一概念)→ C |
| "金融与心理学的关系" | B 还是 C(深入"金融与心理学"这个 topic)? | 已有 wiki/topics/金融与心理学.md → C;若 topic 不存在 → B 重新综合 |
| "我想学 AI" | A 还是无? | 太宽泛,先 A 诊断 AI 学科;太宽则问用户具体想从哪入手 |
| "怎么看 X" | F 还是 D? | F 是知识问题(怎么理解 X);D 是行动问题(我该不该 X) |

### 判定原则

1. **单一概念/topic + "深入/全面"** → C
2. **单一学科 + "诊断/扫描/到几分"** → A
3. **多个概念/学科 + "关系/连接/综合"** → B
4. **真实决策 + "应不应该/帮我想"** → D
5. **stub 维护 + "升级/补"** → E
6. **疑问句、模糊好奇** → F

### 不要中途换车

- 一旦开始 mode N,不在执行中途切换到 mode M
- 若发现 mode 选错了:正常结束当前 session(可写"未完成,本周内重开")
- 下一轮重开时再用对的 mode

### 不要混合 mode

- 一次 session 只跑一个 mode
- 即使有"顺手做"的诱惑,也只在 sessions 末尾的"温和建议"里提议下次

---

## PLAYBOOK 自身的修改

PLAYBOOK 是月复盘的主要修订对象。

- **每月 ≥1 处修订**(强制,不修则系统僵化)
- 修订必须写入 `CHANGELOG.md`
- 版本号:小调(增删步骤、调整时长)+0.01;增删 mode 或重写章节 +0.1

修订触发:
- 月复盘讨论
- 用户在某次 session 后说"这个剧本步骤 X 不好用"(即时反馈,但仍走流程)
- 多次 session 同一处卡壳(数据驱动)
