---
title: Web 安全 Web Security
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/语言/Javascript/04-高级精通层/04-安全与测试/01-前端安全(XSS-CSRF).md
  - raw/计算机/开发学习/语言/PHP/03-应用实践层/安全编程/01-SQL注入防护.md
created: 2026-05-05
updated: 2026-05-05
summary: Web 安全研究 XSS、SQL 注入、CSRF 等攻击与防御,核心原则是不信任用户输入并最小化权限,OWASP Top 10 是工业基准。
---

# Web 安全 Web Security

## 定义

**Web 安全**研究 Web 应用面临的攻击与防御。核心原则:**不信任任何外部输入(Never Trust User Input)**、**最小权限**、**纵深防御**(多层失效不致全军覆没)。

行业基准是 **OWASP Top 10** —— 每几年更新的 Web 应用最严重风险清单(2021 版包括失效的访问控制、加密失败、注入、不安全设计、安全配置错误等)。

## 核心要点

### XSS(跨站脚本)

攻击者把恶意脚本注入网页,在受害者浏览器执行。
- **存储型**:脚本存在数据库,所有访问者中招(评论、留言)
- **反射型**:URL 参数携带,诱导点击
- **DOM 型**:前端 JS 直接把不可信数据写 DOM

**防御**:
- **输出编码(Output Encoding)**:HTML 上下文用 `&lt;`,JS 上下文用 \xNN,URL 上下文用 percent-encode
- **CSP(Content Security Policy)**:HTTP 头限制脚本来源
- **HttpOnly Cookie**:JS 无法读取 Session Cookie
- 框架天然防 XSS(React/Vue 默认转义),用 dangerouslySetInnerHTML 时格外小心

### SQL 注入(SQL Injection)

把 SQL 语句拼接进用户输入。
经典:`SELECT * FROM users WHERE name='${name}'`,name 输入 `' OR '1'='1` → `WHERE name='' OR '1'='1'` 全表泄露。

**防御**:
- **预处理语句(Prepared Statement)**:把数据和代码分离,数据库预编译 SQL,后绑定参数 → 完美防御
- **ORM**:主流 ORM 内部用预处理,默认安全
- **白名单验证**:数字字段强类型转换
- **最小权限**:Web 用户不要给 DROP / GRANT
- **WAF**:作为最后一道防线

### CSRF(跨站请求伪造)

诱导已登录用户的浏览器向受信任站点发起非本意请求。例:用户登录银行后访问恶意页,该页 `<img src="bank.com/transfer?to=attacker&amount=1000">`,浏览器自动带 Cookie 发送转账。

**防御**:
- **CSRF Token**:服务器随机 token 嵌入表单,提交时校验。攻击者无法跨域读取
- **SameSite Cookie**:`SameSite=Lax/Strict` 让浏览器不在跨站请求中带 Cookie
- **检查 Referer / Origin**(辅助)
- 关键操作要求重新输入密码或二次验证

### 其他常见攻击

- **SSRF(服务器端请求伪造)**:服务器代发请求,被滥用攻击内网。防御:URL 白名单、禁用元数据 IP(169.254.169.254)
- **命令注入**:把 shell 元字符注入 system() 调用。防御:不拼接 shell,用参数化 API
- **路径遍历(Path Traversal)**:`../../../etc/passwd`。防御:规范化路径并白名单
- **反序列化漏洞**:不可信数据反序列化为对象触发 RCE。Java、PHP、Python pickle 高危
- **点击劫持(Clickjacking)**:用透明 iframe 诱导误点。防御:`X-Frame-Options: DENY` 或 CSP frame-ancestors
- **暴力破解**:防御:验证码、限频、账号锁定、密码哈希慢函数(bcrypt/argon2)

### 加密基础

- **对称加密**:AES,加解密同一密钥。快但需安全分发密钥
- **非对称加密**:RSA、ECC,公私钥对。慢但解决密钥分发
- **混合**:TLS 用 RSA/ECDHE 协商对称密钥,然后用 AES 加密
- **哈希**:MD5(已破)、SHA-1(已破)、SHA-2/SHA-3。密码用慢哈希(bcrypt/scrypt/argon2)+ salt
- **数字签名**:私钥签、公钥验,防篡改和确权

### 认证与授权

- **认证(Authentication)**:你是谁。密码、TOTP、生物
- **授权(Authorization)**:你能做什么。RBAC、ABAC
- **OAuth 2.0**:第三方授权,Token 而非密码
- **OpenID Connect**:在 OAuth 之上加身份层
- **JWT**:自含签名 token,但要注意算法降级、未及时撤销等坑

### HTTPS 与证书

- TLS 1.2/1.3 是工业标准
- HSTS 头强制 HTTPS
- Let's Encrypt 提供免费证书
- HTTPS 防中间人(MITM)、保密、防篡改;但若服务端被攻陷无济于事

### 安全开发文化

- **左移(Shift Left)**:安全测试在开发早期介入
- **SAST/DAST**:静态/动态应用安全测试
- **依赖扫描**:Snyk、Dependabot 检查第三方库已知漏洞
- **威胁建模**:STRIDE
- **零信任(Zero Trust)**:不基于网络位置授予信任,每次请求都验证

## 和其他概念的关系

Web 安全跨越[[HTTP协议]]、Cookie/Session 机制、[[关系型数据库]] SQL、浏览器同源策略与 CSP、[[函数式编程]]中输入输出隔离思想。它与软件工程、运维、合规深度绑定。

[[微服务]]架构下,每服务都需考虑认证、授权、加密;Service Mesh 提供 mTLS 等一键开启的能力。云时代 IAM(身份与访问管理)、Secret Management(Vault、KMS)、SBOM 等是新标配。

[[Docker容器]]与[[Kubernetes]]需要额外维度的安全(镜像扫描、运行时检测、策略 OPA、Pod Security Standards),传统 Web 漏洞 + 云原生漏洞共同构成现代攻击面。

## 参考源

- raw/计算机/开发学习/语言/Javascript/04-高级精通层/04-安全与测试/01-前端安全(XSS-CSRF).md
- raw/计算机/开发学习/语言/PHP/03-应用实践层/安全编程/01-SQL注入防护.md
