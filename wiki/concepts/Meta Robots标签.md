---
title: Meta Robots标签
type: concept
tags: [seo, stub]
sources: []
created: 2026-05-11
updated: 2026-05-11
summary: Meta Robots 标签是 HTML head 中控制搜索引擎爬虫抓取/索引/跟随链接行为的元数据,与 Robots.txt 是页面级 vs 站点级的互补 SEO 控制。
---

# Meta Robots标签

## 定义

**Meta Robots 标签**(`<meta name="robots">`)是 HTML `<head>` 中放置的元数据,用于向搜索引擎爬虫指示**具体页面**的抓取与索引行为。相比 [[Robots.txt]] 的站点级黑白名单,Meta Robots 是**页面级**、更精细的控制。

## 核心要点

### 常用指令

| 指令 | 效果 |
|---|---|
| `index` / `noindex` | 允许 / 禁止把本页放进索引 |
| `follow` / `nofollow` | 允许 / 禁止跟随本页出链 |
| `noarchive` | 不缓存本页快照 |
| `nosnippet` | 不显示描述摘要 |
| `notranslate` | 不提供翻译选项 |
| `noimageindex` | 不索引本页图片 |
| `unavailable_after: YYYY-MM-DD` | 到期后从索引移除 |

### 示例

```html
<meta name="robots" content="noindex, follow">
<meta name="googlebot" content="index, nosnippet">
```

多个爬虫可分别指定(googlebot / bingbot / etc.)。

### 与 X-Robots-Tag HTTP 头

对非 HTML 资源(PDF、图片),HTTP 响应头 `X-Robots-Tag` 起同样作用。

### 常见误区

- 用 `noindex` 阻止索引后又用 [[Robots.txt]] 屏蔽 → 爬虫看不到 noindex,反而无法执行
- 分页/筛选页大量 noindex 但没配 [[Canonical规范化标签]] → 权重稀释

## 和其他概念的关系

- 与 [[Robots.txt]]、[[XML Sitemap]]、[[Canonical规范化标签]]、[[Hreflang国际化标签]] 构成 SEO 抓取索引控制的**四件套**
- 属于 [[技术SEO]] 基础
- 影响 [[搜索引擎优化]] 中的可索引性

## 参考源

- Google Search Central 文档
