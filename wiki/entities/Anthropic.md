---
title: Anthropic
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md, raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: Anthropic 是 2021 年由前 OpenAI 成员创立的 AI 安全公司,以 Claude 系列大语言模型与 Constitutional AI、MCP 协议著称,聚焦安全与对齐。
---

# Anthropic

## 简介

Anthropic 成立于 2021 年,由前 [[OpenAI]] 研究副总 Dario Amodei、Daniela Amodei 兄妹与一批前 OpenAI 研究员创立,总部位于旧金山。公司使命是"AI 安全"——研究如何开发可靠、可解释、可控的 AI 系统。其旗舰产品 Claude 系列 [[大语言模型]] 与 [[OpenAI]]、Google 形成全球三足鼎立格局。Amazon 与 Google 是其主要战略投资方。

## 关键贡献

**模型系列**

- Claude 1(2023):基于 Constitutional AI 训练
- Claude 2(2023):100K 长 [[上下文窗口]] 引领行业
- Claude 3 系列(2024):Opus/Sonnet/Haiku 三档,综合能力领先
- Claude 3.5 / 3.7 Sonnet(2024):强代码与推理能力
- Claude 4 / Opus 4(2025):Extended Thinking 推理能力
- 所有 Claude 模型在长文本理解、代码、安全性维度长期处于行业前列

**关键技术与方法**

- **Constitutional AI**:用一组"宪法"原则引导模型自我批评和修正,部分替代人工反馈,是 [[RLHF]] 的演化
- **可解释性研究**:大力投入机制可解释性(mech interp),发表系列影响力论文
- **[[MCP协议]]**(2024):开放协议标准化 LLM 与外部工具集成,推动 [[AI Agent]] 生态
- **Claude Code** 与 Claude.ai:产品化代码助手与对话助手
- 长期发表关于 LLM 行为、对齐、安全的高质量研究

**与同行差异**

- 更强调 AI 安全与对齐,公开发表大量安全研究
- 模型在拒绝行为、安全边界处理上更保守
- 商业策略:不做面向公众的 GPT Store,聚焦 API + 企业市场

## 相关概念/实体

- 直接产品:Claude 系列 [[大语言模型]]、[[MCP协议]]、Claude Code
- 关键技术:Constitutional AI、[[RLHF]]、长 [[上下文窗口]]
- 主要竞争者:[[OpenAI]]、[[Google DeepMind]]
- 战略合作:Amazon AWS(主要算力)、Google Cloud
- 关键人物:Dario Amodei(CEO)、Daniela Amodei(总裁)、Jack Clark、Chris Olah(可解释性)

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
- raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md
- raw/AI人工智能/03-应用层/03-04-工程实践/03-04-04-AI伦理与安全.md
