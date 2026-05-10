---
title: GPT 系列模型
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: GPT 是 OpenAI 推出的生成式预训练 Transformer 模型家族,从 GPT-1 到 GPT-5,推动了大规模语言模型(LLM)的工业化应用,塑造了现代 AI 形态。
---

# GPT 系列模型

## 简介

GPT(Generative Pre-trained Transformer)是 [[OpenAI]] 自 2018 年起推出的[[大语言模型]]家族,基于[[Transformer架构|Transformer]] 架构的[[解码器]]部分,采用[[预训练与微调]]两阶段范式。GPT 系列将"自回归生成"与"超大规模参数"结合,验证了规模假说([[规模定律]]),推动 AI 从"任务式"走向"通用基础模型"。

## 关键代际

### GPT-1(2018,1.17 亿参数)

首次系统应用 Transformer + 大规模无监督预训练 + 任务微调,验证迁移学习有效性。

### GPT-2(2019,15 亿参数)

引入 zero-shot 能力,首次以"危险性"为由限制开源,引发 AI 治理讨论。

### GPT-3(2020,1750 亿参数)

提出 [[Few-shot提示]] 与 [[零样本提示]],通过 API 商业化,开启 LLM 应用浪潮。

### GPT-3.5(2022)

InstructGPT + [[RLHF]] 训练范式诞生,ChatGPT 发布,3 个月用户破亿。

### GPT-4(2023)

引入多模态(GPT-4V)、长上下文(128k)、代码与推理能力大幅跃升。

### GPT-4o(2024)

原生多模态(语音/视觉/文本统一),实时对话延迟降到 320ms。

### GPT-5 / o1 / o3(2024-2025)

推理时计算([[Inference-time scaling]])的代表,先思考再回答,STEM 性能逼近博士水平。

## 关键技术贡献

- 大规模 Transformer 解码器
- [[Constitutional AI]] 与 RLHF 方法的工程化
- 系统提示([[System Prompt]])概念
- 函数调用([[Function Calling]])与工具使用
- [[思维链]] 与 [[反思提示]] 的内化(o 系列)

## 与其他模型的对比

- vs [[Claude系列模型]]:训练目标不同,Claude 强调可解释性、Constitutional AI
- vs [[Gemini系列模型]]:Gemini 更早原生多模态
- vs [[Llama系列模型]]:GPT 闭源,Llama 开源
- vs [[DeepSeek]]:DeepSeek 用 MoE+RL 以更低成本逼近性能

## 关联概念

- [[预训练与微调]]、[[指令微调]]、[[RLHF]]、[[DPO直接偏好优化]]
- [[Constitutional AI]]、[[模型量化]]、[[模型蒸馏]]
- [[思维链]]、[[Few-shot提示]]、[[AI红队评估]]
- [[超级对齐]]、[[涌现能力]]
- [[AI Agent框架]]、[[AI编码助手]]

## 参考源

- raw/AI人工智能/04-综合提升层/
- OpenAI 官方技术报告
- Brown et al. (2020) "Language Models are Few-Shot Learners"
