---
title: Robots Meta Tag
type: concept
tags: [seo, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/]
created: 2026-05-05
updated: 2026-05-05
summary: Robots Meta Tag 是页面级别的爬虫指令,通过 head 内 meta 标签或 X-Robots-Tag HTTP 头声明 noindex/nofollow/noarchive/nosnippet 等指令,与 robots.txt 互补——robots.txt 阻止抓取,Robots Meta 控制索引与展示。
---

# Robots Meta Tag

## 定义

Robots Meta Tag(机器人元标签)是页面级别的爬虫指令机制,通过两种方式声明:
1. **HTML head 内的 meta 标签**:`<meta name="robots" content="noindex, nofollow">`
2. **HTTP Response Header**:`X-Robots-Tag: noindex, nofollow`(适用于非 HTML 文件如 PDF、图片)

它与 [[Robots.txt]] 互补:**robots.txt 阻止抓取**(爬虫不下载),**Robots Meta 控制索引与展示**(下载后决定如何处理)。是技术 SEO 中处理"内容存在但不希望出现在搜索结果"场景的核心工具。

## 主要指令

### 索引控制

| 指令 | 效果 |
|---|---|
| index | 允许索引(默认) |
| **noindex** | 不索引,即不在搜索结果出现 |
| none | = noindex + nofollow |
| all | = index + follow(默认) |

### 链接跟踪

| 指令 | 效果 |
|---|---|
| follow | 跟踪页内链接(默认) |
| **nofollow** | 不跟踪页内链接,不传递权重 |

### 缓存与归档

| 指令 | 效果 |
|---|---|
| **noarchive** | 不显示 Google 缓存版本 |
| **nocache** | 同 noarchive |

### 摘要控制

| 指令 | 效果 |
|---|---|
| **nosnippet** | 不展示文本摘要 |
| **max-snippet:50** | 限制摘要最多 50 字符 |
| **max-image-preview:large** | 控制图片预览大小:none/standard/large |
| **max-video-preview:30** | 视频预览最长 30 秒 |
| **notranslate** | 不在搜索结果中提供翻译 |

### 时间控制

| 指令 | 效果 |
|---|---|
| **unavailable_after:Date** | 指定日期后从索引中移除 |

### 其他

| 指令 | 效果 |
|---|---|
| **noimageindex** | 图片不索引 |
| **indexifembedded** | 嵌入内容可被索引(2022 年新增) |

## 多 User-Agent 控制

可针对不同搜索引擎指定:

```html
<meta name="googlebot" content="noindex, nofollow">
<meta name="bingbot" content="noindex">
<meta name="robots" content="index, follow">
```

- googlebot 优先级高于 robots
- 其他搜索引擎各有专用 user agent

## 实战场景

### 1. 测试/Staging 环境

```html
<meta name="robots" content="noindex, nofollow">
```

- 防止搜索引擎索引未上线版本
- **关键警示**:上线后必须删除,否则正式站不被索引(常见严重错误)

### 2. 站内搜索结果页

- 搜索结果是动态、低质量、无搜索价值的页面
- 全部 noindex 避免污染索引

### 3. 用户个人中心、购物车、订单页

- 私人内容,无搜索意义
- noindex 即可

### 4. 重复内容(临时方案)

- 没法用 [[Canonical规范化标签]] 时
- 但 canonical 是更优解

### 5. 旧内容下架

- 业务下线但 URL 仍存在
- noindex + 内链消除自然移出索引

### 6. 限时下架(unavailable_after)

```html
<meta name="robots" content="unavailable_after: 2024-12-31T23:59:59+00:00">
```

- 优惠活动页、限时活动到期自动失效

### 7. PDF / Image 用 X-Robots-Tag

```
HTTP/1.1 200 OK
Content-Type: application/pdf
X-Robots-Tag: noindex
```

- 静态资源无法加 meta 标签,只能 HTTP 头

## 与 [[Robots.txt]] 的关键区别

| 对比 | robots.txt | Robots Meta |
|---|---|---|
| 作用层 | 抓取阶段 | 索引/展示阶段 |
| 阻止抓取 | 是 | 否(必须先抓取才能读到) |
| 控制索引 | 不可靠(不抓取仍可能索引) | 可靠 |
| 设置位置 | 站根 robots.txt | 页面 head 或 HTTP header |
| 粒度 | 路径粒度 | 页面粒度 |

**关键陷阱**:`robots.txt Disallow` 不等于 `noindex`!被 Disallow 的 URL 如果有外链指向,Google 仍可能索引(显示标题但无摘要)。要彻底阻止索引,必须用 noindex,而 noindex 要生效又必须**允许抓取**(否则 Google 读不到 noindex 指令)。

## 验证

1. **直接查看源码**:确认 meta 标签或 HTTP header 存在
2. **Google Search Console URL Inspection**:看 Google 解析的指令
3. **Screaming Frog / Sitebulb**:批量审计全站 meta 标签
4. **HTTP Response 检查**:Chrome DevTools Network → 查看 X-Robots-Tag

## 常见错误

1. **Disallow + noindex 双重设置**:无效——robots.txt 阻止后 Google 读不到 noindex
2. **Staging 上线后忘删 noindex**:全站不被索引,流量蒸发
3. **canonical 与 noindex 同时存在**:逻辑冲突,Google 会忽略一个
4. **X-Robots-Tag 拼写错**:不是 X-Robots-Tags(没 s),不是 X-Robots
5. **大小写错误**:不区分大小写但建议 lowercase
6. **逗号缺失**:`noindex nofollow` 与 `noindex, nofollow` 都被接受,但建议加逗号

## 与其他概念的关系

- 与 [[Robots.txt]]:互补,作用层不同
- 与 [[Canonical规范化标签]]:重复内容处理的两种方式
- 与 [[抓取渲染索引]]:Robots Meta 在索引阶段被解析
- 与 [[XML Sitemap]]、[[Sitemap配置]]:noindex 的页面不应出现在 sitemap
- 与 [[爬虫优化]]、[[抓取预算]]:精细化控制大型站点
- 与 [[企业级SEO]]:复杂站点 Robots Meta 策略关键

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/
- Google Search Central: Robots Meta Tag Specification
- developers.google.com/search/docs/crawling-indexing/robots-meta-tag
