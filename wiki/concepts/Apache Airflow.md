---
title: Apache Airflow
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Apache Airflow 是 Airbnb 开源的工作流编排平台,通过 Python 代码定义有向无环图(DAG)调度数据管道,以"代码即配置"和丰富的 Operator 生态成为数据工程编排事实标准。
---

# Apache Airflow

## 定义

**Apache Airflow** 是 Airbnb 数据团队 Maxime Beauchemin 在 2014 年开源、2019 年从 Apache 毕业的工作流编排平台。它针对数据管道(Data Pipeline)的核心需求:**调度定时任务、表达任务依赖、监控失败、回填历史**,以"**Python 代码定义 DAG**"为核心抽象,成为现代数据工程编排的事实标准。

Airflow 与 [[ETL与ELT]] 工具链共生——抽取、转换、加载的每个步骤是 DAG 中的一个 Task,按依赖顺序执行,失败重试,产出指标。

## 核心抽象

**DAG(Directed Acyclic Graph)**

有向无环图,描述任务依赖:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('daily_etl', start_date=datetime(2025, 1, 1),
         schedule='@daily', catchup=False) as dag:

    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    load = PythonOperator(task_id='load', python_callable=load_data)

    extract >> transform >> load  # 依赖:extract 完成后跑 transform
```

**Task / Operator**

Task 是 DAG 中的节点,由 Operator 实例化:
- PythonOperator:跑 Python 函数
- BashOperator:跑 shell 命令
- PostgresOperator / MySqlOperator:跑 SQL
- S3ToRedshiftOperator:跨服务移数据
- KubernetesPodOperator:K8s 起 Pod
- 几百种内置 + 几千种社区 Operator

**Sensor**

特殊 Operator,等待外部事件:
- FileSensor:文件出现
- ExternalTaskSensor:另一 DAG 任务完成
- S3KeySensor:S3 对象出现
- HttpSensor:URL 返回 200

**Hook**

封装外部系统连接(数据库、API),Operator 通过 Hook 操作:PostgresHook、S3Hook、SlackHook。

**XCom(Cross Communication)**

Task 间小数据传递,默认存元数据库,大数据要用 S3 等外部存储。

## 调度模型

**调度间隔(schedule)**

- @daily / @hourly / @weekly / @monthly
- Cron 表达式 "0 5 * * *"
- timedelta 对象
- 复杂规则:Timetable 自定义类
- @once / None(只手动触发)

**Catchup 与 Backfill**

- catchup=True:从 start_date 跑所有缺失批次
- catchup=False:只跑最新一批
- airflow dags backfill 命令补跑历史

**Execution Date 概念**

每次 DAG 运行有 logical_date(原 execution_date)——这个批次"逻辑上是哪天的"。日报 DAG 在 2025-05-05 02:00 启动,但 logical_date 是 2025-05-04(报告 04 号数据)。

## 架构

```
Web Server  ←→ Metadata DB(Postgres)
   ↑
Scheduler ←→
   ↓
Executor → Worker(s)
              ↑
         任务执行
```

**Scheduler**:扫描 DAG 文件、检查触发条件、写任务到队列
**Executor**:从队列取任务,提交给 Worker:
- LocalExecutor:本机进程
- CeleryExecutor:Celery 分布式
- KubernetesExecutor:K8s Pod 一任务一容器
- DaskExecutor、Sequential(测试)

**Worker**:执行任务,上报状态

**Web Server**:UI、REST API、查看 DAG / 日志

## UI 价值

Airflow 最受欢迎的功能之一:

- **DAG View**:可视化 DAG 结构
- **Tree / Grid View**:历次执行的瀑布图,失败任务红色
- **Gantt Chart**:任务执行时长
- **Task Logs**:点击任务即看日志
- **Trigger / Clear / Mark Success**:运维操作

数据工程师每天对着 Airflow UI 看跑批进度,这是它能成为标准的关键 DX。

## 与同类对比

| 工具 | 特点 |
|---|---|
| Airflow | Python DAG,生态最大 |
| Prefect | 现代化 Airflow 替代,UI 更好,云优先 |
| Dagster | 资产中心(Asset-centric)、强类型 |
| Luigi | Spotify 出品,老牌 |
| Argo Workflows | K8s 原生,YAML 写 DAG |
| Kubeflow Pipelines | ML 专用 |
| Databricks Workflows | 与 Spark 紧密 |

Airflow 仍是部署量最大的,但 Prefect、Dagster 在新项目中崛起,理由:
- Airflow 的 DAG = Python 文件 → 启动慢、动态 DAG 难
- 测试不方便
- 元数据库(Postgres)成瓶颈
- UI 老气

Prefect 2.0 / Dagster 用更现代的 API、动态 Flow、更好的 UI 解决这些痛点。

## 典型用法

**1. ETL / ELT**

```python
extract_orders >> stage_to_s3 >> dbt_run >> data_quality_check >> notify_slack
```

**2. 机器学习管道**

```python
fetch_features >> train_model >> evaluate >> register_model >> deploy
```

**3. 报表生成**

```python
query_warehouse >> render_dashboard >> email_to_stakeholders
```

**4. 数据质量监控**

每天 SLA 检查、新增数据校验、异常告警。

## 部署架构

**云托管**

- AWS MWAA(Managed Workflows for Apache Airflow)
- GCP Cloud Composer
- Astronomer(Airflow 商业公司)
- Astro(Astronomer 的 SaaS)

**自部署**

- Docker Compose(开发)
- Kubernetes(生产推荐,KubernetesExecutor + Helm)
- Docker Swarm / VM

## 局限

**1. DAG 启动慢**

Scheduler 每次扫描所有 DAG 文件,Python import 慢。1000 个 DAG 启动 5 分钟。

**2. 元数据库瓶颈**

PostgreSQL 单点,大量任务 SQL 拥堵。Postgres 调优是常见运维工作。

**3. 动态 DAG 困难**

DAG 需是静态 Python 模块,运行时构造 DAG 复杂。Prefect / Dagster 改进。

**4. 任务间通信**

XCom 默认元数据库 1MB 限,大数据要走 S3。

**5. 测试不便**

DAG 测试 = 跑整个 Airflow,不是单元测试场景。

**6. 资源调度弱**

每任务一 Pod 分配资源,无智能批调度。Kubeflow / Argo 在 ML 场景更优。

## Airflow 2.0+(2020+)的现代化

- **TaskFlow API**:用装饰器写 DAG,简化语法
  ```python
  @task
  def extract(): return data
  @task
  def transform(data): return processed
  ```
- **Smart Sensor → Deferrable Operators**:释放 Worker 等待
- **DAG Versioning**(进行中)
- **Datasets(2.4+)**:数据驱动调度,而非时间驱动

## 数据驱动调度(2.4+)

```python
from airflow.datasets import Dataset

orders_dataset = Dataset("s3://bucket/orders/")

@task(outlets=[orders_dataset])
def update_orders(): ...

# 另一 DAG
with DAG("compute_metrics", schedule=[orders_dataset]):
    ...
```

orders 更新后自动触发 metrics DAG。这是 Dagster Asset 思想的回应。

## 和其他概念的关系

Airflow 与 [[ETL与ELT]] 工具链(Fivetran / Airbyte 抽数,dbt 转换,Snowflake / BigQuery 装载)共生,负责调度。它与 [[Kafka]](实时流)互补——Airflow 处理批/小时级,Kafka 处理秒级。

Airflow 任务大量调用 [[Apache Spark]] 处理大数据,通过 SparkSubmitOperator 或 Databricks Operator 提交。在 [[Kubernetes]] 上跑 Airflow + KubernetesExecutor 是云原生数据工程标准栈。

它体现的"代码即配置"哲学与 [[CI_CD流水线]] 的 IaC、[[Helm Chart]]、Terraform 等是同一家族——人类知识系统化、版本化、可审查。

## 参考源

- raw/计算机/
- 相关:[[ETL与ELT]]、[[Apache Spark]]、[[Kafka]]
