---
title: Pandas 与 NumPy(Python 数据科学基石)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: NumPy 是 Python 数值计算基石(N 维数组、向量化运算),Pandas 在其上构建 DataFrame 抽象处理结构化数据,二者共同构成 Python 数据科学/机器学习生态的不可替代基础层。
---

# Pandas 与 NumPy(Python 数据科学基石)

## 定义

**NumPy**(2005,Travis Oliphant)是 Python 的 N 维数组库,提供 ndarray 类型与一组高度优化的数值计算原语。**Pandas**(2008,Wes McKinney)在 NumPy 之上构建 Series / DataFrame 抽象,处理标签化的结构化数据(类似 Excel / SQL 表)。

二者是 Python 数据科学栈的"基础设施层"——Sklearn、PyTorch、TensorFlow、Statsmodels、Jupyter 等几乎所有数据/AI 库都建立在 NumPy/Pandas 之上。

## NumPy 核心

**ndarray**

- 同类型(dtype)、固定 shape 的多维数组
- 内存连续(C 或 Fortran 顺序)
- 比 Python list 快 10-100 倍(向量化 + SIMD)
- 与 BLAS / LAPACK 链接,矩阵运算调底层 C/Fortran

**关键操作**

```python
import numpy as np

a = np.array([1, 2, 3, 4])      # 1D
b = np.array([[1, 2], [3, 4]])  # 2D
np.zeros((3, 4))                # 3x4 全 0
np.linspace(0, 1, 100)          # 100 个均匀点

# 向量化(无 for 循环)
a * 2                            # 每个元素乘 2
a + b[:, 0]                      # 广播

# 切片
a[1:3]
b[:, 0]                          # 第一列
b[b > 2]                         # 布尔索引

# 矩阵运算
np.dot(b, b.T)
np.linalg.inv(b)
np.linalg.eig(b)
```

**广播(Broadcasting)**

shape 不同时自动扩展:
- (3,4) + (4,) → (3,4)
- (3,1) + (1,4) → (3,4)

是向量化代码的核心机制。

## Pandas 核心

**Series**

带索引的一维数组(类似 dict + ndarray)。

**DataFrame**

带行索引和列名的二维数据,核心数据结构:

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "LA", "Chicago"]
})

df.head()
df.describe()         # 数值列统计
df["age"].mean()
df[df["age"] > 25]    # 过滤
df.groupby("city")["age"].mean()  # SQL 风
```

**核心能力**

- 读写多种格式:CSV、Parquet、Excel、SQL、JSON、HTML、HDF5
- Index / MultiIndex(层级索引)
- 缺失值处理(NaN / NaT)
- 时间序列(date range、resample、rolling window)
- groupby + 聚合(类 SQL)
- pivot_table、crosstab(透视)
- merge / join / concat(类 SQL)
- apply / map(自定义函数)

## 向量化思想

**反例(慢)**

```python
result = []
for x in df["age"]:
    result.append(x * 2 + 1)
```

**正例(快 100 倍)**

```python
result = df["age"] * 2 + 1
```

向量化代码不仅快,而且更短、更可读。这是 NumPy/Pandas 设计灵魂。

## Pandas 数据流模式

**1. 读取**

```python
df = pd.read_csv("data.csv")
df = pd.read_parquet("data.parquet")  # 列式,推荐生产
df = pd.read_sql("SELECT * FROM users", conn)
```

**2. 清洗**

```python
df = df.dropna(subset=["age"])
df["age"] = df["age"].fillna(df["age"].median())
df = df.drop_duplicates()
df["category"] = df["category"].str.lower().str.strip()
```

**3. 特征工程**

```python
df["birth_year"] = pd.to_datetime(df["birthday"]).dt.year
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 60, 120], labels=["child", "young", "mid", "old"])
df["log_revenue"] = np.log1p(df["revenue"])
df = pd.get_dummies(df, columns=["country"])  # one-hot
```

**4. 聚合**

```python
result = (df.groupby(["country", "year"])
            .agg({"revenue": "sum", "user_id": "nunique"})
            .reset_index()
            .rename(columns={"user_id": "unique_users"}))
```

**5. 输出**

```python
result.to_parquet("output.parquet", compression="snappy")
result.to_sql("metrics", conn, if_exists="append", index=False)
```

## 性能与扩展

**单机限制**

- DataFrame 受内存限,几 GB 数据 OK,几十 GB 痛苦
- Pandas 单线程,单机多核难利用

**扩展方案**

- **Dask**:Pandas 兼容 API + 分布式
- **Modin**:把 Pandas 自动并行(改 import)
- **Polars**:Rust 写,2x-10x 快,API 略不同
- **DuckDB**:嵌入式分析数据库,SQL 直查 Parquet
- **PySpark**:超大规模时上 [[Apache Spark]]

近年 **Polars** 异军突起,2023 后许多团队从 Pandas 迁移,理由:
- Rust 实现,速度 5-10 倍
- 真并行
- Lazy 执行,优化查询
- 内存占用低

但 Pandas 生态深(Scikit-learn、Plotly、Statsmodels 都基于 Pandas)使其难以撼动。

## NumPy 在深度学习中的角色

PyTorch / TensorFlow 张量(Tensor)接口模仿 NumPy:
- 同样的 shape、dtype、broadcasting
- 同样的 reshape、permute、stack
- numpy() 与 torch.from_numpy() 互转

学会 NumPy 即学会一半深度学习张量操作。

## 与其他生态对比

| 生态 | DataFrame 等价物 |
|---|---|
| R | data.frame、tibble、data.table |
| Julia | DataFrames.jl |
| Scala | Spark DataFrame |
| JavaScript | dataframe-js(小众) |
| Rust | Polars(主流) |

Pandas 设计灵感来自 R data.frame,反过来又影响 Spark DataFrame、Polars 等后继。

## 常见陷阱

**1. SettingWithCopyWarning**

```python
df_filter = df[df["age"] > 25]
df_filter["age"] = df_filter["age"] + 1  # 警告!
```

正确做法:用 .loc 或 .copy()。

**2. 链式赋值**

```python
df[df["age"] > 25]["score"] = 100  # 不生效
df.loc[df["age"] > 25, "score"] = 100  # 正确
```

**3. 隐式类型转换**

包含 NaN 的整数列变 float。Pandas 1.0+ 引入 Nullable Integer 解决。

**4. 性能陷阱**

- iterrows / itertuples 慢
- apply 慢于向量化
- 字符串操作用 .str API,不要 apply

**5. 内存爆炸**

- 重复 merge 产生 cross join
- to_csv 默认 utf-8 + index=True 多余

## 局限

- 单机内存限制
- 单线程性能
- API 庞杂(同一操作多种写法)
- 类型系统弱
- 与现代 Python 类型(Pydantic、TypedDict)整合差
- 大型项目代码可读性低于 SQL

## 适用场景

**最适合**

- 数据探索(Jupyter)
- 中等规模(< 10GB)分析
- 机器学习特征工程
- 学术研究
- 报表生成

**不适合**

- 大规模(> 100GB):上 Spark / Polars / DuckDB
- 高并发实时:不是它的场景
- 严格类型 / 工程化:Pydantic + DuckDB 更合适

## 和其他概念的关系

NumPy / Pandas 是 Python 数据科学/AI 生态的基础,与 [[Apache Spark]](大规模分布式)互补——单机 Pandas、大规模 Spark。它们与 [[Jupyter哲学]]、Scikit-learn、PyTorch、TensorFlow 等共生。

在数据工程 [[ETL与ELT]] 流程中,Pandas 常用于"小批 transform"步骤,大批量交给 Spark / Polars / DuckDB。机器学习特征工程([[Embedding]]、训练数据准备)Pandas + NumPy 是首选工具。

它们的"向量化"思想与 [[NumPy广播]]、[[GPU]] 张量计算同构,是从 CPU SIMD 到 GPU CUDA 一脉的基础概念。

## 参考源

- raw/计算机/
- 相关:[[Apache Spark]], [[Apache Airflow]], [[ETL与ELT]]
