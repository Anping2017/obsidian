---
title: HTTPS 与 TLS 握手
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: HTTPS 通过 TLS 协议在 HTTP 之下加密通信,握手阶段完成密钥协商、身份验证、加密套件选择,TLS 1.3(2018)把握手简化为 1-RTT,Let's Encrypt 让证书免费,HTTPS 已成为现代 Web 默认。
---

# HTTPS 与 TLS 握手

## 定义

**HTTPS(HTTP Secure)** = HTTP + TLS,把 HTTP 报文用 TLS 协议加密、身份验证、防篡改后传输。它在 OSI 模型中:

```
应用层:    HTTP / HTTP2 / HTTP3
   ↓
安全层:    TLS(1.0/1.1/1.2/1.3)/ DTLS / QUIC
   ↓
传输层:    TCP / UDP
```

[[TLS]] 是 SSL 的继任者——SSL 由 Netscape 1995 推出,TLS 1.0 由 IETF 标准化(1999),TLS 1.3 是 2018 年最新主流版本。

HTTPS 已是现代 Web 默认——浏览器把 HTTP 站标"不安全",[[Let's Encrypt]] 让免费证书普及。

## TLS 1.2 握手(老,但仍广泛)

```
客户端                                      服务器
   │                                          │
   │── ClientHello ──────────────────────→   │
   │   (TLS版本、随机数、加密套件列表、SNI)    │
   │                                          │
   │← ── ServerHello ────────────────────────│
   │     (选定加密套件、随机数)                 │
   │                                          │
   │← ── Certificate ────────────────────────│
   │     (服务器证书链)                         │
   │                                          │
   │← ── ServerKeyExchange ──────────────────│
   │     (DH 公钥、签名)                       │
   │                                          │
   │← ── ServerHelloDone ────────────────────│
   │                                          │
   │── ClientKeyExchange ────────────────→   │
   │   (DH 公钥)                              │
   │                                          │
   │── ChangeCipherSpec ─────────────────→   │
   │── Finished(已加密)──────────────────→   │
   │                                          │
   │←── ChangeCipherSpec ──────────────────  │
   │←── Finished(已加密)─────────────────── │
   │                                          │
   │═══════ 应用数据(已加密)═══════════════│
```

**关键步骤**

1. **ClientHello**:支持的版本、密码套件、SNI(Server Name Indication,虚拟主机识别)
2. **ServerHello + Certificate**:服务器选定套件、发证书
3. **密钥交换(Key Exchange)**:用 ECDHE(椭圆曲线 Diffie-Hellman 临时)协商共享密钥
4. **Finished**:双方用密钥加密消息验证一致

总耗时:**2 RTT**(2 个网络往返)。

## TLS 1.3 握手(2018+)

简化大量,典型 1-RTT:

```
客户端                                      服务器
   │                                          │
   │── ClientHello ──────────────────────→   │
   │   (含 KeyShare:几个候选公钥)             │
   │                                          │
   │← ── ServerHello, KeyShare,──────────── │
   │     EncryptedExtensions,                 │
   │     Certificate, CertificateVerify,      │
   │     Finished(全部已加密)                  │
   │                                          │
   │── Finished ─────────────────────────→   │
   │                                          │
   │═══════ 应用数据 ═══════════════════════│
```

**改进**

- **1-RTT**(对比 1.2 的 2-RTT)
- **0-RTT 恢复**:再次连接时,客户端可直接发数据(有 replay 风险)
- **强制 PFS**:删除 RSA 密钥交换,只用 ECDHE
- **简化套件**:从几十个变 5 个核心套件
- **加密握手**:服务器证书也加密发送(防中间人嗅探域名)
- **删除弱算法**:RC4、3DES、MD5 全去除

## 关键概念

**1. 公钥基础设施(PKI)**

- **CA(Certificate Authority)**:签发证书的可信第三方
  - 商业:DigiCert、Sectigo、GoDaddy
  - 免费:[[Let's Encrypt]]、ZeroSSL
- **证书链**:站点证书 ← 中间 CA ← 根 CA(预装在浏览器/系统)
- **吊销**:CRL(撤销列表)、OCSP(在线查询)

**2. 加密套件(Cipher Suite)**

格式:**TLS_<密钥交换>_<认证>_<对称加密>_<MAC>**

例:`TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
- ECDHE:密钥交换(椭圆曲线 DH)
- RSA:认证
- AES_128_GCM:对称加密(AEAD)
- SHA256:MAC(认证加密时不需要单独 MAC)

TLS 1.3 简化为 5 个套件,不用单独指定密钥交换 / 认证。

**3. 前向保密(PFS)**

每次会话用临时密钥,服务器私钥泄露也不能解密历史流量。ECDHE 提供 PFS。

**4. SNI(Server Name Indication)**

ClientHello 中带域名,让服务器选对应证书(同 IP 多域名场景)。TLS 1.3 进一步加密 SNI(ESNI/ECH,部分浏览器支持)。

**5. ALPN(Application-Layer Protocol Negotiation)**

握手时协商 HTTP 版本(http/1.1、h2、h3)。

## Let's Encrypt 革命

2015 年 ISRG 启动的免费 CA:
- 90 天证书(强制自动续期)
- ACME 协议自动化(Certbot、acme.sh)
- 颁发量超所有商业 CA 总和
- 把 HTTPS 普及率从 30% 推到 90%+

**自动化流程**

```
certbot certonly --standalone -d example.com
# 验证你拥有域名(HTTP-01 / DNS-01)
# 颁发证书 → /etc/letsencrypt/live/example.com/
# 配 Nginx 用证书 → 自动加 cron 续期
```

## HSTS(HTTP Strict Transport Security)

防止用户被降级到 HTTP:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- max-age:浏览器记住"必须 HTTPS"多久
- includeSubDomains:子域名也强制
- preload:加入 Chrome HSTS Preload List(永久强制)

## 证书透明度(CT)

防止恶意 CA 误签证书:
- 所有合法证书必须提交到 CT Log
- 浏览器拒绝未在 CT Log 的证书
- 任何人可监视新颁发的证书(crt.sh 等服务)

## TLS 性能优化

**1. Session Resumption(会话恢复)**

- Session ID(老):服务器存会话状态
- Session Ticket(新):状态加密后给客户端
- TLS 1.3 PSK(Pre-Shared Key):通用机制

恢复连接 0-RTT,比新建快得多。

**2. OCSP Stapling**

服务器在握手中带证书有效性证明,客户端不需查询 CA → 减少延迟。

**3. HTTP/2、HTTP/3**

HTTPS 之上的多路复用、头压缩、QUIC,综合提速。

**4. Edge / CDN**

CDN 终止 TLS,边缘到客户端用 HTTPS,边缘到源站可 HTTP(信任内网)或 mTLS。

## 中间人攻击(MITM)与防御

**攻击方式**

- 公共 WiFi 嗅探(防御:TLS 加密)
- 假 CA 证书(防御:CT Log + Cert Pinning)
- 协议降级(防御:HSTS)
- SSL Strip(防御:HSTS、HTTPS 默认)

**Cert Pinning**

App 内置预期证书指纹,只信任特定证书。但维护痛苦(证书轮换),HTTP Public Key Pinning(HPKP)已被废弃,改用 Expect-CT。

## mTLS(双向 TLS)

不只服务器认证,客户端也提供证书:
- 服务到服务身份验证([[微服务]])
- 设备认证(IoT)
- 银行 / 金融关键场景

[[服务网格]](Istio、Linkerd)默认开 mTLS,自动证书轮换。

## TLS 部署最佳实践

**1. 测试与评分**

- SSL Labs(qualys.com/ssllabs):评 A-F
- testssl.sh:命令行
- 目标:A+

**2. 配置**

- 仅 TLS 1.2 / 1.3
- 优先 1.3
- 禁用 RC4、3DES、SHA1
- 强制 PFS
- HSTS 头
- OCSP Stapling

**3. 证书**

- 用 Let's Encrypt 或商业(信用卡支付场景需 EV / OV)
- 密钥长度:RSA 2048+ 或 ECDSA P-256
- 自动续期

## 调试工具

**OpenSSL**

```bash
# 测试连接
openssl s_client -connect example.com:443 -servername example.com -tls1_3

# 查证书
openssl x509 -in cert.pem -text

# 测试支持的版本
openssl s_client -tls1 / -tls1_2 / -tls1_3
```

**curl**

```bash
curl -v https://example.com  # 看握手细节
```

**浏览器 DevTools**

Network → Headers → Connection details:协议版本、套件、证书。

## 局限

- **CA 信任问题**:商业 CA 历史多次失误(DigiNotar 2011 倒闭)
- **证书管理复杂**:大企业几千证书需 PKI 平台
- **性能开销**:握手延迟,但近年硬件加速大幅降低
- **0-RTT replay 风险**:TLS 1.3 0-RTT 不适合所有场景
- **隐私**:SNI 仍部分明文(ECH 改善中)

## 和其他概念的关系

HTTPS 与 [[TLS]] 是 [[Web安全]] 的根基,与 [[OAuth 2.0]]、[[JWT]]、[[Cookie与Session]] 安全属性、[[CSP内容安全策略]] 等共同构成 Web 安全栈。它的"加密一切"思想是 [[零信任架构]] 的基础。

mTLS 是 [[服务网格]](Istio、Linkerd)实现服务间零信任的关键机制,与 [[Web安全]]、[[OWASP Top 10]] A02 加密失败防御直接相关。

[[HTTP2协议]]、[[HTTP3协议]] 都依赖 TLS 1.2/1.3,共同构成现代 Web 性能 + 安全双重提升。Let's Encrypt 普及让 HTTPS 从"高级"变"基础",体现"安全应该默认开启"的工程哲学。

## 参考源

- raw/计算机/
- 相关:[[TLS]]、[[Web安全]]、[[OAuth 2.0]]
