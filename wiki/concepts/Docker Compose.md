---
title: Docker Compose
type: concept
tags: [programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Docker Compose 是 Docker 的多容器编排工具,用 YAML 文件定义服务、网络、卷,一条命令启动整套应用栈,是开发环境多服务架构和单机生产部署的标准选择。
---

# Docker Compose

## 定义

Docker Compose 是 Docker 官方提供的多容器应用编排工具,源自 2014 年 Orchard Labs 的 Fig 项目(被 Docker 收购)。它通过 docker-compose.yml(后改为 compose.yml)单一 YAML 文件,声明一个应用栈所有的容器、网络、存储卷,并通过简短命令(up、down、logs、restart)管理整套环境。

Compose 是 [[Docker容器]] 之上的"编排第一站":单机内多服务协作场景的最佳工具。比起 [[Kubernetes]] 的复杂度,它配置极简、上手即用;比起原生 docker run + 多个 -p、-v 参数,它声明式可维护。

## 典型场景

- 本地开发环境(Web App + DB + Redis + Queue)
- 单机生产部署(中小规模)
- [[CI_CD流水线|CI/CD]] 中的集成测试环境
- 演示与教程

## YAML 结构示例

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - app

  app:
    build: ./app
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  db-data:

networks:
  default:
    name: myapp-network
```

## 核心概念

**Service(服务)**

容器的逻辑单元,YAML 中一个键。一个服务可有多个容器实例(scale)。

**Network(网络)**

Compose 自动创建一个默认 bridge 网络,所有服务之间可通过服务名互访(DNS)。

**Volume(卷)**

- Named volume(由 Docker 管理,跨重启保留)
- Bind mount(挂载主机目录,代码热更新)
- tmpfs(内存)

**Build vs Image**

- image:已有镜像
- build:.(本地 Dockerfile 构建)

**Environment(环境变量)**

- 直接 KEY: VALUE
- env_file: .env(共享多服务)
- ${VAR}(从外部 shell 环境取)

**depends_on**

声明启动顺序,但不等服务就绪。需要 wait-for-it.sh 或 healthcheck 实现真正的"等待就绪"。

## 常用命令

```bash
docker compose up -d          # 启动所有服务,后台运行
docker compose down           # 停止并删除
docker compose down -v        # 同时删 volumes
docker compose ps             # 查看状态
docker compose logs -f web    # 跟踪某服务日志
docker compose exec app sh    # 进入容器
docker compose restart        # 重启
docker compose pull           # 拉取最新镜像
docker compose config         # 验证 YAML
docker compose build --no-cache  # 重新构建,不用缓存
```

## 多文件组合

不同环境用不同 yml 覆盖:

```bash
docker compose -f compose.yml -f compose.prod.yml up -d
```

后面文件覆盖前面文件的同名字段,适合 dev/staging/prod 配置分离。

## Compose v1 vs v2

- **v1**(Python,docker-compose):2014 至 2022 主流
- **v2**(Go,docker compose 子命令):2022+ 默认,性能更好,Docker Desktop 内置

新项目应直接用 v2(命令是 `docker compose` 不是 `docker-compose`)。

## healthcheck

```yaml
db:
  healthcheck:
    test: ["CMD", "pg_isready", "-U", "user"]
    interval: 5s
    timeout: 3s
    retries: 5
```

配合 depends_on 的 condition: service_healthy 实现真正的就绪等待。

## profiles(条件启用)

```yaml
services:
  debugger:
    image: debugger
    profiles: ["debug"]
```

`docker compose --profile debug up` 才启动 debugger 服务,默认不启。

## 与 Kubernetes 对比

| 维度 | Docker Compose | Kubernetes |
|---|---|---|
| 复杂度 | 低 | 高 |
| 节点 | 单机 | 多机集群 |
| 编排 | 简单 depends_on | 复杂 Deployment/StatefulSet |
| 配置 | YAML 简洁 | YAML/[[Helm Chart|Helm]] 复杂 |
| 适用 | 开发、单机生产 | 生产、大规模、多团队 |

Compose 适合"小到中"复杂度,Kubernetes 适合"中到大"。两者并非互斥,Docker 提供 `docker stack` 把 Compose 文件转换为 Swarm/K8s 部署。

## 与 Swarm 的关系

Docker Swarm 是 Docker 内置集群方案,使用同样的 Compose 格式但增加 deploy 字段(replicas、placement、resources)。Swarm 在 K8s 兴起后逐渐边缘化,但仍是简单集群的轻量选择。

## 局限

- 单机为主,多机需 Swarm 或 K8s
- 滚动更新、自动伸缩功能有限
- 无服务发现复杂逻辑(只有 DNS)
- 大规模时性能不够
- 不适合多团队多服务隔离

## 实践要点

- 开发环境推荐 bind mount 代码目录,改即生效
- 生产环境用 named volumes,避免主机依赖
- Secret(密码、API Key)用环境变量 + .env(.gitignore)
- 日志用 driver: json-file 或 syslog,避免无限增长
- 网络用 networks 隔离不同服务组(前端 vs 后端 vs 数据库)
- restart: unless-stopped 让服务自动恢复

## 参考源

- raw/计算机/
- 相关:[[Docker容器]]、[[现代云原生架构]]、[[Kubernetes]]、[[微服务]]、[[CI_CD流水线]]、[[服务发现]]
