---
title: GPT与LLM家族
type: concept
tags: [ai, stub]
sources: []
created: 2026-05-11
updated: 2026-05-11
summary: GPT 系列开启了当代 LLM 时代,推动全球主流大模型形成家族生态,包括 Claude、Gemini、Llama、Qwen、DeepSeek 等,各自在能力、开源度、优化路径上分野。
---

# GPT与LLM家族

## 定义

**GPT**(Generative Pre-trained Transformer)由 OpenAI 于 2018 年首次发布,GPT-3(2020)首次让"通过 API 调用大模型"成为主流,GPT-3.5(ChatGPT, 2022)引爆全球 AI 浪潮。之后大模型行业形成**多家族并立**的生态,不再是"GPT 一家",各家族在训练路径、对齐方法、开源程度、专长领域上有明显分野。

## 核心要点

### 主流家族

| 家族 | 开发方 | 特点 |
|---|---|---|
| **GPT 系列** | OpenAI | 首创对话对齐,产品化最早,闭源 |
| **Claude 系列** | Anthropic | 长上下文、Constitutional AI 对齐,擅长复杂推理 |
| **Gemini 系列** | Google DeepMind | 原生多模态,深度集成 Google 产品线 |
| **Llama 系列** | Meta | 开源权重,催生本地部署生态 |
| **Qwen 系列** | 阿里 | 中文强、开源,含视觉/音频等多模态 |
| **DeepSeek** | DeepSeek | 强推理、成本极低,颠覆了训练成本认知 |
| **Mistral** | Mistral AI | 欧洲开源代表,MoE 架构成熟 |

### 竞争维度

- **能力**:通过 [[MMLU基准]]、[[HumanEval基准]]、[[Chatbot Arena]] 等对比
- **速度与成本**:推理成本、token 生成速度、缓存机制(见 [[Prompt Caching]])
- **上下文长度**:从早期 4K 扩展到 200K-2M
- **对齐方法**:[[RLHF]]、DPO、Constitutional AI 各有取舍
- **开源度**:完全开源(Llama、Qwen)vs API 闭源(GPT、Claude、Gemini)

## 和其他概念的关系

- 属于 [[大语言模型]] 的具体家族分类
- 每个家族的具体模型见 [[GPT系列模型]]、[[Claude系列模型]]、[[Gemini系列模型]]、[[Llama系列模型]]、[[Qwen系列模型]] 等 entity
- 底层基础是 [[Transformer]] 架构
- 竞争评估依托 [[MMLU基准]]、[[HumanEval基准]]、[[Chatbot Arena]]
- 应用层影响 [[RAG]]、[[AI Agent]]、[[提示词工程]] 等生态

## 参考源

- 综合各家族官方发布与行业评测
