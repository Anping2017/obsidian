---
title: Meta AI
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: Meta(原 Facebook)的 AI 研究与产品组织,以 Llama 系列开源大模型与 PyTorch 框架著称,是 AI 开源运动的核心推动者。
---

# Meta AI

## 简介

Meta AI 是 Meta(原 Facebook)的 AI 研究与产品组织,起源于 2013 年成立的 Facebook AI Research(FAIR),由图灵奖得主 [[Yann LeCun]] 创立并担任首席 AI 科学家。

它是 AI 开源运动的最大推手:开源 PyTorch 深度学习框架(2017)、开源 LLaMA / Llama 系列大模型(2023+)、开源 SAM 视觉模型,在工业界开源派与闭源派(OpenAI / Anthropic)之间形成最重要的对立力量。

## 关键贡献

### 开源框架

- **PyTorch**(2017):深度学习事实标准框架,与 TensorFlow 并立后超越
- **PyTorch 2.0**(2023):TorchDynamo + TorchInductor,编译加速

### Llama 系列大模型

| 版本 | 时间 | 关键 |
|---|---|---|
| LLaMA 1(7B-65B) | 2023.2 | 学术研究授权 |
| Llama 2(7B-70B) | 2023.7 | 商用免费,引爆开源 LLM 浪潮 |
| Llama 3(8B-70B) | 2024.4 | 大幅提升性能 |
| Llama 3.1(8B/70B/405B) | 2024.7 | 开源 405B 媲美 GPT-4 |
| Llama 3.2 Vision | 2024.9 | 多模态能力 |
| Llama 4(2025) | 2025 | MoE 架构 |

### 视觉模型

- **SAM**(Segment Anything Model,2023):零样本分割,开源
- **DINO / DINOv2**:自监督视觉学习
- **VideoMAE**:视频自监督

### 多模态与 AIGC

- **AudioCraft**:开源音乐生成
- **Imagine**(Meta 内置 AIGC)
- **Movie Gen**:视频生成

### 其他研究

- **FAIR**(基础研究):RAG、ImageBind、Self-Rewarding LM
- **Reality Labs**:VR/AR + AI 集成
- **AI 助手**:Meta AI 集成在 WhatsApp、Instagram、Facebook

## 战略与定位

### 开源派立场

[[Yann LeCun]] 长期主张:
- AI 不应被少数公司垄断
- 开源是科学进步的最佳路径
- 担忧 AI 风险但不认同末日论
- 支持以开源对抗闭源垄断

这一立场与 [[OpenAI]]、[[Anthropic]] 的安全优先路线形成鲜明对照。

### 商业模式

- 不直接收 API 费(与 OpenAI 不同)
- 通过 AI 增强广告、推荐、内容生成
- 开源 Llama 提升生态影响力,吸引人才

### 与中国开源的呼应

Llama 推动的开源浪潮启发了中国大模型开源:
- 阿里 Qwen
- DeepSeek
- 智谱 GLM、百川等

## 相关概念/实体

- 直接产品:Llama 系列 [[大语言模型]]、PyTorch
- 关键技术:[[Transformer架构|Transformer]]、[[预训练与微调]]、[[模型蒸馏]]、ImageBind
- 核心人物:[[Yann LeCun]](Chief AI Scientist)、Mark Zuckerberg(CEO)
- 主要竞争者:[[OpenAI]]、[[Anthropic]]、[[Google DeepMind]]
- 战略合作:Hugging Face(开源生态)
- 开源运动伙伴:Mistral AI、Stability AI

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
- raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md
