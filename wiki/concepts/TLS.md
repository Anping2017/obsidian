---
title: TLS
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: TLS 在 TCP 之上提供加密、身份认证、完整性保护,通过非对称密钥协商对称会话密钥,是 HTTPS、邮件、数据库等安全通信的基石。
---

# TLS

## 定义

**TLS(Transport Layer Security,传输层安全)** 是在 [[TCP握手与挥手]] 之上提供**加密(防窃听)、身份认证(防冒充)、完整性(防篡改)** 的协议。前身是 SSL(Secure Sockets Layer),Netscape 1995 年发明;TLS 1.0(1999)→ 1.1 → 1.2(2008,主流)→ 1.3(2018,现代)。是 [[HTTP协议]] 中 HTTPS、SMTP/STARTTLS、IMAP、数据库 TLS 连接、mTLS 服务网格等所有"S 后缀"协议的安全基石。

## 核心要点

- **三个核心保证**
  - **机密性**:对称加密保护数据,他人窃听看到密文
  - **身份验证**:服务端(可选客户端)证书验证身份
  - **完整性**:MAC / AEAD 防止数据被篡改
- **TLS 1.2 握手(经典 4 次往返简化版)**
  - 1. **ClientHello**:客户端 → 服务端,带支持的 TLS 版本、加密套件、随机数
  - 2. **ServerHello + Certificate + ServerKeyExchange**:服务端选定加密套件、发证书、发 DH 公钥(若用 DHE/ECDHE)
  - 3. **ClientKeyExchange + ChangeCipherSpec**:客户端发自己的 DH 公钥,生成会话密钥
  - 4. **Finished**:双方各自验证握手完整性,开始加密通信
  - **共 2 RTT**(基于 TCP 三次握手之上,总 3-4 RTT)
- **TLS 1.3 握手(简化为 1 RTT)**
  - 客户端在 ClientHello 时就发 DH 公钥(因加密套件选择简化,可猜)
  - 服务端 ServerHello + 证书 + Finished 一并发
  - **0-RTT 重连(Pre-Shared Key)**:重连时直接发数据,代价是抗重放略弱
- **加密套件(Cipher Suite)**
  - 形如 `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
  - 包含:**密钥交换(ECDHE)、签名(RSA)、对称加密(AES-256-GCM)、哈希(SHA384)**
  - TLS 1.3 把套件简化:只选对称算法 + 密钥派生,密钥交换固定为 (EC)DHE
- **证书(X.509)**
  - **结构**:主体(域名)、颁发者、有效期、公钥、签名
  - **PKI(Public Key Infrastructure)**:CA(根 → 中间 → 站点)层级签发
  - **验证流程**:浏览器内置根 CA 列表 → 验证证书链 → 检查域名匹配、有效期、CRL/OCSP 撤销
  - **自签名 / Let's Encrypt 免费证书 / 商业 OV/EV 证书**
- **完美前向保密(PFS,Perfect Forward Secrecy)**
  - 即使长期密钥泄露,过往会话仍安全
  - 通过 (EC)DHE 临时密钥实现:每次会话独立临时 DH 密钥对
  - TLS 1.3 强制 PFS,不再支持 RSA 密钥交换
- **mTLS(双向 TLS)**
  - 不仅服务端,客户端也提供证书
  - 服务端验证客户端证书后才允许连接
  - 用于 [[服务网格]] 中服务间通信、零信任网络、API 鉴权
  - Istio / Linkerd 默认 mTLS
- **常见攻击与防御**
  - **POODLE / BEAST / CRIME / Heartbleed**:历史漏洞,新版本 TLS 已修复
  - **降级攻击**:TLS 1.3 引入 downgrade protection
  - **MITM(中间人)**:严格证书验证防御;HSTS / Certificate Pinning 进一步加固
  - **重放攻击(0-RTT)**:仅幂等请求(GET)用 0-RTT
- **TLS 卸载(Termination)**
  - [[负载均衡]] / CDN 处理 HTTPS 解密,后端走 HTTP
  - **优势**:节省后端 CPU,集中管理证书
  - **劣势**:LB 到后端段不加密,内网信任假设
  - **现代趋势**:端到端 mTLS,服务网格透明加密
- **HTTPS = HTTP + TLS**
  - 浏览器地址栏小锁,SEO 加分,API 默认要求
  - HTTP/2 几乎只在 TLS 上工作(理论支持明文,实际浏览器要求 HTTPS)
  - HTTP/3(QUIC)内建 TLS 1.3,不可分离
- **性能优化**
  - **会话复用**:Session ID / Session Ticket 跳过密钥协商
  - **OCSP Stapling**:服务端附带证书撤销状态,免去客户端查询
  - **TLS False Start / 0-RTT**:握手期间提前发数据
  - **硬件加速**:CPU 的 AES-NI 指令、GPU 加速

## 和其他概念的关系

TLS 是 [[HTTP协议]] HTTPS 的安全层,与 [[TCP握手与挥手]] 配合提供 5-7 RTT 内的安全连接(TLS 1.3 已优化到 2-3 RTT)。

[[Web安全]] 中 HTTPS 是 XSS / 中间人 / 会话劫持等多种攻击的基础防线。

[[服务网格]](Istio、Linkerd)用 mTLS 实现服务间零信任通信,Envoy sidecar 透明加密。

[[API网关]] 和 [[负载均衡]] 是 TLS 卸载的典型位置,集中管理证书生命周期(配合 cert-manager / Let's Encrypt 自动续签)。

[[微服务]] 架构下,内部通信也建议 mTLS,放弃"内网安全"的假设。

QUIC / HTTP/3 把 TLS 1.3 内嵌到协议栈,握手与传输融合,1 RTT 完成连接 + 加密。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(安全 / 通信安全)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(数据安全)
