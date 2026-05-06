---
title: Kubernetes
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/运维知识/容器化/Kubernetes/Kubernetes知识地图.md
  - raw/计算机/运维知识/云服务/Kubernetes/
created: 2026-05-05
updated: 2026-05-05
summary: Kubernetes 是 Google 开源的容器编排系统,以声明式 API 管理大规模容器集群的部署、扩缩、自愈与服务发现,是云原生事实标准。
---

# Kubernetes

## 定义

**Kubernetes**(简称 K8s,源自希腊语"舵手")是 Google 2014 年开源的**容器编排平台**,基于 Borg 系统经验。它管理跨多台机器的[[Docker容器|容器]]生命周期:**部署、扩缩、发现、负载均衡、自愈、滚动升级**,并通过**声明式 API**让运维以"期望状态"驱动系统。

K8s 是 CNCF(云原生计算基金会)的旗舰项目,也是云原生(Cloud Native)的事实标准。

## 核心要点

### 核心架构

**控制平面(Control Plane)**:
- **API Server**:所有操作入口,REST API
- **etcd**:存全局状态的 KV(基于 Raft)
- **Scheduler**:为 Pod 选节点
- **Controller Manager**:运行各种控制器(确保状态收敛到期望)
- **Cloud Controller Manager**:与云厂商集成

**数据平面(Worker Node)**:
- **Kubelet**:节点代理,管理 Pod 生命周期
- **Kube-Proxy**:维护节点的网络规则(iptables/IPVS)
- **Container Runtime**:containerd、CRI-O(早期 Docker)

### 关键资源对象

| 对象 | 作用 |
|---|---|
| **Pod** | 最小部署单元,1 或多个容器共享网络/存储 |
| **Deployment** | 管理无状态 Pod 的副本与滚动升级 |
| **StatefulSet** | 管理有状态 Pod(持久身份与存储) |
| **DaemonSet** | 每节点一个 Pod(日志、监控代理) |
| **Job/CronJob** | 一次性/定时任务 |
| **Service** | 给一组 Pod 提供稳定 VIP 与负载均衡 |
| **Ingress** | HTTP 七层网关,域名/路径路由 |
| **ConfigMap/Secret** | 注入配置和敏感信息 |
| **PersistentVolume/Claim** | 存储抽象与申领 |
| **Namespace** | 多租户/项目隔离 |

### Pod:基本单元

Pod 是一组**共享网络命名空间和存储卷**的容器。同一 Pod 内容器通过 localhost 互访。常见模式:
- **Sidecar**:辅助容器(日志收集、Service Mesh 代理)
- **Adapter / Ambassador**

为什么是"Pod 而非容器"?因为有些紧密配合的服务必须同生死、共享 IPC,容器粒度太细。

### 声明式与控制器模型

用户用 YAML 描述"我要 3 个 Nginx 副本",K8s 控制器持续比对实际与期望,差异即调和(Reconcile)。这是 K8s 区别于命令式工具(如 Ansible 单次执行)的核心哲学,使系统**自愈**。

### 网络模型

四个核心网络问题:
1. **容器到容器**(同 Pod):localhost
2. **Pod 到 Pod**(同/跨节点):每 Pod 独立 IP,直接互通(无 NAT) → 由 CNI 插件实现(Calico、Flannel、Cilium)
3. **Pod 到 Service**:虚拟 IP(ClusterIP),由 kube-proxy 转发
4. **外部到 Service**:NodePort、LoadBalancer、Ingress

### 存储

- **emptyDir**:Pod 生命周期临时存储
- **hostPath**:节点本地路径(慎用,绑节点)
- **PV/PVC**:抽象存储申请。底层可对接 NFS、Ceph、云盘
- **StorageClass**:动态供应

### 关键能力

- **滚动升级**:逐步替换旧 Pod,保证可用
- **金丝雀/蓝绿**:流量灰度
- **HPA**:基于 CPU / 自定义指标自动扩缩 Pod
- **VPA**:垂直扩缩(改 Pod 资源)
- **Cluster Autoscaler**:根据需求增减节点
- **健康检查**:liveness / readiness / startup probe
- **资源限制**:requests + limits,QoS 三类
- **滚动更新与回滚**:`kubectl rollout`

### 周边生态

- **Helm**:K8s 包管理器(Chart 模板化部署)
- **Operator**:把领域知识编程化为控制器(如 Postgres Operator)
- **Service Mesh(Istio、Linkerd)**:把流量治理下沉到 sidecar
- **GitOps(Argo CD、Flux)**:Git 是真理之源,自动同步集群
- **Knative、KEDA**:Serverless 在 K8s 上的实现
- **Prometheus、Grafana、Jaeger**:可观测性栈

### 复杂度的代价

K8s 极强大但有显著学习与运维成本:
- 数十种 CRD,YAML 篇幅长
- 升级复杂,API 版本变迁
- 故障排查跨多层(应用、容器、K8s 控制器、节点、网络)
- 小团队可考虑托管(EKS、GKE、AKS、阿里 ACK)或更轻量替代(Nomad、Docker Swarm)

## 和其他概念的关系

K8s 建立在[[Docker容器]]之上,与 CI/CD 流水线、可观测性栈、API Gateway 共同构成云原生平台。它的声明式 API + 控制器模型对软件设计影响深远 —— 推动了"控制器模式"在数据库、中间件管理中的复用(Operator 框架)。

[[微服务]]架构在 K8s 上获得最佳运行环境:服务发现、负载均衡、滚动升级开箱即用。Service Mesh 把通信治理(限流、熔断、追踪)从应用代码下沉到 sidecar。

底层依赖[[操作系统]]内核(Namespace/cgroups)、[[图]]论(调度本质是图匹配)、分布式共识(etcd Raft)。

## 参考源

- raw/计算机/运维知识/容器化/Kubernetes/Kubernetes知识地图.md
- raw/计算机/运维知识/云服务/Kubernetes/
- raw/计算机/运维知识/云服务/容器化+微服务.md
