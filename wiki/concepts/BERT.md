---
title: BERT
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-03-语言模型发展.md, raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md]
created: 2026-05-05
updated: 2026-05-05
summary: BERT 是 2018 年 Google 提出的双向 Transformer 编码器,通过掩码语言模型预训练颠覆 NLP,开启预训练-微调时代,但在大模型生成式范式下逐渐让位。
---

# BERT

## 定义

**BERT(Bidirectional Encoder Representations from Transformers)** 是 Google 在 2018 年发布的预训练语言模型,采用 [[Transformer架构|Transformer]] 的 Encoder-only 架构,通过**掩码语言模型(MLM)** 与下一句预测(NSP)在大规模文本上预训练,然后在下游任务上微调。

它颠覆了 [[自然语言处理]] 领域,把"通用预训练 + 任务微调"确立为黄金范式,直至 2022 年生成式 LLM 兴起后让出主导地位,但仍在文本理解任务和工业流水线中广泛使用。

## 核心要点

**关键创新**

- 双向编码:每个 token 同时利用左右上下文,而非传统语言模型的单向
- 掩码语言模型:随机遮盖 15% token,让模型预测被遮内容(自监督)
- 下一句预测(后被发现非必要):判断两句是否相邻
- 预训练 + 微调范式:在小数据下游任务上效果飞跃

**典型规模**

- BERT-base:12 层,110M 参数
- BERT-large:24 层,340M 参数
- 现代变体动辄数十亿(如 DeBERTa V3)

**重要变体**

| 变体 | 改进点 |
|---|---|
| RoBERTa(2019) | 去 NSP,更长训练,更好数据 |
| ALBERT | 参数共享降本 |
| DistilBERT | 蒸馏小模型,部署友好 |
| ELECTRA | 替换 token 检测,样本利用率高 |
| DeBERTa | 解耦注意力,效果显著 |
| 多语言 mBERT、XLM-R | 跨语言预训练 |

**优势 vs 局限**

- 优势:理解任务上效果强,推理快(无须自回归生成),可并行编码
- 局限:不擅长生成、对话,大模型时代被解码器架构 GPT 类模型超越

**典型用途(至今)**

- 文本分类、情感分析、命名实体识别
- 句子相似度、检索召回 / 重排
- 作为 [[RAG]] 的检索器(Sentence-BERT、Cross-Encoder)
- 作为下游小模型,用 [[大语言模型]] 蒸馏后部署

## 和其他概念的关系

- 架构基础:[[Transformer架构|Transformer]] 的 Encoder-only 实例
- 训练范式:开创性地确立 [[预训练与微调]] 主导地位
- 现代位置:[[大语言模型]] 中 Decoder-only 的 GPT/Claude/Llama 才是当前主流
- 与 [[Embedding]] 关系:Sentence-BERT 是句嵌入主流方法
- 输入处理:WordPiece 分词,见 [[Token]] 词条

## 参考源

- raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-03-语言模型发展.md
- raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md
