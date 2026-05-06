---
title: HTTP 协议
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/语言/PHP/03-应用实践层/Web开发基础/01-HTTP协议基础.md
created: 2026-05-05
updated: 2026-05-05
summary: HTTP 是基于 TCP/IP 的请求-响应应用层协议,从 1.0 到 3.0 经历无连接、长连接、多路复用、QUIC 的演进,是 Web 通信基础。
---

# HTTP 协议

## 定义

**HTTP(HyperText Transfer Protocol,超文本传输协议)**是 Web 上**应用层**的请求-响应协议,1991 年由 Tim Berners-Lee 提出,用于客户端(浏览器、移动应用)与服务器之间传输超文本(HTML)及任意资源。

它建立在传输层(早期 TCP,HTTP/3 改用 QUIC/UDP)之上,典型端口 80(HTTP)/ 443(HTTPS)。**无状态(Stateless)**是其核心特征 —— 每个请求独立,服务器不在协议层保存上下文(状态由 Cookie / Session 等机制补回)。

## 核心要点

### 请求-响应结构

**请求行**:`GET /index.html HTTP/1.1`
**请求头**:Host、User-Agent、Accept、Cookie、Authorization 等
**空行**
**请求体**:可选(GET 通常无,POST/PUT 有)

响应同构:状态行 + 响应头 + 空行 + 响应体。

### 主要方法(动词)

| 方法 | 含义 | 幂等 | 安全 |
|---|---|---|---|
| GET | 获取资源 | √ | √ |
| HEAD | 仅取头 | √ | √ |
| POST | 创建/动作 | × | × |
| PUT | 整体更新 | √ | × |
| PATCH | 部分更新 | × | × |
| DELETE | 删除 | √ | × |
| OPTIONS | 探测 / CORS 预检 | √ | √ |

**幂等**:多次执行效果同一次。**安全**:不修改服务端状态。
[[RESTful API]] 设计严格按动词语义。

### 状态码(Status Code)

| 范围 | 含义 | 例子 |
|---|---|---|
| 1xx | 信息 | 100 Continue, 101 Switching Protocols |
| 2xx | 成功 | 200 OK, 201 Created, 204 No Content |
| 3xx | 重定向 | 301 永久, 302 临时, 304 Not Modified |
| 4xx | 客户端错 | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | 服务器错 | 500 Internal, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

设计 API 时正确使用状态码至关重要。

### 头部分类

- **通用**:Date、Connection、Cache-Control
- **请求**:Host、User-Agent、Accept-*、Authorization、Cookie、Referer
- **响应**:Server、Set-Cookie、Location、ETag、Last-Modified
- **实体**:Content-Type、Content-Length、Content-Encoding

### 协议版本演进

| 版本 | 年份 | 关键特性 |
|---|---|---|
| HTTP/0.9 | 1991 | 仅 GET,纯文本 |
| HTTP/1.0 | 1996 | 头、状态码、多种方法,但每请求新连接 |
| HTTP/1.1 | 1997 | 长连接(Keep-Alive)、管道化、Host 头、分块编码 |
| HTTP/2 | 2015 | 二进制分帧、多路复用、头压缩(HPACK)、服务端推送 |
| HTTP/3 | 2022 | 基于 QUIC(UDP),解决 TCP 队头阻塞 |

HTTP/2 把多个并发请求复用到一个 TCP 连接(消除"6 连接限制");HTTP/3 用 QUIC 在丢包场景下显著降低延迟。

### 缓存控制

- **强缓存**:Cache-Control: max-age=3600 / Expires。直接用本地副本
- **协商缓存**:ETag(资源指纹)/ Last-Modified,304 Not Modified 节省带宽
- 浏览器缓存、CDN 缓存、反向代理缓存(Varnish、Nginx)层层加速

### Cookie / Session / Token

HTTP 无状态,需额外机制保留登录状态:
- **Cookie**:服务器 Set-Cookie,浏览器自动带在后续请求 Cookie 头
- **Session**:服务端存,Cookie 仅放 session ID
- **JWT(Token)**:服务端无状态,token 自含信息,签名验证。便于[[微服务]]/移动端
- **OAuth / OpenID**:第三方授权

### CORS(跨域资源共享)

浏览器同源策略默认禁止跨域 AJAX。CORS 通过响应头 `Access-Control-Allow-Origin` 等控制白名单。复杂请求触发 OPTIONS 预检。

### HTTPS = HTTP + TLS

TLS 提供:加密(对称密钥协商,非对称交换)、身份认证(证书链)、完整性(MAC)。Let's Encrypt 让证书免费,HTTPS 已是事实默认。HTTP/2 和 HTTP/3 实践上几乎只跑在 TLS 之上。

## 和其他概念的关系

HTTP 是[[RESTful API]]、GraphQL、WebSocket(从 HTTP 升级)、gRPC(基于 HTTP/2)等更高层协议的基础。它本身依赖 TCP/IP 协议栈、DNS 解析、TLS 握手。

[[微服务]]内部通信常用 gRPC(高效)或 RESTful HTTP/JSON(易调试);API 网关、负载均衡器、CDN 都在 HTTP 层操作。WebSocket 提供持久双向通信,比轮询效率高得多。

[[缓存]]策略大量基于 HTTP 头;HTTP 状态码也是判定告警/重试/熔断的关键信号(5xx 触发熔断、429 退避重试)。Web 安全(XSS、CSRF、CORS)的核心舞台就是 HTTP 协议。

## 参考源

- raw/计算机/开发学习/语言/PHP/03-应用实践层/Web开发基础/01-HTTP协议基础.md
