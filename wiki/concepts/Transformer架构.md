---
title: Transformer架构
type: concept
tags: [ai, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Transformer 是 2017 年提出的基于自注意力机制的神经网络架构,用并行计算取代循环结构,成为大语言模型与多模态模型的统一基础。
---

# Transformer架构

## 定义

**Transformer 架构**指 Vaswani 等人在 2017 年论文 *Attention is All You Need* 提出的神经网络结构。它完全摒弃 RNN 的循环和 CNN 的局部卷积,核心是**自注意力机制**:每个位置可在一次前向计算中"看见"序列中所有位置,并加权聚合信息。

这一设计使深度学习模型获得了**并行训练能力**和**长距离依赖建模**两个关键属性,直接催生了 GPT、BERT、Claude、Llama 等现代大模型,并外推至视觉(ViT)、语音、多模态领域。

## 核心要点

### 自注意力的数学骨架

输入投影为 Query、Key、Value 三组向量,通过 $\text{Attention}(Q,K,V)=\text{softmax}(QK^T/\sqrt{d_k})V$ 计算加权和。多头注意力将其切分为多个子空间并行,捕捉不同语义关系。

### 主要组件

| 模块 | 作用 |
|---|---|
| 多头自注意力 | 全局依赖建模 |
| 位置编码 | 注入序列顺序(因没有循环) |
| 前馈网络 FFN | 每位置独立的非线性变换 |
| 残差连接 + LayerNorm | 训练稳定、梯度通畅 |

### 三类变体

- **Encoder-Decoder**(原始):机器翻译,代表 T5、BART
- **Encoder-only**:理解任务,代表 [[BERT]]
- **Decoder-only**:自回归生成,代表 GPT、Claude、Llama,**当前最主流**

### Scaling Laws

模型容量、训练数据量与计算资源近似按幂律放大模型能力。这是 GPT-3 → GPT-4 等代际跃迁的理论基础。

### 性能瓶颈与优化

注意力对序列长度复杂度为 $O(n^2)$,长上下文成本高,催生 FlashAttention、稀疏注意力、MoE(混合专家)、KV-Cache、滑动窗口等工程优化。

## 应用场景

- **自然语言**:GPT 类对话、翻译、摘要、代码生成
- **计算机视觉**:Vision Transformer 把图像切分为 patch,统一架构处理
- **科学计算**:AlphaFold 用注意力建模蛋白质氨基酸交互;时间序列预测、推荐系统也开始 Transformer 化

## 局限与陷阱

- **二次复杂度**:超长序列推理慢、显存吃紧
- **数据饥渴**:小数据下不如带归纳偏置的 CNN/RNN
- **可解释性弱**:注意力权重并不直接等于"模型理解"
- **位置编码外推难**:训练时未见过的长度位置常导致性能崩塌

## 与其他概念的关系

- 核心运算:[[自注意力机制]]
- 必须配套:[[位置编码]]
- 直接产物:[[大语言模型]]、[[BERT]]、GPT 系列
- 工程支撑:GPU [[并发与并行]] 计算、KV-Cache 即带键 [[Hash表]]
- 取代了 [[循环神经网络]] 在 NLP 中的统治地位
- 与 [[Transformer架构|Transformer]] 概念页互为补充(本页强调"架构"层面)

## 参考源

- *Attention is All You Need* (Vaswani et al., 2017)
- raw/AI人工智能/02-理解层/02-03-算法与模型/02-03-04-Transformer架构.md
