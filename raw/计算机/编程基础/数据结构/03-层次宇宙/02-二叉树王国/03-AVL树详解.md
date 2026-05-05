# AVL树详解

## 📖 核心概念

**AVL树**是一种自平衡的二叉搜索树，通过维护每个节点的平衡因子来确保树的高度始终保持在O(log n)范围内。AVL树是Adelson-Velskii和Landis在1962年发明的。

### 🏗️ AVL树特征

```mermaid
graph TD
    A[AVL树] --> B[平衡因子]
    A --> C[旋转操作]
    A --> D[插入删除]
    
    B --> B1[左子树高度 - 右子树高度]
    B --> B2[平衡因子 ∈ {-1, 0, 1}]
    
    C --> C1[左旋转]
    C --> C2[右旋转]
    C --> C3[左右旋转]
    C --> C4[右左旋转]
    
    D --> D1[插入后检查平衡]
    D --> D2[删除后检查平衡]
```

## 🔧 AVL树实现

### AVL树节点

```cpp
class AVLNode {
public:
    int key;
    int height;
    AVLNode* left;
    AVLNode* right;
    
    AVLNode(int k) : key(k), height(1), left(nullptr), right(nullptr) {}
};

class AVLTree {
private:
    AVLNode* root;
    
    // 获取节点高度
    int getHeight(AVLNode* node) {
        return node ? node->height : 0;
    }
    
    // 更新节点高度
    void updateHeight(AVLNode* node) {
        if (node) {
            node->height = 1 + max(getHeight(node->left), getHeight(node->right));
        }
    }
    
    // 获取平衡因子
    int getBalance(AVLNode* node) {
        return node ? getHeight(node->left) - getHeight(node->right) : 0;
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
    AVLNode* insert(AVLNode* node, int key) {
        // 1. 执行标准BST插入
        if (!node) {
            return new AVLNode(key);
        }
        
        if (key < node->key) {
            node->left = insert(node->left, key);
        } else if (key > node->key) {
            node->right = insert(node->right, key);
        } else {
            return node; // 不允许重复键
        }
        
        // 2. 更新祖先节点的高度
        updateHeight(node);
        
        // 3. 获取平衡因子
        int balance = getBalance(node);
        
        // 4. 如果不平衡，执行旋转
        // 左左情况
        if (balance > 1 && key < node->left->key) {
            return rightRotate(node);
        }
        
        // 右右情况
        if (balance < -1 && key > node->right->key) {
            return leftRotate(node);
        }
        
        // 左右情况
        if (balance > 1 && key > node->left->key) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        
        // 右左情况
        if (balance < -1 && key < node->right->key) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        
        return node;
    }
    
    // 删除节点
    AVLNode* deleteNode(AVLNode* node, int key) {
        // 1. 执行标准BST删除
        if (!node) {
            return node;
        }
        
        if (key < node->key) {
            node->left = deleteNode(node->left, key);
        } else if (key > node->key) {
            node->right = deleteNode(node->right, key);
        } else {
            // 要删除的节点
            if (!node->left || !node->right) {
                AVLNode* temp = node->left ? node->left : node->right;
                
                if (!temp) {
                    temp = node;
                    node = nullptr;
                } else {
                    *node = *temp;
                }
                delete temp;
            } else {
                AVLNode* temp = getMinValueNode(node->right);
                node->key = temp->key;
                node->right = deleteNode(node->right, temp->key);
            }
        }
        
        if (!node) {
            return node;
        }
        
        // 2. 更新高度
        updateHeight(node);
        
        // 3. 获取平衡因子
        int balance = getBalance(node);
        
        // 4. 如果不平衡，执行旋转
        // 左左情况
        if (balance > 1 && getBalance(node->left) >= 0) {
            return rightRotate(node);
        }
        
        // 左右情况
        if (balance > 1 && getBalance(node->left) < 0) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        
        // 右右情况
        if (balance < -1 && getBalance(node->right) <= 0) {
            return leftRotate(node);
        }
        
        // 右左情况
        if (balance < -1 && getBalance(node->right) > 0) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        
        return node;
    }
    
    // 获取最小值的节点
    AVLNode* getMinValueNode(AVLNode* node) {
        while (node->left) {
            node = node->left;
        }
        return node;
    }
    
    // 搜索节点
    AVLNode* search(AVLNode* node, int key) {
        if (!node || node->key == key) {
            return node;
        }
        
        if (key < node->key) {
            return search(node->left, key);
        } else {
            return search(node->right, key);
        }
    }
    
    // 中序遍历
    void inorderTraversal(AVLNode* node) {
        if (node) {
            inorderTraversal(node->left);
            cout << node->key << " ";
            inorderTraversal(node->right);
        }
    }
    
    // 前序遍历
    void preorderTraversal(AVLNode* node) {
        if (node) {
            cout << node->key << " ";
            preorderTraversal(node->left);
            preorderTraversal(node->right);
        }
    }
    
    // 后序遍历
    void postorderTraversal(AVLNode* node) {
        if (node) {
            postorderTraversal(node->left);
            postorderTraversal(node->right);
            cout << node->key << " ";
        }
    }
    
    // 计算树的高度
    int calculateHeight(AVLNode* node) {
        if (!node) {
            return 0;
        }
        
        int leftHeight = calculateHeight(node->left);
        int rightHeight = calculateHeight(node->right);
        
        return 1 + max(leftHeight, rightHeight);
    }
    
    // 检查是否为AVL树
    bool isAVLTree(AVLNode* node) {
        if (!node) {
            return true;
        }
        
        int balance = getBalance(node);
        if (abs(balance) > 1) {
            return false;
        }
        
        return isAVLTree(node->left) && isAVLTree(node->right);
    }
    
public:
    AVLTree() : root(nullptr) {}
    
    void insert(int key) {
        root = insert(root, key);
    }
    
    void deleteNode(int key) {
        root = deleteNode(root, key);
    }
    
    bool search(int key) {
        return search(root, key) != nullptr;
    }
    
    void displayInorder() {
        cout << "Inorder traversal: ";
        inorderTraversal(root);
        cout << endl;
    }
    
    void displayPreorder() {
        cout << "Preorder traversal: ";
        preorderTraversal(root);
        cout << endl;
    }
    
    void displayPostorder() {
        cout << "Postorder traversal: ";
        postorderTraversal(root);
        cout << endl;
    }
    
    int getHeight() {
        return calculateHeight(root);
    }
    
    bool isBalanced() {
        return isAVLTree(root);
    }
    
    void displayTree() {
        cout << "AVL Tree:" << endl;
        displayTreeHelper(root, 0);
    }
    
private:
    void displayTreeHelper(AVLNode* node, int level) {
        if (node) {
            displayTreeHelper(node->right, level + 1);
            
            for (int i = 0; i < level; ++i) {
                cout << "    ";
            }
            
            cout << node->key << " (h:" << node->height << ", b:" << getBalance(node) << ")" << endl;
            
            displayTreeHelper(node->left, level + 1);
        }
    }
};
```

## 🎯 AVL树应用

### 动态集合操作

```cpp
class DynamicSet {
private:
    AVLTree avlTree;
    
public:
    void insert(int key) {
        avlTree.insert(key);
        cout << "Inserted " << key << endl;
    }
    
    void remove(int key) {
        if (avlTree.search(key)) {
            avlTree.deleteNode(key);
            cout << "Removed " << key << endl;
        } else {
            cout << "Key " << key << " not found" << endl;
        }
    }
    
    bool contains(int key) {
        return avlTree.search(key);
    }
    
    void displaySet() {
        cout << "Dynamic Set Contents:" << endl;
        avlTree.displayInorder();
    }
    
    void displayTreeStructure() {
        avlTree.displayTree();
    }
    
    int getSize() {
        return avlTree.getHeight();
    }
    
    bool isBalanced() {
        return avlTree.isBalanced();
    }
};
```

### 范围查询

```cpp
class RangeQuery {
private:
    AVLTree avlTree;
    
    void rangeQueryHelper(AVLNode* node, int low, int high, vector<int>& result) {
        if (!node) return;
        
        if (node->key > low) {
            rangeQueryHelper(node->left, low, high, result);
        }
        
        if (node->key >= low && node->key <= high) {
            result.push_back(node->key);
        }
        
        if (node->key < high) {
            rangeQueryHelper(node->right, low, high, result);
        }
    }
    
public:
    void insert(int key) {
        avlTree.insert(key);
    }
    
    vector<int> rangeQuery(int low, int high) {
        vector<int> result;
        rangeQueryHelper(avlTree.root, low, high, result);
        return result;
    }
    
    void displayRangeQuery(int low, int high) {
        vector<int> result = rangeQuery(low, high);
        
        cout << "Range query [" << low << ", " << high << "]: ";
        for (int key : result) {
            cout << key << " ";
        }
        cout << endl;
    }
    
    int countInRange(int low, int high) {
        vector<int> result = rangeQuery(low, high);
        return result.size();
    }
    
    int findKthSmallest(int k) {
        vector<int> result;
        rangeQueryHelper(avlTree.root, INT_MIN, INT_MAX, result);
        
        if (k > 0 && k <= result.size()) {
            return result[k - 1];
        }
        
        return -1; // 无效的k
    }
    
    void displayKthSmallest(int k) {
        int result = findKthSmallest(k);
        if (result != -1) {
            cout << k << "th smallest element: " << result << endl;
        } else {
            cout << "Invalid k value" << endl;
        }
    }
};
```

## 📊 AVL树分析

### 时间复杂度分析

```cpp
class AVLAnalysis {
public:
    static void analyzeTimeComplexity() {
        cout << "AVL Tree Time Complexity Analysis:" << endl;
        cout << "=================================" << endl;
        
        cout << "1. Search Operation:" << endl;
        cout << "   - Time Complexity: O(log n)" << endl;
        cout << "   - Space Complexity: O(1)" << endl;
        cout << "   - Height is always O(log n)" << endl;
        
        cout << "2. Insert Operation:" << endl;
        cout << "   - Time Complexity: O(log n)" << endl;
        cout << "   - Space Complexity: O(log n)" << endl;
        cout << "   - Includes rotation operations" << endl;
        
        cout << "3. Delete Operation:" << endl;
        cout << "   - Time Complexity: O(log n)" << endl;
        cout << "   - Space Complexity: O(log n)" << endl;
        cout << "   - Includes rotation operations" << endl;
        
        cout << "4. Rotation Operations:" << endl;
        cout << "   - Time Complexity: O(1)" << endl;
        cout << "   - Space Complexity: O(1)" << endl;
        cout << "   - Constant time operations" << endl;
        
        cout << "5. Traversal Operations:" << endl;
        cout << "   - Time Complexity: O(n)" << endl;
        cout << "   - Space Complexity: O(log n)" << endl;
        cout << "   - Visit every node once" << endl;
    }
    
    static void analyzeSpaceComplexity() {
        cout << "AVL Tree Space Complexity Analysis:" << endl;
        cout << "==================================" << endl;
        
        cout << "1. Node Storage:" << endl;
        cout << "   - Each node stores: key, height, left, right pointers" << endl;
        cout << "   - Space per node: O(1)" << endl;
        cout << "   - Total nodes: O(n)" << endl;
        
        cout << "2. Height Information:" << endl;
        cout << "   - Height stored in each node" << endl;
        cout << "   - Additional space: O(n)" << endl;
        
        cout << "3. Recursion Stack:" << endl;
        cout << "   - Maximum depth: O(log n)" << endl;
        cout << "   - Stack space: O(log n)" << endl;
        
        cout << "4. Total Space Complexity:" << endl;
        cout << "   - O(n) for node storage" << endl;
        cout << "   - O(log n) for recursion stack" << endl;
        cout << "   - Overall: O(n)" << endl;
    }
};
```

### 性能测试

```cpp
class AVLPerformanceTest {
public:
    static void performanceTest() {
        cout << "AVL Tree Performance Test:" << endl;
        cout << "=========================" << endl;
        
        vector<int> sizes = {1000, 5000, 10000};
        
        for (int size : sizes) {
            cout << "Testing with " << size << " elements:" << endl;
            
            AVLTree avlTree;
            
            // 测试插入性能
            auto start = chrono::high_resolution_clock::now();
            for (int i = 0; i < size; ++i) {
                avlTree.insert(rand() % 10000);
            }
            auto end = chrono::high_resolution_clock::now();
            auto insertTime = chrono::duration_cast<chrono::milliseconds>(end - start);
            
            cout << "Insert time: " << insertTime.count() << " ms" << endl;
            cout << "Tree height: " << avlTree.getHeight() << endl;
            cout << "Is balanced: " << (avlTree.isBalanced() ? "Yes" : "No") << endl;
            
            // 测试搜索性能
            start = chrono::high_resolution_clock::now();
            for (int i = 0; i < 1000; ++i) {
                avlTree.search(rand() % 10000);
            }
            end = chrono::high_resolution_clock::now();
            auto searchTime = chrono::duration_cast<chrono::milliseconds>(end - start);
            
            cout << "Search time (1000 operations): " << searchTime.count() << " ms" << endl;
            cout << endl;
        }
    }
};
```

## 🎮 AVL树测试

### 1. 基础功能测试

```cpp
class AVLTest {
public:
    static void testBasicOperations() {
        cout << "Testing AVL Tree Basic Operations:" << endl;
        cout << "=================================" << endl;
        
        AVLTree avlTree;
        
        // 测试插入
        vector<int> keys = {10, 20, 30, 40, 50, 25};
        for (int key : keys) {
            avlTree.insert(key);
            cout << "Inserted " << key << endl;
        }
        
        cout << endl;
        avlTree.displayTree();
        cout << endl;
        
        // 测试遍历
        avlTree.displayInorder();
        avlTree.displayPreorder();
        avlTree.displayPostorder();
        
        // 测试搜索
        cout << "Search 30: " << (avlTree.search(30) ? "Found" : "Not found") << endl;
        cout << "Search 35: " << (avlTree.search(35) ? "Found" : "Not found") << endl;
        
        // 测试删除
        cout << "Deleting 20..." << endl;
        avlTree.deleteNode(20);
        avlTree.displayTree();
    }
    
    static void testDynamicSet() {
        cout << "Testing Dynamic Set:" << endl;
        cout << "===================" << endl;
        
        DynamicSet dynamicSet;
        
        vector<int> keys = {5, 10, 15, 20, 25, 30, 35, 40};
        for (int key : keys) {
            dynamicSet.insert(key);
        }
        
        dynamicSet.displaySet();
        dynamicSet.displayTreeStructure();
        
        cout << "Is balanced: " << (dynamicSet.isBalanced() ? "Yes" : "No") << endl;
        
        dynamicSet.remove(20);
        dynamicSet.displaySet();
    }
    
    static void testRangeQuery() {
        cout << "Testing Range Query:" << endl;
        cout << "===================" << endl;
        
        RangeQuery rangeQuery;
        
        vector<int> keys = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        for (int key : keys) {
            rangeQuery.insert(key);
        }
        
        rangeQuery.displayRangeQuery(25, 75);
        rangeQuery.displayRangeQuery(15, 35);
        rangeQuery.displayRangeQuery(5, 15);
        
        rangeQuery.displayKthSmallest(3);
        rangeQuery.displayKthSmallest(7);
    }
    
    static void testRotationCases() {
        cout << "Testing Rotation Cases:" << endl;
        cout << "======================" << endl;
        
        AVLTree avlTree;
        
        // 测试左左情况
        cout << "Testing Left-Left case:" << endl;
        avlTree.insert(30);
        avlTree.insert(20);
        avlTree.insert(10);
        avlTree.displayTree();
        
        // 测试右右情况
        cout << "Testing Right-Right case:" << endl;
        AVLTree avlTree2;
        avlTree2.insert(10);
        avlTree2.insert(20);
        avlTree2.insert(30);
        avlTree2.displayTree();
        
        // 测试左右情况
        cout << "Testing Left-Right case:" << endl;
        AVLTree avlTree3;
        avlTree3.insert(30);
        avlTree3.insert(10);
        avlTree3.insert(20);
        avlTree3.displayTree();
        
        // 测试右左情况
        cout << "Testing Right-Left case:" << endl;
        AVLTree avlTree4;
        avlTree4.insert(10);
        avlTree4.insert(30);
        avlTree4.insert(20);
        avlTree4.displayTree();
    }
};
```

## 🔗 相关链接

- [[01-二叉树基础|二叉树基础]]
- [[02-二叉搜索树|二叉搜索树]]
- [[04-红黑树详解|红黑树详解]]

## 💡 AVL树要点

1. **平衡因子**: 左子树高度 - 右子树高度
2. **旋转操作**: 四种旋转情况保持平衡
3. **时间复杂度**: 所有操作都是O(log n)
4. **应用场景**: 需要频繁插入删除的有序集合

---

*📝 AVL提示：AVL树是自平衡二叉搜索树的重要实现，掌握旋转操作是关键*
