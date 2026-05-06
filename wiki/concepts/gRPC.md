---
title: gRPC
type: concept
tags: [cs, web, api, network, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: gRPC 是 Google 2015 年开源的高性能 RPC 框架,基于 HTTP/2 + Protocol Buffers,提供四种调用模式与流式双向通信,微服务内部首选 RPC 协议。
---

# gRPC

## 定义

**gRPC**(g 一开始代表 Google,后改为 generic)是 Google 2015 年开源的现代 RPC(Remote Procedure Call)框架。在 [[HTTP2协议]] 上以 Protocol Buffers(protobuf)为序列化格式,通过 IDL(`.proto` 文件)定义服务接口,跨语言生成强类型客户端/服务端代码。

## 核心要点

### 1. Protocol Buffers

```protobuf
syntax = "proto3";
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
}
message User {
  int64 id = 1;
  string name = 2;
}
```

Protobuf 的二进制编码体积比 JSON 小 3-10 倍,解析速度快 5-100 倍,且字段编号保证向后兼容。

### 2. 四种调用模式

- **Unary**:一次请求一次响应(类比函数调用)
- **Server streaming**:一次请求,服务器返回流(类似 [[SSE]])
- **Client streaming**:客户端流式上传,服务器单一响应
- **Bidirectional streaming**:双向流,类似 [[WebSocket]] 但强类型

### 3. 基于 HTTP/2

- 多路复用避免 TCP 连接数爆炸
- 首部压缩(HPACK)降低 RPC 元数据开销
- 流优先级让控制消息优于数据传输

### 4. 跨语言

protoc 编译器为 11+ 语言生成代码:Go、Java、Python、Node、C++、Rust、C#、Kotlin、Swift、Dart、Ruby。同一份 .proto 即接口契约,服务端和客户端独立选语言。

### 5. 与 REST/GraphQL 对比

| 维度 | [[RESTful API]] | [[GraphQL]] | gRPC |
|---|---|---|---|
| 编码 | JSON 文本 | JSON 文本 | Protobuf 二进制 |
| 模式 | 资源 | 查询语言 | RPC |
| 浏览器原生 | 是 | 是 | 否(需 grpc-web) |
| 性能 | 中 | 中 | 高 |
| 跨语言强类型 | 弱 | 中 | 强 |
| 流式 | 弱 | Subscription | 原生四种 |
| 适用 | 公开 API | 移动/聚合 | 内部微服务 |

### 6. grpc-web

浏览器无法直接说原生 gRPC(需 HTTP/2 frame 控制权),通过 envoy / grpc-web 代理可在前端使用 gRPC,但损失部分流式能力。

### 7. 应用

- [[微服务]] 内部通信(Kubernetes、Istio、etcd)
- 多语言后台服务集成
- 移动端高效网络层(Google 自家 App)

## 关系

- 跑在:[[HTTP2协议]] 之上
- 协议:[[微服务]] 间通信首选
- 对比:[[RESTful API]]、[[GraphQL]] 三种主流 API 风格
- 配合:Service Mesh、[[Kubernetes]] 服务发现

## 参考源

- raw/计算机/开发学习/中间层/iPaaS.md
- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md
