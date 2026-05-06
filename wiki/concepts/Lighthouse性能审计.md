---
title: Lighthouse 性能审计
type: concept
tags: [seo, web, stub]
sources:
  - raw/Google SEO/
  - raw/计算机/Web前端/
created: 2026-05-05
updated: 2026-05-05
summary: Lighthouse 是 Google 开源的网页质量自动化审计工具,从性能、可访问性、最佳实践、SEO、PWA 五维度打分,集成在 Chrome DevTools 和 PageSpeed Insights 中。
---

# Lighthouse 性能审计

## 定义

Lighthouse 是 **Google 开源的开源网页质量审计工具**,通过在受控环境中加载页面、测量各项指标、对照最佳实践给出评分与改进建议。它的目标:**帮助开发者构建更快、更易访问、更优化的 Web 应用**。

Lighthouse 可通过以下方式运行:

- Chrome DevTools 内嵌
- PageSpeed Insights 在线工具
- 命令行 CLI(`lighthouse url`)
- Node.js 库
- CI/CD 自动化集成

## 核心要点

### 五大审计维度

| 维度 | 关注 |
|---|---|
| Performance 性能 | 加载速度、Core Web Vitals |
| Accessibility 可访问性 | a11y 标准、ARIA、对比度 |
| Best Practices 最佳实践 | HTTPS、第三方库版本、控制台错误 |
| SEO | 基础 SEO 检查(meta、可索引性、移动友好) |
| PWA | 渐进式 Web 应用清单 |

### 性能维度核心指标

| 指标 | 测量内容 | 良好阈值 |
|---|---|---|
| FCP(First Contentful Paint) | 首次内容渲染 | < 1.8s |
| LCP(Largest Contentful Paint) | 最大元素渲染 | < 2.5s |
| TBT(Total Blocking Time) | 主线程阻塞总时长 | < 200ms |
| CLS(Cumulative Layout Shift) | 累积布局偏移 | < 0.1 |
| Speed Index | 视觉填充速度 | < 3.4s |
| TTI(Time to Interactive) | 完全可交互时间 | < 3.8s(已弱化) |
| INP(Interaction to Next Paint) | 交互响应延迟 | < 200ms |

### Core Web Vitals(CWV)

Google 把 LCP、CLS、INP 三项作为 [[Core Web Vitals]],是 SEO 排名信号:

- **LCP**:衡量加载速度
- **CLS**:衡量视觉稳定
- **INP**(2024 取代 FID):衡量交互响应

### 性能优化常见建议

Lighthouse 给出的具体诊断:

- 减少 JavaScript 执行时间(代码分割、Tree Shaking、移除未用代码)
- 减少主线程工作(Web Worker、虚拟列表)
- 缩短关键请求链(预加载、HTTP/2 推送、Inline critical CSS)
- 启用文本压缩(gzip / brotli)
- 提供下一代图片格式(WebP / AVIF)
- 推迟非关键 JS / CSS
- 移除未使用的 CSS
- 使用 CDN
- 启用 HTTP/2、HTTP/3
- Server-Push 与 Resource Hints(preload、prefetch、dns-prefetch、preconnect)

### 实验室数据 vs 真实用户数据

- **Lab Data(实验室)**:Lighthouse 在受控环境模拟,可重现但与真实差异
- **Field Data(真实用户)**:CrUX(Chrome User Experience Report)收集真实用户的 LCP/CLS/INP

PageSpeed Insights 同时显示二者;真实用户数据是 SEO 排名实际依据。

### 在 CI/CD 中集成

```bash
# 安装
npm install -g @lhci/cli

# 运行
lhci autorun --collect.url=https://example.com --assert.preset=lighthouse:recommended
```

可在 GitHub Actions、GitLab CI、Jenkins 中作为质量门:性能分数低于阈值则阻止部署。

## 和其他概念的关系

Lighthouse 是 [[页面SEO]] 与 [[技术SEO]] 中最常用的自动化工具,与 [[Google Search Console]]、[[Core Web Vitals]] 共同构成网站性能监控体系。

[[企业级SEO]] 中 Lighthouse 用于持续监控大规模站点;[[爬虫优化]] 中性能直接影响抓取效率。

[[Webpack]]、[[Vite]] 等 [[Webpack|构建工具]] 提供专门的性能优化插件;[[CDN]]、[[HTTP2协议|HTTP/2]]、[[HTTP3协议|HTTP/3]]、[[Service Worker]] 是 Lighthouse 高分的常见手段。

[[前端框架]](React、Vue、Next.js)的 SSR / SSG / ISR 模式都是为优化 Lighthouse 性能指标设计;[[Jamstack]] 与 [[现代云原生架构|云原生]] 部署天然 Lighthouse 友好。

[[Helpful Content Update]] 与 [[E-E-A-T]] 之外,Core Web Vitals 是 SEO 的另一硬性要求——再好的内容,加载慢也会被降权。

## 参考源

- raw/Google SEO/
- raw/计算机/Web前端/
- Lighthouse 文档 https://developer.chrome.com/docs/lighthouse/
- web.dev 性能指南
- Google 开发者大会相关 sessions
