## 1️⃣ 基础概念

|分类|内容|
|---|---|
|**定义**|结构化查询语言，用于管理关系型数据库|
|**数据库基础**|数据库、表、列、行、约束、主键、外键|
|**数据类型**|数值型、字符型、日期时间型、布尔型、JSON、枚举|
|**关系操作**|一对一、一对多、多对多|
|**SQL 分类**|DDL、DML、DCL、TCL、查询语句|

---

## 2️⃣ 数据定义语言（DDL）

|操作|描述|示例|
|---|---|---|
|**CREATE TABLE**|创建表|CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(50))|
|**ALTER TABLE**|修改表结构|ALTER TABLE users ADD COLUMN age INT|
|**DROP TABLE**|删除表|DROP TABLE users|
|**TRUNCATE**|清空表数据|TRUNCATE TABLE users|
|**约束**|主键、外键、唯一、非空、检查|PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id)|

---

## 3️⃣ 数据操作语言（DML）

|操作|描述|示例|
|---|---|---|
|**INSERT**|插入数据|INSERT INTO users (id, name) VALUES (1, 'Alice')|
|**UPDATE**|更新数据|UPDATE users SET age=30 WHERE id=1|
|**DELETE**|删除数据|DELETE FROM users WHERE id=1|
|**MERGE / UPSERT**|插入或更新|INSERT ... ON DUPLICATE KEY UPDATE ...|

---

## 4️⃣ 数据查询（DQL）

|分类|语法|描述|
|---|---|---|
|**基本查询**|SELECT column1, column2 FROM table|基础数据提取|
|**条件查询**|WHERE、BETWEEN、IN、LIKE、IS NULL|数据过滤|
|**排序**|ORDER BY ASC/DESC|排序显示|
|**分组**|GROUP BY、HAVING|聚合分析|
|**聚合函数**|COUNT, SUM, AVG, MAX, MIN|数据统计|
|**连接查询**|INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN|多表关联|
|**子查询**|SELECT ... FROM (SELECT ...)|嵌套查询|
|**集合操作**|UNION, INTERSECT, EXCEPT|合并结果集|

---

## 5️⃣ 数据控制语言（DCL）

|操作|描述|
|---|---|
|**GRANT**|授权用户操作权限|
|**REVOKE**|收回用户权限|

---

## 6️⃣ 事务控制（TCL）

|操作|描述|
|---|---|
|**BEGIN / START TRANSACTION**|开始事务|
|**COMMIT**|提交事务|
|**ROLLBACK**|回滚事务|
|**SAVEPOINT**|保存事务点，用于部分回滚|

---

## 7️⃣ 索引与优化

|分类|内容|
|---|---|
|**索引类型**|主键索引、唯一索引、普通索引、全文索引、复合索引|
|**查询优化**|使用索引、避免全表扫描、合理使用JOIN、分页优化|
|**执行计划**|EXPLAIN/EXPLAIN ANALYZE|
|**视图**|普通视图、物化视图|

---

## 8️⃣ 高级特性

|分类|内容|
|---|---|
|**窗口函数**|ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD|
|**CTE（公用表表达式）**|WITH 子句，递归查询|
|**JSON操作**|JSON_EXTRACT, JSON_ARRAYAGG, JSON_OBJECTAGG|
|**存储过程**|CREATE PROCEDURE, 参数、流程控制|
|**触发器**|BEFORE/AFTER INSERT/UPDATE/DELETE|
|**事务隔离级别**|READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE|

---

## 9️⃣ 数据库设计与建模

|分类|内容|
|---|---|
|**范式**|1NF、2NF、3NF、BCNF|
|**ER图**|实体、关系、属性|
|**约束设计**|主键、外键、唯一性、非空、检查约束|
|**分区与分表**|水平分表、垂直分表、分区表|
|**备份与恢复**|数据备份、恢复策略、日志|