# Matplotlib可视化

## 📊 Matplotlib基础

### 1. 基本绘图

**简单绘图：**
```python
import matplotlib.pyplot as plt
import numpy as np

# 基本线图
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()

# 散点图
x = np.random.randn(100)
y = np.random.randn(100)
plt.scatter(x, y, alpha=0.6)
plt.title('Scatter Plot')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# 柱状图
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]
plt.bar(categories, values)
plt.title('Bar Chart')
plt.xlabel('Categories')
plt.ylabel('Values')
plt.show()
```

**子图布局：**
```python
# 创建子图
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 第一个子图
axes[0, 0].plot(x, y)
axes[0, 0].set_title('Line Plot')

# 第二个子图
axes[0, 1].scatter(x, y)
axes[0, 1].set_title('Scatter Plot')

# 第三个子图
axes[1, 0].bar(categories, values)
axes[1, 0].set_title('Bar Chart')

# 第四个子图
axes[1, 1].hist(np.random.randn(1000), bins=30)
axes[1, 1].set_title('Histogram')

plt.tight_layout()
plt.show()
```

### 2. 样式和美化

**颜色和样式：**
```python
# 颜色设置
plt.plot(x, y, color='red', linewidth=2, linestyle='--')
plt.plot(x, y+1, color='blue', linewidth=1, linestyle='-')

# 标记样式
plt.plot(x, y, marker='o', markersize=5, markerfacecolor='red')
plt.plot(x, y+1, marker='s', markersize=3, markerfacecolor='blue')

# 图例
plt.plot(x, y, label='sin(x)')
plt.plot(x, y+1, label='sin(x)+1')
plt.legend()
plt.show()
```

**样式主题：**
```python
# 使用样式
plt.style.use('seaborn-v0_8')
plt.plot(x, y)
plt.title('Styled Plot')
plt.show()

# 可用样式
print(plt.style.available)

# 自定义样式
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
```

## 📈 高级绘图

### 1. 多轴图

```python
# 双y轴
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x) * 100

ax1.plot(x, y1, 'b-', label='sin(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2.plot(x, y2, 'r-', label='100*cos(x)')
ax2.set_ylabel('100*cos(x)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title('Dual Y-Axis Plot')
plt.show()
```

### 2. 3D绘图

```python
from mpl_toolkits.mplot3d import Axes3D

# 3D线图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

t = np.linspace(0, 4*np.pi, 100)
x = np.sin(t)
y = np.cos(t)
z = t

ax.plot(x, y, z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Line Plot')
plt.show()

# 3D表面图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = np.linspace(-5, 5, 50)
Y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))

ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Surface Plot')
plt.show()
```

### 3. 统计图表

```python
# 箱线图
data = [np.random.normal(0, std, 100) for std in range(1, 4)]
plt.boxplot(data, labels=['Group 1', 'Group 2', 'Group 3'])
plt.title('Box Plot')
plt.ylabel('Values')
plt.show()

# 小提琴图
import seaborn as sns
sns.violinplot(data=data)
plt.title('Violin Plot')
plt.show()

# 热力图
data = np.random.randn(10, 10)
plt.imshow(data, cmap='coolwarm')
plt.colorbar()
plt.title('Heatmap')
plt.show()
```

## 🎯 AI数据可视化

### 1. 机器学习结果可视化

**分类结果：**
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# 生成数据
X, y = make_classification(n_samples=1000, n_features=2, n_redundant=0, n_informative=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 可视化决策边界
def plot_decision_boundary(X, y, model):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, alpha=0.8, cmap='viridis')
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='k')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Decision Boundary')
    plt.show()

plot_decision_boundary(X_test, y_test, model)
```

**回归结果：**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 生成回归数据
X = np.random.randn(100, 1)
y = 2 * X.flatten() + 1 + np.random.randn(100) * 0.1

# 训练模型
model = LinearRegression()
model.fit(X, y)

# 预测
y_pred = model.predict(X)

# 可视化
plt.scatter(X, y, alpha=0.6, label='Actual')
plt.plot(X, y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('X')
plt.ylabel('y')
plt.title(f'Linear Regression (R² = {r2_score(y, y_pred):.3f})')
plt.legend()
plt.show()
```

### 2. 深度学习可视化

**训练过程：**
```python
# 模拟训练过程
epochs = range(1, 101)
train_loss = [1.0 * np.exp(-i/50) + 0.1 + np.random.normal(0, 0.05) for i in epochs]
val_loss = [1.2 * np.exp(-i/60) + 0.15 + np.random.normal(0, 0.05) for i in epochs]

plt.plot(epochs, train_loss, label='Training Loss')
plt.plot(epochs, val_loss, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training Progress')
plt.legend()
plt.grid(True)
plt.show()
```

**特征重要性：**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 特征重要性
feature_importance = model.feature_importances_
feature_names = iris.feature_names

# 可视化
plt.barh(feature_names, feature_importance)
plt.xlabel('Feature Importance')
plt.title('Feature Importance in Random Forest')
plt.show()
```

## 🔧 自定义图表

### 1. 自定义样式

```python
# 自定义颜色
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
plt.bar(categories, values, color=colors)
plt.title('Custom Colored Bar Chart')
plt.show()

# 自定义字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(x, y)
plt.title('Custom Font Plot')
plt.show()
```

### 2. 动画图表

```python
from matplotlib.animation import FuncAnimation

# 创建动画
fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot(x, np.sin(x))

def animate(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

anim = FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
plt.title('Animated Sine Wave')
plt.show()
```

### 3. 交互式图表

```python
from matplotlib.widgets import Slider

# 创建交互式图表
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

x = np.linspace(0, 10, 100)
y = np.sin(x)
line, = ax.plot(x, y)

# 添加滑块
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])
slider = Slider(ax_slider, 'Frequency', 0.1, 2.0, valinit=1.0)

def update(val):
    freq = slider.val
    line.set_ydata(np.sin(freq * x))
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
```

## 📊 数据探索可视化

### 1. 分布分析

```python
# 直方图
data = np.random.normal(0, 1, 1000)
plt.hist(data, bins=30, alpha=0.7, density=True)
plt.title('Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Density')
plt.show()

# 密度图
from scipy import stats
density = stats.gaussian_kde(data)
x_range = np.linspace(data.min(), data.max(), 100)
plt.plot(x_range, density(x_range))
plt.hist(data, bins=30, alpha=0.3, density=True)
plt.title('Density Plot')
plt.show()
```

### 2. 相关性分析

```python
# 相关性矩阵
data = np.random.randn(100, 5)
correlation_matrix = np.corrcoef(data.T)

# 热力图
plt.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar()
plt.title('Correlation Matrix')
plt.show()

# 散点图矩阵
from pandas.plotting import scatter_matrix
df = pd.DataFrame(data, columns=['A', 'B', 'C', 'D', 'E'])
scatter_matrix(df, alpha=0.6, figsize=(10, 10))
plt.show()
```

## 🔗 相关链接
- [[01-03-01-Python基础语法]] - Python基础
- [[01-03-02-NumPy数据处理]] - 数值计算
- [[01-03-03-Pandas数据分析]] - 数据分析
- [[02-01-04-模型评估方法]] - 模型评估可视化

## 💡 费曼学习法应用
**概念理解**：Matplotlib就像"画图工具"，可以画出各种图表。图表就像"数据的照片"，帮助我们理解数据的特征和规律。

**实践建议**：学习Matplotlib要像"学画画"，多练习各种图表类型，理解每种图表的适用场景，掌握美化和自定义技巧。

**AI应用**：Matplotlib是AI可视化的"画笔"，所有的机器学习结果都需要可视化来理解。就像数据分析需要图表，AI分析需要可视化。

---
*📝 学习提示：Matplotlib是AI可视化的基础工具，建议多练习各种图表类型，掌握数据可视化技巧*

