---
title: CSP 内容安全策略
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Content Security Policy 是浏览器执行的白名单安全策略,通过 HTTP 头声明合法的脚本/样式/媒体源,阻止内联脚本、未授权外部资源、eval 等 XSS 攻击向量,是 XSS 防御的最后一道关键防线。
---

# CSP 内容安全策略

## 定义

**CSP(Content Security Policy)** 是 W3C 标准的浏览器安全机制——通过 HTTP 响应头或 meta 标签声明合法的资源加载源,浏览器拒绝执行不在白名单中的脚本、样式、字体、媒体等。

CSP 是 [[XSS跨站脚本]] 防御的"最后一道防线"——即使代码层 escape 失败,只要 CSP 严格,恶意脚本也无法执行。它由 Mozilla 在 2007 年提出,2012 年 CSP 1.0 标准化,2016 年 CSP 2.0,后陆续 Level 3 草案。

## 基本语法

通过 HTTP Header 声明:

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com; img-src *
```

**指令**(directives)按资源类型:
- default-src:默认所有
- script-src:JS
- style-src:CSS
- img-src:图片
- font-src:字体
- connect-src:fetch/XHR/WebSocket
- frame-src:iframe
- media-src:audio/video
- worker-src:Web Worker
- object-src:plugin(已废弃推荐 'none')
- base-uri:base 标签
- form-action:表单提交目标
- frame-ancestors:谁能 iframe 我(防点击劫持)

**源(source)关键字**:
- 'self':同源
- 'none':禁止全部
- 'unsafe-inline':允许内联脚本(危险)
- 'unsafe-eval':允许 eval(危险)
- 'nonce-xxx':只允许带特定 nonce 的脚本
- 'sha256-xxx':只允许哈希匹配的脚本
- https:、data:、blob:(协议)

## 严格 CSP 示例

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-r4nd0m';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://images.example.com;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  form-action 'self';
  base-uri 'self';
  object-src 'none';
  upgrade-insecure-requests;
```

页面引用脚本时:
```html
<script nonce="r4nd0m">/* 内联脚本被允许 */</script>
<script src="/app.js"></script>  <!-- self 允许 -->
<script src="https://evil.com/x.js"></script>  <!-- 拒绝!-->
```

## 防御什么

**1. XSS**

- 内联脚本默认禁止(无 'unsafe-inline')
- 外部脚本必须白名单
- eval / setTimeout(string) 默认禁止(无 'unsafe-eval')

**2. 数据外泄**

- connect-src 限制 fetch 目标 → 攻击者不能把数据发到自己服务器
- img-src 限制 → 不能用 `<img src=evil>` 偷数据

**3. 点击劫持**

- frame-ancestors 'none' 替代 X-Frame-Options
- 阻止恶意站把你 iframe 进去诱导点击

**4. Mixed Content**

- upgrade-insecure-requests 自动 HTTPS 化
- block-all-mixed-content 阻止 HTTP 资源

## CSP Level 3 新特性

**Strict Dynamic**

```
script-src 'nonce-r4nd0m' 'strict-dynamic'
```

只允许带 nonce 的脚本,但允许它们动态加载其他脚本(自动信任)。简化大型应用 CSP。

**Trusted Types**

```
require-trusted-types-for 'script'
trusted-types default
```

强制 innerHTML 等危险 API 只接受 TrustedHTML 对象,从根本防 DOM XSS。Chrome 实现,逐步推广。

## 部署策略

**1. 报告模式(Report-Only)**

```
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

不阻拦,只上报违规。先观察,再调整,最后切换为 enforce 模式。

**2. 报告 URI**

```
Content-Security-Policy: ...; report-uri /api/csp-report; report-to csp-endpoint
```

浏览器把违规事件 POST 到该 URL,JSON 格式:
```json
{
  "csp-report": {
    "document-uri": "...",
    "violated-directive": "script-src",
    "blocked-uri": "https://evil.com/x.js",
    ...
  }
}
```

收集后统计、调整策略。

**3. 渐进式收紧**

- 阶段 1:default-src 'self'(基础)
- 阶段 2:加严 script-src(nonce / hash)
- 阶段 3:消灭 unsafe-inline
- 阶段 4:trusted types

完整严格 CSP 部署可能需要数月——重写内联脚本、第三方组件适配、逐步消除 inline event handler。

## 现实中的妥协

**unsafe-inline 困境**

许多遗留代码 / 第三方库依赖 inline script、inline event handler、inline style:
- Google Analytics(老版)
- 各种统计 SDK
- 老版 Bootstrap、jQuery 插件
- 服务端渲染 hydrate 数据(`<script>window.STATE = ...</script>`)

完全消灭 unsafe-inline 难度大,多数生产 CSP 仍允许 'unsafe-inline'(尤其对样式)。

**nonce 的复杂度**

每次响应生成随机 nonce,所有内联脚本嵌入,服务器渲染才能用。CDN 缓存会导致 nonce 失效。

**hash 的脆弱**

inline 脚本变化一字符,hash 变,CSP 失效。维护成本高。

**第三方依赖**

Google Tag Manager、Intercom、Stripe.js 等都需加入白名单,白名单膨胀。

## 与其他安全头组合

完整 Web 安全头部应包括:

```
Content-Security-Policy: ...
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY                # 老,被 frame-ancestors 替代
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Resource-Policy: same-origin
```

可用 securityheaders.com 评分。

## 工具与最佳实践

**生成 / 审查工具**

- Google CSP Evaluator:在线评分
- Mozilla Observatory:综合 Web 安全评分
- Report URI(SaaS):违规收集

**框架支持**

- Helmet.js(Express):一行启用 CSP
- Django:django-csp 中间件
- Rails:content_security_policy DSL
- Spring Security:支持 CSP 配置

**监控**

- 收集 csp-report,识别误判 / 真实攻击
- 与 Sentry / Datadog 集成
- 定期 Review 白名单

## 常见误区

- "CSP = 全部 default-src 'self' 就够了" → 现代应用必须细化
- "CSP 解决 XSS 全部问题" → 只是最后一层,代码 escape 仍要
- "上 CSP 一次性搞定" → 渐进式部署,先 Report-Only
- "unsafe-inline 是必要的" → 重写 inline 脚本可消灭
- "CSP 头多就安全" → 严格性远比指令多重要

## 局限

- 部署成本高(尤其老系统)
- 第三方组件兼容性
- nonce / hash 维护负担
- 浏览器实现差异(IE 不支持)
- 报告噪音多(浏览器扩展、误报)
- 不防御服务端漏洞(SQL 注入)

## 和其他概念的关系

CSP 是 [[Web安全]] 头部体系的核心,与 [[XSS跨站脚本]] 防御紧密相关——是代码层 escape 之外的"纵深防御"。它与 [[CORS跨域资源共享]] 都是浏览器同源安全模型的延伸,但 CORS 关注跨源请求允许性,CSP 关注资源加载白名单。

CSP 与 [[CSRF]]、[[Cookie与Session]] 安全属性、[[TLS]] 共同构成现代 Web 应用的"安全基线"。它的"白名单 + Default Deny"哲学是 [[设计原则SOLID]] / [[设计模式]] 之外的安全设计原则,与零信任架构同源。

在 [[微服务]] / [[BFF]] 时代,CSP 与 [[API网关]] 配合形成"前端 CSP + 后端 API 鉴权"的双层防御。

## 参考源

- raw/计算机/
- 相关:[[Web安全]]、[[XSS跨站脚本]]、[[OWASP Top 10]]
