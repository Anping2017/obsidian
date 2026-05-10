---
title: ELK Stack(Elasticsearch + Logstash + Kibana)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: ELK Stack 是 Elastic 公司推出的开源日志/搜索/分析三件套——Elasticsearch 全文搜索引擎、Logstash 日志摄取、Kibana 可视化,长期是企业日志聚合事实标准,近年因协议变更和 Loki 等替代方案兴起,生态分化明显。
---

# ELK Stack(Elasticsearch + Logstash + Kibana)

## 定义

**ELK Stack** 是 Elastic 公司开源的三件套,长期作为企业日志聚合与全文搜索事实标准:
- **Elasticsearch**:基于 Apache Lucene 的分布式搜索与分析引擎(2010,Shay Banon)
- **Logstash**:日志数据摄取、解析、转换管道(2009)
- **Kibana**:Elasticsearch 数据的 Web 可视化界面(2013)

后期加入 **Beats**(轻量数据采集器,如 Filebeat、Metricbeat),形成 **Elastic Stack(ELK + B)** 完整栈。

## Elasticsearch 核心

**特征**

- 分布式、近实时(NRT)搜索
- 倒排索引(Inverted Index),全文检索毫秒级响应
- RESTful API,JSON 文档存储
- 水平扩展(Shard + Replica)
- 复杂聚合(metrics、histogram、percentile、moving average)
- 地理空间、向量搜索(8+ 起)

**核心概念**

- **Index**:类似数据库表,存文档
- **Document**:JSON 对象,基本存储单位
- **Shard**:Index 切片,主副本分散存储
- **Replica**:副本,提供高可用与并发查询
- **Mapping**:字段类型 schema(text、keyword、long、date)
- **Analyzer**:分词器,中文常用 ik_max_word

**典型查询**

```json
GET /logs/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "message": "error" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  },
  "aggs": {
    "by_service": { "terms": { "field": "service.keyword" } }
  }
}
```

## Logstash 角色

输入 → 过滤 → 输出 的管道:

```
input {
  filebeat { port => 5044 }
}
filter {
  grok { match => { "message" => "%{COMMONAPACHELOG}" } }
  date { match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ] }
  mutate { remove_field => [ "raw" ] }
}
output {
  elasticsearch { hosts => ["es:9200"] index => "nginx-%{+YYYY.MM.dd}" }
}
```

支持几十种 input(Kafka、Redis、Syslog、HTTP)和 output。但消耗资源高(JVM,500MB+),被 Beats 蚕食。

## Beats(轻量采集)

- **Filebeat**:文件日志(Nginx、应用日志)
- **Metricbeat**:系统/服务指标
- **Packetbeat**:网络协议
- **Heartbeat**:健康探活
- **Auditbeat**:审计事件

Go 写,内存几十 MB,可直接发往 Elasticsearch 或 Kafka,绕过 Logstash。

## Kibana 功能

- **Discover**:日志搜索
- **Visualize**:仪表盘构建
- **Dashboard**:多图组合
- **Lens**:拖拽式现代仪表盘
- **APM**:应用性能监控
- **Logs / Metrics / Traces**:专属界面
- **Machine Learning**:异常检测(付费)
- **Alerting**:告警规则

## 协议争议(2021)

Elastic 2021 年改协议——把 Elasticsearch 从 Apache 2.0 改为 SSPL/Elastic License。主要冲击:
- AWS、阿里云等云厂商不能直接卖托管 Elasticsearch
- AWS 分叉为 **OpenSearch**(2021),与 ELK 竞争
- 主流 Linux 发行版禁运 Elastic 仓库

2024 年 Elastic 部分重新支持 AGPL,但生态已分裂。

## OpenSearch(AWS 分叉)

- 完全开源(Apache 2.0)
- 命令行 / API 兼容 ES 7.10
- AWS、阿里、华为云托管
- 缺 Elastic 高级功能(ML、Alerting 部分)
- 社区活跃但商业支持单一

很多企业从 ES 转 OpenSearch 避免许可风险。

## 与 Loki 对比

**Grafana Loki(2018+,Grafana Labs)**

- 思想:**只索引标签,不索引内容**
- 全文搜索弱(grep 后过滤)
- 资源占用极低(对比 ES 1/10)
- 与 [[Grafana]]、Tempo、Mimir 同栈
- 适合:日志量大、查询模式简单

**对比**

| 维度 | ELK | Loki |
|---|---|---|
| 索引 | 全文 | 标签 |
| 存储 | 几 TB / 月成本高 | 几 TB / 月成本低 |
| 查询 | 任意字段毫秒级 | 标签快,内容 grep |
| 仪表盘 | Kibana | Grafana |
| 适合 | 安全审计、复杂查询 | 简单聚合、成本敏感 |

成本敏感场景从 ELK 转 Loki 是 2022-2024 主流趋势。

## 与其他可观测平台对比

| 平台 | 性质 | 强项 |
|---|---|---|
| ELK | 自部署 | 全文搜索、复杂查询 |
| OpenSearch | 自部署 | ELK 替代 |
| Loki | 自部署 | 成本极低 |
| Datadog | SaaS | 一站式 |
| Splunk | 自/SaaS | 企业老牌、安全合规 |
| New Relic | SaaS | APM |

## 部署架构

**典型生产**

```
应用 → Filebeat → Kafka(缓冲)→ Logstash(解析)→ Elasticsearch → Kibana
                                                      ↑
                                               OpenSearch Dashboards
```

Kafka 缓冲层避免 ES 暂时不可用导致日志丢失。

**资源规模(参考)**

- 每天 100GB 日志:ES 集群 3 节点 × 8C32G + 1TB SSD
- 每天 1TB 日志:ES 集群 6+ 节点,需调优
- 索引生命周期管理(ILM)滚动 → 冷存储 → 删除

## 局限

- ES 占用资源大(JVM + Lucene)
- 长期保留成本高(冷存储补 S3 仅部分缓解)
- 升级 / 重建索引耗时
- Mapping 设计需经验(过多字段炸 mapping)
- Logstash 性能瓶颈
- 协议变更带来法律风险

## 实践要点

**索引策略**

- 按天滚动(logs-2025.05.04)
- ILM 自动 hot/warm/cold/delete
- Index Templates 统一 mapping
- 字段数控制(避免动态映射爆炸)

**调优**

- JVM Heap < 32GB(超过反而慢)
- refresh_interval 调长(从 1s 到 30s)
- bulk write 提高吞吐
- 分片数量合理(每 shard 30-50GB)

**安全**

- 启用 X-Pack Security(免费版)
- 禁用 9200 公网暴露
- TLS 内部通信
- 审计日志开启

## 和其他概念的关系

ELK 是 [[可观测性三支柱]] 中"日志"支柱的经典实现,与 [[Prometheus]](指标)、Jaeger(追踪)互补。它在 [[微服务]] / [[Kubernetes]] 体系下是 SRE 排错主战场——所有服务日志通过 Filebeat → Kafka → ES 集中后,Kibana 全栈搜索定位问题。

ES 的全文搜索能力让它超越日志领域,被用于电商搜索([[BERT语义搜索算法]] 也常以 ES 为基础)、APM、SIEM(安全审计)。它是 Lucene 的"分布式包装",属 [[大数据]] 工具圈核心组件。

向量搜索(8+ 起)让 ES 进军 [[RAG]] / [[向量数据库]] 领域,与 Pinecone、Qdrant 形成竞争。

## 参考源

- raw/计算机/
- 相关:[[Grafana]]、[[Prometheus]]、[[可观测性三支柱]]
