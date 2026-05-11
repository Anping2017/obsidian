---
title: Datadog(可观测性 SaaS)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Datadog 是 2010 年创立的可观测性 SaaS 平台,把指标、日志、APM、用户监控、安全集中到一站式 UI,通过 Agent 与 200+ 集成服务覆盖全栈,以"贵但完整"成为云原生企业可观测主流选择。
---

# Datadog(可观测性 SaaS)

## 定义

**Datadog** 是 Olivier Pomel 与 Alexis Lê-Quôc 在 2010 年创立的可观测性 SaaS 平台。它的核心命题:**把分散的监控工具(Nagios + Graphite + ELK + APM)统一到一个 SaaS UI**,工程师在一个仪表盘看完整系统。

Datadog 2019 年纳斯达克上市,2024 年市值数百亿美元,是 SaaS 行业增长标杆,与 New Relic、Splunk Observability 同列三大商业可观测平台。

## 为什么不自部署

[[ELK Stack]] + [[Prometheus]] + [[Grafana]] + Jaeger 自部署需:
- 多套基础设施(ES、Loki、Prom、Cortex 等)
- DBA / SRE 运维成本
- 高可用、扩缩容难
- 跨工具关联难

Datadog 一键搞定。代价:**贵**——按主机、按数据量计费,中型公司年支出 $100k-$1M+。

## 核心模块

**1. Infrastructure Monitoring**

- 服务器 CPU / 内存 / 磁盘 / 网络
- Kubernetes 集群 / Pod / Container
- 云资源(AWS / GCP / Azure 自动发现)
- 网络拓扑(NPM:Network Performance Monitoring)

**2. APM(Application Performance Monitoring)**

- 分布式追踪([[分布式追踪]])
- 服务地图(Service Map)自动生成
- 端点性能(P50/95/99 延迟)
- 错误率与堆栈
- 数据库慢查询
- 与代码部署关联(版本对比)

**3. Logs**

- 日志聚合(类 [[ELK Stack]])
- 全文搜索 + Facet
- Logs to Metrics(从日志生成指标)
- Logs to Traces(关联追踪)
- 数据采样、归档到 S3

**4. RUM(Real User Monitoring)**

- 真实用户浏览器/手机端性能
- [[Core Web Vitals]] 指标
- 用户会话回放(Session Replay)
- 错误监控(类 [[Sentry]])

**5. Synthetic Monitoring**

- 定时探活(类似 Pingdom)
- API 测试
- 浏览器测试(模拟用户操作)

**6. Security**

- Cloud Security Posture Management(CSPM)
- Cloud Workload Security
- Application Security(IAST)
- SIEM-lite

**7. CI Visibility**

- CI/CD 流水线性能监控
- 测试稳定性(flaky 率)
- 与 [[CI_CD流水线]] 集成

**8. Database Monitoring**

PostgreSQL / MySQL / MongoDB 慢查询、Plan 分析。

## Agent 架构

```
Servers / Containers / K8s Pods
       │
       Datadog Agent(Go,~50MB)
       │  - 收集 metrics、logs、traces
       │  - 本地缓冲、压缩
       │
       │ HTTPS
       v
Datadog Cloud(US / EU / 亚太)
       │
       Web UI / API / Alerts
```

Agent 是 Go 写的,资源占用低,自动发现 Docker / K8s 容器。

## 集成生态

200+ 内置集成,包括:
- 云:AWS、GCP、Azure 全部主要服务
- 数据库:PostgreSQL、MongoDB、Redis、Elasticsearch
- 中间件:[[Apache Kafka|Kafka]]、RabbitMQ、Nginx、HAProxy
- Web 框架:Spring、Django、Express、Rails
- AI:OpenAI、Anthropic、Hugging Face
- DevOps:GitHub、Jenkins、CircleCI
- 通知:Slack、PagerDuty、Microsoft Teams、Jira

每个集成自动收集相关指标 / 日志 / 追踪。

## 与 OpenTelemetry

Datadog 长期推自家 SDK(dd-trace-*),近年支持 [[OpenTelemetry]]:
- 接收 OTLP 格式
- 转换为 Datadog 内部格式
- 但部分高级功能仍需 dd-trace 专属

策略上,Datadog 不希望客户用 OTel 后切换到其他平台,但事实上必须支持以保持生态友好。

## 价格(2024 参考)

按维度计费:

| 模块 | 价格 |
|---|---|
| Infrastructure | $15-23/host/月 |
| APM | $31/host/月 |
| Logs | $0.1/GB ingest + $1.7/M event 索引 |
| RUM | $1.5/1000 sessions |
| Synthetic | $5/10000 tests |
| Security | $20/host/月 |

中型公司(50 主机 + APM + Logs)月账单 $5k-$10k,大企业月 $50k-$500k。

## 实战经验

**1. Standard Tags 必备**

每个资源加标签:
- env: prod / staging / dev
- service: order-api
- version: v1.2.3
- team: payments

是后续筛选 / 关联的关键。

**2. SLO / SLI**

定义服务等级目标(99.9% 可用性),Datadog 自动追踪:
- Error Budget 消耗
- 燃尽率
- 关联告警

**3. 告警去噪**

- Composite Alert(多条件组合)
- Anomaly Detection(机器学习)
- Forecast Alerts(预测趋势)
- 抑制相关告警(防雪片)

**4. Dashboard as Code**

Terraform / API 把仪表盘版本化:
```hcl
resource "datadog_dashboard" "main" { ... }
```

避免点点点配置,可 PR 审查。

**5. Logs 分层**

不是所有日志都需索引(贵):
- Index:重要应用日志
- Archive:发到 S3,需要时回放
- Live Tail:实时查看不索引

## 与同类对比

| 平台 | 强项 |
|---|---|
| Datadog | 全栈一站,DX 优 |
| New Relic | APM 老牌 |
| Dynatrace | AI 自动诊断 |
| Splunk Observability | 企业,SIEM |
| Honeycomb | 高基数查询 |
| Lightstep | SLO + 因果 |
| Grafana Cloud | 开源工具 SaaS 化 |

Datadog 最广,但贵;Honeycomb / Lightstep 在工程文化深的团队受欢迎。

## 自部署替代(节省成本)

完整开源栈替代 Datadog:
- Metrics:[[Prometheus]] + Thanos / Mimir
- Logs:Loki / [[ELK Stack]]
- Traces:Jaeger / Tempo
- Dashboard:[[Grafana]]
- Alerts:Alertmanager
- RUM:Sentry + 自建
- Synthetic:checkly / Uptime Robot

代价:运维 SRE 团队、HA 架构、跨工具关联弱。

## 何时上 Datadog

**该上**

- 团队 < 200 工程师,运维能力有限
- 业务复杂、跨多云/区域
- 监控成熟度要快速提升
- 预算可承受

**不上**

- 创业小团队,Sentry + 一两个免费工具够
- 数据合规严(中国大陆部分行业)
- 数据量极大(自建 Prometheus + ClickHouse 反而便宜)
- 已大量自建,迁移成本高

## 局限

- **价格预算难控**:数据量增长 = 账单飙升
- **数据出域**:中国大陆合规挑战
- **Vendor Lock-in**:dd-trace 专属逻辑迁移痛
- **告警泛滥**:工程师 alert fatigue
- **新功能频出**:跟进学习成本

## 与 SRE 实践结合

Google SRE 书的核心实践在 Datadog 上落地:
- SLO / SLI / Error Budget(内置)
- Toil 跟踪(Custom Metrics)
- Postmortem 文化(集成 Jira / Confluence)
- On-call(集成 PagerDuty)

## 和其他概念的关系

Datadog 与 [[ELK Stack]]、[[Grafana]]、[[Prometheus]]、[[Sentry]]、[[分布式追踪]] 等开源工具构成"商业 SaaS vs 自部署开源"两条路径。它把 [[可观测性三支柱]] 的全部内容统一到 SaaS 平台,降低了"小团队也能有大公司监控水平"的门槛。

它的"全栈集成"哲学与 [[Slack协作平台]]、[[Notion文档协作]] 等"一站式 SaaS"思路一致——为分散工具问题提供商业整合。

它与 [[CI_CD流水线]]、[[Kubernetes]]、[[微服务]] 等云原生工具链深度整合,是企业从"工具孤岛"走向"统一平台"的代表实践。

## 参考源

- raw/计算机/
- 相关:[[可观测性三支柱]]、[[Grafana]]、[[Sentry]]
