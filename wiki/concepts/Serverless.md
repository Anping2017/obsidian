---
title: Serverless
type: concept
tags: [cs, cloud, stub]
sources:
  - raw/计算机/云原生/
created: 2026-05-05
updated: 2026-05-05
summary: Serverless 不是「无服务器」,而是「无需关心服务器」的云计算范式;开发者只交付函数或容器,平台按用量计费、自动扩缩容、按调用付费,代表 AWS Lambda、Cloudflare Workers、Vercel Functions。
---

# Serverless

## 定义

Serverless(无服务器)是一种**云计算范式**,开发者**只关注业务代码,无需管理底层服务器、操作系统、容量规划、扩缩容**,云平台按实际使用计费(按调用次数 + CPU 时间 + 内存)。

它不是真的「没有服务器」,而是把服务器的运维责任完全转移到云供应商。Serverless 不等于 FaaS(函数即服务),后者只是其最常见形态;广义 Serverless 还包括无服务器数据库、消息队列、容器(AWS Fargate)等。

## 核心要点

### 两大主流形态

| 形态 | 抽象单位 | 代表 |
|---|---|---|
| FaaS(函数即服务) | 单函数 | AWS Lambda、Google Cloud Functions、Azure Functions |
| 容器型 Serverless | 容器镜像 | Cloud Run、AWS Fargate、Cloudflare Containers |
| 边缘 Serverless | JS 函数 | Cloudflare Workers、Vercel Edge Functions、Deno Deploy |
| 全栈 Serverless | 应用 | Vercel、Netlify、Supabase |

### 核心特征

- **按需运行**:无请求时实例为零
- **冷启动**:从零拉起需要数毫秒到数秒,影响首次响应
- **自动扩缩**:并发请求触发实例克隆
- **无状态**:实例间不共享内存,需借外部存储
- **细粒度计费**:按 100ms 或 1ms 计费,精确到调用次数

### 适用 vs 不适用

适用:

- 事件驱动任务(API 网关、定时任务、消息处理)
- 流量起伏大的应用
- 边缘计算(地理就近响应)
- 创业项目快速验证

不适用:

- 长时间运行(> 15 分钟)
- 状态密集(WebSocket 长连)
- 重 IO 数据库密集应用(冷启动 + 连接池问题)
- 极致低延迟要求(冷启动不可接受)
- 需要稳定 IP / VPC 私有连接

### 冷启动问题

冷启动是 Serverless 的核心痛点:

- Java/.NET:数秒级,业内称「噩梦」
- Node.js / Python:几百毫秒到 1~2 秒
- Go / Rust:数十到数百毫秒
- Cloudflare Workers(V8 isolate):亚毫秒级

缓解方案:

- 预留并发(Provisioned Concurrency,但失去成本优势)
- SnapStart(Lambda 对 Java)
- 选轻量运行时(Edge runtimes、WebAssembly)
- 保持实例热(定时 ping)

### 锁定与可移植性

各 Serverless 平台 API 不兼容,直接编程会高度锁定。缓解方案:

- 抽象框架:Serverless Framework、SST、AWS SAM
- 标准:OpenFaaS、Knative
- 写「无平台」代码:用 HTTP 函数 + 通用库

## 和其他概念的关系

Serverless 是 [[现代云原生架构|云原生]] 演进的下一阶段:从虚拟机 → 容器 → Kubernetes → Serverless,抽象层次不断上升。它与 [[微服务]] 配合可以做到极致细粒度——每个函数即一个服务。

[[边缘计算|Edge Computing]] 与 Serverless 结合催生了「边缘函数」生态(Cloudflare Workers、Vercel Edge),让代码部署到全球数百节点,毫秒级响应。

[[Serverless|FaaS]]、[[Serverless|BaaS]](后端即服务)、[[Jamstack]] 体系都基于 Serverless 思想。Vercel、Netlify、Supabase 等成为「全栈 Serverless 平台」。

[[DevOps]] 在 Serverless 时代演化为 NoOps:运维责任进一步左移到平台。然而可观测性、故障定位、成本管控成为新的复杂度来源。

## 参考源

- raw/计算机/云原生/
- AWS Lambda、Cloudflare Workers 文档
- Mike Roberts《Serverless Architectures》
