---
title: JWT JSON Web Token
type: concept
tags: [cs, web, security, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: JWT 是 RFC 7519 规范的紧凑自包含 Token 格式,由 Header.Payload.Signature 三段 Base64URL 组成,签名保证不可篡改,无状态分布式认证主流方案。
---

# JWT JSON Web Token

## 定义

**JWT(JSON Web Token)** 是 RFC 7519 标准的紧凑、URL 安全、自包含的认证凭证格式。三段式结构 `header.payload.signature` 用 Base64URL 编码后用点连接,签名机制保证内容不可篡改。JWT 常被作为 [[Cookie与Session]] 中服务端 Session 的无状态替代,在分布式系统中尤其流行。

## 核心要点

### 1. 三段结构

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signature
```

- **Header**:`{"alg": "HS256", "typ": "JWT"}` —— 签名算法元数据
- **Payload**:claims 集合,如 `{"sub": "user123", "exp": 1700000000, "role": "admin"}`
- **Signature**:`HMAC-SHA256(base64Url(header) + "." + base64Url(payload), secret)`

### 2. Claim 分类

- **Registered**:`iss`(签发者)、`sub`(主体)、`exp`(过期)、`iat`(签发时间)、`aud`(受众)、`jti`(唯一 ID)
- **Public**:在 IANA JWT Registry 注册的公开 claim
- **Private**:业务自定义,如 `role`、`tenantId`

### 3. 签名算法

- **HS256**:HMAC + 共享密钥,简单但需双方持密
- **RS256**:RSA 非对称,签名方持私钥,验证方用公钥(适合 OAuth/OIDC 场景)
- **ES256**:ECDSA 椭圆曲线,签名更短性能更好

### 4. 与 Session Cookie 对比

| 维度 | Session+Cookie | JWT |
|---|---|---|
| 服务端存储 | 必需 | 不需要(无状态) |
| 撤销 | 删除 sessionId | 困难,需黑名单 |
| 容量 | sessionId 短 | Payload 数百字节~KB |
| 跨域/移动端 | 麻烦 | 灵活 Header 传递 |
| 实时权限变更 | 立即 | 需到期或黑名单 |

### 5. 安全陷阱

- **alg=none 攻击**:历史漏洞,允许无签名 token,所有库已修复
- **算法混淆**:把 RS256 改成 HS256 用公钥当密钥,需服务器严格校验 alg
- **Payload 不加密**:Base64 不是加密,任何人可解码;敏感信息不要放 Payload(用 JWE 加密版)
- **泄漏即长期失控**:exp 过长 + 无撤销机制 = 灾难
- **本地存储 vs Cookie**:localStorage 易被 XSS 偷,HttpOnly Cookie 更安全(代价是要防 CSRF)

### 6. 最佳实践

- 短 access token(15 分钟) + 长 refresh token
- Refresh token 加白名单/黑名单实现撤销
- HTTPS 强制
- Secret 使用 256-bit 强随机
- 关键操作(改密、付款)二次校验

### 7. 关联标准

- **JWS** RFC 7515:签名结构
- **JWE** RFC 7516:加密结构
- **JWK** RFC 7517:公钥发布格式
- **JWT** RFC 7519:claim 集合

## 关系

- 替代:[[Cookie与Session]] 服务端会话
- 应用:[[OAuth 2.0]] access token、[[OIDC]] id token 标准载体
- 跨域:配合 [[CORS跨域资源共享]] 在 Authorization 头传递
- 安全:[[Web安全]] 攻击面新增 token 泄漏维度
- [[微服务]]:无状态扩展的关键基础设施

## 参考源

- raw/计算机/开发学习/语言/HTML/03-实践深化层/安全与最佳实践/
- 已有 wiki: [[Web安全]]
