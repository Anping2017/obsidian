---
title: CORS 跨域资源共享
type: concept
tags: [cs, web, network, security, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: CORS 是浏览器同源策略的受控豁免机制,通过预检请求(OPTIONS)与响应头(Access-Control-*)让服务器声明允许的跨源访问,是前后端分离的基础。
---

# CORS 跨域资源共享

## 定义

**CORS(Cross-Origin Resource Sharing)** 是 W3C 标准,让浏览器在保留**同源策略(Same-Origin Policy, SOP)** 安全保障的前提下,通过特定 HTTP 头协商,允许网页发起跨源(协议+域名+端口任一不同)的请求。它是前后端分离、CDN、第三方 API 集成的基础。

## 核心要点

### 1. 同源策略

浏览器的核心安全模型:`https://a.com` 上的脚本默认不能读 `https://b.com` 的响应。SOP 防止恶意网站窃取其他站点的用户数据。

### 2. 简单请求(Simple Request)

满足三条:GET/HEAD/POST、仅安全首部、Content-Type 为 `text/plain`/`application/x-www-form-urlencoded`/`multipart/form-data`。

直接发送,服务器响应需带:
```
Access-Control-Allow-Origin: https://a.com
```

否则浏览器隔离响应,JS 看不到。

### 3. 预检请求(Preflight)

非简单请求(如 PUT、DELETE、自定义 Header、JSON Content-Type)前,浏览器自动先发 `OPTIONS` 请求探路:

```
OPTIONS /api/x
Origin: https://a.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Authorization, Content-Type
```

服务器返回:
```
Access-Control-Allow-Origin: https://a.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 86400
```

只有都允许才发实际请求。Max-Age 缓存预检结果减少开销。

### 4. 凭证模式

默认 fetch 不带 Cookie。要带:

```js
fetch(url, { credentials: 'include' })
```

服务器必须回 `Access-Control-Allow-Credentials: true` 且 `Access-Control-Allow-Origin` 不能是 `*`(必须是具体域名),这是 CORS 安全核心约束。

### 5. 常见错误

- **后端只设了 Allow-Origin,不允许 Headers**:预检失败
- **Allow-Origin: \* + credentials: include**:浏览器拒绝
- **没在 Nginx 层处理 OPTIONS**:预检 404
- **以为 CORS 是后端校验**:其实**浏览器才是执行者**,curl/Postman 完全无视 CORS

### 6. 替代方案与历史

- **JSONP**:利用 `<script>` 不受 SOP 限制的历史 hack,只支持 GET,已淘汰
- **代理服务器**:前端走同源,后端转发(开发环境常用)
- **postMessage**:跨窗口/iframe 通信
- **Service Worker**:可拦截请求做透明代理

## 关系

- 上层:[[HTTP协议]] 头机制
- 守门:[[Web安全]] 同源策略
- 配合:[[Cookie与Session]]、[[JWT]] 鉴权时凭证模式必读
- 相关:CSRF 与 CORS 不同 — CORS 防读,CSRF 防写
- 工具:nginx/Caddy/API 网关常代为处理

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-3 前后端数据交互.md
- 已有 wiki: [[Web安全]]
