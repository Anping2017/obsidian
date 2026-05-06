---
title: AI Agent框架
type: concept
tags: [ai, programming, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: 帮助开发者构建基于大语言模型的自主智能代理的开发框架,主流包括 LangChain、LlamaIndex、AutoGen、CrewAI 等,形态从工具链到多智能体系统。
---

# AI Agent框架

## 定义

**AI Agent 框架**(AI Agent Frameworks)是帮助开发者构建基于 [[大语言模型]] 的**自主智能代理系统**的开发框架。它们封装 LLM 调用、工具调用、记忆管理、多步规划、状态管理等通用能力,使开发者能聚焦业务逻辑而非底层细节。

主流框架可按"复杂度梯度"排列:**LangChain**(组件库)→ **LlamaIndex**(检索专精)→ **AutoGen**(多 Agent 协作)→ **CrewAI**(角色编排)→ **LangGraph**(状态机)。

## 核心要点

### 主流框架对比

#### 1. LangChain(2022 年 10 月开源)

- 最流行的 LLM 应用框架
- "积木式"组件:LLM、Prompt、Memory、Tools、Chains、Agents
- 生态最丰富但被批"过度抽象"
- 子项目:LangSmith(监控)、LangServe(部署)
- 用于:RAG、对话应用、Agent 原型

#### 2. LlamaIndex(原 GPT Index)

- 专注于 [[RAG]] 与数据接入
- 擅长复杂索引结构(树、图、子查询)
- "Data framework for LLMs"
- 用于:企业知识库、文档问答

#### 3. AutoGen(微软,2023.10)

- 多 Agent 协作框架
- 自然语言定义 Agent 角色与对话规则
- 经典模式:User-Proxy + Assistant 反复迭代
- 用于:复杂任务分解、代码生成 + 执行

#### 4. CrewAI

- 角色驱动的多 Agent 系统
- 类似"组建团队":每个 Agent 有 role、goal、backstory
- 提供 sequential、hierarchical 等编排
- 用于:角色扮演式任务、模拟工作流

#### 5. LangGraph

- LangChain 团队推出的状态机框架
- 节点 = LLM/工具调用,边 = 状态转换
- 比 LangChain 的 Chain 更灵活,支持循环
- 用于:复杂工作流、可控 Agent

#### 6. Haystack(deepset)

- 早期开源 NLP 框架
- 强调企业级工程实践
- 用于:搜索、问答系统

#### 7. DSPy(Stanford)

- "用编程代替 prompt"
- 自动优化 prompt
- 把 LLM 应用编译为优化的 prompt 链
- 用于:复杂推理 pipeline

#### 8. PydanticAI

- 类型安全的 LLM 框架
- 借鉴 Pydantic 思想
- 用于:结构化输出、强类型应用

### 核心组件

无论何种框架,几乎都涵盖:

#### 1. LLM 抽象

统一接口调用 OpenAI、Anthropic、本地 Llama、DeepSeek 等。

#### 2. Prompt 模板

参数化 prompt,支持版本管理。

#### 3. 工具调用(Tool Use / Function Calling)

让 LLM 调用外部 API、数据库、计算器、网页搜索等。
- OpenAI 的 function calling
- Anthropic 的 tool use
- 通用的 ReAct 模式

#### 4. 记忆(Memory)

- 短期:对话历史
- 长期:向量数据库存储
- 工作记忆:scratchpad

#### 5. 检索(Retrieval)

[[RAG]] 实现,从向量库或文档库取相关内容增强 LLM 输入。

#### 6. 规划(Planning)

- ReAct(Reason + Act)
- Plan-and-Solve
- Tree of Thoughts

#### 7. 多 Agent 编排

- Manager-Worker
- 辩论(Debate)
- 共识投票

### 开发模式

#### 简单 Chain(LangChain LCEL 表达式)

```python
chain = prompt | llm | output_parser
result = chain.invoke({"question": "..."})
```

#### Agent 模式(ReAct)

```
观察 → 思考 → 行动(工具调用)→ 观察 → ... → 最终回答
```

#### 多 Agent 协作

```
PM Agent: 拆解任务为子任务
Coder Agent: 写代码
Reviewer Agent: 审查代码
Executor Agent: 运行测试
循环直到通过
```

#### 状态机(LangGraph)

```
def research_node(state): ...
def write_node(state): ...
def review_node(state): ...

graph.add_edge(research_node, write_node)
graph.add_conditional_edge(write_node, review_node, condition=...)
```

### MCP 协议(Anthropic 2024)

[[Anthropic]] 推出的**Model Context Protocol**:统一 LLM 与外部工具/数据源的开放协议。
- 框架无关,各 Agent 框架都可接入
- 工具开发者只需实现一次,所有兼容客户端可用
- 类似"AI 时代的 USB-C"

### 实务挑战

#### 1. 可靠性

LLM 仍可能:
- 误解工具描述
- 错误参数
- 死循环
- 越界回答

需配合:
- 重试机制
- 工具调用验证
- 超时控制
- 人在回路

#### 2. 成本

多步 Agent 调用 → API 费用累加
- 大模型只用关键步
- 简单步骤用小模型
- 缓存重复调用

#### 3. 调试

非确定性 + 多步 → 难复现
- LangSmith、Langfuse 等监控工具
- 录制-回放
- 详细日志

#### 4. 安全

Agent 操作真实系统 → 风险放大
- 沙盒执行
- 权限最小化
- 关键操作人工确认

### 行业现状(2025)

- LangChain 仍是入门首选,但被批"魔法过多"
- AutoGen 在企业级多 Agent 场景占优
- LangGraph、CrewAI 增长快
- "原生" SDK 路线兴起:直接用 OpenAI/Anthropic SDK,不用框架
- AI 编码助手(Cursor、Claude Code、Aider)是 Agent 框架的特化形态

### Agent vs Workflow vs Chatbot

| 类型 | 自主性 | 例 |
|---|---|---|
| **Chatbot** | 低,被动响应 | 客服 FAQ |
| **Workflow** | 中,固定流程 | RAG 问答管线 |
| **Agent** | 高,自主决策 | Devin、AutoGPT、Claude Computer Use |

Agent 概念在 2024+ 实际能落地的多是"半自主"形态——固定步骤 + 局部决策。

### AI 编码 Agent 的特例

| 工具 | 形态 |
|---|---|
| GitHub Copilot | 代码补全(轻 Agent) |
| Cursor | IDE + Agent |
| Claude Code | CLI + Agent |
| Aider | Git-aware CLI |
| Devin(Cognition) | 远程虚拟工程师 |
| Replit Agent | 浏览器 + 项目级 |

它们是 Agent 框架在编程领域的产品化具体形态。

### 长任务 Agent 评估

- **AgentBench**:综合 Agent 能力
- **WebArena / WebShop**:网页操作
- **SWE-Bench**:代码修复
- **GAIA**(Meta):通用助手
- **OSWorld**:操作系统级任务

实测显示:即使最强模型在长任务上完成率仍然有限(< 50%),Agent 还是早期阶段。

## 和其他概念的关系

- 应用基础:[[大语言模型]]、[[RAG]]
- 编排核心:[[思维链]]、[[ReAct提示]]、[[Plan-and-Solve提示]]
- 涉及工具:函数调用、[[MCP协议]]
- 与 [[提示词工程]] 高度关联,prompt 设计是 Agent 性能关键
- 主要厂商:[[Anthropic]] (MCP)、[[OpenAI]](Function Calling)、Microsoft(AutoGen)、Meta、LangChain Inc.
- 与 [[AI Agent]] 概念在产品形态上一致
- [[AI模型评估基准]] 中的 Agent 类专项测试

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md
