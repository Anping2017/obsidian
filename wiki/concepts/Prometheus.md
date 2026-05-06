---
title: Prometheus
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: Prometheus 是 CNCF 时序监控系统,以 pull 模式采集多维指标、用 PromQL 查询、与 Alertmanager 告警联动,是云原生监控事实标准。
---

# Prometheus

## 定义

**Prometheus** 是 SoundCloud 2012 年开源、2016 年捐赠给 CNCF 的时序监控系统,灵感源自 Google 的 Borgmon。它以**主动拉取(pull)** 模式采集指标,数据按"指标名 + 多维 label" 组织,用强大的 PromQL 查询,与 Grafana 可视化和 Alertmanager 告警联动,是 [[Kubernetes]] 时代云原生监控的事实标准。

## 核心要点

- **核心架构**
  - **Prometheus Server**:抓取 + 存储 + 查询
  - **Exporters**:把第三方系统指标转为 Prometheus 格式(node_exporter / mysqld_exporter)
  - **Pushgateway**:批处理 / 短任务推送指标的中转站
  - **Alertmanager**:告警去重、分组、路由、抑制
  - **Service Discovery**:从 K8s / Consul / 文件自动发现要监控的目标
- **数据模型**
  - **Metric Name + Labels**:`http_requests_total{method="GET",status="200"}`
  - **Time Series**:每个 (name, labels) 唯一组合是一个时间序列
  - **Sample**:某时刻的 (timestamp, value)
  - **多维数据**:同一指标按 method/status/path 切片分析
- **四种指标类型**
  - **Counter(计数器)**:单调递增,如 `http_requests_total`
  - **Gauge(仪表)**:可增可减,如 `cpu_usage_percent`
  - **Histogram(直方图)**:采样观察值放入预定义桶,服务端计算分位数
  - **Summary(摘要)**:客户端预计算分位数(P50/P95/P99)
- **Pull 模型**
  - Prometheus 主动从目标拉取(HTTP /metrics endpoint)
  - **优势**
    - 无目标自动剔除(几次拉取失败认为下线)
    - 控制采集频率
    - 简化配置(目标无需知道服务器)
  - **劣势**
    - 短任务(几秒就退出)采不到 → 用 Pushgateway
    - 跨网络复杂(需打通)
- **PromQL(查询语言)**
  - **瞬时向量**:`http_requests_total` 当前值
  - **范围向量**:`http_requests_total[5m]` 过去 5 分钟数据
  - **rate / irate**:计算 Counter 增长率
  - **聚合**:`sum by (status) (rate(http_requests_total[5m]))`
  - **告警规则**:`rate(errors[5m]) > 0.1`
  - **黄金 4 信号**:延迟、流量、错误、饱和度
- **告警(Alertmanager)**
  - **去重**:相同告警合并
  - **分组**:按 label 分组,避免告警洪水
  - **路由**:按服务 / 严重程度路由不同接收人
  - **抑制**:高级告警激活时压制低级
  - **静默**:维护期间临时屏蔽
- **存储**
  - **本地 TSDB**:写入磁盘,默认保留 15 天
  - **挑战**:单机不可水平扩展、数据容易丢
  - **Long-term storage**
    - **Thanos**:全球查询视图 + 对象存储归档
    - **Cortex / Mimir**:多租户云原生方案
    - **VictoriaMetrics**:Prometheus 兼容,性能 / 压缩更优
- **K8s 生态**
  - **Prometheus Operator**:CRD 声明式管理 Prometheus 实例
  - **kube-state-metrics**:K8s 对象指标
  - **node_exporter**:节点指标
  - **cAdvisor**:容器指标
- **使用最佳实践**
  - **Cardinality(基数)控制**:label 高基数(user_id, request_id)会爆炸,慎用
  - **指标命名约定**:`<namespace>_<subsystem>_<name>_<unit>` (如 `http_request_duration_seconds`)
  - **RED 方法**:Rate / Errors / Duration,服务级监控基础
  - **USE 方法**:Utilization / Saturation / Errors,资源级监控基础
- **与可观测性其他支柱的关系**
  - **Logs**:Loki(同公司)与 Prometheus 整合,LogQL 类似 PromQL
  - **Traces**:Tempo + Grafana 联动
  - **OpenTelemetry**:可作为 Prometheus 数据源,OTel Collector 输出 Prometheus 格式
- **替代与竞争**
  - **InfluxDB**:Push 模型,商业版强大
  - **Datadog / New Relic**:商业 SaaS,综合 APM
  - **OpenObserve / SigNoz**:开源 APM 替代

## 和其他概念的关系

Prometheus 是 [[可观测性三支柱]] 中"指标"的事实标准实现,常配合 Grafana(可视化)、Loki(日志)、Tempo(追踪)组成完整可观测性栈。

[[Kubernetes]] 与 Prometheus 是天作之合:K8s 各组件都暴露 /metrics,Prometheus Operator 让安装一键化。

[[微服务]] 中每服务都应暴露指标(请求数、错误率、延迟),由 Prometheus 统一收集。

[[熔断与降级]]、[[限流]] 的阈值调优依赖 Prometheus 数据。[[灰度发布与蓝绿部署]] 中,Prometheus 指标是判断是否扩量的依据。

[[流处理]] 系统可订阅 Prometheus 数据做实时异常检测。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(指标监控)
- raw/计算机/运维知识/容器化/Kubernetes/Kubernetes知识地图.md(监控生态)
