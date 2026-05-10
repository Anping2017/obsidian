---
title: Mistral 系列模型
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: Mistral 是法国 Mistral AI 推出的开源大模型家族,以小参数高性能、首个工业级 MoE 与欧洲 AI 自主路径为特色。
---

# Mistral 系列模型

## 简介

Mistral AI 是 2023 年成立于巴黎的 AI 公司,由前 Meta、DeepMind 研究者创办,被视为欧洲对抗美国 AI 巨头的代表。Mistral 模型以"小巧高效"和"开源为先"著称,在同等参数量下常击败 Llama 同代。

## 关键模型

### Mistral 7B(2023 年 9 月)

7B 参数即超越 Llama 2 13B,引入 Sliding Window Attention 与 Grouped Query Attention(GQA)。

### Mixtral 8x7B(2023 年 12 月)

工业界首个开源 MoE 模型,激活 12.9B 参数获得 47B 效果。

### Mistral Large(2024)

闭源旗舰,通过 API 提供。

### Codestral(2024)

22B 代码专精模型。

### Mistral Small/Medium(2024-2025)

差异化定位,Small 高性价比,Medium 平衡。

### Mistral Large 2(2024 年 7 月)

123B 参数,128k 上下文,数学与代码大幅提升。

## 技术特色

- **GQA + SWA**:Grouped Query Attention 与 Sliding Window Attention 优化推理速度
- **MoE 工业化**:首个高质量开源 MoE
- **Apache 2.0 与 MRL 双轨**:小模型开源,旗舰商业化
- **欧洲数据合规**:GDPR 友好,主权 AI 选项

## 产品形态

- Le Chat(消费者对话)
- La Plateforme(API)
- Mistral Code(IDE 编码助手)
- 微软 Azure、AWS 集成

## 与其他模型对比

- vs [[Llama系列模型]]:Mistral 同参数下性能更高
- vs [[GPT系列模型]] / [[Claude系列模型]]:更小成本部署
- vs [[Qwen系列模型]] / [[DeepSeek]]:阵营不同(欧洲 vs 中国)
- 战略意义:打破美中两极 AI 格局

## 关联概念

- [[大语言模型]]、[[Transformer架构|Transformer]]、[[MoE]]
- [[FlashAttention]]、[[模型量化]]、[[模型蒸馏]]
- [[预训练与微调]]、[[指令微调]]
- [[AI Agent框架]]、[[AI编码助手]]

## 参考源

- raw/AI人工智能/04-综合提升层/
- Mistral 7B / Mixtral 8x7B 技术报告
