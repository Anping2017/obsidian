---
title: Token
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-01-文本预处理技术.md, raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md]
created: 2026-05-05
updated: 2026-05-05
summary: Token 是大语言模型处理文本的最小单位,通常是子词片段,介于字符和单词之间,Tokenization 直接决定模型输入长度与计费成本。
---

# Token

## 定义

**Token** 是 [[大语言模型]] 处理文本的最小单位。模型并不直接读字符或词,而是先用一个**分词器(Tokenizer)** 把文本切分为 token 序列,再把每个 token 通过查表得到其 [[Embedding]] 输入网络。

主流大模型采用**子词(subword)** 级 tokenization:常见词作为整体 token,稀有词被拆为更小片段(如 "tokenization" → "token" + "ization")。

## 核心要点

**主流 Tokenizer 算法**

| 算法 | 思想 | 代表使用 |
|---|---|---|
| BPE(Byte-Pair Encoding) | 反复合并最频繁字符对 | GPT-2/3/4、Llama |
| WordPiece | 类似 BPE,基于似然合并 | [[BERT]] |
| SentencePiece(Unigram) | 概率最大化的子词模型 | T5、XLNet |
| Tiktoken | OpenAI 的 BPE 实现 | GPT-3.5/4 |

**估算经验值(英文)**

- 1 token ≈ 4 字符 ≈ 0.75 单词
- 一段中文约 1-2 字 / token,但变化很大
- 1000 tokens ≈ 750 英文单词 ≈ 一页文档

**关键工程意义**

- **计费单位**:OpenAI、Anthropic、Google 都按 token 计费(输入 + 输出分开)
- [[上下文窗口]] 限制:模型上下文以 token 数为单位(如 128K、1M)
- 输出速度:每秒 token 数(tokens/sec)是推理速度核心指标
- 资源规划:训练数据规模常以 token 计(如 Llama 3 训练用了 15T tokens)

**特殊 Token**

- BOS / EOS:序列起止标记
- PAD:填充
- 角色标签:`<|user|>`、`<|assistant|>` 用于多轮对话
- 工具调用标记:[[函数调用]] 中的特殊格式

## 和其他概念的关系

- 输入流程:文本 → Tokenizer 切分 → Token ID → [[Embedding]] → [[Transformer架构|Transformer]]
- 容量约束:[[上下文窗口]] 上限以 token 数衡量
- 与 [[大语言模型]] 经济模型直接相关:[[Prompt Caching]] 通过缓存输入 token 大幅降本
- 输出方式:LLM 自回归生成本质是逐 token 采样
- 训练目标:next-token prediction 是预训练标准任务

## 参考源

- raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-01-文本预处理技术.md
- raw/AI人工智能/03-应用层/03-02-自然语言处理/03-02-04-大语言模型原理.md
- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
