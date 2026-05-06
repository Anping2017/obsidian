---
title: ReAct提示
type: concept
tags: [ai, mature]
sources: [raw/提示词工程/04-进阶优化/高级技术/04-1-1-提示词链式设计.md, raw/提示词工程/03-应用实践/高级技巧]
created: 2026-05-05
updated: 2026-05-05
summary: ReAct(Reasoning + Acting)由 Yao 等 2022 提出,让 LLM 交替输出"思考"与"行动",通过工具调用与外部反馈解决推理与现实知识获取的结合问题,是 LLM Agent 的基础范式。
---

# ReAct提示

## 定义

**ReAct**(Reasoning + Acting)是 **Shunyu Yao** 等人在 **2022 年** 论文《ReAct: Synergizing Reasoning and Acting in Language Models》中提出的提示工程范式,核心是**让 LLM 在生成回答时交替输出 "Thought(思考)" 与 "Action(行动)" 两类内容**,行动可以是调用外部工具(搜索、计算器、数据库),从环境获得 "Observation(观察)",再继续思考下一步。它是当前 [[AI Agent]] 的基础范式,也是 LangChain、AutoGPT 等框架的核心模式。

## 核心要点

### 三元结构

每一步都遵循 **Thought → Action → Observation** 循环:

```
Thought 1: 我需要找出 ABC 公司的市值
Action 1: search("ABC公司 市值")
Observation 1: ABC公司2024年市值约为3000亿美元

Thought 2: 现在我需要确认这个数据是当前的
Action 2: search("ABC公司 最新市值 2024")
Observation 2: 2024年12月最新数据为3200亿美元

Thought 3: 我得到了准确数据,可以回答了
Action 3: finish("ABC公司当前市值约3200亿美元")
```

### 与 CoT 的对比

| 维度 | [[思维链]](CoT) | ReAct |
|---|---|---|
| 输出 | 仅文字推理 | 推理 + 工具调用 |
| 知识 | 仅靠模型内部 | 可访问外部工具/数据 |
| 错误 | 推理错难纠正 | 工具反馈可纠正 |
| 适合 | 数学、逻辑 | 需要现实信息、操作 |
| 风险 | 幻觉 | 工具调用失败 |

ReAct 实质是把 CoT 扩展到"可验证、可修正、可工具使用"的范式。

### 经典工具集

ReAct 通常配以工具:
- **搜索引擎**:Google、Bing API
- **维基百科**:获得结构化事实
- **计算器 / Python REPL**:精确计算
- **数据库 / SQL**:结构化数据查询
- **API 调用**:天气、地图、票务
- **文件 / RAG**:本地知识库
- **代码执行**:复杂计算与图表
- **浏览器**:多步网页交互

### 与函数调用(Function Calling)的关系

OpenAI、Anthropic 等模型原生支持**函数调用(Function Calling)**:
- 模型直接输出 JSON 描述要调用的函数与参数
- 比文本格式的 ReAct 更稳定
- 但内部逻辑仍是 ReAct 模式

**Function Calling 是 ReAct 的工程化产品形态**。

### Prompt 模板

经典 ReAct prompt:

```
你是一个能调用工具的助手。可用工具:
- search(query): 搜索网络
- calculator(expression): 计算数学表达式
- finish(answer): 提交最终答案

按以下格式工作:
Thought: 你的思考
Action: tool_name(args)
Observation: 工具返回结果
... (重复)
Thought: 我有答案了
Action: finish(最终答案)

问题: {user_question}
```

### 主要变体

**1. Plan-and-Solve / Plan-Act**:先生成计划,再执行
- 适合长 horizon 任务
- 减少中途偏移

**2. Reflexion**(Shinn et al., 2023):
- 失败后让模型反思,生成"教训"
- 加入下一轮 prompt
- 详见 [[Reflexion]]

**3. Tree-of-Thoughts**(Yao et al., 2023):
- 多分支推理,搜索式
- 详见 [[思维树]]

**4. Chain-of-Tools**:
- 多步工具调用串联
- 中间结果作为下一步输入

**5. ReWOO**:
- 把推理与工具调用分阶段,减少 token

### 实战注意

- **避免循环**:模型可能反复调用同一工具,需要循环检测
- **token 成本**:每次调用都附上历史 → 上下文长
- **工具失败处理**:rate limit、超时、参数错误
- **错误纠正**:让模型读到 Observation 后判断是否需要重试
- **输出长度**:Action 可能输出超长 query,需限制

### 经典应用

- **AutoGPT(2023)**:首个引爆的 ReAct agent
- **LangChain Agent**:工程化 ReAct 框架
- **Devin / Cursor**:代码 agent 的核心
- **客服 / 票务 / 旅行助手**:多工具协同
- **数据分析 agent**:SQL + Python + 报表

### 主要挑战

- **可靠性**:成功率随步骤数指数下降
- **成本**:每步 LLM 调用,长任务昂贵
- **解释性**:多步推理难复盘
- **安全**:不当工具调用(执行错误代码、误删除数据)
- **评估**:任务成功率 vs 步骤效率

### 现代发展

- **专门 agent 模型**:Anthropic Claude with computer use、GPT-4o agentic、Gemini Code Assist
- **工具学习(Tool Learning)**:更原生的工具调用训练
- **多模态 ReAct**:加入视觉(截图、图表)
- **multi-agent ReAct**:多个 agent 协作

## 和其他概念的关系

ReAct 是 [[AI Agent]] 的核心范式,扩展自 [[思维链]](CoT)。它与 [[少样本提示]] 兼容(few-shot ReAct examples),与 [[结构化输出]] 配合用 JSON Action。它是 [[Function Calling]] 的概念前身。它支撑 [[Reflexion]]、[[思维树]]、Plan-and-Solve 等更高级范式。在工程化上,它依赖 [[提示词工程方法论]] 中的迭代设计原则。它直接关联 [[大语言模型应用栈]] 中的 "Tool / Agent" 层。在安全上,与 [[提示注入]] 的边界是同一议题——工具调用是注入风险新接口。

## 参考源

- raw/提示词工程/04-进阶优化/高级技术/04-1-1-提示词链式设计.md
- raw/提示词工程/03-应用实践/高级技巧/03-2-2-复杂任务分解.md
