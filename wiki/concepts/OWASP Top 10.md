---
title: OWASP Top 10
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: OWASP Top 10 是开放 Web 应用安全项目每三年发布的 Web 应用十大安全风险清单,2003 年起成为 Web 安全教育、合规和安全测试的标准参考,2021 版以"破损访问控制"取代"注入"位居榜首,反映现代 API 时代的威胁演进。
---

# OWASP Top 10

## 定义

**OWASP(Open Worldwide Application Security Project)** 是 2001 年成立的非营利组织,致力于 Web 应用安全标准、教育与工具。**Top 10** 是其旗舰报告,每 3-4 年发布一次,基于全球数百万应用的安全测试数据,列出最常见、最危险的十大 Web 安全风险。

OWASP Top 10 是 [[Web安全]] 领域的"必读经典"——开发者培训、合规审计(PCI-DSS、ISO 27001)、安全测试工具(SAST/DAST)都以它为基准。

## 2021 版十大风险

**A01 Broken Access Control(破损的访问控制)**

最严重风险(取代 2017 第 5)。
- 用户能访问其他用户数据(IDOR:Insecure Direct Object Reference)
- 缺权限检查(后端只看前端没有按钮 = 致命错误)
- 提权(普通用户改 role=admin)
- 修复:服务端每个请求都验证当前用户对当前资源有权,不信任客户端

**A02 Cryptographic Failures(密码学失败)**

原"敏感数据暴露"。
- 传输不加密(HTTP)
- 弱加密算法(MD5、SHA-1、DES、RC4)
- 硬编码密钥
- 弱密钥长度
- 不验证证书
- 修复:[[TLS]]、AES-256-GCM、bcrypt/Argon2id 哈希密码、密钥用 KMS 管理

**A03 Injection(注入)**

原第 1,跌至第 3(因防御普及)。
- [[SQL注入]](Prepared Statement / ORM 防御)
- 命令注入(shell=True 危险)
- LDAP 注入、NoSQL 注入
- ORM 注入(参数构造不当)
- XSS([[XSS跨站脚本]])归到此类
- 修复:参数化查询、白名单输入校验、ORM/Query Builder

**A04 Insecure Design(不安全设计)**

新分类。强调架构层面缺陷:
- 无威胁建模
- 业务逻辑漏洞(免费试用注册无限次)
- 缺速率限制
- 缺反爬虫
- 修复:威胁建模(STRIDE)、安全设计评审、滥用案例分析

**A05 Security Misconfiguration(安全配置错误)**

- 默认密码
- 调试信息暴露(stack trace 给用户)
- 不必要服务开放
- 错误的 CORS / CSP / HSTS
- 不及时打补丁
- 修复:CIS 基线、自动化配置审计、最小化镜像

**A06 Vulnerable and Outdated Components(易受攻击的组件)**

- 依赖含已知漏洞(CVE)
- Log4Shell、struts2、Spring4Shell 等历史教训
- 修复:SBOM 软件物料清单、Dependabot / Snyk 扫描、定期升级

**A07 Identification and Authentication Failures(认证失败)**

原"破损认证"。
- 弱密码策略
- 凭据填充(撞库)
- Session 管理缺陷
- 多因素认证缺失
- JWT 存在客户端不验签
- 修复:MFA、密码哈希(Argon2)、会话管理([[Cookie与Session]])、Rate Limit

**A08 Software and Data Integrity Failures(软件和数据完整性失败)**

新分类。
- 不验证依赖完整性(npm install 任意包)
- 反序列化漏洞(Java、PHP、Python pickle)
- CI/CD 流水线被入侵
- 自动更新无签名验证
- 修复:依赖签名、SLSA 框架、CI 审计、不反序列化不可信数据

**A09 Security Logging and Monitoring Failures(日志监控失败)**

- 关键事件不记录(登录失败、权限变更)
- 日志缺细节(无 IP、UA)
- 日志被篡改
- 无告警(攻击者潜伏 200 天才被发现)
- 修复:结构化日志、SIEM([[ELK Stack]]、Splunk)、告警阈值、不可变日志

**A10 Server-Side Request Forgery(服务端请求伪造,SSRF)**

新进入 Top 10,因云时代危害放大。
- 攻击者让服务器请求内网资源(Metadata Service: AWS 169.254.169.254)
- 偷云凭据
- 探内网服务
- 历史案例:Capital One 2019 大泄露
- 修复:严格 URL 白名单、禁止内网 IP、出网代理

## 历史演变

| 版本 | 年份 | 主要变化 |
|---|---|---|
| 2003 | 首版 | 10 项基础 |
| 2007 | 2007 | XSS、CSRF 强化 |
| 2010 | 2010 | 注入第 1 |
| 2013 | 2013 | 强调身份认证 |
| 2017 | 2017 | XXE 进入,API 影响 |
| 2021 | 2021 | 设计、完整性、SSRF 新增 |

预计 2025 版会进一步反映 AI / LLM 应用风险。

## 配套项目

OWASP 不只 Top 10,还有几十个项目:

- **OWASP ASVS**:Application Security Verification Standard,详细安全要求
- **OWASP MASVS**:移动应用版
- **OWASP API Security Top 10**:API 专版
- **OWASP LLM Top 10**(2023+):AI 应用风险
- **OWASP Cheat Sheet Series**:具体漏洞防御速查
- **OWASP ZAP**:开源 Web 漏洞扫描器
- **OWASP Dependency-Check**:依赖漏洞扫描
- **OWASP Juice Shop**:故意有漏洞的练习站

## 防御深度示例

针对 SQL 注入,OWASP 推荐多层防御:

1. **应用层**:Prepared Statement / ORM
2. **输入校验**:白名单字符集
3. **错误处理**:不暴露 SQL 错误
4. **数据库账户**:最小权限原则
5. **WAF**:Web 应用防火墙拦截已知 payload
6. **监控**:可疑查询告警

任一层失守不致命。

## 与企业实践

**SDLC 嵌入**

- **设计阶段**:威胁建模(STRIDE)
- **编码阶段**:SAST(静态分析:SonarQube、Semgrep)、IDE 安全插件
- **测试阶段**:DAST(动态扫描:OWASP ZAP、Burp)
- **发布阶段**:依赖扫描(Snyk、Dependabot)
- **运行阶段**:WAF、RASP、SIEM 监控

DevSecOps 把安全左移到 CI/CD([[CI_CD流水线]])。

**合规对接**

- PCI-DSS:支付卡行业必须满足 OWASP Top 10
- ISO 27001:信息安全管理体系参考
- SOC 2:服务组织控制
- GDPR:欧盟数据保护条例

## 局限

- **过度依赖清单**:Top 10 是底线,不是"做了就安全"
- **业务逻辑漏洞难列**:每个应用业务逻辑独有,清单无法穷举
- **新威胁滞后**:3-4 年才更新,AI 安全等需新框架
- **"打勾"心态**:合规思维而非真正安全

## OWASP LLM Top 10(2023+)

针对 [[AI Agent]] / [[RAG]] 等 LLM 应用:

1. Prompt Injection([[提示注入]])
2. Insecure Output Handling
3. Training Data Poisoning
4. Model Denial of Service
5. Supply Chain Vulnerabilities
6. Sensitive Information Disclosure
7. Insecure Plugin Design
8. Excessive Agency
9. Overreliance
10. Model Theft

反映 AI 时代新风险——LLM 输出不可信、训练数据被污染、Agent 权限滥用。

## 和其他概念的关系

OWASP Top 10 是 [[Web安全]] 领域的入门必读,与 [[CSRF]]、[[XSS跨站脚本]]、[[SQL注入]]、[[SSRF]]、[[CSP内容安全策略]] 等具体技术构成完整知识体系。

它的"威胁建模"思想与 [[设计原则SOLID]]、[[设计模式]] 同属软件工程方法论——把人类隐性知识结构化、检查清单化。在 [[CI_CD流水线]] / DevSecOps 实践中,OWASP 工具(ZAP、Dependency-Check)是流水线必备阶段。

OWASP API Security Top 10 是 [[RESTful API]]、[[GraphQL]] 接口设计安全参考;OWASP LLM Top 10 与 [[提示注入]]、[[越狱攻击]] 等 AI 安全研究协同。

## 参考源

- raw/计算机/
- 相关:[[Web安全]]、[[CSRF]]、[[XSS跨站脚本]]
