---
title: 结构化数据JSON-LD
type: concept
tags: [seo, mature]
sources: [raw/Google SEO/02-理解层-核心机制/]
created: 2026-05-05
updated: 2026-05-05
summary: JSON-LD 是 Google 推荐的结构化数据格式(2015 年起),通过 script 标签嵌入页面声明实体类型与属性,支持 Article、Product、Recipe、FAQ、Event、Organization 等数十种 Schema 类型,是 Rich Results、知识图谱、AI 概览的关键基础设施。
---

# 结构化数据 JSON-LD

## 定义

JSON-LD(JavaScript Object Notation for Linked Data)是 W3C 在 2014 年 1 月发布的结构化数据规范,2015 年被 Google 推荐为首选 [[结构化数据]] 格式,通过 `<script type="application/ld+json">` 嵌入网页 head 或 body 声明实体类型与属性。它是 Schema.org 词汇表在网页上的"机器可读载体",支撑 Rich Results(富结果)、Google 知识图谱、AI Overviews 引用等高级搜索特性。本概念是 [[结构化数据]] / [[Schema.org结构化数据]] 的格式与实操延伸。

## 三种结构化数据格式对比

| 格式 | Google 偏好 | 嵌入方式 | 维护 |
|---|---|---|---|
| Microdata | 旧,逐渐淘汰 | HTML 标签内联 | 与内容耦合,难维护 |
| RDFa | 旧,逐渐淘汰 | HTML 属性 | 同上 |
| **JSON-LD** | **首选** | `<script>` 标签独立 | 易维护,可程序化生成 |

JSON-LD 的优势:
- 与 HTML 解耦,可独立维护
- 易程序化生成(后端模板/CMS 插件)
- 支持引用与图表关系(@graph)
- 可整体压缩与验证

## 基础语法示例

### Article(文章)

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "image": "https://example.com/photo.jpg",
  "datePublished": "2024-08-15T08:00:00+08:00",
  "dateModified": "2024-08-20T10:00:00+08:00",
  "author": {
    "@type": "Person",
    "name": "作者名",
    "url": "https://example.com/author"
  },
  "publisher": {
    "@type": "Organization",
    "name": "网站名",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
</script>
```

### Product(产品)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "产品名",
  "image": "https://example.com/product.jpg",
  "description": "产品描述",
  "sku": "SKU-12345",
  "brand": {"@type": "Brand", "name": "品牌"},
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "CNY",
    "price": "999",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "200"
  }
}
```

### FAQ Page

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "什么是 JSON-LD?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "JSON-LD 是基于 JSON 的结构化数据格式..."
    }
  }]
}
```

## Google 支持的主要 Schema 类型

### Article 类(新闻、博客)

- Article、NewsArticle、BlogPosting

### Product 类(电商)

- Product、Offer、AggregateRating、Review

### Recipe(食谱)

- Recipe、HowTo、Step

### Event(活动)

- Event、VirtualLocation、Place

### LocalBusiness(本地商家)

- LocalBusiness、Restaurant、Store、PostalAddress

### Organization & Person

- Organization、Corporation、NGO、Person

### Q&A 类

- FAQPage、QAPage

### Breadcrumb(面包屑)

- BreadcrumbList、ListItem

### How-To(教程)

- HowTo、HowToStep、HowToTip

### Software & App

- SoftwareApplication、MobileApplication

### Book、Course、JobPosting、VideoObject 等

每类都有专属 Rich Result 在 SERP 中展示。

## 生成与维护

### 手工编写

- 适合静态页、单页应用
- 工具:Schema Markup Generator(Merkle、TechnicalSEO.com)

### CMS 插件

- WordPress:Yoast SEO、Rank Math、Schema Pro、Schema All-in-One
- Shopify:JSON-LD for SEO、Smart SEO
- 大多数 CMS 都有插件自动注入主要 Schema

### 后端模板

- 在服务端模板中根据数据动态注入
- 示例(Next.js):

```jsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify(schemaData)
  }}
/>
```

## 验证工具

1. **Rich Results Test**(Google):验证是否符合 Rich Result 格式
2. **Schema Markup Validator**(Schema.org):验证语法正确性
3. **Search Console → Enhancements**:监控生效情况与错误
4. **Lighthouse SEO 审计**:基础检测

## 常见错误与规避

1. **JSON 语法错误**:逗号、引号问题,先 JSON Parser 验证
2. **必需字段缺失**:Product 必需 name + image + offers/review,缺一被拒
3. **数据与可见内容不一致**:Google 政策严禁——结构化数据必须与页面可见内容相符
4. **多个 Article 在一页**:每页通常只有一个主 Article,多个会引起混乱
5. **过期/不存在的 type**:使用 Schema.org 网站验证 type 名是否仍有效
6. **AggregateRating 无评分基础**:不能"虚标",必须真实评论支撑
7. **图片 URL 不可访问**:Google 抓取不到图片,Schema 失效

## Rich Results 收益

- **CTR 提升**:Rich Result 比纯蓝链点击率高 20-40%
- **品牌权威**:在 SERP 中占更大空间
- **AI Overviews 引用**:有结构化数据的页面更易被 AI 概览引用
- **知识图谱进入**:Organization Schema 是企业进入 Google 知识卡片的前置

## 与其他概念的关系

- 与 [[结构化数据]]:本概念是格式与实操延伸
- 与 [[Schema.org结构化数据]]:词汇表
- 与 [[E-E-A-T操作化]]:Person/Organization Schema 是作者权威信号
- 与 [[Featured Snippet精选摘要]]、[[People Also Ask]]、[[AI Overviews]]:Rich Results 形态
- 与 [[抓取渲染索引]]:索引阶段被解析的关键信号
- 与 [[本地SEO]]:LocalBusiness Schema 是核心
- 与 [[电商SEO]]:Product/Review Schema 是核心

## 参考源

- raw/Google SEO/02-理解层-核心机制/、03-应用层-实践技能/
- schema.org Documentation
- Google Search Central: Structured Data Documentation
- developers.google.com/search/docs/appearance/structured-data
