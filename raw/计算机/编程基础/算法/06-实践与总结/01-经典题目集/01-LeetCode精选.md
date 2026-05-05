# LeetCode精选

## 概述

LeetCode精选题目是算法学习中的重要资源，涵盖了各种算法思想和数据结构应用。通过练习这些精选题目，可以快速提升算法能力和编程技巧。

## 核心概念

### 基本定义
- **LeetCode**：在线编程平台
- **精选题目**：经过筛选的高质量题目
- **算法思想**：解决问题的核心思路
- **数据结构**：组织数据的方式

### 关键特性
- **系统性**：题目覆盖全面
- **递进性**：难度逐步提升
- **实用性**：贴近实际应用
- **挑战性**：具有一定难度

## LeetCode精选题目分类

### 基础题目（Easy）

#### 1. 两数之和
**题目描述**：给定一个整数数组和一个目标值，找出数组中两个数的和等于目标值的索引。

**解题思路**：
- 使用哈希表存储已遍历的元素
- 对于每个元素，查找目标值减去当前元素的值
- 时间复杂度：O(n)，空间复杂度：O(n)

**代码实现**：
```python
def two_sum(nums, target):
    """两数之和"""
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

#### 2. 反转链表
**题目描述**：反转一个单链表。

**解题思路**：
- 使用三个指针：prev、current、next
- 逐个反转节点
- 时间复杂度：O(n)，空间复杂度：O(1)

**代码实现**：
```python
def reverse_list(head):
    """反转链表"""
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev
```

#### 3. 有效的括号
**题目描述**：给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。

**解题思路**：
- 使用栈存储左括号
- 遇到右括号时，检查栈顶是否匹配
- 时间复杂度：O(n)，空间复杂度：O(n)

**代码实现**：
```python
def is_valid(s):
    """有效的括号"""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack
```

### 中等题目（Medium）

#### 1. 无重复字符的最长子串
**题目描述**：给定一个字符串，找出其中不含有重复字符的最长子串的长度。

**解题思路**：
- 使用滑动窗口
- 维护一个字符集合
- 时间复杂度：O(n)，空间复杂度：O(k)

**代码实现**：
```python
def length_of_longest_substring(s):
    """无重复字符的最长子串"""
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

#### 2. 最长回文子串
**题目描述**：给定一个字符串，找出其中最长的回文子串。

**解题思路**：
- 使用中心扩展法
- 从每个位置向两边扩展
- 时间复杂度：O(n²)，空间复杂度：O(1)

**代码实现**：
```python
def longest_palindrome(s):
    """最长回文子串"""
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    if not s:
        return ""
    
    longest = ""
    for i in range(len(s)):
        # 奇数长度
        palindrome1 = expand_around_center(i, i)
        # 偶数长度
        palindrome2 = expand_around_center(i, i + 1)
        
        longest = max(longest, palindrome1, palindrome2, key=len)
    
    return longest
```

#### 3. 盛最多水的容器
**题目描述**：给定n个非负整数，表示容器的高度，找出能够盛最多水的容器。

**解题思路**：
- 使用双指针
- 从两端向中间移动
- 时间复杂度：O(n)，空间复杂度：O(1)

**代码实现**：
```python
def max_area(height):
    """盛最多水的容器"""
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area
```

### 困难题目（Hard）

#### 1. 合并K个排序链表
**题目描述**：合并k个排序链表，返回合并后的排序链表。

**解题思路**：
- 使用分治法
- 递归合并两个链表
- 时间复杂度：O(n log k)，空间复杂度：O(log k)

**代码实现**：
```python
def merge_k_lists(lists):
    """合并K个排序链表"""
    if not lists:
        return None
    
    def merge_two_lists(l1, l2):
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 or l2
        return dummy.next
    
    def merge_lists(lists, left, right):
        if left == right:
            return lists[left]
        
        mid = (left + right) // 2
        left_list = merge_lists(lists, left, mid)
        right_list = merge_lists(lists, mid + 1, right)
        
        return merge_two_lists(left_list, right_list)
    
    return merge_lists(lists, 0, len(lists) - 1)
```

#### 2. 正则表达式匹配
**题目描述**：实现正则表达式匹配，支持 '.' 和 '*'。

**解题思路**：
- 使用动态规划
- 处理 '*' 的特殊情况
- 时间复杂度：O(mn)，空间复杂度：O(mn)

**代码实现**：
```python
def is_match(s, p):
    """正则表达式匹配"""
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    dp[0][0] = True
    
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2] or (dp[i - 1][j] and (s[i - 1] == p[j - 2] or p[j - 2] == '.'))
            else:
                dp[i][j] = dp[i - 1][j - 1] and (s[i - 1] == p[j - 1] or p[j - 1] == '.')
    
    return dp[m][n]
```

## 题目分类索引

### 按算法思想分类

| 算法思想 | 题目数量 | 代表题目 | 难度分布 |
|---------|---------|---------|----------|
| 双指针 | 15 | 两数之和、盛最多水的容器 | Easy-Medium |
| 滑动窗口 | 12 | 无重复字符的最长子串 | Medium |
| 动态规划 | 25 | 最长回文子串、正则表达式匹配 | Medium-Hard |
| 贪心算法 | 18 | 跳跃游戏、加油站 | Medium |
| 分治算法 | 10 | 合并K个排序链表 | Hard |
| 回溯算法 | 20 | 全排列、N皇后 | Medium-Hard |
| 图算法 | 15 | 课程表、岛屿数量 | Medium |
| 树算法 | 22 | 二叉树遍历、路径总和 | Easy-Medium |

### 按数据结构分类

| 数据结构 | 题目数量 | 代表题目 | 难度分布 |
|---------|---------|---------|----------|
| 数组 | 30 | 两数之和、三数之和 | Easy-Medium |
| 链表 | 18 | 反转链表、合并两个有序链表 | Easy-Medium |
| 栈 | 12 | 有效的括号、最小栈 | Easy-Medium |
| 队列 | 8 | 滑动窗口最大值 | Medium |
| 哈希表 | 20 | 两数之和、字母异位词分组 | Easy-Medium |
| 树 | 25 | 二叉树遍历、路径总和 | Easy-Medium |
| 图 | 15 | 课程表、岛屿数量 | Medium |
| 堆 | 10 | 合并K个排序链表 | Hard |

## 解题技巧总结

### 1. 双指针技巧
- **对撞指针**：从两端向中间移动
- **快慢指针**：两个指针以不同速度移动
- **滑动窗口**：维护一个动态窗口

### 2. 动态规划技巧
- **状态定义**：明确状态的含义
- **状态转移**：找到状态之间的关系
- **边界条件**：处理特殊情况

### 3. 回溯算法技巧
- **选择列表**：当前可以做的选择
- **路径**：已经做过的选择
- **结束条件**：满足条件时结束

### 4. 图算法技巧
- **DFS**：深度优先搜索
- **BFS**：广度优先搜索
- **拓扑排序**：处理有向无环图

## 学习建议

### 费曼学习法
1. **理解题目**：用简单语言解释题目要求
2. **分析思路**：分析解题思路和算法思想
3. **实现代码**：编写完整的代码实现
4. **教授他人**：向他人解释解题过程

### 刻意练习
1. **基础练习**：从Easy题目开始
2. **进阶练习**：逐步挑战Medium和Hard题目
3. **综合练习**：练习不同类型的题目
4. **创新练习**：尝试优化算法

### 学习路径
1. **理论学习**：理解各种算法思想
2. **实践练习**：大量练习LeetCode题目
3. **总结归纳**：总结解题规律和技巧
4. **持续改进**：不断优化解题方法
