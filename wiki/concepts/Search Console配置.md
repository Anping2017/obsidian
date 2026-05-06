---
title: Search Console配置
type: concept
tags: [seo, mature]
sources: [raw/SEO/03-SEO工具应用/03-1-免费工具使用/Google Search Console使用指南.md]
created: 2026-05-05
updated: 2026-05-05
summary: Google 官方 SEO 仪表盘,展示来自 Google 搜索的真实查询、点击、覆盖率、技术问题。
---

# Search Console配置

## 定义

Google Search Console(GSC,曾名 Webmaster Tools)是 Google 提供给网站所有者的免费仪表盘,展示该站点在 Google 搜索的真实表现数据(关键词、CTR、平均排名、点击)、技术健康(索引状态、抓取错误、Core Web Vitals)、外链与内链等。它是任何网站做 [[搜索引擎优化]] 的必备工具——不安装 GSC 等于盲飞。配置看似简单(添加资源 + 验证),但深度使用需要数据导出 + API + 与 [[GA4配置]] 联动。

## 核心要点

**两种资源类型**:

- **网址前缀属性(URL-Prefix Property)**:针对 `https://www.example.com/` 单一 URL 形式,需 HTML 文件 / Meta 标签 / GA / GTM / DNS 验证。
- **网域属性(Domain Property)**:针对所有协议 + 子域(http、https、www、m. 等都覆盖),只能 DNS TXT 记录验证。**强烈推荐**域属性,数据完整。

**核心模块**:

### 1. 性能(Performance)

- **查询(Queries)**:用户搜索的关键词、点击数、展示数、CTR、平均排名。
- **页面(Pages)**:每个页面的搜索表现。
- **国家、设备、外观、日期、过滤**。
- **限制**:每个组合最多返回 1000 行,通过 **Search Console API** 或导出能突破。

**关键用法**:

- 找"高展示低 CTR"页面 → 重写 Title + Meta Description。
- 找"接近 Top 10 但排名 11-20"关键词 → 优先优化(Quick Win)。
- 看 Search Appearance(SERP 特征)→ 哪些页拿到 Featured Snippet / Rich Result。

### 2. 索引(Indexing)

- **页面(Pages)**:已索引、未索引(原因细分)、被排除。常见错误:
  - "已发现 - 尚未索引":Google 发现了但还没爬。
  - "已抓取 - 尚未索引":爬过觉得不值得索引(质量信号)。
  - "重复网页,Google 选择了不同的规范":canonical 问题。
  - "404 / 软 404":页面不存在或返回不正确状态码。
- **Sitemap**:提交 XML 站点地图。
- **Removals**:临时移除 URL(6 个月)。

### 3. 体验(Experience)

- **Core Web Vitals**:LCP / INP / CLS,移动 + 桌面分别看,差 / 可改 / 良好分级。
- **HTTPS**:站点 HTTPS 覆盖率。
- **Page Experience**(2024 整合到 Helpful Content,但仍可看)。

### 4. 增强功能(Enhancements)

每种 [[Schema.org结构化数据]] 一个独立报告:Breadcrumb、FAQ、Recipe、Product、Logo、HowTo 等。看哪些有效、哪些有错误。

### 5. 链接(Links)

- **外部链接(External Links)**:总外链数、最常链接的页、最常被链接的锚文本、最常链接的站点。
- **内部链接(Internal Links)**:Google 识别的内链分布,验证 [[内链优化]] 是否到位。

### 6. 安全与手动操作(Security & Manual Actions)

- **手动操作(Manual Actions)**:被人工处罚记录(垃圾内容、链接 schemes 等)。
- **安全问题**:被黑、恶意软件警告。

### 7. URL 检查工具(URL Inspection)

输入任何 URL,看:

- 是否在索引中。
- 上次抓取时间、抓取时的 HTML、抓取时使用的 User-Agent。
- 移动可用性、Schema 状态。
- "请求重新抓取" → 紧急更新内容后通知 Google。

**API 使用**:

- Search Console API(Google Cloud Console 启用)。
- 突破 1000 行限制,导出全部查询。
- 集成 Looker Studio / Google Sheets / Python 自动化报告。
- 推荐工具:Search Console Insights、Looker Studio 模板、Python 库 `searchconsole`。

**Bing Webmaster Tools / 百度站长平台**:

- Bing:GSC 的等价物,可一键导入 GSC 验证状态。
- 百度站长平台:中文站点必备,提交 sitemap、抓取诊断、HTTPS 认证。

**反模式**:

- 不安装 → SEO 全凭感觉。
- 只用 URL-Prefix Property → 数据不全。
- 不导出长期数据 → GSC 默认仅保留 16 个月,丢失历史。
- 不监测核心错误 → 索引大量页面被自动排除而不知。
- 看 GSC 排名等同实际排名 → GSC 排名是平均位置,不等于实时 SERP。

## 和其他概念的关系

GSC 与 [[GA4配置]] 是 SEO 与流量分析的左右手:GSC 看"Google 搜索内"的表现,GA4 看"网站内"的用户行为。两者关联后(GA4 设置 → 产品关联 → GSC 关联),可在 GA4 看 SEO 流量的关键词来源。

GSC 是 [[网站审计]] 与 [[关键词研究]] 的核心数据源——自有站点真实查询比第三方工具(Ahrefs / SEMrush)的预估更准。它直接监测 [[Core Web Vitals]]、[[移动优先索引]]、[[Schema.org结构化数据]] 健康度。

[[Featured Snippet精选摘要]]、[[Local Pack本地包]]、Image Pack 等 [[SERP特征]] 表现都在 GSC 的 Search Appearance 维度可见。它是 [[漏斗优化]] 上游"流量入口"的眼睛,与 [[搜索引擎优化]] 整体 KPI 监测一一对应。

## 参考源

- raw/SEO/03-SEO工具应用/03-1-免费工具使用/Google Search Console使用指南.md
- raw/SEO/03-SEO工具应用/03-3-数据监控体系/SEO数据监控框架.md
- raw/SEO/03-SEO工具应用/03-3-数据监控体系/排名监控策略.md
