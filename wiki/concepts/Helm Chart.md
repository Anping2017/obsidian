---
title: Helm Chart
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Helm 是 Kubernetes 包管理器,Chart 把一组 K8s YAML 模板化、版本化、参数化,实现"一条命令部署完整应用",是云原生应用分发与升级的事实标准。
---

# Helm Chart

## 定义

**Helm** 是 [[Kubernetes]] 的包管理器,2015 年由 Deis(后并入 Microsoft)发起,2018 年成为 CNCF 毕业项目。**Helm Chart** 是它的核心抽象——把一个 K8s 应用所需的全部 YAML(Deployment、Service、Ingress、ConfigMap、Secret、PVC……)打包为模板化、参数化、版本化的发行包。

Helm 之于 K8s 类似 [[包管理器对比]] 中 npm 之于 Node:你可以发布 Chart 到仓库,他人通过 helm install 一条命令部署完整应用。Bitnami、Grafana、Prometheus、PostgreSQL 等几乎所有主流 OSS 都提供官方 Chart。

## 核心概念

**Chart**

一个目录,包含:
- Chart.yaml:元数据(名字、版本、依赖)
- values.yaml:默认参数
- templates/:K8s YAML 模板(用 Go template 语法)
- charts/:依赖的子 Chart
- README.md、NOTES.txt

**Release**

Chart + 用户值 → 部署到集群即一个 Release。同一 Chart 可部署多次(不同 namespace / 不同名字)。

**Repository**

Chart 的发布仓库:
- 公共:artifacthub.io、bitnami.com/charts
- 私有:Harbor、ChartMuseum、OCI 注册表

**Helm 命令**

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-pg bitnami/postgresql --set auth.password=secret
helm upgrade my-pg bitnami/postgresql --set persistence.size=20Gi
helm rollback my-pg 1
helm uninstall my-pg
helm list
```

## 模板语法示例

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels: {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          resources: {{- toYaml .Values.resources | nindent 12 }}
```

values.yaml:

```yaml
replicaCount: 3
image:
  repository: myapp
  tag: 1.2.3
service:
  port: 8080
resources:
  requests:
    cpu: 100m
    memory: 128Mi
```

通过 --set 或 -f my-values.yaml 在 install/upgrade 时覆盖。

## Helm v2 vs v3

**v2(2018-2020)**

- 服务端组件 Tiller,集群中常驻
- 安全模型有争议(Tiller 权限大)
- 已停止支持

**v3(2019+)**

- 移除 Tiller,改为客户端 + K8s Secret 存状态
- OCI 仓库支持(可推送到 Docker Hub、Harbor)
- 严格 schema 校验
- 库 Chart 与依赖更现代

当前所有教程默认 v3。

## 典型生产用法

**1. 应用部署**

```bash
helm install myapp ./charts/myapp \
  -f values-production.yaml \
  --namespace prod \
  --create-namespace
```

**2. 升级与回滚**

```bash
helm upgrade myapp ./charts/myapp -f values-production.yaml
# 失败回滚
helm rollback myapp
```

**3. 灰度发布**

通过多 Release 实现:
```bash
helm install myapp-v1 ./charts/myapp --set replicaCount=8
helm install myapp-v2 ./charts/myapp --set replicaCount=2,image.tag=2.0
# 逐步切流量
```

**4. CI/CD 集成**

GitHub Actions / GitLab CI 构建镜像 → helm upgrade --install。
配合 Argo CD / Flux CD 实现 GitOps([[CI_CD流水线]])。

## Helm 的优势

- **标准化分发**:OSS 与商业 K8s 应用都用 Helm
- **参数化**:同一 Chart 部署多环境(dev/staging/prod)
- **依赖管理**:Chart 可依赖其他 Chart(如 myapp 依赖 postgresql)
- **版本化与回滚**:每次 upgrade 留 Revision,可一键回滚
- **生态**:Artifact Hub 几千 Chart 即装即用

## Helm 的批评

**1. Go Template 语法痛苦**

YAML + Go template 混合,缩进、空格敏感:
```yaml
{{- range .Values.servers }}
  - name: {{ .name }}
{{- end }}
```
错一个空格全 Chart 渲染崩。

**2. 复杂 Chart 难维护**

Bitnami 等专业 Chart 几百行模板,新人难懂。

**3. 替代方案兴起**

- **Kustomize**:K8s 内置(kubectl apply -k),纯 YAML 叠加,不用模板
- **CDK8s**:用代码(TypeScript/Python)生成 YAML
- **Jsonnet / cuelang**:声明式语言生成 K8s 资源
- **Operator + CRD**:把应用部署逻辑封装为 K8s 原生资源

各有适用场景,Helm 仍是分发应用主流,内部应用很多团队用 Kustomize。

## 与 Operator 的关系

[[Operator模式]] 把"运维知识"编程化为 Controller。Helm Chart 适合"无状态 / 简单应用",Operator 适合"复杂有状态应用"——如数据库的备份、扩容、版本升级需要业务感知逻辑。

很多商业产品同时提供 Helm Chart(快速部署)和 Operator(生产级管理)。

## 安全实践

- 不直接暴露 ServiceAccount 全权限
- Secret 通过外部工具(External Secrets、Sealed Secrets)管理,不进 values.yaml
- helm install --dry-run --debug 先看渲染产物
- 用 helm lint 校验 Chart
- 限制 helm upgrade 权限到指定 namespace
- Chart 来源审核(只信任官方/内部仓库)

## 局限

- 模板可读性差
- 调试困难(渲染失败定位难)
- 不支持复杂条件逻辑(不及编程语言)
- 多环境配置膨胀
- helm template 输出仍需 kubectl apply,不直接管资源生命周期

## 和其他概念的关系

Helm 是 [[Kubernetes]] 应用分发的标准层,与 [[Docker容器]] 形成"镜像 + 部署声明"的分层组合。它在 [[CI_CD流水线]] 中是"构建后的下一步"——CI 构建镜像,CD 用 Helm 部署。

GitOps([[GitFlow与TrunkBased]] 的进一步)实践中,Helm Chart 与 Argo CD / Flux CD 配合——Git 仓库存 values.yaml,Argo 监控 Git 变化自动 helm upgrade。

Helm 与 [[Operator模式]]、[[服务网格]](Istio/Linkerd 自身的部署也用 Helm)、[[可观测性三支柱]] 工具链共同构成云原生运维基础。

## 参考源

- raw/计算机/
- 相关:[[Kubernetes]]、[[Docker容器]]、[[CI_CD流水线]]
