---
title: Core Web Vitals
type: concept
tags: [seo, mature]
sources: [raw/Google SEO/02-理解层-核心机制/2.1-Google算法深度解析/04-Core Web Vitals.md, raw/Google SEO/02-理解层-核心机制/2.5-用户体验/01-用户体验指标.md]
created: 2026-05-05
updated: 2026-05-05
summary: Core Web Vitals 是 Google 衡量页面用户体验的三大核心指标(LCP、INP/FID、CLS),自 2021 年起成为正式排名信号。
---

# Core Web Vitals

## 定义

**Core Web Vitals(CWV,核心网页指标)** 是 Google 在 2020 年提出、2021 年正式纳入排名因素的**网页用户体验三指标**:**LCP(加载性能)、INP/FID(交互响应)、CLS(视觉稳定性)**。这三个指标试图用可量化的方式衡量"页面加载是否快、是否好响应、是否不晃眼"。

CWV 是 Google "Page Experience" 评分体系的核心,与 HTTPS、移动友好、安全浏览、无侵入式插页广告共同构成页面体验信号。CWV 不是排名最重的因素,但在内容质量相近时是关键的"决胜因素",且差体验会被算法显著压制。

## 核心要点

- **LCP(Largest Contentful Paint,最大内容绘制)**:
  - **测量**:页面视口内最大可见元素(图片、视频、大块文本)绘制完成的时刻
  - **阈值**:良好 ≤2.5s,需改进 2.5-4s,差 >4s
  - **影响因素**:服务器响应(TTFB)、渲染阻塞 CSS/JS、资源加载、客户端渲染
  - **优化**:CDN、HTTP/2、关键 CSS 内联、图片预加载、字体优化、减少重定向、SSR/SSG
- **INP(Interaction to Next Paint,交互响应)**——2024 年 3 月正式替代 FID:
  - **测量**:用户与页面所有交互的响应延迟,取最差值(更严格)
  - **阈值**:良好 ≤200ms,需改进 200-500ms,差 >500ms
  - **影响因素**:主线程繁忙、长任务、第三方脚本、事件处理器开销
  - **优化**:减少 JS 主线程工作、代码拆分、Web Workers、延迟非关键 JS、移除多余事件监听
  - **历史**:FID(First Input Delay)只测首次交互的输入延迟,2024 年被认为不够严苛
- **CLS(Cumulative Layout Shift,累积布局偏移)**:
  - **测量**:页面生命周期中因布局突变造成的累积分数
  - **阈值**:良好 ≤0.1,需改进 0.1-0.25,差 >0.25
  - **影响因素**:无尺寸图片/视频、动态注入内容(广告、Banner)、字体闪烁(FOIT/FOUT)、第三方组件
  - **优化**:为媒体设置宽高属性、为广告位预留空间、用 font-display: swap、避免在用户交互前注入内容
- **测量工具**:
  - **真实用户数据(Field Data)**:Chrome User Experience Report(CrUX)、PageSpeed Insights、GSC 的 Core Web Vitals 报告
  - **实验室数据(Lab Data)**:Lighthouse、WebPageTest、Chrome DevTools Performance
  - **关键差异**:Google 排名用真实用户数据(Field),而不是 Lighthouse 的实验室分数
- **75 分位数原则**:同一页面在 75% 用户的体验中达标才算"通过"——单纯优化平均值不够,要管理长尾。
- **常见误区**:
  - 只优化首页忽略产品页(产品页流量更大)
  - 只看 Lighthouse 分数不看真实数据
  - 优化测试设备而忽视真实用户(老旧手机、慢网络)
  - 第三方脚本(分析、广告、客服)是 INP 与 LCP 的常见杀手,需要严格审查
- **CWV 与排名**:
  - 不是单一决定因素,但当多个页面内容质量相近时 CWV 决定胜负
  - 移动端权重高于桌面端
  - 大幅恶化会触发用户体验类降权
  - 大幅改善带来的排名提升通常 1-3 个月显现

## 和其他概念的关系

Core Web Vitals 是 [[技术SEO]] 中"页面速度与体验"的具象化指标体系,2021 年起作为 [[Google算法更新]] 中 Page Experience Update 引入排名。

CWV 是 [[E-E-A-T]] 中 Trustworthiness 在"用户体验"侧的延伸——加载慢、闪烁多、卡顿严重的网站难以被信任。

CWV 直接影响 [[转化漏斗]] 顶部:LCP > 4 秒会让 70%+ 用户跳出,CTR 与转化率随速度提升显著上升(亚马逊 100ms 提升 1% 销售)。

CWV 在 [[移动端SEO]] 中尤为关键——移动设备网络与算力差异大,优化难度高于桌面。

CWV 测量需要 [[数据驱动营销]] 的方法,真实数据来源(GSC、CrUX)与实验室数据要交叉验证。

CWV 与现代前端架构选择强相关:SSR/SSG 框架(Next.js、Nuxt、SvelteKit、Astro)的兴起部分原因就是为了 CWV 优化。

## 参考源

- raw/Google SEO/02-理解层-核心机制/2.1-Google算法深度解析/04-Core Web Vitals.md
- raw/Google SEO/02-理解层-核心机制/2.5-用户体验/01-用户体验指标.md
- raw/Google SEO/02-理解层-核心机制/2.3-技术SEO/02-页面速度优化.md
