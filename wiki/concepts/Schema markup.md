---
title: Schema markup
type: concept
tags: [seo, 技术SEO, 结构化数据, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/04-结构化数据.md]
created: 2026-05-05
updated: 2026-05-05
summary: Schema markup 是 Google/Bing/Yahoo/Yandex 2011 年联合推出的语义化数据标记,基于 Schema.org 词汇表用 JSON-LD/Microdata/RDFa 给网页内容打机器可读标签;它让搜索引擎理解实体与关系,触发富结果,是 SEO 进入 AI 时代的关键基础设施。
---

# Schema markup

## 定义

**Schema markup**(也称 Structured Data Markup)是基于 [[Schema.org结构化数据]] 词汇表,用 JSON-LD、Microdata 或 RDFa 三种格式,**给网页内容添加机器可读标签** 的实践。它让搜索引擎与 AI 不只看到"文字",还能理解 **"这是一篇文章/产品/食谱/活动/人物/组织,它的属性是 X 与 Y"**。

它是 [[搜索引擎优化]] 进入 [[AI Overviews]]、[[E-E-A-T]]、[[Topical Authority主题权威]] 时代的关键基础设施。

注:本页是 [[结构化数据]] 与 [[Schema.org结构化数据]] 的实操扩展。

## 核心要点

### 1. 三种实现格式

#### JSON-LD(主流推荐)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "标题",
  "author": {
    "@type": "Person",
    "name": "作者名"
  },
  "datePublished": "2026-04-15",
  "image": "https://..."
}
</script>
```

放在 `<head>` 或 `<body>` 任何位置,不影响页面渲染。Google 优先推荐。

#### Microdata
```html
<article itemscope itemtype="https://schema.org/Article">
  <h1 itemprop="headline">标题</h1>
  <span itemprop="author">作者名</span>
</article>
```

嵌入在 HTML 中,与显示内容耦合。

#### RDFa
类似 Microdata 但用不同属性。最少使用。

### 2. 主要类型与触发的富结果

| Schema 类型 | 触发的 SERP 特性 |
|---|---|
| **Article / NewsArticle** | 新闻轮播、Top Stories |
| **Product** | 产品价格、评分、库存富片段 |
| **Recipe** | 烹饪时间、营养、评分轮播 |
| **FAQPage** | 折叠 FAQ 富片段 |
| **HowTo** | 步骤化富片段 |
| **Event** | 活动卡片 |
| **VideoObject** | 视频缩略图、Key Moments |
| **LocalBusiness** | 知识面板、地图 |
| **Person** | 知识面板 |
| **Organization** | 知识面板、Sitelinks |
| **Course** | 课程信息 |
| **JobPosting** | Google for Jobs |
| **BreadcrumbList** | 面包屑导航 |
| **Review** | 评分星级 |
| **Recipe + Aggregate Rating** | 食谱评分 |
| **SoftwareApplication** | 应用评分、价格 |

### 3. 富结果的 SEO 价值

#### a) 提升 CTR
富结果在 SERP 占据更大视觉空间,CTR 提升 30-150%(具体看类型)。

#### b) 触发零点击但建立品牌
即使用户不点击,信息已通过富结果展示——是 [[零点击搜索]] 时代的品牌曝光。

#### c) 知识图谱集成
Schema 帮助 Google 把内容关联到 [[Google知识图谱]] 实体,提升 [[E-E-A-T]] 与 [[Topical Authority主题权威]]。

#### d) AI Overviews 引用
[[AI Overviews]] 与 [[ChatGPT Search]] 等 AI 搜索更易引用结构化清晰的内容。

#### e) Voice Search
语音助手优先选 FAQ Schema 与简洁段落作为答案。

### 4. 关键实践原则

#### a) 真实性
Schema 标记必须 **反映页面真实可见内容**。隐藏文字、虚假评分等会被 Google 视为作弊。

#### b) 完整性
关键属性必须填全(产品的 price、availability、rating)。半全 Schema 可能不触发富结果。

#### c) 可见性
被标记的内容应该是用户能看到的。"不可见但有标记"是违规。

#### d) 专一性
如果一个页面是产品详情页,用 Product;不要又加 Article 又加 Product 造成混淆。

#### e) 唯一性
同一类型内容只用一个 Schema 标记,避免重复嵌套。

### 5. 工作流

```
1. 内容审计:每个页面类型应该用什么 Schema?
   ↓
2. 模板设计:CMS 中给每种内容类型配 Schema 模板
   ↓
3. 字段映射:把 CMS 字段映射到 Schema 属性
   ↓
4. 实施:输出 JSON-LD
   ↓
5. 测试:用 Schema.org Validator + Google Rich Results Test
   ↓
6. 监测:GSC 看是否生效与是否有错误
   ↓
7. 迭代:补充缺失字段、修复错误
```

### 6. 工具

| 工具 | 用途 |
|---|---|
| **Google Rich Results Test** | 测单页是否能触发富结果 |
| **Schema.org Validator** | 校验 Schema 语法 |
| **Google Search Console** | 监测全站 Schema 生效与错误 |
| **Schema App / Yoast / RankMath** | 自动化生成 Schema |
| **Merkle Schema Markup Generator** | 在线生成各类型 Schema |

### 7. 常见错误

| 错误 | 影响 |
|---|---|
| **JSON-LD 语法错误** | Google 不解析 |
| **属性值类型错误**(string 应该是 date) | 部分忽略 |
| **必填字段缺失** | 不触发富结果 |
| **隐藏内容标记** | 被视为作弊 |
| **错误类型选择** | 不触发或低相关 |
| **重复嵌套** | 可能冲突 |
| **Schema 与可见内容不一致** | 违反指南 |

### 8. 进阶:实体关联

通过 Schema 把页面内容关联到 [[Google知识图谱]] 实体:

```json
{
  "@type": "Person",
  "name": "张三",
  "sameAs": [
    "https://en.wikipedia.org/wiki/Zhang_San",
    "https://twitter.com/zhangsan",
    "https://linkedin.com/in/zhangsan"
  ]
}
```

`sameAs` 让 Google 把"张三"与维基/Twitter/LinkedIn 上的同一实体关联,大幅强化 [[E-E-A-T]] 中的 Author Authority。

### 9. AI Overviews 时代的 Schema 战略

#### 强化 FAQ Schema
让常见问题易被 [[AI Overviews]] 提取作为答案。

#### HowTo Schema
分步教程极易被 AI 引用作为完整答案。

#### Article Schema 加 author
作者实体关联强化 E-E-A-T,是被 AI 引用的关键信号。

#### Product Schema 完整字段
价格、库存、评分、规格——AI 比较型查询会综合多源数据。

#### LocalBusiness 全字段
本地查询的 AI 答案高度依赖 Schema 数据。

## 与其他概念的关系

- **核心母体**:[[Schema.org结构化数据]] / [[结构化数据]] / [[技术SEO]]
- **战略配套**:[[E-E-A-T]] / [[E-E-A-T操作化]] / [[Topical Authority主题权威]] / [[页面SEO]]
- **AI 时代**:[[AI Overviews]] / [[Topical Authority主题权威]] / [[Featured Snippet精选摘要]] / [[零点击搜索]]
- **跨域**:[[Google知识图谱]] / [[实体识别]] / [[BERT语义搜索算法]]

## 业内共识

Schema markup 已从 "nice-to-have" 变成 **基本卫生**——大型电商、新闻、SaaS、本地业态没有 Schema 几乎等于在 SEO 上自废武功。在 [[AI Overviews]] 时代,缺 Schema = 不被 AI 引用 = 失去新形态心智份额。

## 当代演进

### 新类型不断推出
Schema.org 持续添加类型:Course、Quiz、HowTo、CreativeWorkSeason、AcademicArticle 等。

### Speakable Schema(语音)
为语音助手设计的内容片段标记。

### Job Posting & For Jobs
Google for Jobs 的核心是 JobPosting Schema。

### Open Graph & Twitter Card 协同
社交分享时除了 Schema,Open Graph 与 Twitter Card 同样重要。

### AI 对 Schema 的依赖加深
LLM 训练过程中,结构化数据是高质量信号。提供 Schema 让 AI 更易"信任"内容。

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/04-结构化数据.md
- Google Search Central, Structured Data Documentation
- Schema.org 官网
- 关联:[[Schema.org结构化数据]] / [[结构化数据]] / [[技术SEO]] / [[E-E-A-T]] / [[AI Overviews]]
