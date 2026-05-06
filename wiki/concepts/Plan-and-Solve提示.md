---
title: Plan-and-Solve提示
type: concept
tags: [ai, mature]
sources: [raw/提示词工程/04-进阶优化/高级技术, raw/提示词工程/03-应用实践/高级技巧/03-2-2-复杂任务分解.md]
created: 2026-05-05
updated: 2026-05-05
summary: Plan-and-Solve(Wang 等 2023)是 CoT 的两阶段升级,先让 LLM 制定计划再分步执行,显著改善复杂多步推理任务的可靠性,是计划驱动的提示工程范式。
---

# Plan-and-Solve提示

## 定义

**Plan-and-Solve Prompting**(P-and-S, Wang 等 **2023** 论文《Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models》)是 [[思维链]](CoT)的两阶段升级范式,核心是**让 LLM 在推理前先制定一个高层"计划",然后按计划分步执行**。它解决了普通 CoT 在复杂多步问题上"边想边迷路"的问题,通过显式规划让推理更连贯、更可靠。它是计划驱动(plan-driven)提示工程的代表方法,也是许多 [[AI Agent]] 的基础结构。

## 核心要点

### 与普通 CoT 的对比

| 维度 | 标准 CoT | Plan-and-Solve |
|---|---|---|
| 阶段 | 1 步:边想边算 | 2 步:先计划,再执行 |
| 提示语 | "Let's think step by step" | "Let's first plan, then solve" |
| 可控性 | 低 | 高(计划可被检视) |
| 长任务 | 易迷路 | 较稳健 |
| 成本 | 1× | 略高(更长输出) |

### 经典 Prompt 模板

#### 零样本版本(P-and-S Zero-Shot)

```
[问题]: {problem}

让我们先理解问题并设计解决方案的步骤,
然后按步骤一一执行,最终得到答案。

Plan:
1. ...
2. ...

Solving according to the plan:
Step 1: ...
Step 2: ...

Answer: ...
```

#### P-and-S+(增强版)

加入对计算细节的明确指导:

```
让我们先理解问题:
1. 列出已知条件
2. 列出待求量
3. 设计求解步骤

然后按计划求解,注意:
- 计算时显示中间结果
- 单位要保持一致
- 检查每步的合理性
```

### 实证效果

Wang 等 2023 在 GSM8K、SVAMP、MultiArith、AQuA、CSQA、StrategyQA 等基准上测试 GPT-3:

| 任务 | 标准 CoT | Plan-and-Solve | 提升 |
|---|---|---|---|
| GSM8K | 56.4% | 58.2% | +1.8 |
| SVAMP | 64.5% | 65.6% | +1.1 |
| MultiArith | 88.5% | 91.3% | +2.8 |
| AQuA | 35.4% | 37.7% | +2.3 |

P-and-S+ 进一步提升 1-3pp。整体效果优于普通 CoT,但不如 [[自一致性]] + CoT 投票。

### 为何有效

理论解释:
1. **元认知分离**:计划是"思考如何思考",降低执行时的认知负担
2. **结构化推理**:计划提供"骨架",防止偏题
3. **错误隔离**:计划错与执行错可分别诊断
4. **可中断与回顾**:计划是"checkpoint",可以反思
5. **类似人类专家行为**:专家解题前先想方法

### 主要变体

#### 1. 显式计划与执行分离(Multi-shot)

把计划与执行作为两次独立的 LLM 调用:

```python
# 第一次调用:生成计划
plan = llm.generate(f"Plan to solve: {question}\n\nSteps:")

# 第二次调用:按计划执行
answer = llm.generate(f"Question: {question}\n\nPlan: {plan}\n\nExecute:")
```

优点:计划可被人类审查、修改、重用。
缺点:多一次 LLM 调用。

#### 2. ReAct + Plan-and-Solve

在 [[ReAct提示]] 框架内加入显式计划:
- 先生成 Action Plan(整体)
- 然后逐步执行(每步可调工具)
- 失败时重新规划

LangChain 的 Plan-and-Execute Agent 是典型实现。

#### 3. Tree-of-Thoughts 视角

[[思维树]] 可视为 Plan-and-Solve 的分支版本:
- ToT 生成多个候选计划
- 评估筛选后执行
- 适合不确定性高的任务

#### 4. Reflexion 反馈

执行失败 → 反思 → 修改计划 → 重试,详见 [[Reflexion]]。

### 适用任务

**适合**:
- 复杂多步推理(数学题、逻辑题)
- 多模块工作流(代码 → 测试 → 部署)
- 项目规划(写论文、产品发布)
- 需要权衡多个因素的决策
- Agent 任务(多步操作)

**不适合**:
- 简单问答
- 创意写作(规划反而僵化)
- 反应速度要求高的对话
- 不确定性极大的探索任务(更适合 ToT)

### 工程实践

#### Prompt 设计要点

1. **明确"先计划"**:用清晰指令分离两阶段
2. **规定计划结构**:编号步骤、关键里程碑
3. **明确"执行规则"**:遵循计划但不僵化
4. **预留"修正机制"**:发现计划错误时如何处理

#### 计划质量评估

- 步骤是否覆盖全部子任务
- 步骤是否合理可行
- 步骤间逻辑是否清晰
- 计划是否可执行(资源、时间、能力)

#### 与 CoT 的组合

Plan-and-Solve + CoT 内嵌每步:
```
Plan:
1. 计算 A
2. 用 A 算 B
3. 用 B 算 C

Step 1: A = ...(详细推理)
Step 2: B = A × ...
Step 3: C = B + ...
```

### 与人类规划的类比

教育心理学的"元认知策略":
- **计划(Planning)**:理解任务、设定目标、选择策略
- **监控(Monitoring)**:执行中检查进度
- **评估(Evaluating)**:回顾结果与改进

Plan-and-Solve 是其中"计划"阶段的 LLM 化。

### 局限

- **计划的"好"难定义**:同一问题多种合理计划
- **计划僵化**:严格按计划可能错过更好路径
- **依赖任务可分解性**:复杂任务分解本身困难
- **额外 token 成本**:计划部分本身耗 token
- **不一定优于 SC**:[[自一致性]] 投票常更高效

### 现代落地

- **LangChain Plan-and-Execute Agent**
- **AutoGPT**:核心是"任务列表 + 顺序执行"的简化 P-and-S
- **Anthropic Claude with task lists**:在长任务中常隐式 P-and-S
- **OpenAI o1 / Gemini reasoning**:内含计划 + 执行的更精细机制

### 主要批评

- **过度结构化**:对自由思考反而束缚
- **计划阶段错误传播**:差计划 → 差执行
- **多轮决策易累积错误**:每步都用 LLM,错误率乘积
- **被更先进方法部分取代**:ToT、Reflexion、o1 等

但作为简单、易实施的提升 CoT 可靠性的技巧,Plan-and-Solve 仍是工程师常用工具。

## 和其他概念的关系

Plan-and-Solve 是 [[思维链]](CoT)的两阶段升级,与 [[自一致性]] 在"提升 CoT"路径上互补——SC 是多采样投票,P-and-S 是结构化分阶段。它与 [[ReAct提示]] 在 Agent 中常组合(Plan-and-Execute Agent)。它与 [[思维树]] 在"显式规划"思想上相通,但 ToT 是树搜索,P-and-S 是线性两阶段。它与 [[Reflexion]] 在"失败后修正"上互补——Reflexion 在多轮间反思,P-and-S 在单轮内规划。它属于 [[提示词工程方法论]] 中"任务分解"原则的具体技术。

## 参考源

- raw/提示词工程/04-进阶优化/高级技术
- raw/提示词工程/03-应用实践/高级技巧/03-2-2-复杂任务分解.md
