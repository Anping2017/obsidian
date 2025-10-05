# 二叉搜索树BST

## 📖 核心概念

**二叉搜索树（Binary Search Tree, BST）**是一种特殊的二叉树，满足左子树所有节点值小于根节点，右子树所有节点值大于根节点的性质。

### 🏗️ BST特性

```mermaid
graph TD
    A[二叉搜索树] --> B[有序性质]
    A --> C[查找效率]
    A --> D[插入删除]
    A --> E[中序遍历]
    
    B --> B1[左子树 < 根 < 右子树]
    B --> B2[递归定义]
    B --> B3[全局有序]
    
    C --> C1[平均O(log n)]
    C --> C2[最坏O(n)]
    C --> C3[二分查找]
    
    D --> D1[保持有序性]
    D --> D2[动态维护]
    D --> D3[结构调整]
    
    E --> E1[有序序列]
    E --> E2[排序算法]
    E --> E3[范围查询]
```

## 🔧 BST实现

### 基础BST类

```cpp
template<typename T>
class BinarySearchTree {
private:
    struct TreeNode {
        T data;
        TreeNode* left;
        TreeNode* right;
        
        TreeNode(const T& value) : data(value), left(nullptr), right(nullptr) {}
    };
    
    TreeNode* root;
    
    // 插入辅助函数
    TreeNode* insertHelper(TreeNode* node, const T& value) {
        if (!node) {
            return new TreeNode(value);
        }
        
        if (value < node->data) {
            node->left = insertHelper(node->left, value);
        } else if (value > node->data) {
            node->right = insertHelper(node->right, value);
        }
        // 相等时不插入（或根据需求处理）
        
        return node;
    }
    
    // 查找辅助函数
    TreeNode* searchHelper(TreeNode* node, const T& value) const {
        if (!node || node->data == value) {
            return node;
        }
        
        if (value < node->data) {
            return searchHelper(node->left, value);
        } else {
            return searchHelper(node->right, value);
        }
    }
    
    // 删除辅助函数
    TreeNode* deleteHelper(TreeNode* node, const T& value) {
        if (!node) return nullptr;
        
        if (value < node->data) {
            node->left = deleteHelper(node->left, value);
        } else if (value > node->data) {
            node->right = deleteHelper(node->right, value);
        } else {
            // 找到要删除的节点
            if (!node->left) {
                TreeNode* temp = node->right;
                delete node;
                return temp;
            } else if (!node->right) {
                TreeNode* temp = node->left;
                delete node;
                return temp;
            }
            
            // 有两个子节点，找到右子树的最小值
            TreeNode* minNode = findMin(node->right);
            node->data = minNode->data;
            node->right = deleteHelper(node->right, minNode->data);
        }
        
        return node;
    }
    
    // 找到最小节点
    TreeNode* findMin(TreeNode* node) const {
        while (node && node->left) {
            node = node->left;
        }
        return node;
    }
    
    // 找到最大节点
    TreeNode* findMax(TreeNode* node) const {
        while (node && node->right) {
            node = node->right;
        }
        return node;
    }
    
    // 中序遍历辅助函数
    void inorderHelper(TreeNode* node, vector<T>& result) const {
        if (node) {
            inorderHelper(node->left, result);
            result.push_back(node->data);
            inorderHelper(node->right, result);
        }
    }
    
    // 计算高度
    int heightHelper(TreeNode* node) const {
        if (!node) return -1;
        
        int leftHeight = heightHelper(node->left);
        int rightHeight = heightHelper(node->right);
        
        return max(leftHeight, rightHeight) + 1;
    }
    
    // 计算节点数
    int countNodesHelper(TreeNode* node) const {
        if (!node) return 0;
        
        return 1 + countNodesHelper(node->left) + countNodesHelper(node->right);
    }
    
    // 验证BST性质
    bool isValidBSTHelper(TreeNode* node, T minVal, T maxVal) const {
        if (!node) return true;
        
        if (node->data <= minVal || node->data >= maxVal) {
            return false;
        }
        
        return isValidBSTHelper(node->left, minVal, node->data) &&
               isValidBSTHelper(node->right, node->data, maxVal);
    }
    
    // 清理树
    void clearHelper(TreeNode* node) {
        if (node) {
            clearHelper(node->left);
            clearHelper(node->right);
            delete node;
        }
    }
    
public:
    BinarySearchTree() : root(nullptr) {}
    
    ~BinarySearchTree() {
        clear();
    }
    
    // 插入元素
    void insert(const T& value) {
        root = insertHelper(root, value);
    }
    
    // 查找元素
    bool search(const T& value) const {
        return searchHelper(root, value) != nullptr;
    }
    
    // 删除元素
    bool remove(const T& value) {
        if (!search(value)) return false;
        root = deleteHelper(root, value);
        return true;
    }
    
    // 获取最小值
    T getMin() const {
        TreeNode* minNode = findMin(root);
        if (!minNode) {
            throw std::runtime_error("Tree is empty");
        }
        return minNode->data;
    }
    
    // 获取最大值
    T getMax() const {
        TreeNode* maxNode = findMax(root);
        if (!maxNode) {
            throw std::runtime_error("Tree is empty");
        }
        return maxNode->data;
    }
    
    // 中序遍历
    vector<T> inorderTraversal() const {
        vector<T> result;
        inorderHelper(root, result);
        return result;
    }
    
    // 获取高度
    int height() const {
        return heightHelper(root);
    }
    
    // 获取节点数
    int size() const {
        return countNodesHelper(root);
    }
    
    // 检查是否为空
    bool isEmpty() const {
        return root == nullptr;
    }
    
    // 验证BST性质
    bool isValidBST() const {
        return isValidBSTHelper(root, numeric_limits<T>::min(), numeric_limits<T>::max());
    }
    
    // 清空树
    void clear() {
        clearHelper(root);
        root = nullptr;
    }
    
    // 打印树结构
    void printTree() const {
        printTreeHelper(root, 0);
    }
    
private:
    void printTreeHelper(TreeNode* node, int depth) const {
        if (!node) return;
        
        printTreeHelper(node->right, depth + 1);
        
        for (int i = 0; i < depth; ++i) {
            cout << "  ";
        }
        cout << node->data << endl;
        
        printTreeHelper(node->left, depth + 1);
    }
};
```

## 🎯 BST操作

### 1. 范围查询

```cpp
    // 范围查询
    vector<T> rangeQuery(const T& minVal, const T& maxVal) const {
        vector<T> result;
        rangeQueryHelper(root, minVal, maxVal, result);
        return result;
    }
    
    void rangeQueryHelper(TreeNode* node, const T& minVal, const T& maxVal, 
                         vector<T>& result) const {
        if (!node) return;
        
        if (node->data > minVal) {
            rangeQueryHelper(node->left, minVal, maxVal, result);
        }
        
        if (node->data >= minVal && node->data <= maxVal) {
            result.push_back(node->data);
        }
        
        if (node->data < maxVal) {
            rangeQueryHelper(node->right, minVal, maxVal, result);
        }
    }
    
    // 查找第k小元素
    T kthSmallest(int k) const {
        int count = 0;
        return kthSmallestHelper(root, k, count);
    }
    
    T kthSmallestHelper(TreeNode* node, int k, int& count) const {
        if (!node) {
            throw std::runtime_error("Not enough elements");
        }
        
        T leftResult = kthSmallestHelper(node->left, k, count);
        if (count == k) {
            return leftResult;
        }
        
        count++;
        if (count == k) {
            return node->data;
        }
        
        return kthSmallestHelper(node->right, k, count);
    }
    
    // 查找前驱
    T predecessor(const T& value) const {
        TreeNode* pred = nullptr;
        TreeNode* current = root;
        
        while (current) {
            if (value > current->data) {
                pred = current;
                current = current->right;
            } else {
                current = current->left;
            }
        }
        
        if (!pred) {
            throw std::runtime_error("No predecessor found");
        }
        return pred->data;
    }
    
    // 查找后继
    T successor(const T& value) const {
        TreeNode* succ = nullptr;
        TreeNode* current = root;
        
        while (current) {
            if (value < current->data) {
                succ = current;
                current = current->left;
            } else {
                current = current->right;
            }
        }
        
        if (!succ) {
            throw std::runtime_error("No successor found");
        }
        return succ->data;
    }
```

### 2. BST转换

```cpp
    // 将BST转换为有序数组
    vector<T> toArray() const {
        return inorderTraversal();
    }
    
    // 从有序数组构建BST
    static BinarySearchTree<T> fromArray(const vector<T>& arr) {
        BinarySearchTree<T> bst;
        bst.root = buildBSTFromArray(arr, 0, arr.size() - 1);
        return bst;
    }
    
    static TreeNode* buildBSTFromArray(const vector<T>& arr, int start, int end) {
        if (start > end) return nullptr;
        
        int mid = start + (end - start) / 2;
        TreeNode* node = new TreeNode(arr[mid]);
        
        node->left = buildBSTFromArray(arr, start, mid - 1);
        node->right = buildBSTFromArray(arr, mid + 1, end);
        
        return node;
    }
    
    // 将BST转换为双向链表
    TreeNode* toDoublyLinkedList() {
        TreeNode* head = nullptr;
        TreeNode* prev = nullptr;
        
        convertToDLLHelper(root, head, prev);
        
        return head;
    }
    
    void convertToDLLHelper(TreeNode* node, TreeNode*& head, TreeNode*& prev) {
        if (!node) return;
        
        convertToDLLHelper(node->left, head, prev);
        
        if (!prev) {
            head = node;
        } else {
            prev->right = node;
            node->left = prev;
        }
        
        prev = node;
        convertToDLLHelper(node->right, head, prev);
    }
```

## 📊 性能分析

### 时间复杂度

| 操作 | 平均情况 | 最坏情况 | 说明 |
|------|----------|----------|------|
| **查找** | O(log n) | O(n) | 树高度决定 |
| **插入** | O(log n) | O(n) | 需要找到插入位置 |
| **删除** | O(log n) | O(n) | 需要找到删除位置 |
| **最小值** | O(log n) | O(n) | 最左节点 |
| **最大值** | O(log n) | O(n) | 最右节点 |
| **范围查询** | O(log n + k) | O(n + k) | k为结果数量 |

### 空间复杂度

| 情况 | 空间复杂度 | 说明 |
|------|------------|------|
| **存储** | O(n) | n个节点 |
| **递归栈** | O(h) | h为树高度 |
| **最坏情况** | O(n) | 退化为链表 |

## 🎮 应用场景

### 1. 动态集合

```cpp
class DynamicSet {
private:
    BinarySearchTree<int> bst;
    
public:
    void insert(int value) {
        bst.insert(value);
    }
    
    void remove(int value) {
        bst.remove(value);
    }
    
    bool contains(int value) {
        return bst.search(value);
    }
    
    int getMin() {
        return bst.getMin();
    }
    
    int getMax() {
        return bst.getMax();
    }
    
    vector<int> getRange(int min, int max) {
        return bst.rangeQuery(min, max);
    }
    
    vector<int> getAllElements() {
        return bst.inorderTraversal();
    }
};
```

### 2. 优先队列

```cpp
class BSTPriorityQueue {
private:
    BinarySearchTree<int> bst;
    
public:
    void enqueue(int priority) {
        bst.insert(priority);
    }
    
    int dequeue() {
        int maxPriority = bst.getMax();
        bst.remove(maxPriority);
        return maxPriority;
    }
    
    int peek() {
        return bst.getMax();
    }
    
    bool isEmpty() {
        return bst.isEmpty();
    }
    
    int size() {
        return bst.size();
    }
};
```

## 🔗 相关链接

- [[01-二叉树基础|二叉树基础]]
- [[03-AVL树详解|AVL树]]
- [[04-红黑树原理|红黑树]]

## 💡 BST要点

1. **有序性质**：左子树 < 根 < 右子树
2. **查找效率**：平均O(log n)，最坏O(n)
3. **动态维护**：支持插入、删除、查找
4. **应用广泛**：动态集合、优先队列、范围查询

---

*📝 实现提示：BST是平衡树的基础，掌握其实现有助于理解更复杂的树结构*
