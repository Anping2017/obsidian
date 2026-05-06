---
title: XML Sitemap
type: concept
tags: [seo, 技术SEO, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/, raw/Google SEO/03-SEO工具应用/]
created: 2026-05-05
updated: 2026-05-05
summary: XML Sitemap 是 2005 年 Google 推出、Yahoo/MSN 跟进的标准协议,以 XML 列出网站重要 URL 帮搜索引擎更全面地发现页面;sitemap 不保证索引但显著提升发现效率,大型站、新站、深层页、媒体内容受益最大。
---

# XML Sitemap

## 定义

**XML Sitemap** 是 [[技术SEO]] 的页面发现工具,2005 年 6 月由 Google 推出,2006 年 11 月与 Yahoo、Microsoft 联合标准化为 sitemaps.org 协议。它是 XML 格式文件,列出网站希望被搜索引擎发现的重要 URL,可附带 lastmod(最后更新时间)、changefreq(更新频率)、priority(相对优先级)等元数据。

Sitemap **不保证页面被索引**,但能显著提高 [[Google搜索工作原理]] 的发现效率,对大型站、新站、深层页、最近更新的内容、视频/图片等富媒体内容效果最显著。

## 核心要点

### 1. 基本格式

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page1</loc>
    <lastmod>2026-04-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### 2. 限制

- 单个 sitemap 最多 50,000 URL 或 50MB(未压缩)
- 超出需拆分为多个 + sitemap index
- 必须 UTF-8 编码,URL 完全限定(不能相对路径)

### 3. Sitemap Index(索引)

```xml
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2026-04-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
  </sitemap>
</sitemapindex>
```

### 4. 专门 sitemap 类型

| 类型 | 用途 |
|---|---|
| **常规 XML** | 普通页面 |
| **Image sitemap** | 图片 SEO,标 `<image:loc>` |
| **Video sitemap** | 视频内容,带时长、缩略图 |
| **News sitemap** | 新闻内容,2 天有效 |
| **Hreflang in sitemap** | 多语言关联 |

### 5. 提交方式

- 在 [[Search Console配置]] / Bing Webmaster 直接提交
- 在 [[Robots.txt]] 中声明:`Sitemap: https://example.com/sitemap.xml`
- ping URL:`https://www.google.com/ping?sitemap=...`(Google 2023 年废弃)

### 6. 哪些页面应该列入

✅ 应该列入:
- 重要的、想被索引的页面
- 最新更新的内容
- 深层页(从首页 4+ 跳)
- 难以通过链接发现的页面

❌ 不应列入:
- noindex 页
- 被 robots.txt Disallow 的页
- 重定向页(放 301 后的目标 URL)
- 重复内容(只放 canonical 版本)
- 4xx/5xx 错误页

### 7. 动态生成 vs 静态 XML

电商、CMS 站通常 **动态生成**(每次有新产品自动加入),博客可定期重生成。WordPress、Yoast、Rank Math、Next.js 均自动支持。

## 与其他概念的关系

- **配套**:[[Robots.txt]] / [[Canonical规范化标签]] / [[Hreflang国际化标签]]
- **上层**:[[技术SEO]] / [[爬虫优化]] / [[抓取预算]]
- **诊断**:[[Search Console配置]] 的 Sitemaps 报告与 Coverage 报告
- **跨域**:[[国际SEO]] / [[电商SEO]] / [[企业级SEO]]

## 重要性等级(按场景)

| 场景 | sitemap 重要性 |
|---|---|
| 千页以下博客 | 中(站内链接通常够) |
| 大型电商(百万+ URL) | 极高(抓取预算关键) |
| 新站点 | 极高(无外链时唯一发现路径) |
| 多语言站 | 高(配合 hreflang) |
| 富媒体站(视频/图) | 高(专属 sitemap 提升曝光) |
| 频繁更新的新闻站 | 极高(News Sitemap) |

## 当代演进

- **2023 年 Google 弃用 ping**:必须通过 GSC 提交
- **lastmod 信号在 2023 后受重视**:Google 工程师明确说会使用,但要诚实(假更新会被识破)
- **changefreq/priority 已被 Google 忽略**:多年只看实际抓取行为
- **AI 时代**:LLM 训练爬虫(GPTBot、Claude-Web)也读 sitemap

## 工具

- Yoast SEO / Rank Math(WordPress 自动)
- Screaming Frog 生成与验证
- Sitemap-generator-cli(Node.js)
- XML-Sitemaps.com(在线小工具)

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/
- sitemaps.org 协议
- 关联:[[技术SEO]] / [[Robots.txt]] / [[Canonical规范化标签]] / [[爬虫优化]] / [[Search Console配置]]
