---
title: Gemini 系列模型
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: Gemini 是 Google DeepMind 推出的多模态原生大模型家族,从设计之初即统一处理文本、图像、音频、视频、代码,深度集成于 Google 产品矩阵。
---

# Gemini 系列模型

## 简介

Gemini 是 Google DeepMind 于 2023 年推出的[[大语言模型]]家族,标志性特点是"原生多模态"——从训练阶段即用图、文、视频、音频、代码混合数据,而非事后接入图像编码器。Gemini 是 Google 整合 Brain 与 DeepMind 后的旗舰 AI 产品。

## 关键代际

### Gemini 1.0(2023 年 12 月)

三档:Ultra、Pro、Nano(端侧)。

### Gemini 1.5 Pro(2024 年 2 月)

引入 [[MoE]] 混合专家架构,1M 上下文窗口(实验版 10M)。

### Gemini 2.0(2024 年 12 月)

代理能力(Astra、Mariner、Jules)突显。

### Gemini 2.5 Pro / Ultra(2025-2026)

推理增强、Deep Research、Veo 视频生成集成。

## 技术特色

- **原生多模态**:统一 token 化处理多模态信号
- **MoE 架构**:稀疏激活降低推理成本
- **长上下文**:1M-2M tokens 工业级
- **TPU 训练**:运行于 Google 自研 TPU 而非 NVIDIA GPU
- **Search Grounding**:深度整合 Google Search 提升时效性

## 产品形态

- Gemini App(消费者)
- Vertex AI(企业)
- Google Workspace 集成(Gmail、Docs、Sheets)
- AI Studio(开发者实验)
- Project Astra(实时多模态助手)

## 与其他模型对比

- vs [[GPT系列模型]]:Gemini 多模态原生,GPT-4o 后追赶
- vs [[Claude系列模型]]:Gemini 全能,Claude 专精
- vs [[Llama系列模型]]:Gemini 闭源 + 大规模分布,Llama 开源
- 数据优势:Google 拥有 YouTube、Search 等数据源

## 关联概念

- [[多模态AI]]、[[Vision Transformer]]、[[CLIP]]、[[Whisper语音识别]]
- [[模型量化]]、[[模型蒸馏]]、[[FlashAttention]]
- [[预训练与微调]]、[[指令微调]]、[[RLHF]]
- [[AI Agent框架]]
- [[Stable Diffusion]] 与 Veo(视频生成)对照

## 关键贡献

- Mixture-of-Experts 工业化
- 1M 上下文与"针 in 海"全召回
- Project Astra 实时多模态代理
- AlphaProof / AlphaGeometry 数学推理(背后用 Gemini 衍生)

## 参考源

- raw/AI人工智能/04-综合提升层/
- Gemini Technical Report (Google DeepMind)
