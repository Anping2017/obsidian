# AVL树详解

## 📖 核心概念

**AVL树**是一种自平衡二叉搜索树，通过维护平衡因子来保证树的高度平衡。AVL树保证任何节点的左右子树高度差不超过1，从而确保O(log n)的查找、插入和删除操作。

### 🏗️ AVL树特性

```mermaid
graph TD
    A[AVL树] --> B[平衡因子]
    A --> C[旋转操作]
    A --> D[插入删除]
    A --> E[性能保证]
    
    B --> B1[左子树高度-右子树高度]
    B --> B2[范围-1到1]
    B --> B3[自动维护]
    
    C --> C1[左旋转]
    C --> C2[右旋转]
    C --> C3[左右旋转]
    C --> C4[右左旋转]
    
    D --> D1[插入后平衡]
    D --> D2[删除后平衡]
    D --> D3[递归调整]
    
    E --> E1[O(log n)操作]
    E --> E2[高度平衡]
    E --> E3[稳定性能]
```

## 🔧 AVL树实现

### 基础AVL树类

```cpp
template<typename T>
class AVLTree {
private:
    struct AVLNode {
        T data;
        int height;
        AVLNode* left;
        AVLNode* right;
        
        AVLNode(const T& value) 
            : data(value), height(1), left(nullptr), right(nullptr) {}
    };
    
    AVLNode* root;
    
    // 获取节点高度
    int getHeight(AVLNode* node) const {
        return node ? node->height : 0;
    }
    
    // 更新节点高度
    void updateHeight(AVLNode* node) {
        if (node) {
            node->height = 1 + max(getHeight(node->left), getHeight(node->right));
        }
    }
    
    // 获取平衡因子
    int getBalanceFactor(AVLNode* node) const {
        if (!node) return 0;
        return getHeight(node->left) - getHeight(node->right);
    }
    
    // 右旋转
    AVLNode* rightRotate(AVLNode* y) {
        AVLNode* x = y->left;
        AVLNode* T2 = x->right;
        
        // 执行旋转
        x->right = y;
        y->left = T2;
        
        // 更新高度
        updateHeight(y);
        updateHeight(x);
        
        return x;
    }
    
    // 左旋转
    AVLNode* leftRotate(AVLNode* x) {
        AVLNode* y = x->right;
        AVLNode* T2 = y->left;
        
        // 执行旋转
        y->left = x;
        x->right = T2;
        
        // 更新高度
        updateHeight(x);
        updateHeight(y);
        
        return y;
    }
    
    // 插入节点
    AVLNode* insertHelper(AVLNode* node, const T& value) {
        // 1. 执行标准BST插入
        if (!node) {
            return new AVLNode(value);
        }
        
        if (value < node->data) {
            node->left = insertHelper(node->left, value);
        } else if (value > node->data) {
            node->right = insertHelper(node->right, value);
        } else {
            return node;  // 不允许重复值
        }
        
        // 2. 更新祖先节点的高度
        updateHeight(node);
        
        // 3. 获取平衡因子
        int balance = getBalanceFactor(node);
        
        // 4. 如果不平衡，执行旋转
        // Left Left Case
        if (balance > 1 && value < node->left->data) {
            return rightRotate(node);
        }
        
        // Right Right Case
        if (balance < -1 && value > node->right->data) {
            return leftRotate(node);
        }
        
        // Left Right Case
        if (balance > 1 && value > node->left->data) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        
        // Right Left Case
        if (balance < -1 && value < node->right->data) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        
        return node;
    }
    
    // 删除节点
    AVLNode* deleteHelper(AVLNode* node, const T& value) {
        // 1. 执行标准BST删除
        if (!node) {
            return node;
        }
        
        if (value < node->data) {
            node->left = deleteHelper(node->left, value);
        } else if (value > node->data) {
            node->right = deleteHelper(node->right, value);
        } else {
            // 要删除的节点
            if (!node->left || !node->right) {
                AVLNode* temp = node->left ? node->left : node->right;
                
                if (!temp) {
                    // 没有子节点
                    temp = node;
                    node = nullptr;
                } else {
                    // 一个子节点
                    *node = *temp;
                }
                delete temp;
            } else {
                // 两个子节点，找到中序遍历后继
                AVLNode* temp = findMin(node->right);
                node->data = temp->data;
                node->right = deleteHelper(node->right, temp->data);
            }
        }
        
        if (!node) {
            return node;
        }
        
        // 2. 更新高度
        updateHeight(node);
        
        // 3. 获取平衡因子
        int balance = getBalanceFactor(node);
        
        // 4. 如果不平衡，执行旋转
        // Left Left Case
        if (balance > 1 && getBalanceFactor(node->left) >= 0) {
            return rightRotate(node);
        }
        
        // Left Right Case
        if (balance > 1 && getBalanceFactor(node->left) < 0) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        
        // Right Right Case
        if (balance < -1 && getBalanceFactor(node->right) <= 0) {
            return leftRotate(node);
        }
        
        // Right Left Case
        if (balance < -1 && getBalanceFactor(node->right) > 0) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        
        return node;
    }
    
    // 查找最小节点
    AVLNode* findMin(AVLNode* node) const {
        while (node && node->left) {
            node = node->left;
        }
        return node;
    }
    
    // 查找节点
    AVLNode* searchHelper(AVLNode* node, const T& value) const {
        if (!node || node->data == value) {
            return node;
        }
        
        if (value < node->data) {
            return searchHelper(node->left, value);
        } else {
            return searchHelper(node->right, value);
        }
    }
    
    // 中序遍历
    void inorderHelper(AVLNode* node, vector<T>& result) const {
        if (node) {
            inorderHelper(node->left, result);
            result.push_back(node->data);
            inorderHelper(node->right, result);
        }
    }
    
    // 清理树
    void clearHelper(AVLNode* node) {
        if (node) {
            clearHelper(node->left);
            clearHelper(node->right);
            delete node;
        }
    }
    
    // 打印树结构
    void printTreeHelper(AVLNode* node, int depth, const string& prefix) const {
        if (!node) return;
        
        printTreeHelper(node->right, depth + 1, prefix + "    ");
        
        cout << prefix;
        if (depth > 0) {
            cout << "└── ";
        }
        cout << node->data << " (h:" << node->height << ", bf:" << getBalanceFactor(node) << ")" << endl;
        
        printTreeHelper(node->left, depth + 1, prefix + "    ");
    }
    
public:
    AVLTree() : root(nullptr) {}
    
    ~AVLTree() {
        clear();
    }
    
    // 插入元素
    void insert(const T& value) {
        root = insertHelper(root, value);
    }
    
    // 删除元素
    bool remove(const T& value) {
        if (!search(value)) return false;
        root = deleteHelper(root, value);
        return true;
    }
    
    // 查找元素
    bool search(const T& value) const {
        return searchHelper(root, value) != nullptr;
    }
    
    // 获取最小值
    T getMin() const {
        AVLNode* minNode = findMin(root);
        if (!minNode) {
            throw runtime_error("Tree is empty");
        }
        return minNode->data;
    }
    
    // 获取最大值
    T getMax() const {
        AVLNode* current = root;
        while (current && current->right) {
            current = current->right;
        }
        if (!current) {
            throw runtime_error("Tree is empty");
        }
        return current->data;
    }
    
    // 中序遍历
    vector<T> inorderTraversal() const {
        vector<T> result;
        inorderHelper(root, result);
        return result;
    }
    
    // 获取树高度
    int getHeight() const {
        return getHeight(root);
    }
    
    // 检查是否为空
    bool isEmpty() const {
        return root == nullptr;
    }
    
    // 获取大小
    int size() const {
        return inorderTraversal().size();
    }
    
    // 清空树
    void clear() {
        clearHelper(root);
        root = nullptr;
    }
    
    // 验证AVL性质
    bool isValidAVL() const {
        return isValidAVLHelper(root);
    }
    
    // 打印树
    void printTree() const {
        cout << "AVL Tree Structure:" << endl;
        printTreeHelper(root, 0, "");
    }
    
private:
    bool isValidAVLHelper(AVLNode* node) const {
        if (!node) return true;
        
        int balance = getBalanceFactor(node);
        
        // 检查平衡因子
        if (balance < -1 || balance > 1) {
            return false;
        }
        
        // 递归检查子树
        return isValidAVLHelper(node->left) && isValidAVLHelper(node->right);
    }
};
```

## 🎯 旋转操作详解

### 旋转操作分析

```cpp
class AVLRotationAnalysis {
public:
    // 分析旋转操作
    void analyzeRotations() {
        cout << "AVL Tree Rotation Analysis:" << endl;
        cout << "1. Left Rotation (LL):" << endl;
        cout << "   - 当右子树比左子树高2时" << endl;
        cout << "   - 右子节点成为新的根" << endl;
        cout << "   - 原根成为新根的左子节点" << endl;
        
        cout << "2. Right Rotation (RR):" << endl;
        cout << "   - 当左子树比右子树高2时" << endl;
        cout << "   - 左子节点成为新的根" << endl;
        cout << "   - 原根成为新根的右子节点" << endl;
        
        cout << "3. Left-Right Rotation (LR):" << endl;
        cout << "   - 先对左子树执行左旋转" << endl;
        cout << "   - 再对根节点执行右旋转" << endl;
        
        cout << "4. Right-Left Rotation (RL):" << endl;
        cout << "   - 先对右子树执行右旋转" << endl;
        cout << "   - 再对根节点执行左旋转" << endl;
    }
    
    // 演示旋转操作
    void demonstrateRotations() {
        AVLTree<int> tree;
        
        cout << "Demonstrating AVL rotations:" << endl;
        
        // 演示右旋转
        cout << "\n1. Right Rotation (RR case):" << endl;
        tree.insert(30);
        tree.insert(20);
        tree.insert(10);
        tree.printTree();
        
        // 演示左旋转
        cout << "\n2. Left Rotation (LL case):" << endl;
        tree.clear();
        tree.insert(10);
        tree.insert(20);
        tree.insert(30);
        tree.printTree();
        
        // 演示左右旋转
        cout << "\n3. Left-Right Rotation (LR case):" << endl;
        tree.clear();
        tree.insert(30);
        tree.insert(10);
        tree.insert(20);
        tree.printTree();
        
        // 演示右左旋转
        cout << "\n4. Right-Left Rotation (RL case):" << endl;
        tree.clear();
        tree.insert(10);
        tree.insert(30);
        tree.insert(20);
        tree.printTree();
    }
};
```

## 📊 性能分析

### 时间复杂度分析

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| **查找** | O(log n) | 树高度保证为O(log n) |
| **插入** | O(log n) | 最多需要2次旋转 |
| **删除** | O(log n) | 最多需要2次旋转 |
| **最小值** | O(log n) | 最左节点 |
| **最大值** | O(log n) | 最右节点 |

### 空间复杂度分析

| 情况 | 空间复杂度 | 说明 |
|------|------------|------|
| **存储** | O(n) | n个节点 |
| **递归栈** | O(log n) | 树高度 |
| **额外空间** | O(1) | 高度字段 |

### 与红黑树对比

| 特性 | AVL树 | 红黑树 |
|------|-------|--------|
| **平衡性** | 严格平衡 | 近似平衡 |
| **查找性能** | 更好 | 稍差 |
| **插入删除** | 更多旋转 | 较少旋转 |
| **实现复杂度** | 中等 | 复杂 |
| **适用场景** | 查找频繁 | 插入删除频繁 |

## 🎮 应用场景

### 1. 数据库索引

```cpp
class DatabaseIndex {
private:
    AVLTree<string> index;
    map<string, vector<int>> recordMap;  // 记录ID列表
    
public:
    // 添加索引
    void addIndex(const string& key, int recordId) {
        index.insert(key);
        recordMap[key].push_back(recordId);
    }
    
    // 查找记录
    vector<int> findRecords(const string& key) {
        if (index.search(key)) {
            return recordMap[key];
        }
        return {};
    }
    
    // 范围查询
    vector<int> rangeQuery(const string& startKey, const string& endKey) {
        vector<string> allKeys = index.inorderTraversal();
        vector<int> result;
        
        for (const string& key : allKeys) {
            if (key >= startKey && key <= endKey) {
                vector<int> records = recordMap[key];
                result.insert(result.end(), records.begin(), records.end());
            }
        }
        
        return result;
    }
    
    // 删除索引
    void removeIndex(const string& key, int recordId) {
        auto it = find(recordMap[key].begin(), recordMap[key].end(), recordId);
        if (it != recordMap[key].end()) {
            recordMap[key].erase(it);
            
            if (recordMap[key].empty()) {
                index.remove(key);
                recordMap.erase(key);
            }
        }
    }
};
```

### 2. 有序集合

```cpp
class OrderedSet {
private:
    AVLTree<int> tree;
    
public:
    // 添加元素
    void add(int value) {
        tree.insert(value);
    }
    
    // 删除元素
    void remove(int value) {
        tree.remove(value);
    }
    
    // 检查元素是否存在
    bool contains(int value) {
        return tree.search(value);
    }
    
    // 获取所有元素（有序）
    vector<int> getAllElements() {
        return tree.inorderTraversal();
    }
    
    // 获取第k小元素
    int getKthSmallest(int k) {
        vector<int> elements = tree.inorderTraversal();
        if (k > 0 && k <= elements.size()) {
            return elements[k - 1];
        }
        throw runtime_error("Invalid k");
    }
    
    // 获取元素排名
    int getRank(int value) {
        vector<int> elements = tree.inorderTraversal();
        for (int i = 0; i < elements.size(); ++i) {
            if (elements[i] == value) {
                return i + 1;
            }
        }
        return -1;  // 未找到
    }
    
    // 获取大小
    int size() {
        return tree.size();
    }
    
    // 清空集合
    void clear() {
        tree.clear();
    }
};
```

## 🔧 优化技巧

### 1. 批量操作优化

```cpp
class OptimizedAVLTree {
private:
    AVLTree<int> tree;
    
public:
    // 批量插入优化
    void batchInsert(const vector<int>& values) {
        // 先排序，然后构建平衡树
        vector<int> sortedValues = values;
        sort(sortedValues.begin(), sortedValues.end());
        
        // 使用分治法构建平衡树
        root = buildBalancedTree(sortedValues, 0, sortedValues.size() - 1);
    }
    
private:
    AVLNode* buildBalancedTree(const vector<int>& values, int start, int end) {
        if (start > end) return nullptr;
        
        int mid = start + (end - start) / 2;
        AVLNode* node = new AVLNode(values[mid]);
        
        node->left = buildBalancedTree(values, start, mid - 1);
        node->right = buildBalancedTree(values, mid + 1, end);
        
        updateHeight(node);
        return node;
    }
};
```

### 2. 内存优化

```cpp
class MemoryOptimizedAVL {
private:
    // 使用内存池
    struct MemoryPool {
        vector<AVLNode> nodes;
        vector<bool> used;
        size_t nextIndex;
        
        MemoryPool(size_t size) : nextIndex(0) {
            nodes.resize(size);
            used.assign(size, false);
        }
        
        AVLNode* allocate() {
            if (nextIndex < nodes.size()) {
                used[nextIndex] = true;
                return &nodes[nextIndex++];
            }
            return nullptr;
        }
        
        void deallocate(AVLNode* node) {
            // 简化实现
        }
    };
    
    MemoryPool pool;
    
public:
    MemoryOptimizedAVL(size_t poolSize = 1000) : pool(poolSize) {}
};
```

## 🔗 相关链接

- [[01-二叉树基础|二叉树基础]]
- [[02-二叉搜索树BST|二叉搜索树]]
- [[02-红黑树详解|红黑树]]

## 💡 AVL树要点

1. **严格平衡**：保证树高度为O(log n)
2. **旋转操作**：四种旋转类型处理不平衡
3. **性能稳定**：查找性能优于红黑树
4. **实现复杂**：需要维护高度和平衡因子

---

*📝 平衡提示：AVL树是严格平衡的二叉搜索树，适合查找频繁的场景*