---
title: SSRF 服务器端请求伪造
type: concept
tags: [security, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: SSRF 是攻击者诱使服务器代为发起任意请求的漏洞,利用服务端可信网络位置访问内网、云元数据、回环地址,Capital One 1 亿用户泄漏即典型案例,OWASP API Top 10 重点项。
---

# SSRF 服务器端请求伪造

## 定义

**SSRF(Server-Side Request Forgery,服务器端请求伪造)** 是一类 Web 安全漏洞:攻击者构造请求,让**服务端**而非自己发起对任意 URL 的网络访问。由于服务器通常处于"可信网络"(能访问内网、云元数据、数据库管理面),SSRF 让攻击者借服务器身份穿透外部边界,触达本应隔离的资源。OWASP 在 2021 年单独将 SSRF 列入 Top 10(A10),并在 [[OWASP API Top 10]] 中保留。

## 核心要点

### 1. 漏洞模式

任何接受用户提供 URL 后由服务端发起请求的功能都是潜在入口:

- 网页"通过 URL 抓取图片预览"
- Webhook 配置、回调地址
- PDF 生成器(渲染外部资源)
- OAuth redirect_uri 处理不当
- 文件上传中的"从 URL 导入"
- XML 解析中的外部实体(XXE)派生 SSRF
- SSRF + Open Redirect 串联绕过过滤

### 2. 经典攻击目标

- **回环地址**:`http://127.0.0.1:8080/admin` 访问本机管理面
- **内网横移**:`http://10.0.0.5/` 内网服务发现
- **云元数据**:AWS `http://169.254.169.254/latest/meta-data/iam/security-credentials/` 拿到临时凭证
- **协议滥用**:`file://`、`gopher://`、`dict://` 触发文件读、未授权 Redis、SMTP 攻击
- **DNS Rebind**:绕过基于域名的过滤

### 3. 代表案例

- **Capital One(2019)**:WAF 配置不当 + SSRF 拿到 IAM 角色,泄漏 1 亿+ 用户数据,FFIEC 罚款 8000 万美元
- **GitLab、Slack、Shopify** 等多次曝出 SSRF 高危漏洞
- **MS Exchange ProxyLogon、ProxyShell** 链路含 SSRF 步骤

### 4. 防御要点

- **白名单出站域名 / IP**,默认拒绝
- 显式拒绝**保留地址段**:127.0.0.0/8、10.0.0.0/8、172.16.0.0/12、192.168.0.0/16、169.254.0.0/16、::1、fc00::/7
- 仅允许 `http`/`https` schema,禁用 file/gopher/dict
- **DNS 解析后再校验 IP**,防 DNS Rebind(应用层重新解析并对比)
- 禁用或代理掉**云元数据服务**(AWS IMDSv2 强制要求会话 token,缓解 SSRF)
- 输出请求**经独立网络命名空间 / 出站代理**,与业务网络隔离
- 配合 [[WAF]]、出站流量监控、DLP

### 5. 与相邻漏洞区分

- **CSRF**:让"用户浏览器"代替用户发请求;SSRF 让"服务器"代替攻击者发请求
- **XXE**:XML 解析触发外部实体加载,常作为 SSRF 入口
- **Open Redirect**:仅做跳转,不发请求,但常被用作 SSRF 绕过

## 典型应用 / 防御工具

- **Burp Suite Collaborator** 检测盲打 SSRF
- **AWS IMDSv2**、Azure / GCP 元数据服务加固
- **Cloudflare Zero Trust / Egress Gateway** 出站统一管控
- 库级别防御:Python `requests` + 自定义 adapter、Java URLConnection 域名验证

## 局限与陷阱

- 完全禁止用户输入 URL 不现实(预览、Webhook 等业务必备)
- 简单字符串过滤极易绕过:`@`、八进制、十六进制 IP、URL 编码、IPv4 映射 IPv6
- "DNS 检查 + 实际请求"两次解析时间窗导致 DNS Rebind 攻击
- 中间件 / 框架默认行为不同,统一治理难度大
- 修复后仍要**轮转所有云端凭证**,假设已被读出

## 与其他概念的关系

- 同族漏洞:[[CSRF]]、[[XXE]]、[[Open Redirect]]、[[OWASP Top 10]]
- 上位概念:[[Web安全]]、[[云安全]]
- 攻击链路:[[内网横向移动]]、[[凭证窃取]]
- 防御协同:[[WAF]]、[[Zero Trust]]、[[IMDSv2]]
- 工具链:[[Burp Suite]]、[[ZAP]]
- 案例参考:[[Capital One数据泄漏]]

## 参考源

- OWASP Top 10 2021 - A10:2021 SSRF
- PortSwigger Web Security Academy - SSRF
- Capital One 漏洞披露报告(2019)
- AWS 安全最佳实践文档(IMDSv2)
