---
title: DFS 深度优先搜索 Depth-First Search
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/编程基础/数据结构/04-算法武器库/01-搜索技术/01-深度优先搜索.md
  - raw/计算机/编程基础/数据结构/04-算法武器库/03-图论算法/01-BFS与DFS详解.md
created: 2026-05-05
updated: 2026-05-05
summary: DFS 沿一条路径走到底再回溯,用栈或递归实现,是连通分量、拓扑排序、回溯枚举、强连通分量等算法的核心。
---

# DFS 深度优先搜索 Depth-First Search

## 定义

**深度优先搜索(DFS)**是一种[[图]]/[[树]]遍历算法:从起点出发,沿一条边走到底再**回溯**到上一个节点,继续探索其他边。它强调"尽可能深",直到不能前进才退回。

DFS 用[[栈]]或[[递归]]实现。复杂度 **O(V + E)**,空间 O(V)(栈深度 + 已访问标记)。

## 核心要点

### 实现:递归 vs 显式栈

```
def dfs_recursive(node):
    if node in visited: return
    visited.add(node)
    process(node)
    for neighbor in node.neighbors:
        dfs_recursive(neighbor)
```

```
def dfs_iterative(start):
    stack = [start]; visited = {start}
    while stack:
        node = stack.pop()
        process(node)
        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor); stack.push(neighbor)
```

递归代码简洁但深度大时栈溢出;显式栈版本更可控。

### 三色标记(白/灰/黑)

经典 CLRS 模型:
- **白色**:未访问
- **灰色**:在 DFS 栈中(正在探索其子树)
- **黑色**:子树探索完毕

灰→灰的边即"后向边(Back Edge)",意味着环存在 → 用于环检测。

### 边的分类(有向图 DFS 树)

- **树边(Tree)**:DFS 走过的边
- **后向边(Back)**:指向祖先 → 有环
- **前向边(Forward)**:指向自己的非子代后代
- **横叉边(Cross)**:连接不同子树

无向图只有树边和后向边。

### 经典应用

1. **连通分量**:对每个未访问节点 DFS 一次,记录次数 = 分量数
2. **拓扑排序(逆后序)**:DFS 后按完成时间逆序输出 → DAG 拓扑序
3. **环检测**:有向图通过后向边、无向图通过非父亲的已访问邻居
4. **强连通分量**:Tarjan(单次 DFS + 栈)、Kosaraju(两次 DFS)
5. **二分图染色**
6. **路径问题**:走迷宫、找路径、子树和
7. **[[回溯算法]]**:全排列、N 皇后、数独本质上是带剪枝的 DFS
8. **桥与割点**:Tarjan 单次 DFS 求关节点(network reliability)

### DFS 与[[BFS广度优先搜索]]对比

| 维度 | DFS | BFS |
|---|---|---|
| 数据结构 | [[栈]]/[[递归]] | [[队列]] |
| 扩展顺序 | 深度 | 层次 |
| 空间(树) | O(深度) | O(宽度) |
| 最短路径 | 无保证 | 无权图正确 |
| 拓扑/强连通 | 自然 | 不直接 |

经验法则:
- 求**最短路径** → BFS
- 求**所有解 / 路径存在** → DFS
- 求**拓扑序、SCC、桥、割点** → DFS

### 迭代加深 DFS(IDDFS)

逐渐增加深度上界 1, 2, 3... 重复 DFS。结合 BFS 的最短性 + DFS 的低空间。常用于博弈树搜索(国际象棋引擎)。

## 和其他概念的关系

DFS 是与 BFS 并列的图遍历两大基石。[[回溯算法]]是 DFS 的特殊用法(强调撤销选择)。[[递归]]在底层依赖[[栈]],与 DFS 共享栈展开机制。

[[操作系统]]文件系统遍历(`find`, `du`)、依赖解析(包管理 npm/Maven)、[[Git]] commit 历史回溯都是 DFS 应用。[[编译原理]]中,语义分析在 AST 上的访问者模式即树形 DFS。

死锁检测(资源分配图找环)、电路布线、迷宫游戏 AI 也是 DFS 典型场景。

## 参考源

- raw/计算机/编程基础/数据结构/04-算法武器库/01-搜索技术/01-深度优先搜索.md
- raw/计算机/编程基础/数据结构/04-算法武器库/03-图论算法/01-BFS与DFS详解.md
