---
title: Grafana
type: concept
tags: [programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Grafana 是 2014 年开源的可视化仪表盘平台,通过插件化数据源支持 Prometheus、InfluxDB、Loki、Elasticsearch 等数十种后端,是云原生监控、可观测性的标准前端。
---

# Grafana

## 定义

Grafana 是 Torkel Ödegaard 在 2014 年开源的数据可视化与监控仪表盘平台。它的核心价值在于:**不存储数据,只可视化**——通过插件化的"数据源(Data Source)"对接 Prometheus、InfluxDB、Loki、Elasticsearch、MySQL、CloudWatch 等几十种后端,统一呈现指标、日志、追踪数据。

它是云原生可观测性(Observability)的事实前端,与 Prometheus 一同成为 SRE/DevOps 工具链标配。Grafana Labs 公司围绕开源建立商业生态,推出 Loki(日志)、Tempo(追踪)、Mimir(指标存储)、Grafana Cloud(SaaS)。

## 核心概念

**Data Source(数据源)**

支持的主要类型:
- 时序指标:Prometheus、InfluxDB、Graphite、OpenTSDB
- 日志:Loki、Elasticsearch、Splunk
- 追踪:Jaeger、Zipkin、Tempo
- 关系数据库:MySQL、PostgreSQL、SQL Server
- 云监控:CloudWatch、Azure Monitor、Stackdriver
- APM:Datadog、New Relic(付费)

**Dashboard(仪表盘)**

可视化面板的容器,JSON 定义。

**Panel(面板)**

仪表盘上的单个图表,支持多种类型:
- Graph / Time series:时序折线图
- Stat / Single Stat:单值大数字
- Gauge:仪表盘
- Bar Chart / Heatmap:柱状/热力图
- Table:表格
- Logs:日志面板
- Pie Chart、Histogram、Geomap、Status Map 等

**Variables(变量)**

仪表盘下拉框,使用户切换 region、namespace、host 等过滤维度,一份仪表盘服务多场景。

**Annotations(注释)**

时间轴上标注事件(部署、告警、重启),帮助关联指标变化与具体事件。

**Alerting(告警)**

阈值告警,触发后通知 Slack、Email、PagerDuty、Webhook、钉钉、企业微信。

## 典型架构

```
[Apps] → [Prometheus] → [Grafana]
[Apps] → [Loki]       → [Grafana]
[Apps] → [Tempo]      → [Grafana]
                           ↓
                      [Slack/Email]
                       (Alert)
```

或基础设施监控:
```
[Servers] → [Node Exporter] → [Prometheus] → [Grafana]
[K8s]     → [kube-state-metrics] → [Prometheus] → [Grafana]
```

## 仪表盘示例

**主机监控**

- CPU、内存、磁盘、网络
- Load Average
- 进程 Top
- 异常告警

**应用监控**

- QPS / 延迟 / 错误率(RED 三原则)
- JVM 堆 / GC(Java)
- Goroutines(Go)
- 自定义业务指标

**Kubernetes 监控**

- 集群总览
- Node 资源使用
- Pod 状态、CPU、内存
- Deployment 滚动情况
- 网络流量

## Grafana 生态

**Loki**

Grafana 自家轻量日志系统,模仿 Prometheus 设计哲学:
- 只索引 label,不索引内容
- 与 Prometheus 共享 query 语法(LogQL)
- 价格远低于 Elasticsearch

**Tempo**

分布式追踪后端,与 Jaeger/Zipkin 兼容,无索引、按 trace_id 直查。

**Mimir**

水平扩展的 Prometheus 兼容存储,大规模指标场景。

**Grafana Cloud**

托管版,免费层 10K 系列指标 + 50GB 日志,中小企业首选。

## 三大可观测性支柱

Grafana 把传统的"监控"扩展为"可观测性(Observability)":
- **Metrics(指标)**:数值时序,Prometheus
- **Logs(日志)**:文本事件,Loki
- **Traces(追踪)**:请求路径,Tempo

三者通过 trace_id、label、时间互相关联,在 Grafana 中跳转探索。

## Grafana vs 其他工具

| 维度 | Grafana | Datadog | New Relic | Kibana |
|---|---|---|---|---|
| 开源 | 是 | 否 | 否 | 是 |
| 数据源 | 多 | 自家 | 自家 | Elasticsearch |
| 价格 | 自部署免费 | 高 | 高 | 自部署免费 |
| UI | 灵活 | 极强 | 强 | 中 |
| 适合 | 自建/混合 | SaaS 简单 | 企业 | 日志为主 |

## 商业模式

Grafana Labs 双轨:
- 开源核心(Apache 2.0,2024 起部分新功能改 AGPL)
- 商业版 Enterprise:RBAC、SSO、审计、White-Label
- Grafana Cloud SaaS

2024 年 Grafana 反垄断挑战 Datadog 一定程度成功,被认为是"开源可观测性"的赢家。

## 实践经验

- 仪表盘设计原则:USE(Utilization、Saturation、Errors)资源用,RED(Rate、Errors、Duration)服务用
- 不要过度仪表盘化,5-10 张关键面板比 50 张烦杂的好
- 模板变量(Variables)让一份仪表盘服务多场景
- 折扇视图避免分散注意力
- 用 Annotation 关联部署事件
- 告警优先,可视化第二

## 局限

- 仅可视化,不存数据(需配合 Prometheus 等)
- 大规模面板加载慢
- 新手学习曲线(LogQL、PromQL、变量)
- 复杂业务指标需大量 dashboard 定制
- 移动端体验一般

## 参考源

- raw/计算机/
- 相关:[[现代云原生架构]]、[[Docker容器]]
