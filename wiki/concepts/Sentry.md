---
title: Sentry(错误监控)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Sentry 是面向开发者的错误与性能监控平台,通过 SDK 自动捕获前端、后端、移动端的异常堆栈与性能瓶颈,以可分组、可分配、可上下文化的工作流成为现代应用错误观测事实标准。
---

# Sentry(错误监控)

## 定义

**Sentry** 是 David Cramer 在 2008 年作为内部工具创建、2012 年开源、2015 年 SaaS 化的应用错误与性能监控平台。它围绕一个核心命题:"**生产环境出问题时,开发者需要立即知道发生了什么、在哪、影响多少用户**"。

不同于日志聚合([[ELK Stack]]、Loki)和指标监控([[Prometheus]]、[[Grafana]]),Sentry 专注于**异常与性能事件**——把每个错误连同堆栈、上下文、用户信息、版本、设备信息一起捕获,聚合成可处理的工单。

## 核心能力

**1. 错误捕获**

- 浏览器 JS 异常
- Node、Python、Ruby、Java、Go、PHP、Rust 等服务端
- iOS、Android 原生
- React Native、Flutter
- Unity / Unreal(游戏引擎)

SDK 自动 hook 全局 try/catch、Promise rejection、事件监听器异常,无需开发者手动捕获。

**2. 堆栈与源映射**

- 完整堆栈(stack trace)+ 局部变量
- Source Maps 反混淆 JS(显示原始 TypeScript)
- DSym 反混淆 iOS / dSYM
- ProGuard / R8 反混淆 Android

**3. 错误分组(Issue)**

相同根因的错误自动聚合为一个 Issue:
- 显示总次数、影响用户数、首次/最近发生
- 不同环境(prod/staging)分开
- 不同版本对比(回归检测)

**4. 上下文丰富**

- 用户身份(自动或手动 setUser)
- Tag(release、environment、app version)
- Breadcrumbs(异常前用户操作链)
- HTTP 请求 / 响应快照
- 设备(OS、浏览器、内存)
- 自定义 context

**5. 性能监控(2020+)**

- 事务追踪(类似 [[可观测性三支柱]] 中的分布式追踪)
- Web Vitals([[Core Web Vitals]] LCP/FID/CLS)
- 慢查询、慢 API、慢路由
- 与错误数据关联

**6. Session Replay(2022+)**

- 录制用户操作前后 30 秒的 DOM 视频
- 可隐私脱敏(密码、信用卡自动遮盖)
- 帮助重现难复现 bug

## SDK 集成示例

**JavaScript / React**

```javascript
import * as Sentry from "@sentry/react"

Sentry.init({
  dsn: "https://xxx@sentry.io/123",
  environment: "production",
  release: "myapp@1.2.3",
  tracesSampleRate: 0.1,  // 10% 性能采样
  replaysSessionSampleRate: 0.1,
})
```

**Python**

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://xxx@sentry.io/123",
    traces_sample_rate=0.1,
    send_default_pii=True,
)
```

集成几行代码,SDK 接管全部异常上报。

## 工作流

**Issue 生命周期**

1. 新错误自动创建 Issue
2. Slack / 邮件 / Jira 通知
3. 分配给负责工程师
4. 工程师查看堆栈、复现、修复
5. 标记为 Resolved
6. 同 Issue 在新 Release 后再现 → "Regressed"自动重开
7. Ignore / Mute / Resolve in Next Release

**Release Health**

每个版本的:
- Crash-free Sessions(% 用户无崩溃)
- Crash-free Users
- Adoption(新版安装率)
- 与上一版本对比(性能、错误数)

## 自部署 vs SaaS

**Sentry SaaS**

- sentry.io 托管
- 起步免费(5000 errors/月)
- 团队 $26/月起,有 Cap
- 低运维成本

**Sentry 自部署**

- 完整开源(Functional Source License,2024 改 BSL)
- docker-compose 一键搭建
- 适合数据合规、欧美数据隔离需求
- 运维成本(PostgreSQL + Redis + Kafka + ClickHouse)
- 性能略慢于 SaaS

中国企业为合规多自部署,海外多用 SaaS。

## 与同类对比

| 工具 | 特点 |
|---|---|
| Sentry | 错误 + 性能,开发者友好 |
| Bugsnag | 错误监控老牌,与 Sentry 类似 |
| Rollbar | 类似,强企业市场 |
| Datadog APM | 全栈,性能为主 |
| New Relic | 全栈,APM 强 |
| Honeybadger | Ruby on Rails 友好 |
| Raygun | Microsoft 生态 |

Sentry 的差异化:**开源 + 自部署 + 开发者优先 DX**。

## 性能采样策略

错误必采,性能事务可采样:
- 100% 采样:数据完整但贵
- 10% 采样:常规生产
- 1% 采样:大流量
- Dynamic Sampling:对慢请求、错误自动加采,常规减采

## 隐私与合规

- send_default_pii 控制是否发用户信息
- beforeSend 钩子可篡改/丢弃事件
- Mask sensitive fields(密码、信用卡正则脱敏)
- 数据驻留(EU/US/SG 区域)
- GDPR、HIPAA 合规模式

## 集成生态

- **Source Code Management**:GitHub、GitLab、Bitbucket(commit 自动关联 Release)
- **Issue Tracker**:Jira、Linear、ClickUp、Asana(一键创建 ticket)
- **Notification**:Slack、Discord、PagerDuty、Teams
- **CI/CD**:Sentry CLI 上传 Source Maps
- **Auth**:SSO、SAML

## 局限

- 高流量场景(百万级日错误)成本爆炸
- Replay 受隐私法规限制
- 自部署运维门槛(尤其 ClickHouse)
- 移动端 dSYM/Mapping 上传配置烦
- 性能监控不如专门 APM 深度

## 最佳实践

**1. Release 必关联**

每次部署 sentry-cli releases new && sentry-cli releases set-commits,让 Sentry 知道哪个 commit 引入 bug。

**2. 用户标记**

```javascript
Sentry.setUser({ id: "user-123", email: "..." })
```

让错误能定位到具体用户群体(付费用户优先修)。

**3. 业务关键路径加 Span**

```javascript
const tx = Sentry.startTransaction({ name: "checkout" })
// ...
tx.finish()
```

知道支付环节多慢、瓶颈在哪。

**4. 报警阈值**

- 新 Issue 首次出现 → 立即 Slack
- Issue 每小时 > 100 次 → 告警
- 新 Release 错误率上升 → 告警(可能是回归)

## 和其他概念的关系

Sentry 与 [[ELK Stack]]、[[Prometheus]]、[[Grafana]] 共同构成 [[可观测性三支柱]] 的不同切面——Sentry 专注于错误与开发者工作流,日志/指标聚合让位于其他工具。

它的"问题分组"思想抽象自人类工程实践:相同堆栈 = 同类 bug。这与 [[设计模式]] 中模板方法、责任链等思想一脉相承——把人类直觉编程化。

Sentry 与 [[CI_CD流水线]] 紧密结合,Release 数据让"哪次发布带来 bug"定位精确,推动了 [[GitFlow与TrunkBased]] 中 Trunk-Based 与频繁小发布的实践。

## 参考源

- raw/计算机/
- 相关:[[可观测性三支柱]]、[[Grafana]]、[[Prometheus]]
