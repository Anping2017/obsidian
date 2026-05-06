---
title: OIDC OpenID Connect
type: concept
tags: [cs, web, security, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: OIDC 是 OAuth 2.0 之上的身份层,通过 ID Token(JWT)与标准化用户信息端点提供"登录"语义,是现代单点登录与社交登录的事实标准。
---

# OIDC OpenID Connect

## 定义

**OIDC(OpenID Connect)** 是 OpenID Foundation 2014 年发布的认证协议,在 [[OAuth 2.0]] 授权框架之上**加一个身份层**。OAuth 2.0 只回答"client 能做什么",OIDC 多回答"用户是谁"。它通过标准化的 ID Token、UserInfo 端点和发现文档,让 Google/Microsoft/Auth0 等身份提供商(IdP)可以被任意应用直接接入。

## 核心要点

### 1. ID Token

OAuth 流程返回的 access token 之外,OIDC 多发一个 ID Token —— 一个关于**用户身份**的 [[JWT]]:

```json
{
  "iss": "https://accounts.google.com",
  "sub": "1234567890",
  "aud": "client-id",
  "exp": 1700000000,
  "iat": 1699996400,
  "email": "user@example.com",
  "email_verified": true,
  "name": "Alice"
}
```

Client 验证 ID Token 签名后,即可知道"这个用户是谁",无需再调用 API。

### 2. 标准 Claim

OIDC 规定一组身份相关 claim:`sub`、`name`、`given_name`、`family_name`、`email`、`picture`、`locale` 等。

### 3. UserInfo 端点

`/userinfo` 标准端点,Client 拿 access token 调用获取更详细的用户资料(scope 内的)。

### 4. Discovery

`https://example.com/.well-known/openid-configuration` 自动告诉 Client:

- 授权端点 URL
- Token 端点 URL
- 公钥位置(JWKS)
- 支持的 scope/claim/算法

实现"零配置接入"。

### 5. Scope

OIDC 在 OAuth scope 上扩展:`openid`(必需触发 OIDC 流程)、`profile`、`email`、`address`、`phone`、`offline_access`(发 refresh token)。

### 6. Flow 选择

- **Authorization Code Flow**:Web 后端、SPA(配 PKCE)
- **Hybrid Flow**:同时获得 code 和 ID token,前端立即知用户
- **Implicit**:已弃用

### 7. 单点登录(SSO)

OIDC 是企业 SSO 标准:Okta、Azure AD、Keycloak、Auth0 都通过 OIDC 协议接入应用。一次登录,N 个应用共享身份。

### 8. SAML 对比

| 维度 | SAML 2.0 | OIDC |
|---|---|---|
| 数据格式 | XML | JSON |
| 复杂度 | 高 | 中 |
| 移动/SPA 友好 | 差 | 好 |
| 适用 | 企业老系统 | 现代 Web/移动 |

## 关系

- 基于:[[OAuth 2.0]] 授权流
- 载体:[[JWT]] 作为 ID Token 标准格式
- 应用:Google/微信/GitHub 第三方登录
- 替代:SAML 在新建系统中
- 安全:[[Web安全]] 身份层基础

## 参考源

- raw/计算机/开发学习/中间层/iPaaS.md
- raw/计算机/开发学习/语言/HTML/03-实践深化层/安全与最佳实践/
