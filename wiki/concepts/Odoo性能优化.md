---
title: Odoo 性能优化
type: concept
tags: [erp, mature]
sources: [raw/Odoo/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 性能优化跨越数据库索引、ORM 缓存、Worker 进程模型、前端懒加载、报表预渲染等多层,典型瓶颈是 N+1 查询、计算字段无索引、Worker 数与并发不匹配。
---

# Odoo 性能优化

## 定义

Odoo 性能优化指对 Odoo 系统在响应时间、并发吞吐、报表生成、批量操作等方面的端到端调优。Odoo 的性能问题通常不是单一瓶颈,而是**数据库 + ORM + Worker + 前端**四层协作中的薄弱环节。理解 Odoo 进程模型和 ORM 行为是定位瓶颈的前提。

## 核心要点

**性能瓶颈五大常见来源**

1. **N+1 查询**:循环调用 `record.partner_id.name` 触发逐条 SQL,需 `prefetch` 或一次性批量取值
2. **计算字段无 store=True**:每次访问重算,大数据集慢;开 store + index 加速
3. **Worker 进程不足**:并发用户多但 longpolling / Worker 数少
4. **慢 SQL**:复杂报表 query 没建索引
5. **前端 RPC 暴增**:每次刷视图都调用全量字段,需精简 fields_get

**数据库层优化**

- **索引策略**:
  - 主键、外键自动有索引
  - 频繁过滤 / 排序的字段加 `index=True`
  - 多字段组合索引:`_sql_constraints` 或迁移脚本中 `CREATE INDEX`
- **PostgreSQL 调参**:
  - `shared_buffers` ≈ 物理内存 25%
  - `effective_cache_size` ≈ 物理内存 75%
  - `work_mem`:大查询需调高
  - `max_connections`:避免连接耗尽
- **VACUUM / ANALYZE** 定期执行,防止表膨胀

**ORM 层优化**

- **批量操作而非循环**:`records.write({'state': 'done'})` vs `for r in records: r.write(...)`
- **prefetch_fields**:`records = self.env['x'].search([], limit=1000); records.partner_id.name` 自动预取
- **flush() 与 invalidate_cache()** 控制何时同步到 DB
- **跳过 ORM 走原生 SQL**:超大批量场景用 `self.env.cr.execute()`,但牺牲触发器和约束

**Worker 进程模型**

Odoo 的多进程架构:
- **HTTP Worker**:处理普通 Web 请求,数量 = `--workers`(通常 = CPU 核数 × 2 + 1)
- **Cron Worker**:跑定时任务,`--max-cron-threads`(常 1-2)
- **Longpolling Worker**:维持长连接(聊天、通知),独立端口

公式参考:`--workers = (核数 × 2) + 1`,内存按 `--limit-memory-soft` / `--limit-memory-hard` 限制。

**前端 / 报表优化**

- **List View 字段精简**:不要默认显示几十列
- **Kanban / Tree 分页**:`limit=80` 默认,大数据集用搜索过滤
- **报表预渲染**:复杂 PDF 报表通过 Cron 提前生成
- **CDN / Nginx 静态加速**:assets bundle 大,反代缓存重要
- **assets manifest**:开发模式 (`--dev=assets`) 不要在生产开启

**缓存策略**

- **ir.attachment**:文件附件可外置存储(S3、文件系统)
- **redis 缓存 session**:多 Worker 间 session 共享
- **PG bouncer**:连接池减少连接开销

**监控与诊断**

- 启用 `--log-sql=DEBUG_RPC_ANSWER` 看 SQL 时间
- `pg_stat_statements` 找慢 SQL
- New Relic / Datadog / Sentry 监控请求时延
- Odoo 自带 *Settings > Technical > Server Tools > Profile* 看请求 trace

## 与其他概念的关系

Odoo 性能优化建立在 [[Odoo部署架构]] 与 [[Odoo ORM]] 之上;数据库部分关联 [[Odoo工作流]] 触发频率;监控与运维属 [[OpenTelemetry]] 等通用技术栈。Worker 模型的并发设计与 [[Kubernetes]] 在 ERP 应用中的部署紧密相关。

## 高频陷阱

- 增加 Worker 数不一定提速,瓶颈可能在 DB
- store=True 的计算字段在批量改主表时全量重算,可能比无 store 还慢
- 大查询用 `limit` 别忘了 `order`,无 order 的 limit 结果不稳定
- 开发模式 (`--dev`) 严禁上生产,反复编译 assets 拖慢一切
- N+1 检测:开 SQL 日志,看到同一表反复查就是

## 参考源

- raw/Odoo/(性能优化章节)
- 相关:[[Odoo部署架构]]、[[Odoo ORM]]、[[Odoo工作流]]、[[Odoo报表引擎]]
