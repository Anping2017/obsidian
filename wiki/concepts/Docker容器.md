---
title: Docker 容器化
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/语言/PHP/04-高级应用层/部署运维/01-Docker容器化.md
  - raw/计算机/运维知识/容器化/Docker/
  - raw/计算机/运维知识/云服务/容器化+微服务.md
created: 2026-05-05
updated: 2026-05-05
summary: Docker 是基于 Linux Namespace 与 cgroups 的轻量级容器,把应用与依赖打包为可移植镜像,让"在我机器能跑"成为历史。
---

# Docker 容器化

## 定义

**Docker** 是流行的**容器化(Containerization)**平台:基于 Linux 内核的 Namespace 与 cgroups 机制,把应用及其全部依赖打包为**镜像(Image)**,运行时以**容器(Container)**形式与宿主机和其它容器隔离。

容器可以视为"轻量级虚拟机":共享内核,启动毫秒级,资源占用 MB 级,但具备进程、文件系统、网络的隔离视图。

## 核心要点

### 容器 vs 虚拟机

| | 虚拟机(VM) | 容器 |
|---|---|---|
| 隔离层 | Hypervisor | Linux 内核 |
| 启动 | 几十秒到分钟 | 毫秒到秒 |
| 资源 | 几 GB | 几 MB |
| 内核 | 各自独立 | 共享宿主机 |
| 隔离强度 | 强 | 中(共享内核) |
| 镜像 | GB 级 | MB - 几百 MB |

容器更轻、密度高;VM 更安全、跨内核能力(Linux VM 跑在 Windows 宿主)。

### 核心概念

- **镜像(Image)**:只读模板,按层(Layer)叠加,共享基础层节省空间
- **容器(Container)**:镜像运行实例,可启停删除
- **Dockerfile**:声明式构建脚本
- **仓库(Registry)**:存镜像,Docker Hub、Harbor、ECR
- **数据卷(Volume)**:持久化数据,生命周期独立于容器
- **网络(Network)**:bridge / host / overlay / macvlan

### Linux 内核基础

- **Namespace**:隔离 PID、Network、Mount、UTS、IPC、User
- **cgroups**:限制 CPU、内存、IO、网络配额
- **Union FS**(OverlayFS、AUFS):层叠文件系统,实现镜像的分层共享与 Copy-on-Write

### Dockerfile 关键指令

```dockerfile
FROM node:20-alpine          # 基础镜像
WORKDIR /app                  # 工作目录
COPY package*.json ./         # 复制(利用 Docker 层缓存)
RUN npm ci --production       # 执行命令
COPY . .                      # 复制源码
EXPOSE 3000                   # 声明端口
CMD ["node", "server.js"]     # 启动命令
```

设计原则:
- 利用层缓存(变化频率低的指令放前面)
- 多阶段构建(Build → Runtime)显著减小最终镜像
- 选小基础镜像(alpine、distroless)
- 一容器一进程

### 镜像优化

- 多阶段构建(Multi-stage Build)分离编译和运行
- 用 `.dockerignore` 排除 node_modules、.git
- 合并 RUN 减少层数
- 用小镜像(alpine 仅 5 MB,distroless 更精简)

### Docker Compose

通过 docker-compose.yml 一键启动多容器服务(Web + DB + Redis 等)。开发与简单部署常用,生产环境多用[[Kubernetes]]。

### 容器编排:Kubernetes

单机 Docker 解决"如何打包",[[Kubernetes]]解决"如何在集群中调度、弹性、自愈、滚动升级"。容器化是 K8s 的输入。

### 安全注意

- **不要以 root 运行容器进程**(USER 指令切换非 root)
- **镜像扫描**(Trivy、Snyk、Clair)检漏洞
- **最小权限**:--cap-drop=ALL --cap-add 必要权限
- **签名校验**:Sigstore、Notary 验证镜像来源
- **运行时安全**:Falco 监控异常行为

### 常见误区

- "Docker = 虚拟化":容器共享内核,不是 VM
- "Docker = 微服务":容器只是打包运行方式,单体也能用
- "用 Docker 就一定快":错误的 Dockerfile 反而慢、镜像臃肿

## 和其他概念的关系

Docker 是[[微服务]]架构事实上的标准打包方式 —— 每服务一镜像。它在底层依赖[[操作系统]]内核功能(Namespace/cgroups),向上被[[Kubernetes]]、Service Mesh、CI/CD 流水线消费。

容器化推动了不可变基础设施(Immutable Infrastructure)、声明式部署、十二要素应用(Twelve-Factor App)等理念的普及。Serverless(Lambda、Cloud Run)在底层多数也是某种轻量容器(Firecracker、gVisor)。

[[进程与线程]]的概念在容器内部仍适用 —— 容器只是进程的"隔离视图"。从宿主机看就是带特殊 namespace 的进程组。

## 参考源

- raw/计算机/开发学习/语言/PHP/04-高级应用层/部署运维/01-Docker容器化.md
- raw/计算机/运维知识/容器化/Docker/
- raw/计算机/运维知识/云服务/容器化+微服务.md
