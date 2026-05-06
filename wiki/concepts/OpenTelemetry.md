---
title: OpenTelemetry
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: OpenTelemetry 是 CNCF 统一的可观测性数据采集标准,合并 OpenTracing + OpenCensus,提供跨语言 SDK、Collector、协议,使指标/日志/追踪三支柱与厂商解耦。
---

# OpenTelemetry

## 定义

**OpenTelemetry(OTel)** 是 CNCF 的孵化级项目,2019 年由 OpenTracing 与 OpenCensus 合并而来,目标是为应用提供**统一的可观测性数据(指标、日志、追踪)采集标准**。它定义了规范、API、SDK、协议(OTLP)、Collector,让用户与具体后端(Jaeger / Prometheus / Datadog)解耦,是当代可观测性的事实标准。

## 核心要点

- **诞生背景**
  - **OpenTracing**(2016):仅追踪规范,API 无实现
  - **OpenCensus**(Google,2018):追踪 + 指标 + 完整 SDK
  - 两者用户重叠,2019 年合并为 OpenTelemetry
  - 同时支持三支柱:Traces / Metrics / Logs
- **核心组件**
  - **API**:语言无关的接口定义
  - **SDK**:各语言实现(Java / Go / Python / .NET / Node.js / Ruby...)
  - **Instrumentation Libraries**:对常见框架(Spring / Express / Flask / gRPC)自动埋点
  - **Collector**:独立进程,接收 / 处理 / 导出遥测数据
  - **OTLP(OpenTelemetry Protocol)**:统一传输协议(gRPC + Protobuf / HTTP)
- **数据模型**
  - **Trace**:由多个 Span 组成的有向无环图
  - **Span**:一段操作,含 name、start/end、attributes(键值对)、events、links
  - **Metric**:Counter / Gauge / Histogram / ExponentialHistogram
  - **Log**:LogRecord 含 timestamp、severity、body、attributes、trace_id 关联
  - **Context Propagation**:W3C TraceContext 标准,trace_id / span_id 通过 HTTP / gRPC Header 跨服务传递
- **Collector 架构**
  - **Receiver**:接收数据(OTLP / Jaeger / Prometheus / Zipkin)
  - **Processor**:批处理 / 采样 / 重打 label / 增减字段
  - **Exporter**:发送到后端(Prometheus / Jaeger / Datadog / Loki / Splunk)
  - **配置即代码**:YAML 声明 pipeline,组合极灵活
- **采样策略**
  - **Head-based(头部采样)**:Span 创建时按概率决定保留
  - **Tail-based(尾部采样)**:在 Collector 等所有 Span 完成后,按规则保留(慢请求 / 错误请求)
  - **Probabilistic / Rate Limiting / Error Sampling**
- **自动埋点 vs 手动埋点**
  - **自动**:无需改代码,Java Agent / .NET Profiler / Python Bytecode 注入
  - **手动**:开发者主动 startSpan / addAttribute,粒度更精细
  - 实际混合使用
- **生态与采纳**
  - **后端无关**:输出 OTLP,后端任选(Jaeger / Tempo / Datadog / Honeycomb / 商业)
  - **CNCF 毕业项目**(2024)
  - **Datadog / New Relic / Dynatrace** 等商业 APM 全面拥抱 OTel SDK
  - **K8s** Operator 简化部署
- **典型架构**
  - 应用集成 OTel SDK → 输出 OTLP →
  - OTel Collector(集群 / Sidecar)→
  - 分发到 Prometheus(指标)+ Jaeger(追踪)+ Loki(日志)
  - Grafana 统一查询 + 关联三支柱
- **与传统方案对比**
  - **OTel 优势**
    - 厂商无关,降低 lock-in
    - 跨语言一致 API
    - 三支柱统一采集
    - 社区生态丰富
  - **挑战**
    - 仍在演进,API 偶有变更
    - SDK 性能开销需关注
- **OTel + eBPF**
  - eBPF 工具(Pixie、Cilium)可生成 OTel 格式数据
  - 实现"零代码改造"的可观测性
- **采用建议**
  - 新项目直接用 OTel
  - 老项目逐步迁移:先 SDK 改 OTLP 输出,后端不变
  - Collector 部署为 DaemonSet(每节点一个)+ Gateway(集群级聚合)

## 和其他概念的关系

OpenTelemetry 是 [[可观测性三支柱]] 的统一采集标准,与 [[Prometheus]](指标存储)、Jaeger / Tempo(追踪存储)、Loki / ELK(日志存储)互补:OTel 收数据,后端存数据。

OTel Collector 本质是数据管道,与 [[流处理]](Kafka Streams / Flink)思想相通,具备路由 / 过滤 / 转换能力。

[[微服务]] 调用链跨服务传递 trace_id,正是 OTel Context Propagation 的核心。

[[服务网格]] (Istio / Linkerd) 内置 OTel 支持,sidecar 自动产生指标 + 追踪。

[[Kubernetes]] Operator 让 OTel 部署一键化,K8s 元数据(pod/namespace)自动加到遥测属性。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(观测与监控)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(可观测性栈)
