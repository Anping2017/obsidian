---
title: OAuth 2.0
type: concept
tags: [cs, web, security, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: OAuth 2.0 是 RFC 6749 定义的授权框架,通过四种授权模式让第三方应用代表用户访问受保护资源,核心是用 Access Token 解耦"我是谁"与"能做什么"。
---

# OAuth 2.0

## 定义

**OAuth 2.0** 是 IETF 在 RFC 6749(2012)发布的开放**授权(Authorization)** 框架。它解决一个核心问题:让第三方应用在**不获得用户密码**的前提下,代表用户访问其在另一服务上的资源。OAuth 2.0 不是登录协议(那是 [[OIDC]] 的工作),而是授权协议。

## 核心要点

### 1. 四个角色

- **Resource Owner**:用户(资源所有者)
- **Client**:第三方应用(想访问数据)
- **Authorization Server**:授权服务器(发 token)
- **Resource Server**:资源服务器(拿 token 取数据)

### 2. 四种授权模式(Grant Type)

#### Authorization Code(授权码,最常用)

```
1. Client → AS:重定向用户携带 client_id, redirect_uri, scope
2. 用户登录、同意
3. AS → Client:回调带 code
4. Client → AS:用 code + client_secret 换 access_token(后端发起)
5. Client → RS:Bearer access_token 调 API
```

加 PKCE 后是公开客户端(SPA、移动端)的标准。

#### Implicit(隐式,已弃用)

直接在 fragment 返回 token,token 暴露在浏览器历史。已被 Authorization Code + PKCE 取代。

#### Resource Owner Password Credentials

用户把账号密码直接给 Client。仅限官方第一方应用,违背 OAuth 初衷。

#### Client Credentials

服务到服务调用,无用户上下文,Client 用自己的凭证拿 token。机器对机器(M2M)场景用。

### 3. PKCE(Proof Key for Code Exchange)

公开客户端无法保密 client_secret。PKCE 让客户端生成随机 verifier,把它的 SHA-256 摘要(challenge)发给 AS,换 token 时再交 verifier。AS 校验通过才发 token。RFC 7636,现已被推荐为所有客户端默认。

### 4. Token 类型

- **Access Token**:访问 RS 的凭证,通常是 [[JWT]] 或不透明字符串,短期(15 分-1 小时)
- **Refresh Token**:用于换新的 access token,长期(数天-数月),仅在后端流转
- **ID Token**:[[OIDC]] 扩展才有,身份信息

### 5. Scope

Client 申请的权限范围,如 `read:profile`、`write:posts`。AS 在同意页向用户展示,授权服务器后续按 scope 限制 token 能力。

### 6. 安全考量

- redirect_uri 必须严格白名单
- state 参数防 CSRF
- HTTPS 强制
- 短 access token + refresh token rotation
- Token 存储:Web 后端 + httpOnly cookie 优先,SPA 内存优先

### 7. 历史

- OAuth 1.0(2010)签名复杂、流程繁琐
- OAuth 2.0(2012)简化但被批评"安全靠实现"
- OAuth 2.1(草案)整合 PKCE 强制、移除 Implicit、明确最佳实践

## 关系

- 扩展:[[OIDC]] 在 OAuth 2.0 基础上加身份层
- 载体:[[JWT]] 是 access token 常用格式
- 配合:[[Cookie与Session]] 用于保存 session 关联
- 应用:微信、Google、GitHub 登录都基于 OAuth
- 安全:[[Web安全]] 中专门一章

## 参考源

- raw/计算机/开发学习/语言/HTML/03-实践深化层/安全与最佳实践/
- 已有 wiki: [[Web安全]]
