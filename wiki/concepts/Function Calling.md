---
title: Function Calling
type: concept
tags: [ai, mature]
sources: []
created: 2026-05-11
updated: 2026-05-11
summary: Function Calling 是大语言模型按预定义 schema 输出结构化参数、调用外部函数或 API 的能力,是 LLM 从聊天工具升级为可执行 agent 的核心机制。
---

# Function Calling

## 定义

**Function Calling**(函数调用,亦称 Tool Use、Tool Calling)指 [[大语言模型]] 根据用户意图,**按预定义的 schema 输出结构化 JSON 参数**,以触发外部函数、API 或工具执行,并把执行结果回灌给模型继续推理的能力。

它解决了 LLM 的三个根本短板:

1. 训练后知识无法更新 → 调用搜索 / 数据库
2. 不能精确计算与执行确定性逻辑 → 调用计算器 / 代码解释器
3. 无法影响外部世界 → 调用发邮件 / 下订单 / 控制设备

Function Calling 是 LLM 从"会聊天"升级为"会做事的 agent"的关键基础设施。

## 核心要点

### 工作流程

```
用户提问
   ↓
LLM 判断需要调用工具,输出 {tool_name, arguments}
   ↓
应用层解析 JSON,执行真实函数
   ↓
把函数返回值作为新消息回灌给 LLM
   ↓
LLM 综合工具结果生成最终回答
```

整个循环可多轮迭代,形成 ReAct(Reason + Act)模式。

### Schema 约定

开发者向模型注册工具时提供:

- **name**:函数名
- **description**:函数用途(模型靠这段文字决定何时调用)
- **parameters**:JSON Schema 描述参数类型、是否必填、枚举值
- **返回格式**:通常是字符串或 JSON

模型生成的调用以严格 JSON 输出,主流厂商已支持 **JSON mode / structured output** 强约束。

### 三大厂商实现对比

| 厂商 | API 字段 | 特性 |
|---|---|---|
| **OpenAI** | `tools` + `tool_choice` | 最早发布(2023-06),支持并行调用 |
| **Anthropic Claude** | `tools` | 强调思维链可见,Claude Code 深度集成 |
| **Google Gemini** | `function_declarations` | 与 Google 服务原生集成 |
| **开源模型** | LLaMA / Qwen / DeepSeek 经微调支持 | 需要 prompt 模板或专用模型版本 |

### 并行 / 串行 / 嵌套调用

- **并行**:一次 turn 内同时调用多个独立工具(查天气 + 查日历)
- **串行**:前一个工具结果作为下一个工具输入
- **嵌套**:工具内部再触发模型推理,形成多层 agent

### MCP(Model Context Protocol)

Anthropic 2024 年提出的开放协议,把 Function Calling 标准化为客户端—服务器架构:模型客户端通过 MCP server 接入文件系统、数据库、第三方服务,工具提供方无需关心模型实现。已成为事实标准。

## 典型应用 / 主流模型工具

- **AI Agent 框架**:LangChain、LlamaIndex、CrewAI、AutoGen
- **编程助手**:Claude Code、Cursor、GitHub Copilot —— 调用 shell、文件读写、git
- **企业搜索**:连接 Notion、Slack、Confluence 检索内部知识
- **办公自动化**:发邮件、建日程、改 Sheet、生成 PPT
- **检索增强**:与 [[检索增强生成]] 结合,先调检索工具再生成答案

## 局限与挑战

| 挑战 | 描述 |
|---|---|
| **幻觉调用** | 模型可能编造不存在的工具或乱填参数 |
| **链路过长** | 多轮工具调用会显著抬高延迟与成本 |
| **安全风险** | 恶意 prompt 可诱导模型调用危险函数(删文件、转账) |
| **工具描述膨胀** | 工具一多,description 占满上下文窗口 |
| **错误处理** | 工具失败时模型未必能优雅降级 |
| **跨厂商不兼容** | 各家 schema 命名不同,迁移成本高(MCP 在弥合) |

## 与其他概念的关系

- 基座是 [[大语言模型]] 与 [[预训练语言模型]] 的指令跟随能力
- 与 [[检索增强生成]] 互补 —— RAG 是被动检索,Function Calling 是主动调用
- 通过 [[Embedding]] 实现工具描述的语义召回(工具过多时)
- 是构建 AI Agent 的基本机制,扩展为 [[多模态AI]] 中的图像 / 音频工具
- 主流模型 [[Gemini系列模型]] 与 Claude、GPT 都原生支持
- 配合 [[Transformer架构]] 的 attention 机制实现长上下文工具编排

## 参考源

- OpenAI, *Function calling and other API updates*, 2023-06
- Anthropic, *Tool use with Claude*, 2024
- Google, *Gemini function calling guide*, 2024
- Anthropic, *Introducing the Model Context Protocol*, 2024-11
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, 2022
