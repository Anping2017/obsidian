---
title: CSRF 跨站请求伪造
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: CSRF 是攻击者诱导已登录用户的浏览器在不知情下发起请求的攻击,核心防御是 CSRF Token、SameSite Cookie 与同源策略检查,现代框架默认配置已大幅降低风险。
---

# CSRF 跨站请求伪造

## 定义

**CSRF(Cross-Site Request Forgery)**,又称 XSRF、Sea Surf,是攻击者构造特殊页面或链接,**诱导已登录用户的浏览器在用户不知情下,以用户身份向目标网站发起请求**的攻击。

它利用浏览器自动携带 Cookie 的特性——只要受害者已登录目标站,即使在攻击者控制的页面上,跨站请求也会带上 Session Cookie,后端无法区分是用户自愿还是被诱导。

CSRF 长期是 [[OWASP Top 10]] 高危,2021 版归入"破损访问控制"类。

## 经典攻击场景

**1. 转账场景**

银行 example-bank.com 转账 API:
```
POST /api/transfer
Body: { "to": "xxx", "amount": 1000 }
```

攻击者在 evil.com 放:
```html
<form action="https://example-bank.com/api/transfer" method="POST" id="f">
  <input name="to" value="attacker-account">
  <input name="amount" value="1000">
</form>
<script>document.getElementById('f').submit()</script>
```

受害者已登录银行,访问 evil.com 即"被转账"。

**2. 修改邮箱**

```
POST /account/email
Body: { "email": "attacker@evil.com" }
```

随后攻击者用"忘记密码"功能接管账户。

**3. GET 请求型**

不严谨的 API 用 GET 处理修改:
```
<img src="https://app/admin/delete-user?id=123">
```

仅访问含 img 的页面就触发。

## 攻击前提

- 受害者已登录目标网站
- 目标网站 Cookie 没禁跨站
- 没有 CSRF 防御机制
- 攻击者能让受害者打开特定页面/链接

只要这四条满足,攻击就成立。

## 与 XSS 的区别

| 维度 | CSRF | XSS |
|---|---|---|
| 攻击点 | 让浏览器发请求 | 让浏览器执行恶意 JS |
| 信任利用 | 用户对站的信任 | 站对用户输入的信任 |
| 偷 Cookie | 不能(看不见响应) | 能 |
| 任意操作 | 限于 API 接口 | 完全控制浏览器 |
| 防御 | Token / SameSite | 转义 / CSP |

XSS 比 CSRF 危害大得多,但二者互补——XSS 站点也可被用来发起 CSRF,XSS 是 CSRF 防御的"破墙锤"。

## 防御方法

**1. CSRF Token(Synchronizer Token Pattern)**

服务器每次渲染表单嵌入随机 Token:

```html
<form action="/transfer" method="POST">
  <input type="hidden" name="csrf_token" value="aBc123XyZ789">
  <input name="to">
  ...
</form>
```

服务器验证 Token 与 Session 中存的一致。攻击者跨站构造表单时,无法获得 Token(同源策略不让读),请求失败。

**框架支持**

- Django:CsrfViewMiddleware 默认开
- Rails:protect_from_forgery 默认开
- Laravel:VerifyCsrfToken 默认开
- Spring Security:csrf 默认开
- Express:csurf 中间件
- ASP.NET:AntiForgeryToken

**SPA / API 场景**

JSON API + JWT 时,Token 存在 LocalStorage / 通过 Authorization Header 发送。攻击者跨站无法读 LocalStorage,Cookie 不自动发,天然防 CSRF。

但要注意:**不要把 JWT 存 Cookie 又不加 SameSite**——又回到 CSRF 风险。

**2. SameSite Cookie**

主流浏览器 2020+ 支持的 Cookie 属性:

```
Set-Cookie: session=abc; SameSite=Lax
Set-Cookie: session=abc; SameSite=Strict
Set-Cookie: session=abc; SameSite=None; Secure
```

- **Strict**:跨站完全不发 Cookie
- **Lax**:GET 顶层导航可发,POST / 子资源不发
- **None**:总发(需 Secure)

Chrome 2020 起把没声明 SameSite 的 Cookie 当 Lax 处理,这一改动**大幅消灭了 GET 型 CSRF**,POST 型 CSRF 也受重创。

**3. Origin / Referer 检查**

验证请求来源:
```
Origin: https://example.com  ← 比对自己的域名
Referer: https://example.com/page
```

简单有效但有边缘情况:
- 浏览器有时不发 Referer(隐私设置)
- 不同协议 HTTPS / HTTP 转换
- 移动端 App 内 WebView

通常作为辅助防御,不依赖。

**4. 双重提交 Cookie(Double Submit Cookie)**

Token 同时放 Cookie 和请求 Header / Body,服务器比对一致。无需 Session 存储。SPA 常用方案。

**5. 用户重新认证**

敏感操作(转账、改密码)要求再次输入密码或 OTP。即使 CSRF 通过仍需密码,有效阻断。

**6. Custom Header**

简单 SPA 防御:对所有 API 请求加自定义 Header(如 X-Requested-With: XMLHttpRequest)。浏览器跨站脚本不能加自定义 Header(预检请求),后端检查这个 Header 即可拦截大部分 CSRF。

## 现代框架默认配置

- **React + REST API + JWT in Authorization Header**:天然防 CSRF
- **Cookie-based Session + 框架默认 Token**:防御充足
- **混合方案**(JWT in Cookie):需自己加 CSRF Token 或 SameSite=Strict

## 测试方法

**手工测试**

构造跨站 HTML / JS 触发请求:
```html
<form action="https://target/api/action" method="POST">...</form>
<script>document.forms[0].submit()</script>
```

观察是否成功。

**Burp Suite**

CSRF PoC 生成器,基于现有请求自动生成攻击页面。

**OWASP ZAP**

Active Scan 中包含 CSRF 检测。

**自动化**

CSRFTester、Sleekflow 等工具生成测试用例。

## 历史教训

- **NetGear 路由器(2008)**:CSRF 改 DNS,劫持流量
- **Gmail(2007)**:CSRF 改邮件转发规则
- **Twitter(2010)**:CSRF 强制关注
- **YouTube(2008)**:CSRF 加好友
- **众多银行系统**:转账 CSRF

## CSRF 在 GraphQL / API 中

**GraphQL** 默认请求 Content-Type: application/json,跨站表单不能发(预检),天然部分防御。但若开启 application/x-www-form-urlencoded 端点,CSRF 风险回归。

**REST API**

JWT in Authorization 是首选。Cookie-Based 必须配 SameSite + CSRF Token。

## 局限

- 老式 Web 应用(没用现代框架)防御少
- 嵌入 iframe / Webhook 场景复杂
- 子域名(b.example.com → a.example.com)Cookie 共享要小心
- 移动 App 内 WebView 行为不一致

## 工程实践要点

- 不写 GET 修改类 API(REST 原则:GET 只读)
- 现代框架 CSRF 防御默认开,不主动关闭
- Cookie 全部加 SameSite=Lax 或 Strict
- 敏感操作二次验证
- API 网关层加 Origin 检查

## 和其他概念的关系

CSRF 与 [[XSS跨站脚本]]、[[SQL注入]]、[[SSRF]] 同属 [[OWASP Top 10]] 经典 Web 攻击。它的防御深度依赖 [[Cookie与Session]] 安全属性、[[CORS跨域资源共享]] 同源策略,与 [[Web安全]] 头部组合。

CSRF 与 [[RESTful API]] 设计原则深度关联——遵循"GET 只读"等 HTTP 语义本身就是防御。在 SPA 时代,JWT in Header 模式让 CSRF 风险天然降低,显示安全策略与架构选择的耦合。

SameSite Cookie 是浏览器层降低 CSRF 风险的关键创新,展示了"基础设施改进"如何系统性消灭一类漏洞。

## 参考源

- raw/计算机/
- 相关:[[OWASP Top 10]]、[[XSS跨站脚本]]、[[Cookie与Session]]
