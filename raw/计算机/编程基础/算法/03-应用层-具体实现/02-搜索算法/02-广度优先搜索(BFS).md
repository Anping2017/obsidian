# 广度优先搜索(BFS)

## 🎯 核心概念

**广度优先搜索(Breadth-First Search, BFS)**是一种用于遍历或搜索树或图的算法。它从根节点开始，逐层访问节点，先访问距离根节点最近的节点，然后访问距离根节点更远的节点。

## 🔍 算法原理

### 1. 基本思想
```python
def bfs_basic_concept():
    """BFS基本思想"""
    # 1. 从起始节点开始
    # 2. 将起始节点加入队列
    # 3. 当队列不为空时：
    #    a. 取出队列头部节点
    #    b. 访问该节点
    #    c. 将该节点的所有未访问邻接节点加入队列
    # 4. 重复步骤3直到队列为空
    
    pass

def bfs_core_principles():
    """BFS核心原理"""
    # 1. 广度优先：按层次遍历，先访问同层节点
    # 2. 队列机制：使用队列保证访问顺序
    # 3. 访问标记：避免重复访问同一节点
    # 4. 层次遍历：保证最短路径特性
    
    pass
```

### 2. 算法特点
```python
def bfs_characteristics():
    """BFS算法特点"""
    characteristics = {
        "空间复杂度": "O(w) - w为树的最大宽度",
        "时间复杂度": "O(V + E) - V为顶点数，E为边数",
        "实现方式": ["队列"],
        "遍历顺序": "广度优先",
        "应用场景": ["最短路径", "层次遍历", "连通性检测"]
    }
    
    return characteristics

def bfs_vs_dfs():
    """BFS vs DFS对比"""
    comparison = {
        "BFS": {
            "遍历方式": "广度优先",
            "数据结构": "队列",
            "空间复杂度": "O(w)",
            "适用场景": "最短路径、层次遍历"
        },
        "DFS": {
            "遍历方式": "深度优先",
            "数据结构": "栈（递归）",
            "空间复杂度": "O(h)",
            "适用场景": "路径查找、回溯问题"
        }
    }
    
    return comparison
```

## 🎨 算法实现

### 1. 基本实现
```python
def bfs_basic():
    """BFS基本实现"""
    
    def bfs_graph(graph, start):
        """图的BFS实现"""
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            # 取出队列头部节点
            node = queue.pop(0)
            print(f"访问节点: {node}")
            
            # 将邻接节点加入队列
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited
    
    def bfs_tree(root):
        """树的BFS实现"""
        if root is None:
            return
        
        queue = [root]
        
        while queue:
            # 取出队列头部节点
            node = queue.pop(0)
            print(f"访问节点: {node.val}")
            
            # 将子节点加入队列
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return bfs_graph, bfs_tree

def bfs_basic_examples():
    """BFS基本示例"""
    
    # 图示例
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    def bfs_graph_example():
        """图BFS示例"""
        return bfs_graph(graph, 'A')
    
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
    
    def bfs_tree_example():
        """树BFS示例"""
        root = create_sample_tree()
        bfs_tree(root)
    
    return bfs_graph_example, bfs_tree_example
```

### 2. 层次遍历实现
```python
def bfs_level_order():
    """BFS层次遍历实现"""
    
    def bfs_level_order_tree(root):
        """树的层次遍历"""
        if root is None:
            return []
        
        result = []
        queue = [root]
        
        while queue:
            level_size = len(queue)
            level = []
            
            # 处理当前层的所有节点
            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.val)
                
                # 将子节点加入队列
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level)
        
        return result
    
    def bfs_level_order_graph(graph, start):
        """图的层次遍历"""
        visited = set()
        queue = [(start, 0)]  # (节点, 层级)
        visited.add(start)
        result = {}
        
        while queue:
            node, level = queue.pop(0)
            
            # 将节点添加到对应层级
            if level not in result:
                result[level] = []
            result[level].append(node)
            
            # 将邻接节点加入队列
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))
        
        return result
    
    def bfs_zigzag_level_order(root):
        """之字形层次遍历"""
        if root is None:
            return []
        
        result = []
        queue = [root]
        left_to_right = True
        
        while queue:
            level_size = len(queue)
            level = []
            
            for _ in range(level_size):
                node = queue.pop(0)
                
                if left_to_right:
                    level.append(node.val)
                else:
                    level.insert(0, node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level)
            left_to_right = not left_to_right
        
        return result
    
    return bfs_level_order_tree, bfs_level_order_graph, bfs_zigzag_level_order

def level_order_examples():
    """层次遍历示例"""
    
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
    
    def level_order_example():
        """层次遍历示例"""
        root = create_sample_tree()
        
        # 层次遍历
        level_order = bfs_level_order_tree(root)
        print(f"层次遍历结果: {level_order}")
        
        # 之字形层次遍历
        zigzag_order = bfs_zigzag_level_order(root)
        print(f"之字形层次遍历结果: {zigzag_order}")
    
    return level_order_example
```

### 3. 最短路径实现
```python
def bfs_shortest_path():
    """BFS最短路径实现"""
    
    def bfs_shortest_path_unweighted(graph, start, end):
        """无权图最短路径"""
        if start == end:
            return [start]
        
        visited = set()
        queue = [(start, [start])]  # (节点, 路径)
        visited.add(start)
        
        while queue:
            node, path = queue.pop(0)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    
                    if neighbor == end:
                        return new_path
                    
                    visited.add(neighbor)
                    queue.append((neighbor, new_path))
        
        return None  # 无路径
    
    def bfs_shortest_path_length(graph, start, end):
        """最短路径长度"""
        if start == end:
            return 0
        
        visited = set()
        queue = [(start, 0)]  # (节点, 距离)
        visited.add(start)
        
        while queue:
            node, distance = queue.pop(0)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if neighbor == end:
                        return distance + 1
                    
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return -1  # 无路径
    
    def bfs_all_shortest_paths(graph, start, end):
        """所有最短路径"""
        if start == end:
            return [[start]]
        
        visited = set()
        queue = [(start, [start])]  # (节点, 路径)
        visited.add(start)
        shortest_paths = []
        min_length = float('inf')
        
        while queue:
            node, path = queue.pop(0)
            
            # 如果当前路径长度超过已知最短路径，跳过
            if len(path) > min_length:
                continue
            
            for neighbor in graph.get(node, []):
                if neighbor not in path:  # 避免循环
                    new_path = path + [neighbor]
                    
                    if neighbor == end:
                        if len(new_path) < min_length:
                            min_length = len(new_path)
                            shortest_paths = [new_path]
                        elif len(new_path) == min_length:
                            shortest_paths.append(new_path)
                    else:
                        queue.append((neighbor, new_path))
        
        return shortest_paths
    
    return bfs_shortest_path_unweighted, bfs_shortest_path_length, bfs_all_shortest_paths

def shortest_path_examples():
    """最短路径示例"""
    
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    def shortest_path_example():
        """最短路径示例"""
        # 最短路径
        path = bfs_shortest_path_unweighted(graph, 'A', 'F')
        print(f"从A到F的最短路径: {path}")
        
        # 最短路径长度
        length = bfs_shortest_path_length(graph, 'A', 'F')
        print(f"从A到F的最短路径长度: {length}")
        
        # 所有最短路径
        all_paths = bfs_all_shortest_paths(graph, 'A', 'F')
        print(f"从A到F的所有最短路径: {all_paths}")
    
    return shortest_path_example
```

## 🔧 高级应用

### 1. 连通性检测
```python
def bfs_connectivity():
    """BFS连通性检测"""
    
    def bfs_connected_components(graph):
        """检测连通分量"""
        visited = set()
        components = []
        
        for node in graph:
            if node not in visited:
                # 开始新的连通分量
                component = []
                bfs_component(graph, node, visited, component)
                components.append(component)
        
        return components
    
    def bfs_component(graph, start, visited, component):
        """BFS遍历连通分量"""
        queue = [start]
        visited.add(start)
        
        while queue:
            node = queue.pop(0)
            component.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    def bfs_is_connected(graph):
        """检测图是否连通"""
        if not graph:
            return True
        
        visited = set()
        start_node = next(iter(graph))
        queue = [start_node]
        visited.add(start_node)
        
        while queue:
            node = queue.pop(0)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        # 检查是否所有节点都被访问
        return len(visited) == len(graph)
    
    def bfs_bipartite_check(graph):
        """检测二分图"""
        if not graph:
            return True
        
        color = {}
        
        for node in graph:
            if node not in color:
                queue = [node]
                color[node] = 0
                
                while queue:
                    current = queue.pop(0)
                    
                    for neighbor in graph.get(current, []):
                        if neighbor not in color:
                            color[neighbor] = 1 - color[current]
                            queue.append(neighbor)
                        elif color[neighbor] == color[current]:
                            return False
        
        return True
    
    return bfs_connected_components, bfs_is_connected, bfs_bipartite_check

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
    
    # 二分图
    bipartite_graph = {
        'A': ['D', 'E'],
        'B': ['D', 'E'],
        'C': ['D', 'E'],
        'D': ['A', 'B', 'C'],
        'E': ['A', 'B', 'C']
    }
    
    def connectivity_example():
        """连通性检测示例"""
        # 检测连通分量
        components = bfs_connected_components(disconnected_graph)
        print(f"连通分量: {components}")
        
        # 检测是否连通
        is_connected = bfs_is_connected(connected_graph)
        print(f"图是否连通: {is_connected}")
        
        # 检测二分图
        is_bipartite = bfs_bipartite_check(bipartite_graph)
        print(f"图是否为二分图: {is_bipartite}")
    
    return connectivity_example
```

### 2. 拓扑排序
```python
def bfs_topological_sort():
    """BFS拓扑排序（Kahn算法）"""
    
    def bfs_topological_sort_kahn(graph):
        """使用Kahn算法进行拓扑排序"""
        # 计算入度
        in_degree = {node: 0 for node in graph}
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] += 1
        
        # 找到所有入度为0的节点
        queue = [node for node in in_degree if in_degree[node] == 0]
        result = []
        
        while queue:
            # 取出入度为0的节点
            node = queue.pop(0)
            result.append(node)
            
            # 减少邻接节点的入度
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # 检查是否有环
        if len(result) != len(graph):
            return None  # 有环，无法拓扑排序
        
        return result
    
    def bfs_detect_cycle_indegree(graph):
        """使用入度检测环"""
        # 计算入度
        in_degree = {node: 0 for node in graph}
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] += 1
        
        # 找到所有入度为0的节点
        queue = [node for node in in_degree if in_degree[node] == 0]
        processed = 0
        
        while queue:
            node = queue.pop(0)
            processed += 1
            
            # 减少邻接节点的入度
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # 如果处理的节点数不等于总节点数，说明有环
        return processed != len(graph)
    
    def bfs_topological_sort_with_cycle_detection(graph):
        """带环检测的拓扑排序"""
        if bfs_detect_cycle_indegree(graph):
            return None  # 有环，无法拓扑排序
        
        return bfs_topological_sort_kahn(graph)
    
    return bfs_topological_sort_kahn, bfs_detect_cycle_indegree, bfs_topological_sort_with_cycle_detection

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
        topo_order = bfs_topological_sort_kahn(dag)
        print(f"拓扑排序结果: {topo_order}")
        
        # 环检测
        has_cycle = bfs_detect_cycle_indegree(cyclic_graph)
        print(f"图是否有环: {has_cycle}")
        
        # 带环检测的拓扑排序
        topo_order_with_cycle = bfs_topological_sort_with_cycle_detection(dag)
        print(f"带环检测的拓扑排序: {topo_order_with_cycle}")
    
    return topological_sort_example
```

### 3. 多源BFS
```python
def bfs_multi_source():
    """多源BFS"""
    
    def bfs_multi_source_shortest_path(graph, sources):
        """多源最短路径"""
        visited = set()
        queue = [(source, 0) for source in sources]  # (节点, 距离)
        visited.update(sources)
        distances = {source: 0 for source in sources}
        
        while queue:
            node, distance = queue.pop(0)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = distance + 1
                    queue.append((neighbor, distance + 1))
        
        return distances
    
    def bfs_rotten_oranges(grid):
        """腐烂的橘子问题"""
        if not grid or not grid[0]:
            return -1
        
        rows, cols = len(grid), len(grid[0])
        queue = []
        fresh_count = 0
        
        # 找到所有腐烂的橘子和新鲜橘子的数量
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:  # 腐烂的橘子
                    queue.append((i, j, 0))
                elif grid[i][j] == 1:  # 新鲜的橘子
                    fresh_count += 1
        
        if fresh_count == 0:
            return 0
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        max_time = 0
        
        while queue:
            row, col, time = queue.pop(0)
            max_time = max(max_time, time)
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < rows and 0 <= new_col < cols and 
                    grid[new_row][new_col] == 1):
                    
                    grid[new_row][new_col] = 2
                    fresh_count -= 1
                    queue.append((new_row, new_col, time + 1))
        
        return max_time if fresh_count == 0 else -1
    
    def bfs_walls_and_gates(rooms):
        """墙与门问题"""
        if not rooms or not rooms[0]:
            return
        
        rows, cols = len(rooms), len(rooms[0])
        queue = []
        
        # 找到所有门
        for i in range(rows):
            for j in range(cols):
                if rooms[i][j] == 0:  # 门
                    queue.append((i, j, 0))
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            row, col, distance = queue.pop(0)
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < rows and 0 <= new_col < cols and 
                    rooms[new_row][new_col] == 2147483647):  # 空房间
                    
                    rooms[new_row][new_col] = distance + 1
                    queue.append((new_row, new_col, distance + 1))
    
    return bfs_multi_source_shortest_path, bfs_rotten_oranges, bfs_walls_and_gates

def multi_source_examples():
    """多源BFS示例"""
    
    def multi_source_example():
        """多源BFS示例"""
        # 多源最短路径
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'D'],
            'D': ['B', 'C', 'E'],
            'E': ['D']
        }
        
        sources = ['A', 'C']
        distances = bfs_multi_source_shortest_path(graph, sources)
        print(f"多源最短路径: {distances}")
        
        # 腐烂的橘子
        grid = [
            [2, 1, 1],
            [1, 1, 0],
            [0, 1, 1]
        ]
        time = bfs_rotten_oranges(grid)
        print(f"腐烂橘子时间: {time}")
        
        # 墙与门
        rooms = [
            [2147483647, -1, 0, 2147483647],
            [2147483647, 2147483647, 2147483647, -1],
            [2147483647, -1, 2147483647, -1],
            [0, -1, 2147483647, 2147483647]
        ]
        bfs_walls_and_gates(rooms)
        print(f"墙与门结果: {rooms}")
    
    return multi_source_example
```

## 📊 性能分析

### 1. 时间复杂度分析
```python
def bfs_time_complexity():
    """BFS时间复杂度分析"""
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
        "最短路径": {
            "时间复杂度": "O(V + E)",
            "说明": "最坏情况下需要遍历整个图",
            "最坏情况": "O(V + E)"
        },
        "层次遍历": {
            "时间复杂度": "O(N)",
            "说明": "N为节点数，每个节点都被访问一次",
            "最坏情况": "O(N)"
        }
    }
    
    return complexity_analysis

def bfs_space_complexity():
    """BFS空间复杂度分析"""
    space_analysis = {
        "队列空间": {
            "空间复杂度": "O(w)",
            "说明": "w为树的最大宽度或图的最大分支数",
            "影响因素": ["图的宽度", "队列大小"]
        },
        "访问标记": {
            "空间复杂度": "O(V)",
            "说明": "V为顶点数，需要标记每个顶点",
            "影响因素": ["顶点数量", "标记方式"]
        },
        "路径存储": {
            "空间复杂度": "O(V)",
            "说明": "存储路径信息",
            "影响因素": ["路径长度", "存储方式"]
        },
        "层次信息": {
            "空间复杂度": "O(h)",
            "说明": "h为树的高度",
            "影响因素": ["树的高度", "层次数量"]
        }
    }
    
    return space_analysis
```

### 2. 优化策略
```python
def bfs_optimization():
    """BFS优化策略"""
    optimization_strategies = {
        "双向BFS": {
            "策略": "从起点和终点同时搜索",
            "方法": ["双向队列", "相遇检测"],
            "应用": ["最短路径", "状态空间搜索"],
            "优势": "减少搜索空间"
        },
        "A*搜索": {
            "策略": "结合启发式信息",
            "方法": ["优先级队列", "启发式函数"],
            "应用": ["路径规划", "游戏AI"],
            "优势": "提高搜索效率"
        },
        "分层BFS": {
            "策略": "按层次处理节点",
            "方法": ["层次标记", "批量处理"],
            "应用": ["层次遍历", "最短路径"],
            "优势": "减少内存使用"
        },
        "并行BFS": {
            "策略": "并行处理多个节点",
            "方法": ["多线程", "分布式计算"],
            "应用": ["大规模图", "高性能计算"],
            "优势": "提高处理速度"
        }
    }
    
    return optimization_strategies

def bfs_optimization_examples():
    """BFS优化示例"""
    
    def bidirectional_bfs(graph, start, end):
        """双向BFS"""
        if start == end:
            return [start]
        
        # 从起点开始的搜索
        start_queue = [start]
        start_visited = {start: [start]}
        
        # 从终点开始的搜索
        end_queue = [end]
        end_visited = {end: [end]}
        
        while start_queue and end_queue:
            # 从起点扩展
            start_node = start_queue.pop(0)
            for neighbor in graph.get(start_node, []):
                if neighbor not in start_visited:
                    start_visited[neighbor] = start_visited[start_node] + [neighbor]
                    start_queue.append(neighbor)
                    
                    # 检查是否相遇
                    if neighbor in end_visited:
                        return start_visited[neighbor] + end_visited[neighbor][::-1][1:]
            
            # 从终点扩展
            end_node = end_queue.pop(0)
            for neighbor in graph.get(end_node, []):
                if neighbor not in end_visited:
                    end_visited[neighbor] = end_visited[end_node] + [neighbor]
                    end_queue.append(neighbor)
                    
                    # 检查是否相遇
                    if neighbor in start_visited:
                        return start_visited[neighbor] + end_visited[neighbor][::-1][1:]
        
        return None
    
    def bfs_with_heuristic(graph, start, end, heuristic):
        """带启发式的BFS"""
        import heapq
        
        queue = [(heuristic(start, end), 0, start, [start])]
        visited = set()
        
        while queue:
            f_cost, g_cost, node, path = heapq.heappop(queue)
            
            if node == end:
                return path
            
            if node in visited:
                continue
            
            visited.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_g_cost = g_cost + 1
                    new_f_cost = new_g_cost + heuristic(neighbor, end)
                    heapq.heappush(queue, (new_f_cost, new_g_cost, neighbor, new_path))
        
        return None
    
    return bidirectional_bfs, bfs_with_heuristic
```

## 🔗 相关概念

### 深度优先搜索
- **关系**：BFS和DFS是图遍历的两种基本方法
- **链接**：[[01-深度优先搜索(DFS)]]

### 双向搜索
- **关系**：双向搜索可以结合BFS和DFS
- **链接**：[[03-双向搜索]]

### A星算法
- **关系**：A*算法结合了BFS的广度搜索和启发式信息
- **链接**：[[04-A星算法]]

### 搜索算法应用
- **关系**：BFS是搜索算法的重要应用
- **链接**：[[05-搜索算法应用场景]]

### 队列数据结构
- **关系**：BFS依赖队列数据结构
- **链接**：[[01-基础层-认识/03-数据结构基础/05-队列详解]]

### 图算法
- **关系**：BFS是图算法的基础
- **链接**：[[03-图算法]]

## 📚 学习建议

### 费曼学习法
1. **选择概念**：广度优先搜索
2. **教授他人**：解释BFS的原理和应用
3. **回顾简化**：找出理解不足
4. **重新组织**：用更简单的方式表达

### 刻意练习
1. **实现练习**：实现各种BFS变体
2. **应用练习**：解决BFS相关问题
3. **优化练习**：优化BFS性能
4. **对比练习**：对比BFS与其他搜索算法

## 🔗 相关链接
- [[01-深度优先搜索(DFS)]] - 深度优先搜索算法
- [[03-双向搜索]] - 双向搜索算法
- [[04-A星算法]] - A*搜索算法
- [[05-搜索算法应用场景]] - 搜索算法应用场景
- [[01-基础层-认识/03-数据结构基础/05-队列详解]] - 队列数据结构
- [[03-图算法]] - 图算法
