---
title: HTTPS 加密超文本传输协议
type: concept
tags: [network, security, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: HTTPS 是 HTTP over TLS 的合称,通过 TLS 提供机密性、完整性、身份认证三重保障,已成为现代 Web 的事实默认。
---

# HTTPS 加密超文本传输协议

## 定义

**HTTPS(HyperText Transfer Protocol Secure)** 是 HTTP 协议在 [[TLS]](原 SSL)之上运行的加密版本,即 **HTTP over TLS**。它在保留 [[HTTP协议]] 应用层语义的同时,通过 TLS 提供三大安全保证:

1. **机密性(Confidentiality)**:对称加密载荷,中间人窃听无效。
2. **完整性(Integrity)**:消息认证码(MAC)防止篡改。
3. **身份认证(Authentication)**:X.509 证书 + CA 信任链验证服务器(可选双向)。

默认端口 **443**。自 2018 年 Chrome 标记 HTTP 为"不安全"、Let's Encrypt 让证书免费以来,HTTPS 已是 Web 通信的事实默认,**HTTP/2、HTTP/3 实际上只跑在 TLS 之上**。

## 核心要点

### 协议栈位置

```
应用层  : HTTP / HTTP/2 / HTTP/3
安全层  : TLS 1.2 / 1.3(HTTPS 的核心)
传输层  : TCP(HTTPS 标准)/ QUIC(HTTP/3 用 UDP)
网络层  : IP
```

[[QUIC]] 把 TLS 融入传输层,HTTP/3 的"HTTPS"严格来说是 HTTP-over-QUIC,但用户感知一致。

### TLS 1.3 握手简化

TLS 1.3 把握手压缩到 **1-RTT**(0-RTT 复用模式更短):

- ClientHello + 预选密钥参数 + 公钥
- ServerHello + 证书 + 预共享密钥确认 + Finished
- Client Finished + 应用数据

详见 [[HTTPS与TLS握手]] 条目。

### 证书与信任链

- **DV(Domain Validation)**:仅验证域名所有权,Let's Encrypt 等免费提供。
- **OV(Organization Validation)**:验证组织身份。
- **EV(Extended Validation)**:严格审核,过去浏览器有"绿条"标识(2019 后取消)。
- **根 CA → 中间 CA → 服务器证书**:信任链由操作系统/浏览器内置根证书校验。

### 现代特性

- **HSTS(HTTP Strict Transport Security)**:服务器响应头强制浏览器后续只用 HTTPS,防止降级攻击。
- **HSTS Preload**:加入 Chromium 静态名单,首访就走 HTTPS。
- **OCSP Stapling**:服务器代查证书状态,减少客户端 CA 查询延迟。
- **Certificate Transparency**:CA 颁发证书必须公开记录,防止恶意误发。
- **mTLS(双向 TLS)**:服务器与客户端互相验证,常用于零信任架构与微服务间通信。

### 部署影响

- **SEO**:Google 把 HTTPS 作为排名因素之一。
- **用户信任**:浏览器对 HTTP 显示"不安全",对 HTTPS 显示锁标。
- **安全合规**:[[GDPR]]、[[CCPA]]、PCI-DSS 等几乎都隐含或显式要求 HTTPS。
- **API 强制**:OAuth 2.0、Webhook、支付接口等基本要求 HTTPS。

## 典型应用 / 主要工具

- **证书签发**:Let's Encrypt、ZeroSSL、DigiCert、Sectigo;ACME 协议自动化签发与续期。
- **客户端**:浏览器、curl、wget、Postman 默认信任系统根 CA。
- **服务器配置**:Nginx、Apache、Caddy(自动 HTTPS)、HAProxy、Envoy。
- **CDN**:Cloudflare、Fastly、CloudFront 提供边缘 HTTPS 卸载。
- **检测工具**:SSL Labs Server Test、testssl.sh、Mozilla Observatory。
- **零信任**:[[零信任架构]] 内 mTLS 是身份验证的基石。

## 局限与陷阱

- **证书过期事故**:大型企业仍频繁发生因证书过期导致的服务下线。需自动续期 + 监控告警。
- **混合内容(Mixed Content)**:HTTPS 页面引入 HTTP 资源,浏览器拦截或警告。
- **SNI 泄露**:客户端连接时 SNI(目标域名)明文,Encrypted ClientHello (ECH) 在解决。
- **中间盒解密**:企业 SSL 检查、家长控制等会重发证书,削弱端到端安全。
- **CPU 成本**:握手计算 + 加密带来开销,需 hardware offload 或 session resumption。
- **私钥泄露**:一旦根 CA 或服务器私钥泄露,后果严重,需密钥轮换与 HSM 保护。

## 与其他概念的关系

- 协议基础:对应 [[HTTP协议]],HTTPS 是 HTTP + [[TLS]] 的合体。
- 握手细节:[[HTTPS与TLS握手]] 详细描述 1.2/1.3 握手过程。
- 协议演进:[[HTTP2协议]]、[[HTTP3协议]] 实践上几乎只用 HTTPS。
- 传输层:HTTP/3 + HTTPS 跑在 [[QUIC]] 上;HTTP/1.1、HTTP/2 + HTTPS 跑在 [[TCP握手与挥手]] 之上。
- 安全合规:与 [[GDPR]]、[[CCPA]]、[[隐私优先时代]] 等隐私合规体系紧密关联。
- 架构应用:[[零信任架构]] 中 mTLS 是核心验证机制。

## 参考源

- IETF RFC 8446: TLS 1.3
- Let's Encrypt 文档与 ACME 规范
- Mozilla SSL 配置生成器、SSL Labs 实践指南
