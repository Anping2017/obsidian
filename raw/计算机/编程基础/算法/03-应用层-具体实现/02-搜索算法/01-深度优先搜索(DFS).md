# 深度优先搜索(DFS)

## 🎯 核心概念

**深度优先搜索(Depth-First Search, DFS)**是一种用于遍历或搜索树或图的算法。它沿着树的深度遍历树的节点，尽可能深地搜索树的分支。当节点v的所在边都已被探寻过，搜索将回溯到发现节点v的那条边的起始节点。

## 🔍 算法原理

### 1. 基本思想
```python
def dfs_basic_concept():
    """DFS基本思想"""
    # 1. 从起始节点开始
    # 2. 访问当前节点
    # 3. 标记当前节点为已访问
    # 4. 递归访问所有未访问的邻接节点
    # 5. 回溯到上一个节点
    
    pass

def dfs_core_principles():
    """DFS核心原理"""
    # 1. 深度优先：尽可能深地搜索每个分支
    # 2. 回溯机制：当无法继续深入时，回退到上一个节点
    # 3. 访问标记：避免重复访问同一节点
    # 4. 递归实现：利用系统栈进行回溯
    
    pass
```

### 2. 算法特点
```python
def dfs_characteristics():
    """DFS算法特点"""
    characteristics = {
        "空间复杂度": "O(h) - h为树的高度",
        "时间复杂度": "O(V + E) - V为顶点数，E为边数",
        "实现方式": ["递归", "栈"],
        "遍历顺序": "深度优先",
        "应用场景": ["路径查找", "拓扑排序", "连通性检测"]
    }
    
    return characteristics

def dfs_vs_bfs():
    """DFS vs BFS对比"""
    comparison = {
        "DFS": {
            "遍历方式": "深度优先",
            "数据结构": "栈（递归）",
            "空间复杂度": "O(h)",
            "适用场景": "路径查找、回溯问题"
        },
        "BFS": {
            "遍历方式": "广度优先", 
            "数据结构": "队列",
            "空间复杂度": "O(w)",
            "适用场景": "最短路径、层次遍历"
        }
    }
    
    return comparison
```

## 🎨 算法实现

### 1. 递归实现
```python
def dfs_recursive():
    """DFS递归实现"""
    
    def dfs_recursive_graph(graph, start, visited=None):
        """图的DFS递归实现"""
        if visited is None:
            visited = set()
        
        # 访问当前节点
        print(f"访问节点: {start}")
        visited.add(start)
        
        # 递归访问邻接节点
        for neighbor in graph.get(start, []):
            if neighbor not in visited:
                dfs_recursive_graph(graph, neighbor, visited)
        
        return visited
    
    def dfs_recursive_tree(root):
        """树的DFS递归实现"""
        if root is None:
            return
        
        # 访问当前节点
        print(f"访问节点: {root.val}")
        
        # 递归访问子节点
        if root.left:
            dfs_recursive_tree(root.left)
        if root.right:
            dfs_recursive_tree(root.right)
    
    return dfs_recursive_graph, dfs_recursive_tree

def dfs_recursive_examples():
    """DFS递归示例"""
    
    # 图示例
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    def dfs_graph_example():
        """图DFS示例"""
        visited = set()
        dfs_recursive_graph(graph, 'A', visited)
        return visited
    
    # 树示例
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    
    def create_sample_tree():
        """创建示例树"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(7)
        return root
    
    def dfs_tree_example():
        """树DFS示例"""
        root = create_sample_tree()
        dfs_recursive_tree(root)
    
    return dfs_graph_example, dfs_tree_example
```

### 2. 迭代实现
```python
def dfs_iterative():
    """DFS迭代实现"""
    
    def dfs_iterative_graph(graph, start):
        """图的DFS迭代实现"""
        visited = set()
        stack = [start]
        
        while stack:
            # 弹出栈顶节点
            node = stack.pop()
            
            if node not in visited:
                # 访问节点
                print(f"访问节点: {node}")
                visited.add(node)
                
                # 将邻接节点压入栈
                for neighbor in reversed(graph.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return visited
    
    def dfs_iterative_tree(root):
        """树的DFS迭代实现"""
        if root is None:
            return
        
        stack = [root]
        
        while stack:
            # 弹出栈顶节点
            node = stack.pop()
            
            # 访问节点
            print(f"访问节点: {node.val}")
            
            # 将子节点压入栈（注意顺序）
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
    
    return dfs_iterative_graph, dfs_iterative_tree

def dfs_iterative_examples():
    """DFS迭代示例"""
    
    # 图示例
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    def dfs_graph_iterative_example():
        """图DFS迭代示例"""
        return dfs_iterative_graph(graph, 'A')
    
    # 树示例
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    
    def create_sample_tree():
        """创建示例树"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(7)
        return root
    
    def dfs_tree_iterative_example():
        """树DFS迭代示例"""
        root = create_sample_tree()
        dfs_iterative_tree(root)
    
    return dfs_graph_iterative_example, dfs_tree_iterative_example
```

### 3. 路径查找实现
```python
def dfs_path_finding():
    """DFS路径查找实现"""
    
    def dfs_find_path(graph, start, end, path=None):
        """查找从start到end的路径"""
        if path is None:
            path = []
        
        # 将当前节点添加到路径
        path = path + [start]
        
        # 如果到达目标节点，返回路径
        if start == end:
            return path
        
        # 递归搜索邻接节点
        for neighbor in graph.get(start, []):
            if neighbor not in path:  # 避免循环
                new_path = dfs_find_path(graph, neighbor, end, path)
                if new_path:
                    return new_path
        
        return None
    
    def dfs_find_all_paths(graph, start, end, path=None):
        """查找从start到end的所有路径"""
        if path is None:
            path = []
        
        # 将当前节点添加到路径
        path = path + [start]
        
        # 如果到达目标节点，返回路径
        if start == end:
            return [path]
        
        # 存储所有路径
        paths = []
        
        # 递归搜索邻接节点
        for neighbor in graph.get(start, []):
            if neighbor not in path:  # 避免循环
                new_paths = dfs_find_all_paths(graph, neighbor, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        
        return paths
    
    def dfs_find_shortest_path(graph, start, end):
        """查找最短路径（DFS版本）"""
        all_paths = dfs_find_all_paths(graph, start, end)
        if not all_paths:
            return None
        
        # 返回最短路径
        return min(all_paths, key=len)
    
    return dfs_find_path, dfs_find_all_paths, dfs_find_shortest_path

def dfs_path_examples():
    """DFS路径查找示例"""
    
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    def path_finding_example():
        """路径查找示例"""
        # 查找单条路径
        path = dfs_find_path(graph, 'A', 'F')
        print(f"从A到F的路径: {path}")
        
        # 查找所有路径
        all_paths = dfs_find_all_paths(graph, 'A', 'F')
        print(f"从A到F的所有路径: {all_paths}")
        
        # 查找最短路径
        shortest_path = dfs_find_shortest_path(graph, 'A', 'F')
        print(f"从A到F的最短路径: {shortest_path}")
    
    return path_finding_example
```

## 🔧 高级应用

### 1. 连通性检测
```python
def dfs_connectivity():
    """DFS连通性检测"""
    
    def dfs_connected_components(graph):
        """检测连通分量"""
        visited = set()
        components = []
        
        for node in graph:
            if node not in visited:
                # 开始新的连通分量
                component = []
                dfs_component(graph, node, visited, component)
                components.append(component)
        
        return components
    
    def dfs_component(graph, start, visited, component):
        """DFS遍历连通分量"""
        visited.add(start)
        component.append(start)
        
        for neighbor in graph.get(start, []):
            if neighbor not in visited:
                dfs_component(graph, neighbor, visited, component)
    
    def dfs_is_connected(graph):
        """检测图是否连通"""
        if not graph:
            return True
        
        visited = set()
        start_node = next(iter(graph))
        dfs_component(graph, start_node, visited, [])
        
        # 检查是否所有节点都被访问
        return len(visited) == len(graph)
    
    def dfs_articulation_points(graph):
        """查找割点（关节点）"""
        visited = set()
        discovery_time = {}
        low_time = {}
        parent = {}
        articulation_points = set()
        time = 0
        
        def dfs_articulation(node):
            nonlocal time
            visited.add(node)
            discovery_time[node] = time
            low_time[node] = time
            time += 1
            
            children = 0
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    parent[neighbor] = node
                    children += 1
                    dfs_articulation(neighbor)
                    
                    # 更新low_time
                    low_time[node] = min(low_time[node], low_time[neighbor])
                    
                    # 检查是否为割点
                    if parent[node] is None and children > 1:
                        articulation_points.add(node)
                    if parent[node] is not None and low_time[neighbor] >= discovery_time[node]:
                        articulation_points.add(node)
                
                elif neighbor != parent[node]:
                    low_time[node] = min(low_time[node], discovery_time[neighbor])
        
        # 对每个未访问的节点进行DFS
        for node in graph:
            if node not in visited:
                parent[node] = None
                dfs_articulation(node)
        
        return articulation_points
    
    return dfs_connected_components, dfs_is_connected, dfs_articulation_points

def connectivity_examples():
    """连通性检测示例"""
    
    # 连通图
    connected_graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }
    
    # 非连通图
    disconnected_graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C']
    }
    
    def connectivity_example():
        """连通性检测示例"""
        # 检测连通分量
        components = dfs_connected_components(disconnected_graph)
        print(f"连通分量: {components}")
        
        # 检测是否连通
        is_connected = dfs_is_connected(connected_graph)
        print(f"图是否连通: {is_connected}")
        
        # 查找割点
        articulation_points = dfs_articulation_points(connected_graph)
        print(f"割点: {articulation_points}")
    
    return connectivity_example
```

### 2. 拓扑排序
```python
def dfs_topological_sort():
    """DFS拓扑排序"""
    
    def dfs_topological_sort_dfs(graph):
        """使用DFS进行拓扑排序"""
        visited = set()
        stack = []
        
        def dfs_visit(node):
            visited.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs_visit(neighbor)
            
            # 将节点压入栈
            stack.append(node)
        
        # 对每个未访问的节点进行DFS
        for node in graph:
            if node not in visited:
                dfs_visit(node)
        
        # 返回逆序（栈顶到底）
        return stack[::-1]
    
    def dfs_detect_cycle(graph):
        """检测有向图中的环"""
        visited = set()
        rec_stack = set()
        
        def dfs_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if dfs_cycle(node):
                    return True
        
        return False
    
    def dfs_topological_sort_with_cycle_detection(graph):
        """带环检测的拓扑排序"""
        if dfs_detect_cycle(graph):
            return None  # 有环，无法拓扑排序
        
        return dfs_topological_sort_dfs(graph)
    
    return dfs_topological_sort_dfs, dfs_detect_cycle, dfs_topological_sort_with_cycle_detection

def topological_sort_examples():
    """拓扑排序示例"""
    
    # 有向无环图
    dag = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': ['E'],
        'E': []
    }
    
    # 有环图
    cyclic_graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }
    
    def topological_sort_example():
        """拓扑排序示例"""
        # 拓扑排序
        topo_order = dfs_topological_sort_dfs(dag)
        print(f"拓扑排序结果: {topo_order}")
        
        # 环检测
        has_cycle = dfs_detect_cycle(cyclic_graph)
        print(f"图是否有环: {has_cycle}")
        
        # 带环检测的拓扑排序
        topo_order_with_cycle = dfs_topological_sort_with_cycle_detection(dag)
        print(f"带环检测的拓扑排序: {topo_order_with_cycle}")
    
    return topological_sort_example
```

### 3. 回溯算法
```python
def dfs_backtracking():
    """DFS回溯算法"""
    
    def dfs_n_queens(n):
        """N皇后问题"""
        def is_safe(board, row, col):
            """检查位置是否安全"""
            # 检查列
            for i in range(row):
                if board[i][col] == 1:
                    return False
            
            # 检查对角线
            for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
                if board[i][j] == 1:
                    return False
            
            for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
                if board[i][j] == 1:
                    return False
            
            return True
        
        def solve_n_queens(board, row):
            """递归解决N皇后问题"""
            if row == n:
                return True
            
            for col in range(n):
                if is_safe(board, row, col):
                    board[row][col] = 1
                    
                    if solve_n_queens(board, row + 1):
                        return True
                    
                    board[row][col] = 0  # 回溯
            
            return False
        
        # 初始化棋盘
        board = [[0] * n for _ in range(n)]
        
        if solve_n_queens(board, 0):
            return board
        else:
            return None
    
    def dfs_sudoku_solver(board):
        """数独求解器"""
        def is_valid(board, row, col, num):
            """检查数字是否有效"""
            # 检查行
            for x in range(9):
                if board[row][x] == num:
                    return False
            
            # 检查列
            for x in range(9):
                if board[x][col] == num:
                    return False
            
            # 检查3x3宫格
            start_row = row - row % 3
            start_col = col - col % 3
            for i in range(3):
                for j in range(3):
                    if board[i + start_row][j + start_col] == num:
                        return False
            
            return True
        
        def solve_sudoku(board):
            """递归解决数独"""
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                
                                if solve_sudoku(board):
                                    return True
                                
                                board[row][col] = 0  # 回溯
                        
                        return False
            
            return True
        
        if solve_sudoku(board):
            return board
        else:
            return None
    
    def dfs_permutations(nums):
        """生成全排列"""
        def backtrack(path, used):
            """回溯生成排列"""
            if len(path) == len(nums):
                result.append(path[:])
                return
            
            for i in range(len(nums)):
                if not used[i]:
                    used[i] = True
                    path.append(nums[i])
                    backtrack(path, used)
                    path.pop()
                    used[i] = False
        
        result = []
        backtrack([], [False] * len(nums))
        return result
    
    return dfs_n_queens, dfs_sudoku_solver, dfs_permutations

def backtracking_examples():
    """回溯算法示例"""
    
    def n_queens_example():
        """N皇后示例"""
        n = 4
        solution = dfs_n_queens(n)
        if solution:
            print("N皇后解决方案:")
            for row in solution:
                print(row)
        else:
            print("无解")
    
    def sudoku_example():
        """数独示例"""
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        solution = dfs_sudoku_solver(board)
        if solution:
            print("数独解决方案:")
            for row in solution:
                print(row)
        else:
            print("无解")
    
    def permutations_example():
        """全排列示例"""
        nums = [1, 2, 3]
        permutations = dfs_permutations(nums)
        print(f"全排列: {permutations}")
    
    return n_queens_example, sudoku_example, permutations_example
```

## 📊 性能分析

### 1. 时间复杂度分析
```python
def dfs_time_complexity():
    """DFS时间复杂度分析"""
    complexity_analysis = {
        "图遍历": {
            "时间复杂度": "O(V + E)",
            "说明": "V为顶点数，E为边数，每个顶点和边都被访问一次",
            "最坏情况": "O(V + E)"
        },
        "树遍历": {
            "时间复杂度": "O(N)",
            "说明": "N为节点数，每个节点都被访问一次",
            "最坏情况": "O(N)"
        },
        "路径查找": {
            "时间复杂度": "O(V + E)",
            "说明": "最坏情况下需要遍历整个图",
            "最坏情况": "O(V + E)"
        },
        "回溯算法": {
            "时间复杂度": "指数级",
            "说明": "取决于问题的解空间大小",
            "最坏情况": "O(b^d) - b为分支因子，d为深度"
        }
    }
    
    return complexity_analysis

def dfs_space_complexity():
    """DFS空间复杂度分析"""
    space_analysis = {
        "递归实现": {
            "空间复杂度": "O(h)",
            "说明": "h为递归深度（树的高度或图的深度）",
            "影响因素": ["递归深度", "系统栈大小"]
        },
        "迭代实现": {
            "空间复杂度": "O(h)",
            "说明": "h为栈的最大深度",
            "影响因素": ["栈大小", "访问顺序"]
        },
        "路径查找": {
            "空间复杂度": "O(h)",
            "说明": "存储当前路径",
            "影响因素": ["路径长度", "递归深度"]
        },
        "回溯算法": {
            "空间复杂度": "O(d)",
            "说明": "d为搜索深度",
            "影响因素": ["问题规模", "搜索深度"]
        }
    }
    
    return space_analysis
```

### 2. 优化策略
```python
def dfs_optimization():
    """DFS优化策略"""
    optimization_strategies = {
        "剪枝优化": {
            "策略": "提前终止无效搜索",
            "方法": ["可行性剪枝", "最优性剪枝", "重复性剪枝"],
            "应用": ["回溯算法", "路径查找"]
        },
        "记忆化": {
            "策略": "缓存已计算的结果",
            "方法": ["动态规划", "缓存中间结果"],
            "应用": ["重复子问题", "状态空间搜索"]
        },
        "迭代深化": {
            "策略": "限制搜索深度",
            "方法": ["深度限制", "逐步增加深度"],
            "应用": ["无限深度搜索", "内存受限场景"]
        },
        "双向搜索": {
            "策略": "从起点和终点同时搜索",
            "方法": ["双向DFS", "相遇检测"],
            "应用": ["路径查找", "状态空间搜索"]
        }
    }
    
    return optimization_strategies

def dfs_optimization_examples():
    """DFS优化示例"""
    
    def dfs_with_pruning():
        """带剪枝的DFS"""
        def dfs_pruned_path(graph, start, end, max_depth, path=None, depth=0):
            """带深度限制的路径查找"""
            if path is None:
                path = []
            
            # 剪枝：超过最大深度
            if depth > max_depth:
                return None
            
            path = path + [start]
            
            if start == end:
                return path
            
            for neighbor in graph.get(start, []):
                if neighbor not in path:
                    result = dfs_pruned_path(graph, neighbor, end, max_depth, path, depth + 1)
                    if result:
                        return result
            
            return None
        
        return dfs_pruned_path
    
    def dfs_with_memoization():
        """带记忆化的DFS"""
        def dfs_memoized(graph, start, end, memo=None):
            """带记忆化的路径查找"""
            if memo is None:
                memo = {}
            
            if (start, end) in memo:
                return memo[(start, end)]
            
            if start == end:
                return [start]
            
            for neighbor in graph.get(start, []):
                path = dfs_memoized(graph, neighbor, end, memo)
                if path:
                    result = [start] + path
                    memo[(start, end)] = result
                    return result
            
            memo[(start, end)] = None
            return None
        
        return dfs_memoized
    
    return dfs_with_pruning, dfs_with_memoization
```

## 🔗 相关概念

### 广度优先搜索
- **关系**：DFS和BFS是图遍历的两种基本方法
- **链接**：[[02-广度优先搜索(BFS)]]

### 双向搜索
- **关系**：双向搜索可以结合DFS和BFS
- **链接**：[[03-双向搜索]]

### A星算法
- **关系**：A*算法结合了DFS的深度搜索和启发式信息
- **链接**：[[04-A星算法]]

### 搜索算法应用
- **关系**：DFS是搜索算法的重要应用
- **链接**：[[05-搜索算法应用场景]]

### 递归与分治
- **关系**：DFS是递归思想的重要应用
- **链接**：[[02-理解层-核心思想/01-递归与分治]]

### 回溯算法
- **关系**：DFS是回溯算法的基础
- **链接**：[[02-理解层-核心思想/04-回溯算法]]

## 📚 学习建议

### 费曼学习法
1. **选择概念**：深度优先搜索
2. **教授他人**：解释DFS的原理和应用
3. **回顾简化**：找出理解不足
4. **重新组织**：用更简单的方式表达

### 刻意练习
1. **实现练习**：实现各种DFS变体
2. **应用练习**：解决DFS相关问题
3. **优化练习**：优化DFS性能
4. **对比练习**：对比DFS与其他搜索算法

## 🔗 相关链接
- [[02-广度优先搜索(BFS)]] - 广度优先搜索算法
- [[03-双向搜索]] - 双向搜索算法
- [[04-A星算法]] - A*搜索算法
- [[05-搜索算法应用场景]] - 搜索算法应用场景
- [[02-理解层-核心思想/01-递归与分治]] - 递归与分治思想
- [[02-理解层-核心思想/04-回溯算法]] - 回溯算法
