---
title: Llama 系列模型
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: Llama 是 Meta 推出的开源大语言模型家族,通过开放权重重塑行业格局,催生了海量微调与部署生态,是开源 AI 运动的旗帜。
---

# Llama 系列模型

## 简介

Llama(Large Language Model Meta AI)是 [[Meta AI]] 自 2023 年推出的[[大语言模型]]家族。区别于 OpenAI、Google 的闭源策略,Meta 选择开放权重(Open Weights),让 Llama 成为研究界与小公司构建私有 AI 的事实标准底座。

## 关键代际

### Llama 1(2023 年 2 月)

7B/13B/33B/65B 四种规模,初版仅向研究者开放,但权重很快泄露,加速开源运动。

### Llama 2(2023 年 7 月)

商业可用许可,引入 RLHF 训练版 Llama-2-Chat。

### Llama 3(2024 年 4 月)

8B/70B,质量大幅追平闭源模型。

### Llama 3.1(2024 年 7 月,405B)

首个开源前沿级模型,128k 上下文,性能接近 GPT-4。

### Llama 3.2(2024 年 9 月)

引入视觉理解(11B/90B Vision)与端侧模型(1B/3B)。

### Llama 4(2025)

更大规模、原生多模态、MoE 架构。

## 技术与生态

- **开放权重**:可下载、本地部署、商业使用
- **生态衍生**:数千个微调版本(Alpaca、Vicuna、Mistral 早期、CodeLlama)
- **量化与部署**:[[模型量化]] 后可在消费级 GPU 甚至 CPU 运行
- **Meta 用例**:Meta AI(Instagram、WhatsApp、Messenger 内置)

## 与其他模型对比

- vs [[GPT系列模型]] / [[Claude系列模型]] / [[Gemini系列模型]]:Llama 性能略低但完全可控可部署
- vs [[DeepSeek]] / [[Mistral系列模型]] / [[Qwen系列模型]]:同属开源阵营,Llama 是事实标准
- 商业策略:开源对抗闭源,瓦解他人护城河,做自己的生态

## 行业影响

- 推动 [[AI Agent框架]] 工具(LangChain、Ollama、vLLM)
- 推动 [[模型量化]] 与 [[模型蒸馏]] 民主化
- 推动 [[AI编码助手]] 本地化
- 重塑[[Hugging Face]] 等开源平台地位

## 关联概念

- [[预训练与微调]]、[[指令微调]]、[[RLHF]]、[[DPO直接偏好优化]]
- [[模型量化]]、[[模型蒸馏]]、[[FlashAttention]]
- [[大语言模型]]、[[Transformer]]
- [[AI红队评估]]、[[超级对齐]]
- [[Meta AI]]

## 参考源

- raw/AI人工智能/04-综合提升层/
- Llama 1/2/3 Technical Reports (Meta AI)
