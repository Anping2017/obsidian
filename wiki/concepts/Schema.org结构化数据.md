---
title: Schema.org结构化数据
type: concept
tags: [seo, mature]
sources: [raw/SEO/02-SEO技术理解/02-1-网站技术SEO/页面技术优化.md, raw/SEO/01-SEO基础认知/01-2-搜索引擎工作原理/搜索引擎索引建立.md]
created: 2026-05-05
updated: 2026-05-05
summary: Google/Bing/Yandex 联合维护的语义词汇表,标记网页内容让搜索引擎理解实体关系。
---

# Schema.org结构化数据

## 定义

Schema.org 是 Google、Bing、Yahoo、Yandex 四大搜索引擎在 2011 年联合发起、共同维护的网页结构化数据词汇表(Vocabulary)。它定义了一套类型(Type)和属性(Property)体系,如 Organization、Person、Product、Article、Recipe、Event、Review,让网页可以用机器可读的方式声明"这个内容是什么实体、有哪些属性、与其他实体什么关系"。这是 [[结构化数据]] 在搜索引擎生态中的事实标准,直接驱动 [[SERP特征]] 中的 [[Rich Result]]、[[Featured Snippet]]、知识图谱卡片。

## 核心要点

**核心类型(高频使用)**:

- **Organization / LocalBusiness**:公司基础信息,LocalBusiness 子类型适用本地服务/门店,关联 [[本地SEO]] 和 [[Google Business Profile]]。
- **Product**:商品名称、价格、库存、品牌、型号、变种、聚合评分。电商必备。
- **Article / NewsArticle / BlogPosting**:文章作者、发布时间、修改时间、封面图。新闻 SEO 标配。
- **Recipe**:菜谱字段(食材、步骤、烹饪时间、热量),美食类网站红利字段。
- **Event**:线下/线上活动,日期、地点、票务。
- **FAQPage**:问答列表,直接展示在搜索结果。
- **HowTo**:分步操作指南,被 Google 当作 "How-to Rich Result" 展示。
- **Review / AggregateRating**:用户评分,显示在搜索结果中的星级。
- **BreadcrumbList**:面包屑路径,SERP 中显示完整路径而非长 URL。
- **VideoObject**:视频缩略图、时长、上传时间,关键时刻(Key Moments)分段。
- **JobPosting**:招聘信息,Google for Jobs 的入口。
- **Course / Quiz / Book / Movie / Recipe**:垂直类别。

**三种语法格式**:

| 格式 | 描述 | 推荐度 |
|---|---|---|
| **JSON-LD** | 嵌入 `<script type="application/ld+json">` 标签 | Google 强烈推荐 |
| Microdata | HTML 标签中的 itemscope/itemprop | 旧式,与内容耦合 |
| RDFa | 类似 Microdata 的属性扩展 | 学术/政府偏好 |

**JSON-LD 范例**(产品页):
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "iPhone 15 Pro",
  "image": "https://example.com/img.jpg",
  "brand": {"@type": "Brand", "name": "Apple"},
  "offers": {
    "@type": "Offer",
    "price": "999.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "1245"
  }
}
```

**SEO 价值**:

- **Rich Result(富媒体结果)**:CTR 提升 20-30%,星级、价格、面包屑等直接展示。
- **知识图谱(Knowledge Graph)**:Organization 加 sameAs 指向官网/Wiki/社交,品牌实体被识别。
- **语义理解**:让 Google 准确理解内容结构(标题 vs 内容 vs 评论 vs 价格)。
- **AI Overview / AI Search**:LLM 生成的搜索摘要会优先引用结构化数据,这是 GEO(Generative Engine Optimization)的核心。
- **垂直产品入口**:Google for Jobs、Google Travel、Google Shopping 等都靠 Schema 喂数据。

**实施流程**:

1. **识别页面类型**:首页 = Organization;文章 = Article;商品 = Product。
2. **必填属性 + 推荐属性**:每种类型查 Google 官方文档。
3. **JSON-LD 输出**:CMS 模板自动生成,常用插件 Yoast / Rank Math / Schema App。
4. **测试**:Google Rich Results Test、Schema Markup Validator。
5. **GSC 监控**:Search Console 中"增强功能"页查看错误与展示量。

**反模式**:

- 标记不在页面可见的内容(Google 视为垃圾标记)。
- AggregateRating 没有真实评论支撑(违反 Google 政策,可能被处罚)。
- 同一页面多个 Schema 互相冲突。
- 标记错误类型(如新闻文章用 Product)。
- 不做面包屑标记 → 错失 SERP 展示优化。

## 和其他概念的关系

Schema.org 是 [[结构化数据]] 在网页生态的具体规范,与 OpenGraph、Twitter Card 等社交协议互补。它是 [[技术SEO]] 与 [[页面SEO]] 的交集——同时是技术实施任务与内容信号增强。

在 [[Google搜索工作原理]] 中,Schema 直接喂给 Google 的语义索引层,影响 [[搜索意图]] 匹配与 [[E-E-A-T]] 信号识别。它与 [[AI对营销与SEO的影响]] 中的 GEO 趋势深度关联——LLM-based 搜索引擎(SGE、Perplexity)依赖结构化数据形成可信引用。

[[本地SEO]] 中的 LocalBusiness 标记是 [[Local Pack]] 排名的关键。[[电商SEO]] 中 Product + Review 标记直接影响 SERP CTR。Schema 也是 [[网站审计]] 的重要检查项——大型站点常因模板不当导致大规模 Schema 错误。

## 参考源

- raw/SEO/02-SEO技术理解/02-1-网站技术SEO/页面技术优化.md
- raw/SEO/01-SEO基础认知/01-2-搜索引擎工作原理/搜索引擎索引建立.md
- raw/SEO/04-SEO策略精通/04-1-高级SEO技术/电商SEO技术.md
