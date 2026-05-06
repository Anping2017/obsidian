---
title: MCP协议
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md, raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: MCP(Model Context Protocol)是 Anthropic 2024 年提出的开放协议,标准化大语言模型应用与外部工具、数据源、上下文之间的连接方式。
---

# MCP协议

## 定义

**MCP(Model Context Protocol, 模型上下文协议)** 是 Anthropic 在 2024 年底提出的**开放协议**,用于标准化 [[大语言模型]] 应用(Host)与外部工具、数据源、上下文(Server)之间的连接方式。它在 [[函数调用]] 之上抽象出"模型如何发现并调用任意外部能力"的统一规范。

可类比于"AI 时代的 USB 标准":一次实现 MCP Server,所有支持 MCP 的客户端(Claude Desktop、Cursor、Continue 等)都能直接接入。

## 核心要点

**核心概念**

| 角色 | 作用 |
|---|---|
| Host | LLM 应用,如 Claude Desktop、IDE 插件 |
| Client | Host 内嵌的协议客户端,管理与 Server 的连接 |
| Server | 暴露具体能力的服务进程(本地或远程) |

**Server 提供三类原语**

- **Tools**:可被模型调用的函数(读文件、查数据库、发请求)
- **Resources**:可被模型读取的数据(文件、API 响应、日志)
- **Prompts**:预定义的提示模板,供用户/模型快速复用

**协议特征**

- 基于 JSON-RPC 2.0,通过 stdio 或 HTTP+SSE 传输
- 双向通信:Server 也可向 Host 发起请求(如要求确认)
- 模型无关:协议本身不绑定特定 LLM 厂商
- 开源参考实现:Python、TypeScript SDK 与一众官方 Server(filesystem、git、postgres 等)

**为什么重要**

- 打破"工具适配器"地狱:每接入一个新工具都要在每个 Host 中重写
- 把企业内部工具/数据生态化:一次开发,各 LLM 客户端可用
- 推动 [[AI Agent]] 工具生态从厂商私有走向开放标准
- 安全边界:Server 进程隔离,权限可控

**典型场景**

- IDE 中让 Claude 直接读写本地仓库、查数据库
- 让聊天助手访问 Google Drive、Notion、Slack
- 把企业内部 API(CRM、工单、监控)暴露给 LLM
- 跨 LLM 客户端共用同一套工具

## 和其他概念的关系

- 上层抽象:[[函数调用]] 是模型层能力,MCP 是系统层标准
- 直接受益者:[[AI Agent]] 工具生态从碎片化走向统一
- 与 [[RAG]] 互补:Resources 原语让外部数据可被 LLM 直接读取
- 推动者:Anthropic 提出,逐步被 OpenAI、Google、开源生态采纳
- 安全考量:MCP Server 接入相当于授予 [[大语言模型]] 系统权限,[[提示注入]] 攻击面需谨慎防范

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md
- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
