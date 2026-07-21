---
title: RAG
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md, raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md]
created: 2026-05-05
updated: 2026-05-11
summary: RAG(检索增强生成)在生成前先从外部知识库检索相关片段塞入 prompt,为大语言模型注入最新、专属、可验证的事实,显著降低幻觉,是企业级 LLM 应用最主流的架构。
---

# RAG

## 定义

**RAG(Retrieval-Augmented Generation,检索增强生成)** 是把外部知识检索与 [[大语言模型]] 生成相结合的范式:回答问题前,先用查询去向量库或搜索引擎检索若干相关文档片段,把这些片段连同原始问题一起塞入 prompt,让模型基于真实材料生成答案。

它把"参数化记忆"(模型权重)与"非参数化记忆"(外部文档)分离,让模型像"开卷考试"一样作答。由 Lewis et al.(2020,NeurIPS)提出,如今已是企业级 LLM 应用最主流的架构。

> 中文社区常用全称"检索增强生成",与 RAG 指同一概念,可互换。

## 核心要点

### 标准流水线

```
1. 离线索引(Indexing)
   文档 → 切块(chunking)→ Embedding → 向量库

2. 在线查询(Querying)
   用户问题 → Embedding → 向量库相似度检索 → Top-K 片段

3. 增强生成(Generation)
   [Top-K 片段 + 问题] → LLM → 答案 + 引用
```

### 关键组件与决策点

| 组件 / 阶段 | 作用 | 常见实现 / 关键决策 |
|---|---|---|
| **切块(Chunking)** | 把长文档切成段 | 大小(常 200-1000 token)、重叠、按语义/段落/层次切 |
| **嵌入(Embedder)** | 文本转向量 | OpenAI text-embedding-3、BGE、Cohere |
| **向量库** | 存储与召回向量 | Pinecone、Milvus、Weaviate、Chroma、pgvector |
| **重排(Reranker)** | 二次精排 Top-K | Cohere Rerank、bge-reranker、cross-encoder |
| **Prompt 拼装** | 组织上下文 | 引用格式、上下文优先级、系统指令 |
| **生成器** | 基于上下文回答 | GPT-4、Claude、Gemini 等 |
| **评估** | 质量度量 | 检索召回率、生成忠实度、回答相关性 |

### 检索方式

- **稠密检索**(Dense Retrieval):基于 Embedding 的语义相似度,即 [[向量召回]]
- **稀疏检索**(Sparse Retrieval):BM25 等关键词匹配,擅长精确名词
- **混合检索**(Hybrid):稠密 + 稀疏融合,工业界主流
- **多跳检索**(Multi-hop):一次召回不够时迭代多次

### 为何主流

- 解决 [[幻觉]]:模型基于真实文档生成,可校验
- 解决知识过时:更新知识库即可,无须重训模型
- 解决私有知识:企业内部文档不进训练,但可检索
- 成本低于微调:更新效率高、可解释性强

### Advanced RAG 进化方向

| 模式 | 思路 |
|---|---|
| **HyDE** | 让模型先生成"假设答案",用假答案去检索 |
| **Self-RAG** | 模型自己决定是否需要检索、检索什么、并自评检索质量 |
| **GraphRAG** | 把文档构建为知识图谱,沿图遍历召回 |
| **Agentic RAG** | 把检索包装为工具,通过 [[Function Calling]] 多轮调用 |
| **Long-Context** | 长上下文模型(100K+)部分替代检索,二者关系重新平衡 |

### 评估指标

- **检索质量**:Recall@K、MRR、NDCG
- **生成质量**:Faithfulness(忠实度)、Answer Relevance、Context Precision
- **端到端**:RAGAS、TruLens、人工标注

## 典型应用 / 主流框架

- **企业知识库**:把 Confluence、Notion、SharePoint 接入 RAG,做内部问答
- **客服机器人**:基于产品文档与历史工单回答用户
- **法律 / 医疗 / 金融**:严格引用源文档,降低合规风险
- **代码助手**:Cursor、Continue 把代码库做 RAG,实现"懂你项目"的补全
- **学术研究**:Elicit、Consensus、ChatPaper —— 检索论文 + 总结
- **框架工具**:LangChain、LlamaIndex、Haystack、Dify、RAGFlow

## 局限与陷阱

| 问题 | 描述 |
|---|---|
| **切块陷阱** | 切太大召回噪声多,切太小破坏语义连贯 |
| **语义鸿沟** | 问题与文档表述差异大时,Embedding 相似度失效,需混合 BM25 |
| **多跳推理** | 答案需多个文档拼接时,单轮检索不够 |
| **来源冲突** | 多个文档说法矛盾,模型无判断标准 |
| **噪声放大** | 检索到无关文档反而误导模型 |
| **更新一致性** | 文档更新后,向量库需要重建索引 |
| **幻觉残留** | 即使有上下文,模型仍可能脑补;需 prompt 约束"仅基于上下文" |
| **成本** | 长上下文 + 多次检索显著抬高 token 成本 |

## 和其他概念的关系

- 核心组件:[[Embedding]] + [[向量数据库]] + [[大语言模型]]
- 检索机制:依赖 [[向量召回]](稠密)与 BM25(稀疏)
- 主要价值:大幅降低 [[幻觉]] 风险,提供可溯源答案
- 与 [[预训练与微调]] 对比:更新知识不必动权重,运维更轻
- 与 [[上下文窗口]] 关系:窗口越大,可塞入更多检索片段,但二者并非互相替代
- 与 [[Function Calling]] 协同:RAG 解决"查文档",函数调用解决"调 API",[[AI Agent]] 中常并存
- 基座来自 [[预训练语言模型]];跨模态延伸见 [[多模态学习]] 的图文检索
- 数据安全场景可与 [[联邦学习]] 结合,做不出本地的知识检索
- 工程优化:[[Prompt Caching]] 可缓存长固定指导部分降低成本
- 计算机科学基础:精确召回常用 [[Hash表]] 去重;分布式向量检索分片路由依赖 [[一致性Hash]];混合检索的关键词通道与 [[搜索引擎优化]] 的倒排索引、BM25 共享技术栈

## 参考源

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020
- Gao et al., *Retrieval-Augmented Generation for Large Language Models: A Survey*, 2023
- Asai et al., *Self-RAG: Learning to Retrieve, Generate, and Critique*, 2023
- Microsoft Research, *GraphRAG: Unlocking LLM Discovery on Narrative Private Data*, 2024
- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
- raw/AI人工智能/04-前沿技术专题/04-08-AI Agent技术.md
