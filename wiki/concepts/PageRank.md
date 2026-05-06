---
title: PageRank
type: concept
tags: [seo, 算法, 链接分析, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.1-Google算法深度解析/01-Google核心算法.md]
created: 2026-05-05
updated: 2026-05-05
summary: PageRank 是 Larry Page 与 Sergey Brin 1996 年提出的网页重要性算法,通过把网页与链接建模为图、迭代计算每页的"投票权重",成为 Google 的搜索排名基石;虽然 2016 年公开 Toolbar PR 已停,但 PageRank 内核仍是现代排名信号之一。
---

# PageRank

## 定义

**PageRank(PR)** 是 Larry Page 与 Sergey Brin 1996 年在斯坦福读博期间发明的算法,1998 年发表于论文 *"The Anatomy of a Large-Scale Hypertextual Web Search Engine"*——也就是 Google 创始论文。PageRank 是 Google 的奠基算法,把整个互联网建模为有向图(网页是节点、链接是边),通过迭代计算每个网页的"重要性分数"。核心直觉:**被重要网页链接的网页也重要**。

虽然 Google 2016 年关闭了公开的 Toolbar PageRank,但 PageRank 内核仍是 Google [[Google算法更新]] 体系的关键排名信号之一。它是 [[链接建设]]、[[域权威]]、[[内链优化]] 的理论基石。

## 核心要点

### 1. 直觉公式

```
PR(A) = (1-d)/N + d × Σ [ PR(Ti) / C(Ti) ]
```

- A 是当前页面
- T1...Tn 是所有指向 A 的页面
- C(Ti) 是 Ti 的出链总数
- d 是阻尼系数,通常 0.85
- N 是网络中页面总数

直观:**A 的得分 = 所有指向 A 的页面将其得分平分到 A 的总和 × 0.85,再加上一个随机访问基线**。

### 2. 三大核心思想

#### a) 链接是投票
被链接 = 收到一票。投票越多越重要。

#### b) 投票有权重
重要网页的投票更重(纽约时报的链接 > 个人博客的链接)。

#### c) 投票被稀释
出链多的页面每条链接的权重小(出 2 链各 1/2,出 100 链各 1/100)。

### 3. 阻尼系数 d 的含义

阻尼 d=0.85 意味着:**用户 85% 概率沿链接走,15% 随机跳到任何页面**。这模拟了真实用户行为,也防止 PageRank 被陷入"链接陷阱"(无出链的死页面)。

### 4. 为什么是革命性的

1998 年前的搜索引擎(AltaVista、Lycos)只看页面内容关键词匹配,容易被关键词堆砌作弊。PageRank 把 **整个网络的链接结构** 作为信号,作弊难度陡升,质量结果显著优。这是 Google 颠覆搜索市场的核心技术。

### 5. PageRank 的演进

| 时期 | 状态 |
|---|---|
| **1998-2007** | 核心排名信号,Toolbar PR 公开 |
| **2008-2014** | 算法不断细化,但仍是核心 |
| **2014-2016** | Google 不再更新 Toolbar PR |
| **2016** | Toolbar PR 完全关闭 |
| **2016-至今** | PR 内核仍在,但与 200+ 信号一起使用,且基于话题、信任、新鲜度等加权 |

### 6. 现代代替指标

由于 Google 不再公开 PR,SEO 工具用各自的反向链接指标作为代理:

| 工具 | 指标 | 范围 |
|---|---|---|
| **Ahrefs** | DR(Domain Rating)/ UR(URL Rating)| 0-100 |
| **Moz** | DA(Domain Authority)/ PA | 0-100 |
| **Semrush** | Authority Score | 0-100 |
| **Majestic** | Trust Flow / Citation Flow | 0-100 |

这些都不是真实 PR,但能近似排序。

### 7. PageRank 的演化:话题敏感、个性化

#### a) Topic-Sensitive PageRank(2002, Haveliwala)
不同话题独立计算 PR,体育站对体育主题的 PR 高,对科技主题低。

#### b) Personalized PageRank
每个用户的兴趣偏好下的 PR,推荐系统基础。

#### c) TrustRank(2004, Yahoo)
从一组种子可信网站出发的 PR 变体,打击垃圾。

#### d) HITS / Hubs & Authorities(Kleinberg 1999)
平行算法,把页面分为 Hub(优质指向他人)与 Authority(被优质 Hub 指向)。

### 8. SEO 实践含义

- **链接建设的本质就是积累 PageRank 信号**
- **链接质量 > 数量**:1 个权威站链接 > 100 个论坛链接
- **内链优化分配 PageRank**:把 PageRank 流向重要页面
- **避免 PageRank 流失**:nofollow 一些不重要的出链
- **沉重的页面引出 PageRank**:广告、Footer 链接稀释主内容 PR

## 与其他概念的关系

- **直接关联**:[[链接建设]] / [[内链优化]] / [[Google搜索工作原理]] / [[Google算法更新]]
- **算法谱系**:[[HITS算法]] / [[TrustRank]] / [[Topical Authority主题权威]]
- **理论母体**:图论、马尔可夫链(PR 是马尔可夫链的稳态分布)、谷歌矩阵
- **现代演进**:[[E-E-A-T]] / [[Helpful Content Update]] 等内容信号补充链接信号
- **学术影响**:被引用 60000+ 次,是计算机科学最有影响力论文之一

## 趣闻

- "PageRank" 是 Larry Page 自己的姓双关,不是"网页排名"
- 算法基于 Eugene Garfield 1955 年学术引用分析(Citation Analysis)的灵感
- 1998 年 Page 与 Brin 曾愿以 100 万美元卖给 Yahoo 被拒
- 阻尼系数 0.85 没有理论最优,是经验取值

## 当代地位

- PageRank 仍是 Google 排名的"核心引力" 之一,但与 BERT、MUM、Helpful Content 等内容/语义/质量信号共同作用
- 在 [[E-E-A-T]] 时代,链接的"主题相关性"和"权威性"比纯数量更重要
- AI 搜索时代,PageRank 思想被扩展到 知识图谱实体重要性、模型训练数据加权 等领域

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.1-Google算法深度解析/01-Google核心算法.md
- Page, Brin, Motwani, Winograd(1998), "The PageRank Citation Ranking"
- 关联:[[Google搜索工作原理]] / [[链接建设]] / [[Google算法更新]] / [[拉里·佩奇]] / [[谢尔盖·布林]]
