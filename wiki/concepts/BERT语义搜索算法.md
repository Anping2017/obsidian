---
title: BERT语义搜索算法
type: concept
tags: [seo, 算法, NLP, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.1-Google算法深度解析/, raw/Google SEO/07-进阶专题/]
created: 2026-05-05
updated: 2026-05-05
summary: BERT(Bidirectional Encoder Representations from Transformers)是 Google 2018 年提出、2019 年应用到搜索的双向 Transformer 编码器,大幅提升对长查询、自然语言、上下文意图的理解能力,是 Google 搜索从"关键词匹配"走向"语义理解"的关键里程碑。
---

# BERT 语义搜索算法

## 定义

**BERT(Bidirectional Encoder Representations from Transformers)** 是 Google AI 团队 2018 年 10 月开源的预训练语言模型,2019 年 10 月起应用到 Google 搜索,2020 年覆盖几乎所有英语查询,逐步扩展到 70+ 语言。它是 Google 搜索 **从词袋匹配到深度语言理解** 的转折点,Google 称其为"过去 5 年最重要的算法升级"。

注意:[[BERT]] 已有更技术向的 wiki 页(从 NLP 角度)。本页聚焦 **BERT 在 Google 搜索中的应用与对 SEO 的影响**。

## 核心要点

### 1. BERT 解决的搜索难题

#### 例 1:介词理解

查询:**"巴西人去美国 2019 是否需要签证"**

BERT 之前:Google 不理解 "to USA",可能返回美国人去巴西的签证信息。
BERT 之后:正确理解方向,返回巴西人申请美国签证流程。

#### 例 2:细节区分

查询:**"can you get medicine for someone pharmacy"**

BERT 之前:返回如何获取药物的一般信息。
BERT 之后:理解关键是 "for someone"(代别人取药),返回相关法规要求。

#### 例 3:意图识别

长尾问句、口语化表达、多义词在 BERT 之后都能更精准匹配。

### 2. 双向上下文(Bidirectional)

之前的语言模型(LSTM、GPT-1)单向阅读句子(从左到右),BERT **同时从两边理解每个词的上下文**:

```
"我去 [银行] 取钱"      ← 左右联系都指向"金融机构"
"我去 [银行] 边钓鱼"    ← 左右联系都指向"河岸"
```

这种双向能力靠 Transformer 的 Self-Attention 机制实现。

### 3. 影响最大的查询类型

| 查询类型 | BERT 改进幅度 |
|---|---|
| 长查询(8 词+) | 巨大 |
| 自然语言问句 | 巨大 |
| 介词、连词关键的查询 | 巨大 |
| 口语化、对话式查询 | 巨大 |
| 关键词查询(2-3 词) | 较小(仍以词袋为主) |
| 导航查询(品牌词) | 几乎不变 |

### 4. 对 SEO 的影响

#### 对 SEO 写作的影响

- **关键词堆砌彻底失效**:BERT 看上下文不是关键词出现频率
- **自然语言写作受奖励**:写给人看而非搜索引擎
- **更深入的内容覆盖**:回答 "如何"、"为什么"、"什么时候" 这类语义问题
- **People Also Ask 与 Featured Snippet 选 BERT 解析意图后的最佳答案**

#### 对关键词研究的影响

- **同义词聚类**:不必为每个变体写独立页,BERT 能识别同义
- **意图聚类**:相同意图的查询被合并对待
- **长尾价值上升**:BERT 让长尾理解更准,长尾流量被更精准导向

### 5. BERT 与其他算法的关系

| 算法 | 时间 | 作用 | 与 BERT 关系 |
|---|---|---|---|
| **PageRank** | 1998 | 链接重要性 | 互补 |
| **Hummingbird** | 2013 | 整体语义 | BERT 深化语义理解 |
| **RankBrain** | 2015 | ML 处理新查询 | BERT 是更深的 ML 升级 |
| **MUM** | 2021 | 跨模态、跨语言 | BERT 的下一代 |
| **SGE / AI Overviews** | 2023+ | 生成式答案 | 共用 Transformer 架构 |

## 与其他概念的关系

- **NLP 母体**:[[BERT]](技术细节)/ [[Transformer架构]] / [[自注意力机制]] / [[预训练语言模型]]
- **搜索算法谱系**:[[Google算法更新]] / [[PageRank]] / [[RankBrain]] / [[MUM]]
- **SEO 影响**:[[搜索意图]] / [[长尾关键词]] / [[Topical Authority主题权威]] / [[Helpful Content Update]]
- **跨域**:[[GPT与LLM家族]] / [[语义搜索]] / [[知识图谱]]

## 历史时间线

- **2017** Google "Attention is All You Need" 论文,Transformer 诞生
- **2018.10** BERT 论文与开源
- **2019.10** Google 搜索英语版上线 BERT
- **2020.10** BERT 扩展到 70+ 语言、近 100% 英语查询
- **2021** Google 公布 MUM(BERT 后继)
- **2023** SGE / AI Overviews 上线,Transformer 仍是基础

## SEO 写作启示

1. **写给真人**:BERT 让搜索引擎"读懂"自然语言写作,堆砌反而被惩罚
2. **回答完整问题**:不只点提关键词,要把问题讲透
3. **包含上下文**:让段落能独立成义,被 BERT 提取做 Featured Snippet
4. **结构化数据**:Schema.org 帮助 BERT 解释实体关系
5. **质量优先**:BERT 让 [[Helpful Content Update]] 等质量信号更精准

## 当代演进

- **2021 MUM**:多模态、多语言、1000 倍 BERT 复杂度
- **2023+ AI Overviews**:Gemini 直接合成答案,BERT 仍处理意图理解
- **Multimodal BERT**:支持图、视频、音频
- **AI 时代 SEO 启示**:[[Generative Engine Optimization]] / 优化目标从"关键词"到"被 AI 引用"

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.1-Google算法深度解析/
- raw/Google SEO/07-进阶专题/
- Google Search Central, "Understanding searches better than ever before"(2019)
- Devlin et al.(2018), "BERT: Pre-training of Deep Bidirectional Transformers"
- 关联:[[BERT]] / [[Google算法更新]] / [[搜索意图]] / [[长尾关键词]] / [[Transformer架构]]
