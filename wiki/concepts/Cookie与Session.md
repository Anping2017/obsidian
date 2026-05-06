---
title: Cookie 与 Session
type: concept
tags: [cs, web, security, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: Cookie 是浏览器自动携带的小型键值对,Session 是服务器维护的会话状态,二者配合解决 HTTP 无状态痛点;现代 Web 还需关注 SameSite、HttpOnly、Secure 三大属性。
---

# Cookie 与 Session

## 定义

**Cookie** 是服务器通过 `Set-Cookie` 头下发、浏览器存储并在后续请求中自动携带的键值对。**Session** 是服务器端为每个用户维护的会话状态,通常以 sessionId(存于 Cookie)关联。两者共同解决 [[HTTP协议]] 无状态、每次请求独立的根本限制。

## 核心要点

### 1. Cookie 关键属性

| 属性 | 作用 |
|---|---|
| `Domain` | 哪些域名可访问 |
| `Path` | 哪些路径生效 |
| `Expires`/`Max-Age` | 过期时间;无则为会话 Cookie(关浏览器消失) |
| `Secure` | 仅 HTTPS 传输 |
| `HttpOnly` | JS 不可读取(防 XSS 偷取) |
| `SameSite` | Strict/Lax/None,防 CSRF |

### 2. SameSite 演进

- **Strict**:跨站请求一律不带 Cookie(连点链接也不带)
- **Lax**(2020 Chrome 默认):top-level GET 导航带,POST 不带
- **None**:跨站照带,但必须 `Secure`

强制 Lax 默认 + 第三方 Cookie 即将退出(Chrome 2024-2025 阶段性弃用),广告追踪面临重构。

### 3. Session 存储模式

- **服务器内存**:简单,但多实例无法共享、重启丢失
- **Redis 集中存储**:生产标准,毫秒级,带过期
- **数据库**:可靠但慢
- **JWT 替代**:把状态搬到客户端,服务器无状态(详见 [[JWT]])

### 4. Cookie 与 Token 对比

| 维度 | Cookie+Session | [[JWT]] Token |
|---|---|---|
| 存储 | 服务器维护 | 客户端持有 |
| 携带 | 浏览器自动 | 需手动加 Header |
| 撤销 | 删 sessionId 即可 | 必须维护黑名单 |
| 跨域 | 受 [[CORS跨域资源共享]] 限制 | 灵活 |
| 无状态扩展 | 难 | 易 |

### 5. 安全风险

- **会话劫持**:HTTPS 必须 + HttpOnly 防 [[Web安全]] 中的 XSS
- **CSRF**:浏览器自动带 Cookie 的副作用,SameSite=Lax + Token 双重防御
- **Cookie 注入**:对 SET-COOKIE 拼接用户输入需转义

### 6. 单点登录(SSO)

跨域共享会话靠:

- 共同顶级域名 + Domain=.example.com
- CAS / OAuth 协议中的票据交换
- [[OAuth 2.0]] / [[JWT]] 跨域携带

## 关系

- 解决:[[HTTP协议]] 无状态
- 防御:CSRF(SameSite)、XSS(HttpOnly)— [[Web安全]] 核心
- 替代:[[JWT]] 的无状态方案
- 跨域:与 [[CORS跨域资源共享]] credentials 模式联动
- 上层:[[OAuth 2.0]] 与 [[OIDC]] 的会话载体之一

## 参考源

- raw/计算机/开发学习/语言/HTML/03-实践深化层/安全与最佳实践/
- 已有 wiki: [[Web安全]], [[HTTP协议]]
