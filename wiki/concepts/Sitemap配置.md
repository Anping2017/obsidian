---
title: Sitemap配置
type: concept
tags: [seo, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/]
created: 2026-05-05
updated: 2026-05-05
summary: Sitemap 配置是把网站重要 URL 以 XML 格式提交给搜索引擎以加速发现与索引的核心技术 SEO 实践,涵盖 Sitemap Index 分片、URL 优先级、更新频率、媒体专用 sitemap、Sitemap 错误诊断等实操维度。
---

# Sitemap 配置

## 定义

Sitemap 配置是把网站重要 URL 以 [[XML Sitemap]] 格式编排并提交给搜索引擎(Google/Bing/Baidu),以加速 URL 发现、引导抓取优先级、补充内链结构未触达页面的技术 SEO 实践。本概念是 [[XML Sitemap]] 的实操延伸,聚焦于大型站点的多 sitemap 体系、错误诊断与高级用法。

## Sitemap 的核心字段

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page1</loc>
    <lastmod>2024-08-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

- **loc**(必需):URL,绝对路径,需 200 状态码
- **lastmod**(强烈建议):最后修改时间,Google 实际重视
- **changefreq**(可选,Google 已忽略):always/hourly/daily/weekly/monthly/yearly/never
- **priority**(可选,Google 已忽略):0.0-1.0
- 每个 sitemap 文件最多 50,000 URL 或 50 MB(未压缩)

## 大型站点 Sitemap 体系

### Sitemap Index(索引文件)

```xml
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2024-08-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-articles.xml</loc>
    <lastmod>2024-08-15</lastmod>
  </sitemap>
</sitemapindex>
```

### 分片策略

| 站点类型 | 推荐分片 |
|---|---|
| 电商 | 按品类(/sitemap-category-1.xml)、产品(分批)、品牌、博客 |
| 新闻媒体 | 按时间(/sitemap-2024-08.xml)、栏目 |
| 大型 SaaS | 按语言(/sitemap-en.xml)、产品文档、登陆页 |
| UGC 论坛 | 按板块、按月份 |

## 媒体专用 Sitemap

### Image Sitemap

```xml
<url>
  <loc>https://example.com/page</loc>
  <image:image>
    <image:loc>https://example.com/img.jpg</image:loc>
    <image:title>图片标题</image:title>
    <image:caption>说明</image:caption>
  </image:image>
</url>
```

### Video Sitemap

```xml
<url>
  <loc>https://example.com/video</loc>
  <video:video>
    <video:thumbnail_loc>https://example.com/thumb.jpg</video:thumbnail_loc>
    <video:title>视频标题</video:title>
    <video:description>描述</video:description>
    <video:content_loc>https://example.com/video.mp4</video:content_loc>
    <video:duration>300</video:duration>
  </video:video>
</url>
```

### News Sitemap

```xml
<url>
  <loc>https://example.com/news/article</loc>
  <news:news>
    <news:publication>
      <news:name>News Site</news:name>
      <news:language>zh-CN</news:language>
    </news:publication>
    <news:publication_date>2024-08-15</news:publication_date>
    <news:title>新闻标题</news:title>
  </news:news>
</url>
```

## 提交方式

### 1. Search Console 提交

- Google Search Console → Sitemaps → 添加新 sitemap → 输入 URL
- Bing Webmaster Tools → Sitemaps → 提交

### 2. robots.txt 引用

```
Sitemap: https://example.com/sitemap.xml
```

- 所有遵循协议的爬虫可发现
- 多个 sitemap 多行声明

### 3. HTTP Ping(2023 年 6 月 Google 弃用)

旧方法 `https://www.google.com/ping?sitemap=URL` 已被 Google 弃用,但 Bing 仍支持。

## 自动化生成

| 平台 | 方案 |
|---|---|
| WordPress | Yoast / RankMath 插件自动 |
| Shopify | 内置 /sitemap.xml |
| Next.js | next-sitemap、@vercel/og 等 |
| Magento | 自动化 cronjob |
| 自定义 | 后端构建任务,每日重新生成 |

最佳实践:**lastmod 必须真实**——不要每次请求都"更新"为今天,Google 会识别后忽略你的 sitemap。

## 错误诊断(Search Console)

| 错误 | 原因 | 修复 |
|---|---|---|
| Couldn't fetch | 服务器无法响应 | 检查可访问性 |
| Sitemap is HTML | 返回 HTML 而非 XML | 检查 Content-Type |
| Sitemap is too large | > 50MB / 50000 URL | 分片 |
| Empty sitemap | 无 URL | 检查生成逻辑 |
| Includes URL not on site | 域名不一致 | 修正 URL |
| Includes blocked URL | URL 被 robots 屏蔽 | 不要把屏蔽 URL 列入 |
| Includes noindex URL | URL 有 noindex meta | 不要列入 |

## 高级技巧

1. **动态优先级排序**:把高价值页面(转化页、热门页)放在 sitemap 顶部
2. **lastmod 严格诚实**:只在真实修改时更新,否则 Google 不再信任
3. **不要把所有 URL 都放**:robots 屏蔽、noindex、canonical 指向他处的 URL 不应在 sitemap 中
4. **数据驱动审计**:Search Console "Sitemaps" 页面看"提交 vs 已索引"比例,识别低质内容
5. **大站点优先 Indexing API**:Google Indexing API 直接通知 URL 更新,但仅限招聘与直播事件类目

## 与其他 SEO 概念的关系

- 与 [[Robots.txt]]:互补——sitemap 引导爬虫去哪,robots 限制爬虫不去哪
- 与 [[抓取预算]]:好的 sitemap 优化抓取预算分配
- 与 [[Canonical规范化标签]]:sitemap 应只列 canonical URL
- 与 [[Hreflang国际化标签]]:多语言 sitemap 配合 hreflang 使用
- 与 [[爬虫优化]]:sitemap 是爬虫优化的输入信号
- 与 [[企业级SEO]]:大型站点 sitemap 设计是核心环节
- 与 [[Search Console配置]]:提交与监控载体

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/
- Google Search Central: Build and submit a sitemap
- sitemaps.org 协议规范
