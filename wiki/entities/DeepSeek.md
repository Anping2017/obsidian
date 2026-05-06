---
title: DeepSeek
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: 中国杭州深度求索公司,以 DeepSeek-V3 与 R1 推理模型展示极低成本下接近 GPT-4 水平的能力,2025 年初引爆全球 AI 算力效率讨论。
---

# DeepSeek

## 简介

DeepSeek(深度求索)是中国杭州的 AI 公司,由量化对冲基金幻方量化(High-Flyer)CEO 梁文锋于 2023 年创立。它以**极低训练成本**实现接近 GPT-4 水平的开源大模型,2024-2025 年成为全球 AI 行业最受关注的中国力量。

2025 年 1 月发布的 **DeepSeek-R1** 推理模型在用约 $5.6M 训练成本(对比 GPT-4 估计 $100M+)达到 OpenAI o1 水平,并完全开源,直接冲击美国 AI 股价(Nvidia 单日跌 17%),被称为"DeepSeek 时刻"。

## 关键贡献

### 模型系列

| 模型 | 时间 | 关键 |
|---|---|---|
| DeepSeek-Coder | 2023 | 代码模型,开源 |
| DeepSeek LLM(7B/67B) | 2023 | 通用大模型 |
| DeepSeekMath 7B | 2024 | 数学推理 |
| DeepSeek-V2(236B MoE) | 2024 | MoE 架构,激活 21B |
| DeepSeek-V3(671B MoE) | 2024.12 | 激活 37B,性能接近 GPT-4 |
| DeepSeek-R1 / R1-Zero | 2025.1 | 推理模型,逻辑能力对标 o1 |

### 关键技术创新

#### MLA(Multi-head Latent Attention)

把 KV-Cache 压缩到低维潜空间,显存占用降低 93.3%,长上下文推理大幅提速。

#### MoE 架构精细化

DeepSeek-V3 用 256 个细粒度专家 + 1 共享专家 + 路由策略,有效提升参数效率。

#### GRPO(Group Relative Policy Optimization)

省去 critic 模型,直接用组内相对优势优化策略,显著降低 RL 训练成本——R1 训练核心。

#### Reasoning via Pure RL

R1-Zero 完全跳过指令微调,纯靠 RL 训练涌现出 [[思维链]] 推理能力。这一发现挑战了"必须经过 SFT"的常识。

#### 训练效率优化

- 自研 HAI-LLM 训练框架
- FP8 训练精度
- 3D 并行优化
- 集群利用率行业领先

### 完全开源策略

- 模型权重 MIT 协议开源
- 训练论文公开技术细节
- 推理代码开源
- 与 [[Meta AI]]([[Llama]])形成开源双雄

### API 价格颠覆

API 定价远低于美国同类:
- DeepSeek V3 API:输入 $0.14 / 1M,输出 $0.28 / 1M
- 对比 GPT-4o:输入 $2.5 / 1M,输出 $10 / 1M
- 推动行业整体降价

## 战略意义

### 算力效率论

挑战"GPU 越多越好"的硅谷叙事:
- 美国对中国 GPU 出口管制本意限制 AI 发展
- 限制反而催生 DeepSeek 极致效率优化
- 显示 AI 竞争不止是算力规模,算法创新空间巨大

### 开源 vs 闭源

- DeepSeek 的成功证明开源能与闭源平起平坐
- 推动 OpenAI、Anthropic 重新评估闭源模型优势
- 影响美国 AI 监管对开源的态度

### 蒸馏与法律争议

OpenAI 指控 DeepSeek 通过 ChatGPT API 输出蒸馏训练 R1,违反 ToS:
- 双方各有诉求
- 引发"是否任何公司都能蒸馏闭源模型"的讨论
- 凸显 [[模型蒸馏]] 在 AI 行业的灰色地带

## 团队与文化

- 团队规模 200 人(对比 OpenAI 1500+)
- 主要由清华、北大年轻博士组成
- 不接受融资(自有资金)
- 创始人梁文锋强调"做长期正确的事"
- 与高校合作密切

## 与全球 AI 生态

- **影响美国资本市场**:Nvidia、Microsoft、OpenAI 估值受冲击
- **推动开源生态**:吸引大量开发者
- **国际外交话题**:中美 AI 竞争的标志事件
- **学术影响**:论文引用量飙升,GRPO、MLA 被广泛采用
- **监管挑战**:数据训练来源、内容审查标准的不同

## 相关概念/实体

- 直接产品:DeepSeek-V3、R1、Coder 等 [[大语言模型]]
- 关键技术:MoE、MLA、GRPO、FP8 训练、[[模型蒸馏]]、[[思维链]]
- 核心人物:梁文锋(创始人 / CEO)
- 主要竞争者:[[OpenAI]]、[[Anthropic]]、[[Google DeepMind]]、[[Meta AI]]、Qwen
- 母公司:幻方量化(High-Flyer Capital)

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
- raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md
