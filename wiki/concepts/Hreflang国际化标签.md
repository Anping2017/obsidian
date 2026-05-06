---
title: Hreflang国际化标签
type: concept
tags: [seo, 技术SEO, 国际SEO, mature]
sources: [raw/Google SEO/04-精通层-高级策略/4.2-国际SEO与文化因素/]
created: 2026-05-05
updated: 2026-05-05
summary: hreflang 是 Google 2011 年引入的多语言/区域注解,让搜索引擎理解同一内容不同语言/区域版本之间的关系,避免重复内容判罚并把对的版本展示给对的用户;实现方式有 link 标签、HTTP Header、XML Sitemap 三种。
---

# Hreflang 国际化标签

## 定义

**hreflang** 是 [[国际SEO]] 的核心技术信号,2011 年 12 月 Google 引入(Bing 2013 年跟进)。它告诉搜索引擎:**这个页面有英语、法语、德语等多个对应版本,请把对应语言/区域的用户引到对应版本**。没有 hreflang 的多语言站可能被 Google 判定为重复内容(Duplicate Content),或者把英国用户引到美国版导致价格、库存信息全错。

## 核心要点

### 1. 三种实现方式

#### a) HTML link 标签(最常见)

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/us/page" />
<link rel="alternate" hreflang="fr-FR" href="https://example.com/fr/page" />
<link rel="alternate" hreflang="x-default" href="https://example.com/page" />
```

每个版本必须列出 **所有版本**(包括自己)。

#### b) HTTP Header(适用于 PDF 等非 HTML)

```
Link: <https://example.com/us/page>; rel="alternate"; hreflang="en-US"
```

#### c) XML Sitemap(大型站推荐)

```xml
<url>
  <loc>https://example.com/us/page</loc>
  <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/us/page"/>
  <xhtml:link rel="alternate" hreflang="fr-FR" href="https://example.com/fr/page"/>
</url>
```

### 2. hreflang 值规范

- 仅语言:`en`、`fr`、`zh`(ISO 639-1)
- 语言-区域:`en-US`、`zh-CN`、`pt-BR`(ISO 639-1 + ISO 3166-1)
- 特殊值:**`x-default`**(默认 fallback,当无匹配时使用,通常指向语言选择页或全球版)

### 3. 三大铁律

1. **双向引用(Bidirectional)**:A 指向 B,B 必须指向 A,否则 Google 忽略
2. **每个版本必须自指(Self-referencing)**
3. **绝对 URL,不能用相对路径**

### 4. 与 [[Canonical规范化标签]] 关系

- hreflang 处理**语言/区域版本**之间的关系
- canonical 处理**重复/相似内容**的首选 URL
- 两者必须协调:每个语言版本的 canonical 应指向自己,然后用 hreflang 互相关联,不可让法语版的 canonical 指向英语版

### 5. 常见错误(Google Search Console 报告)

| 错误 | 含义 |
|---|---|
| **No return tags** | A 指 B 但 B 不指 A |
| **Invalid hreflang code** | en-uk(应为 en-GB)、zh(应明确 zh-CN/zh-TW) |
| **Hreflang to non-canonical URL** | 指向被 noindex 或 redirect 的 URL |
| **Hreflang to 404** | 目标页不存在 |
| **Mixed self-canonicals** | canonical 与 hreflang 冲突 |

### 6. 决策树:用 ccTLD、子域、子目录?

| 结构 | 优点 | 缺点 |
|---|---|---|
| **ccTLD**(example.fr) | 强地理信号、信任 | 各域权重独立,贵 |
| **子域**(fr.example.com) | 灵活 | 权重稀释 |
| **子目录**(example.com/fr/) | 共享主域权重 | 服务器配置稍复杂 |
| **URL 参数**(?lang=fr) | 不推荐 | Google 难以识别 |

## 与其他概念的关系

- **核心配套**:[[Canonical规范化标签]] / [[XML Sitemap]] / [[Robots.txt]]
- **上层**:[[国际SEO]] / [[技术SEO]] / [[Google搜索工作原理]]
- **诊断**:[[Search Console配置]] 的 International Targeting 报告
- **跨域**:与多语言内容策略、本地化(L10n)、文化适配工作流相关

## 工具

- Google Search Console "International Targeting" 报告
- Screaming Frog SEO Spider — 抓取并校验 hreflang
- hreflang.sirgraph.io — 图形化校验工具
- Aleyda Solis 的 hreflang Tags Generator

## 当代演进

- **Google 2018 弃用 rel=alternate media** 移动版分离过时,统一在响应式 + hreflang
- **Bing 2023+ 改进**:对 hreflang 信号更敏感
- **AI Mode**:多语言 AI 概览(Gemini、SGE)依赖 hreflang 给用户对应语种答案

## 参考源

- raw/Google SEO/04-精通层-高级策略/4.2-国际SEO与文化因素/
- 关联:[[国际SEO]] / [[Canonical规范化标签]] / [[技术SEO]] / [[XML Sitemap]] / [[Search Console配置]]
