---
title: Odoo 部署架构
type: concept
tags: [odoo, programming, mature]
sources: [raw/Odoo/04-精通创新层/01-架构设计/, raw/Odoo/04-精通创新层/02-性能优化/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 生产部署的经典架构是 Nginx 反向代理 + Odoo Workers + PostgreSQL,通过 Worker 进程数调优、缓存、负载均衡解决并发与性能瓶颈,Docker 化已成为现代部署主流。
---

# Odoo 部署架构

## 定义

Odoo 部署架构指 Odoo 系统从开发到生产环境的完整运行栈。Odoo 是 Python + PostgreSQL 的 Web ERP,但其多模块、多公司、长事务、报表渲染等特性带来独特的部署挑战。

经典生产架构由四层构成:
1. **反向代理层**:Nginx / Caddy / Apache 处理 HTTPS、静态资源、负载均衡
2. **应用层**:Odoo Workers(多进程模式)
3. **数据库层**:PostgreSQL(可主从复制 / 读写分离)
4. **存储层**:文件系统 / S3 用于附件(Attachments)

## 经典架构图

```
[Internet]
    ↓ HTTPS
[Nginx 反向代理]   ← SSL 终止、静态资源、Gzip
    ↓ HTTP
[Odoo Workers]     ← 多进程,每个 Worker 一个 Python 进程
    ├── HTTP Workers(处理 Web 请求)
    └── Cron Workers(处理定时任务)
    ↓
[PostgreSQL]       ← 数据库
    ↓
[共享存储]         ← 附件(filestore)
```

## 关键组件

**1. Nginx 配置要点**

- HTTPS 终止(Let's Encrypt 证书)
- 静态资源(/web/static、/<module>/static)直接返回,不打扰 Odoo
- WebSocket(longpolling)代理到独立端口(默认 8072)
- proxy_buffering off 用于报表导出大文件
- client_max_body_size 调大支持大附件上传

**2. Odoo Workers 模式**

Odoo 默认单进程,生产必须开 multiprocessing 模式:
- workers = 数量(典型 2 × CPU 核数 + 1)
- max_cron_threads = 1-2(后台定时任务)
- limit_memory_hard / limit_memory_soft 控内存
- limit_time_cpu / limit_time_real 防长事务卡死

**3. PostgreSQL 调优**

- shared_buffers = 1/4 内存
- work_mem = 32-64MB
- max_connections = Workers * 2 + 安全冗余
- pg_stat_statements 监控慢查询
- 使用 PgBouncer 做连接池(推荐)
- WAL 配置和归档(用于 PITR 备份)

**4. 文件存储**

- 默认本地 filestore(/var/lib/odoo/filestore/<dbname>)
- 多服务器集群必须共享:NFS、S3(通过模块)、CephFS
- 大量附件场景推荐 S3 模式,降低本地磁盘压力

## Docker 化部署

**官方 Docker 镜像**

`docker pull odoo:18` 即获取最新版,搭配 PostgreSQL 镜像一键启动:

```yaml
# docker-compose.yml 示意
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:18
    depends_on: [db]
    ports: ["8069:8069", "8072:8072"]
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
```

**Kubernetes 部署**

- StatefulSet 部署 PostgreSQL(或用云托管 RDS)
- Deployment 部署 Odoo Workers,根据负载自动扩缩
- Ingress + cert-manager 自动 HTTPS
- ConfigMap 管理 odoo.conf,Secret 管理密码
- PVC 共享 filestore(多副本时必须)

## 性能优化层次

**1. 数据库层**

- 索引优化:常查字段索引、复合索引
- 物化视图(Materialized View)存重报表
- 分区表(按日期、公司)
- VACUUM、ANALYZE 定期

**2. 应用层**

- 减少 ORM N+1 查询(用 prefetch、read_group 替代 search + read)
- 计算字段加 store=True 减少实时计算
- 长事务拆分,避免锁
- Cron 任务时段调度,避开高峰

**3. 缓存**

- Odoo 内置 ORM 缓存(每个 Worker 独立)
- 静态资源 Nginx 强缓存
- 反向代理缓存(Cloudflare)
- Redis 用于 Session 与 Queue Job(配合 queue_job 模块)

## 高可用与备份

**主备模式**

- PostgreSQL 流复制(streaming replication)主从
- Odoo Workers 部署在多台机器
- 共享文件存储(NFS/S3)
- 故障切换:自动或手动 failover 到 standby PostgreSQL

**备份策略**

- 每日全备(pg_dump 或 pg_basebackup)
- 持续 WAL 归档(PITR)
- filestore 同步(rsync 或 S3 版本控制)
- 异地副本(灾备)

## 监控与日志

**关键指标**

- Worker 进程数、活跃数、CPU/内存
- DB 连接数、长事务、慢查询
- Cron 任务执行情况
- 业务指标:登录失败率、API 调用延迟

**日志收集**

- Odoo 日志:logfile 配置或 stdout(Docker)
- 通过 Filebeat → Elasticsearch → Kibana 集中分析
- 错误监控:Sentry / Rollbar 集成

## 多公司架构

Odoo 支持多公司(multi-company)单数据库部署,业务上隔离公司,但共享:
- 用户/合同/产品(可配)
- 财务报表分公司
- 库存仓库分公司

复杂场景拆为多数据库,每库一公司,部署成本高但隔离强。

## 参考源

- raw/Odoo/04-精通创新层/01-架构设计/
- raw/Odoo/04-精通创新层/02-性能优化/
- 相关:[[Odoo模块体系]]、[[Odoo ORM]]、[[Docker容器]]
