# Jupyter使用指南

## 📓 Jupyter Notebook基础

### 1. 环境设置

**安装Jupyter：**
```bash
# 使用pip安装
pip install jupyter

# 使用conda安装
conda install jupyter

# 启动Jupyter
jupyter notebook
```

**JupyterLab安装：**
```bash
# 安装JupyterLab
pip install jupyterlab

# 启动JupyterLab
jupyter lab
```

### 2. 基本操作

**单元格类型：**
- **Code单元格**：执行Python代码
- **Markdown单元格**：编写文档和说明
- **Raw单元格**：原始文本，不执行

**快捷键：**
| 操作 | 快捷键 | 说明 |
|------|--------|------|
| **运行单元格** | Shift + Enter | 运行并移到下一个单元格 |
| **运行单元格** | Ctrl + Enter | 运行但停留在当前单元格 |
| **插入单元格** | A | 在上方插入 |
| **插入单元格** | B | 在下方插入 |
| **删除单元格** | DD | 删除当前单元格 |
| **编辑模式** | Enter | 进入编辑模式 |
| **命令模式** | Esc | 进入命令模式 |

## 🔧 高级功能

### 1. 魔法命令

**行魔法命令：**
```python
# 时间测量
%time sum(range(1000000))

# 详细时间测量
%timeit sum(range(1000000))

# 内存使用
%memit sum(range(1000000))

# 执行系统命令
%ls
%pwd
%cd /path/to/directory

# 显示变量
%whos
%who

# 历史命令
%history
```

**单元格魔法命令：**
```python
# 执行外部脚本
%%time
import time
time.sleep(1)

# 执行系统命令
%%bash
echo "Hello from bash"
ls -la

# 执行HTML
%%html
<h1>Hello World</h1>
<p>This is HTML content</p>

# 执行JavaScript
%%javascript
console.log("Hello from JavaScript");
```

### 2. 扩展功能

**安装扩展：**
```bash
# 安装Jupyter扩展
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# 安装JupyterLab扩展
pip install jupyterlab-git
pip install jupyterlab-lsp
```

**常用扩展：**
- **Table of Contents**：自动生成目录
- **Variable Inspector**：变量查看器
- **Code Folding**：代码折叠
- **ExecuteTime**：显示执行时间
- **Autopep8**：代码格式化

## 📊 数据科学工作流

### 1. 数据探索模板

```python
# 导入必要的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 设置显示选项
pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8')
```

**数据加载和探索：**
```python
# 加载数据
df = pd.read_csv('data.csv')

# 数据基本信息
print("数据形状:", df.shape)
print("\n数据类型:")
print(df.dtypes)
print("\n缺失值:")
print(df.isnull().sum())
print("\n数据统计:")
print(df.describe())
```

**数据可视化：**
```python
# 数据分布
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 数值变量分布
df.hist(ax=axes[0, 0])
axes[0, 0].set_title('数值变量分布')

# 相关性热力图
correlation = df.corr()
sns.heatmap(correlation, annot=True, ax=axes[0, 1])
axes[0, 1].set_title('相关性热力图')

# 箱线图
df.boxplot(ax=axes[1, 0])
axes[1, 0].set_title('箱线图')

# 散点图矩阵
pd.plotting.scatter_matrix(df, ax=axes[1, 1])
axes[1, 1].set_title('散点图矩阵')

plt.tight_layout()
plt.show()
```

### 2. 机器学习模板

**数据预处理：**
```python
# 处理缺失值
df = df.fillna(df.mean())

# 特征工程
df['new_feature'] = df['feature1'] * df['feature2']

# 编码分类变量
df = pd.get_dummies(df, columns=['categorical_column'])

# 特征选择
from sklearn.feature_selection import SelectKBest, f_classif
X = df.drop('target', axis=1)
y = df['target']
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)
```

**模型训练和评估：**
```python
# 分割数据
X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, random_state=42
)

# 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
print("分类报告:")
print(classification_report(y_test, y_pred))

# 特征重要性
feature_importance = model.feature_importances_
feature_names = X.columns[selector.get_support()]
plt.barh(feature_names, feature_importance)
plt.title('特征重要性')
plt.show()
```

## 🎯 最佳实践

### 1. 代码组织

**单元格结构：**
```python
# 1. 导入库
import pandas as pd
import numpy as np

# 2. 数据加载
df = pd.read_csv('data.csv')

# 3. 数据探索
print(df.head())
print(df.info())

# 4. 数据预处理
df = df.dropna()
df = df.fillna(df.mean())

# 5. 特征工程
df['new_feature'] = df['feature1'] + df['feature2']

# 6. 模型训练
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)

# 7. 模型评估
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
print(f"MSE: {mse}")
```

**Markdown文档：**
```markdown
# 项目标题

## 项目描述
这是一个数据科学项目的描述。

## 数据来源
数据来源于...

## 方法
我们使用了以下方法：
1. 数据预处理
2. 特征工程
3. 模型训练
4. 模型评估

## 结果
模型达到了以下性能：
- 准确率：85%
- 精确率：82%
- 召回率：88%

## 结论
基于以上结果，我们可以得出以下结论...
```

### 2. 性能优化

**内存管理：**
```python
# 检查内存使用
%memit df = pd.read_csv('large_file.csv')

# 优化数据类型
df['int_column'] = df['int_column'].astype('int32')
df['float_column'] = df['float_column'].astype('float32')
df['category_column'] = df['category_column'].astype('category')

# 分块处理大文件
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

**并行处理：**
```python
# 使用multiprocessing
from multiprocessing import Pool
import multiprocessing as mp

def process_data(data):
    return data.groupby('category').sum()

# 分块处理
chunks = [df[i:i+1000] for i in range(0, len(df), 1000)]
with Pool(mp.cpu_count()) as pool:
    results = pool.map(process_data, chunks)
```

### 3. 版本控制

**Git集成：**
```bash
# 初始化Git仓库
git init

# 添加文件
git add .

# 提交更改
git commit -m "Initial commit"

# 推送到远程仓库
git push origin main
```

**Jupyter Git扩展：**
```python
# 安装Jupyter Git扩展
!pip install jupyterlab-git

# 使用Git命令
!git status
!git add .
!git commit -m "Update notebook"
!git push
```

## 🔧 调试技巧

### 1. 错误处理

**异常处理：**
```python
try:
    # 可能出错的代码
    result = risky_operation()
except Exception as e:
    print(f"错误: {e}")
    # 错误处理代码
else:
    print("操作成功")
finally:
    print("清理工作")
```

**调试工具：**
```python
# 使用pdb调试
import pdb
pdb.set_trace()

# 使用ipdb调试
import ipdb
ipdb.set_trace()

# 使用%debug魔法命令
%debug
```

### 2. 性能分析

**代码分析：**
```python
# 性能分析
%prun -s cumulative my_function()

# 内存分析
%memit my_function()

# 时间分析
%timeit my_function()

# 详细时间分析
%time my_function()
```

**可视化性能：**
```python
# 使用line_profiler
%load_ext line_profiler
%lprun -f my_function my_function()

# 使用memory_profiler
%load_ext memory_profiler
%mprun -f my_function my_function()
```

## 📱 移动端使用

### 1. Jupyter App

**安装Jupyter App：**
- 在手机应用商店搜索"Jupyter"
- 安装Jupyter App
- 连接本地或远程Jupyter服务器

**移动端功能：**
- 查看和编辑Notebook
- 运行代码单元格
- 查看图表和输出
- 同步到云端

### 2. 云端Jupyter

**Google Colab：**
```python
# 在Google Colab中
!pip install pandas matplotlib seaborn

# 上传文件
from google.colab import files
uploaded = files.upload()

# 读取上传的文件
df = pd.read_csv('uploaded_file.csv')
```

**Kaggle Kernels：**
```python
# 在Kaggle Kernels中
import pandas as pd
import numpy as np

# 读取Kaggle数据集
df = pd.read_csv('/kaggle/input/dataset/train.csv')
```

## 🔗 相关链接
- [[01-03-01-Python基础语法]] - Python基础
- [[01-03-02-NumPy数据处理]] - 数值计算
- [[01-03-03-Pandas数据分析]] - 数据分析
- [[01-03-04-Matplotlib可视化]] - 数据可视化

## 💡 费曼学习法应用
**概念理解**：Jupyter就像"交互式实验室"，可以边写代码边看结果。Notebook就像"实验记录本"，记录整个分析过程。

**实践建议**：学习Jupyter要像"学做实验"，多练习各种功能，理解交互式编程的优势，掌握数据科学工作流。

**AI应用**：Jupyter是AI开发的"实验平台"，所有的机器学习项目都可以在Jupyter中完成。就像实验室是科学研究的平台，Jupyter是AI研究的平台。

---
*📝 学习提示：Jupyter是AI开发的重要工具，建议多练习各种功能，掌握交互式编程和数据科学工作流*

