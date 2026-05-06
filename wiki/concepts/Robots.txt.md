---
title: Robots.txt
type: concept
tags: [seo, 技术SEO, 爬虫管理, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/06-爬虫优化.md]
created: 2026-05-05
updated: 2026-05-05
summary: robots.txt 是放在网站根目录的纯文本文件,基于 1994 年 Martijn Koster 的 Robots Exclusion Protocol(REP),告诉爬虫哪些路径不应抓取;它是抓取控制的第一道闸门,但不是索引控制工具。
---

# Robots.txt

## 定义

**robots.txt** 是一个放在域名根目录(如 `https://example.com/robots.txt`)的纯文本文件,遵循 1994 年 Martijn Koster 提出的 **Robots Exclusion Protocol(REP)**。文件以"User-agent + Disallow/Allow"结构告诉爬虫:**"哪些路径不要抓取"**。Google 2019 年牵头将其推为 IETF 正式标准 RFC 9309(2022 发布)。

它是 [[技术SEO]] 中 [[爬虫优化]] 的第一道闸门,但常被滥用——许多 SEO 误以为"robots.txt 不让爬就不会被索引",其实**两者是不同概念**。

## 核心要点

### 1. 基本语法

```
User-agent: *
Disallow: /admin/
Disallow: /tmp/
Allow: /tmp/public/

User-agent: Googlebot
Disallow: /no-google/

Sitemap: https://example.com/sitemap.xml
```

- `User-agent`:指定爬虫(`*` 通配)
- `Disallow`:禁止抓取的路径前缀
- `Allow`:在 Disallow 范围内的例外
- `Sitemap`:声明 sitemap 位置(可多个)

### 2. 关键认知:robots.txt 控制的是"抓取"而非"索引"

**Disallow 不能阻止页面被索引**。如果其他网站链接到被 Disallow 的页面,Google 仍可能索引这个 URL(虽然不爬取内容,只显示 URL+锚文本)。

要确保 **不索引**,必须用 `<meta name="robots" content="noindex">`,但这又要求 Google **能爬取**该页面读到 noindex——所以 noindex 与 robots.txt Disallow 不应同时使用。

### 3. 主要 SEO 用途

| 场景 | 推荐设置 |
|---|---|
| 后台、管理面板 | `Disallow: /admin/` |
| 内部搜索结果页 | `Disallow: /search` |
| 重复参数 URL | `Disallow: /*?sort=` |
| 大型 staging 环境 | `Disallow: /` 但更安全是 HTTP 401 |
| 机密文档 | **不要用 robots.txt!** 它公开可见,反成"路标" |
| 浪费抓取预算的资源 | `Disallow: /api/`、`Disallow: /print/` |

### 4. 抓取预算管理

对大型站(百万+ URL),robots.txt 是 **抓取预算(Crawl Budget)** 优化的关键工具。Google 不会无限爬取,把低价值 URL 屏蔽能让抓取集中到重要页面。

### 5. 与其他工具的协同

```
robots.txt:    我能爬这页吗?         ← 抓取层
canonical:     这页内容首选哪个 URL?   ← 信号层
meta robots:   这页能索引吗?可跟踪吗? ← 索引层
HTTP 401/403:  授权访问                ← 安全层
sitemap:       请优先来爬这些页面     ← 发现层
```

### 6. 大小敏感与 URL 匹配

- 路径区分大小写
- `*` 通配符(Googlebot 支持)
- `$` 锚定结尾
- 例:`Disallow: /*.pdf$` 屏蔽所有 PDF

## 与其他概念的关系

- **配套**:[[XML Sitemap]] / [[Canonical规范化标签]] / [[Meta Robots标签]] / [[Hreflang国际化标签]]
- **上层**:[[技术SEO]] / [[爬虫优化]] / [[Google搜索工作原理]]
- **诊断**:[[Search Console配置]] robots.txt 测试器
- **延伸**:[[抓取预算]] / [[渲染]] / [[索引]]

## 常见错误

| 错误 | 影响 |
|---|---|
| 错误屏蔽 CSS/JS | Google 无法渲染页面,降低排名 |
| 把整站设 Disallow: / | 灾难,通常发布事故 |
| 用 robots.txt 隐藏机密 | 公开可见,反指路 |
| Noindex + Disallow 同用 | Google 永远读不到 noindex |
| 大写路径写错 | 静默失败 |

## 历史里程碑

- **1994** Martijn Koster 提出 REP
- **2007** Google 加入 sitemap 指令
- **2019** Google 提交 IETF 草案
- **2019** Google 不再支持 `noindex` in robots.txt
- **2022** RFC 9309 正式发布,REP 标准化

## 工具

- Google Search Console robots.txt 测试器
- Screaming Frog robots.txt 模拟
- Ryte / Sitebulb 自动诊断

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/06-爬虫优化.md
- Google Search Central Documentation
- 关联:[[技术SEO]] / [[爬虫优化]] / [[XML Sitemap]] / [[Canonical规范化标签]] / [[Search Console配置]]
