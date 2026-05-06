---
title: SQL 高级特性
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/数据存储/数据库/SQL/]
created: 2026-05-05
updated: 2026-05-05
summary: SQL 高级特性涵盖 JOIN 类型、窗口函数、CTE、子查询、集合操作、PIVOT 等,从简单查询升级到复杂分析,是数据工程师与分析师的核心工具。
---

# SQL 高级特性

## 定义

**SQL 高级特性** 指超出基本 SELECT/INSERT/UPDATE/DELETE 之外的查询语言能力,包括各种 JOIN 类型、窗口函数(Window Functions)、公用表表达式(CTE)、复杂子查询、集合操作、行列转换等。这些特性把 SQL 从简单数据访问提升为强大的分析语言,是数据库开发与分析的核心。

## 核心要点

- **JOIN 类型**
  - **INNER JOIN**:两表交集,匹配条件成立的行
  - **LEFT JOIN(LEFT OUTER)**:左表全保留,右表无匹配则填 NULL
  - **RIGHT JOIN**:对称,实践中可改写为 LEFT JOIN 提升可读性
  - **FULL OUTER JOIN**:两表并集,缺失填 NULL
  - **CROSS JOIN**:笛卡尔积,N×M 行,慎用
  - **SELF JOIN**:表与自己 JOIN,如查上下级关系
  - **NATURAL JOIN**:按同名列自动 JOIN,不推荐(隐式)
- **JOIN 算法(由 [[查询优化器]] 选择)**
  - **Nested Loop Join**:外层循环 × 内层(可加索引);适合小表 × 大表
  - **Hash Join**:小表建哈希表,大表流式查找;适合大表 × 大表
  - **Sort-Merge Join**:两表排序后归并;适合已排序或需要排序输出
- **窗口函数(Window Functions)**
  - 语法:`func() OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN ...)`
  - **聚合窗口**:SUM/AVG/COUNT,在分组上滑动
  - **排名函数**:ROW_NUMBER / RANK / DENSE_RANK
  - **偏移函数**:LAG / LEAD,前后行取值
  - **取值函数**:FIRST_VALUE / LAST_VALUE / NTH_VALUE
  - **NTILE(n)**:分桶
  - 经典用例:每组 Top N、移动平均、环比同比、留存计算
- **公用表表达式(CTE)**
  - `WITH cte_name AS (SELECT ...) SELECT ... FROM cte_name`
  - **优势**:可读性强、可重用、可拆分复杂查询
  - **递归 CTE**:`WITH RECURSIVE`,处理树状 / 图结构(组织架构、评论树、最短路径)
- **子查询(Subquery)**
  - **标量子查询**:返回单值,可放任意表达式
  - **行子查询**:返回单行多列
  - **表子查询**:作为 FROM 中的派生表
  - **关联子查询(Correlated)**:子查询引用外层列,每行执行一次,慎用,常可改写为 JOIN
  - **EXISTS / NOT EXISTS**:存在性判断,通常比 IN 子查询性能好
- **集合操作**
  - **UNION / UNION ALL**:并集(去重 / 不去重)
  - **INTERSECT**:交集
  - **EXCEPT / MINUS**:差集
- **行列转换**
  - **PIVOT**:行转列(报表常用),SQL Server 原生支持,MySQL 用 CASE WHEN
  - **UNPIVOT**:列转行
- **GROUPING SETS / ROLLUP / CUBE**
  - 一次查询多个分组维度,数仓常用
  - ROLLUP:层级小计
  - CUBE:所有维度组合
- **JSON 操作**
  - PostgreSQL: `->`、`->>`、`@>`、`jsonb_path_exists`
  - MySQL 5.7+: `JSON_EXTRACT`、`->`、`JSON_TABLE`(8.0)
  - 半结构化数据查询神器
- **公共陷阱**
  - LEFT JOIN + WHERE 右表条件 → 实际变 INNER JOIN
  - GROUP BY 选择非聚合列 → 标准 SQL 报错(MySQL 默认放过)
  - DISTINCT + ORDER BY → 排序列必须在 DISTINCT 列内

## 和其他概念的关系

SQL 高级特性使 [[关系型数据库]] 不仅是 OLTP 工具,还能胜任复杂分析,触及 [[OLAP vs OLTP]] 的边界。窗口函数 + CTE 是分析师 SQL 的核心。

[[查询优化器]] 决定 JOIN 算法、子查询重写,优化器越强大、用户写法越自由。

[[数据仓库]] 中,GROUPING SETS / ROLLUP / CUBE 是预聚合 Cube 的 SQL 表达。

[[NoSQL数据库]] 多数缺少 JOIN,促使应用反范式或在应用层做 JOIN,这正是 SQL 长盛不衰的原因。现代分布式数据库(TiDB / CockroachDB / Trino)努力把 SQL 高级特性推到 PB 级数据。

[[慢查询优化]] 中,误用相关子查询、深度嵌套是常见性能杀手,常通过改写 JOIN 或 CTE 优化。

## 参考源

- raw/计算机/数据存储/数据库/SQL/(子目录,概念基于通用 CS 知识整理)
- raw/计算机/开发学习/系统/Wordpress/02-核心理解层/01-架构原理/数据库结构.md(MySQL 查询示例)
