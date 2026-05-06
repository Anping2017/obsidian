---
title: Transformer
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/02-理解层/02-03-算法与模型/02-03-04-Transformer架构.md, raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md]
created: 2026-05-05
updated: 2026-05-05
summary: Transformer 是 2017 年 Vaswani 等人提出的基于自注意力机制的神经网络架构,完全摒弃循环和卷积,主导现代 NLP、CV、多模态 AI。
---

# Transformer

## 定义

**Transformer** 是 Google 团队在 2017 年论文 *Attention Is All You Need* 中提出的 [[神经网络]] 架构。其核心创新是用**自注意力机制**完全取代 RNN 的循环结构,使序列内部所有位置可在一次计算中互相"看到"对方,具备并行性与长距离依赖建模能力。

它是现代 [[大语言模型]](GPT、Claude、Llama)、视觉模型(ViT)与多模态模型的统一架构基础。

## 核心要点

**核心组件**

| 组件 | 作用 |
|---|---|
| [[自注意力机制]] | 每个位置加权聚合所有位置信息 |
| 多头注意力(Multi-Head) | 并行多个注意力子空间,捕捉不同关系 |
| [[位置编码]] | 因没有循环结构,需显式注入序列顺序信息 |
| 前馈网络(FFN) | 每个位置独立的两层 MLP,提供非线性容量 |
| 残差连接 + LayerNorm | 稳定深层训练、为 [[反向传播]] 提供梯度通道 |

**经典架构两分支**

- Encoder-Decoder(原始论文):机器翻译等 seq2seq 任务,代表 T5、BART
- Encoder-only:[[BERT]],擅长理解任务(分类、NER)
- Decoder-only:GPT 系列、Claude、Llama,主导生成与对话,**当前最主流**

**关键属性**

- 完全并行训练(相对 RNN 必须串行)
- 上下文窗口可扩展(从 512 → 100K+ tokens)
- 复杂度 $O(n^2)$ 关于序列长度,催生 FlashAttention、稀疏注意力等优化
- 参数 scaling laws:模型容量、数据、计算近似幂律提升能力

**演化里程碑**

- 2017:Transformer 原始论文
- 2018:[[BERT]] 用 Encoder + 掩码语言建模
- 2018-2023:GPT-1/2/3/4 用 Decoder + 自回归
- 2020:ViT 把 Transformer 引入计算机视觉
- 2022+:多模态(GPT-4V、Gemini)、超长上下文、混合专家(MoE)

## 和其他概念的关系

- 直接基础:[[自注意力机制]] 是 Transformer 的核心运算
- 必须配套:[[位置编码]] 提供顺序信息
- 主要载体:[[大语言模型]]、[[BERT]]、GPT 等都基于 Transformer
- 训练依赖:海量数据 + [[反向传播]] + Adam 优化器
- 现代生态:[[RAG]]、[[函数调用]]、[[MCP协议]] 都构建在 Transformer 模型之上
- 与 [[循环神经网络]] 关系:几乎完全替代了 RNN/LSTM 在 NLP 中的地位
- 计算机科学基础:注意力的 $O(n^2)$ 复杂度是 [[复杂度分析]] 的典型瓶颈,催生 FlashAttention 等优化;训练与推理高度依赖 GPU 集群的 [[并发与并行]] 计算;KV-Cache 的实现本质上是带键的 [[Hash表]] 用于加速自回归解码

## 参考源

- raw/AI人工智能/02-理解层/02-03-算法与模型/02-03-04-Transformer架构.md
- raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md
- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
