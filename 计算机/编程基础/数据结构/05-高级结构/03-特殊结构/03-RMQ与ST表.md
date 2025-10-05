# RMQ与ST表

## 📖 核心概念

**RMQ（Range Minimum Query）**是区间最值查询问题，**ST表（Sparse Table）**是解决RMQ问题的高效数据结构。ST表通过预处理实现O(1)的区间查询，但需要O(n log n)的预处理时间。

### 🏗️ RMQ与ST表结构

```mermaid
graph TD
    A[RMQ与ST表] --> B[RMQ问题]
    A --> C[ST表结构]
    A --> D[预处理算法]
    A --> E[查询算法]
    
    B --> B1[区间最小值查询]
    B --> B2[区间最大值查询]
    B --> B3[静态数组查询]
    
    C --> C1[二维数组存储]
    C --> C2[稀疏表结构]
    C --> C3[对数级别空间]
    
    D --> D1[动态规划预处理]
    D --> D2[O(n log n)时间]
    D --> D3[O(n log n)空间]
    
    E --> E1[O(1)查询时间]
    E --> E2[区间重叠查询]
    E --> E3[幂次长度查询]
```

## 🔧 RMQ与ST表实现

### 基础ST表

```cpp
class SparseTable {
private:
    vector<vector<int>> st;
    vector<int> log2;
    int n;
    
    // 计算对数
    void precomputeLog2() {
        log2.resize(n + 1);
        log2[1] = 0;
        for (int i = 2; i <= n; i++) {
            log2[i] = log2[i / 2] + 1;
        }
    }
    
public:
    SparseTable(const vector<int>& arr) : n(arr.size()) {
        int maxLog = log2[n] + 1;
        st.resize(n, vector<int>(maxLog));
        
        // 初始化第一列
        for (int i = 0; i < n; i++) {
            st[i][0] = arr[i];
        }
        
        // 预处理
        for (int j = 1; j < maxLog; j++) {
            for (int i = 0; i + (1 << j) <= n; i++) {
                st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
        
        precomputeLog2();
    }
    
    // RMQ查询
    int query(int left, int right) {
        int length = right - left + 1;
        int k = log2[length];
        return min(st[left][k], st[right - (1 << k) + 1][k]);
    }
    
    // 显示ST表
    void display() {
        cout << "Sparse Table:" << endl;
        cout << "============" << endl;
        
        for (int i = 0; i < n; i++) {
            cout << "Row " << i << ": ";
            for (int j = 0; j < st[i].size(); j++) {
                cout << st[i][j] << " ";
            }
            cout << endl;
        }
    }
    
    // 显示统计信息
    void displayStats() {
        cout << "Sparse Table Statistics:" << endl;
        cout << "======================" << endl;
        
        cout << "Array size: " << n << endl;
        cout << "Max log: " << log2[n] + 1 << endl;
        cout << "Space complexity: O(n log n)" << endl;
        cout << "Query time: O(1)" << endl;
    }
};
```

### 高级ST表

```cpp
class AdvancedSparseTable {
private:
    vector<vector<int>> st;
    vector<int> log2;
    int n;
    bool isMinQuery;
    
    // 计算对数
    void precomputeLog2() {
        log2.resize(n + 1);
        log2[1] = 0;
        for (int i = 2; i <= n; i++) {
            log2[i] = log2[i / 2] + 1;
        }
    }
    
    // 比较函数
    int compare(int a, int b) {
        return isMinQuery ? min(a, b) : max(a, b);
    }
    
public:
    AdvancedSparseTable(const vector<int>& arr, bool minQuery = true) 
        : n(arr.size()), isMinQuery(minQuery) {
        int maxLog = log2[n] + 1;
        st.resize(n, vector<int>(maxLog));
        
        // 初始化第一列
        for (int i = 0; i < n; i++) {
            st[i][0] = arr[i];
        }
        
        // 预处理
        for (int j = 1; j < maxLog; j++) {
            for (int i = 0; i + (1 << j) <= n; i++) {
                st[i][j] = compare(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
        
        precomputeLog2();
    }
    
    // RMQ查询
    int query(int left, int right) {
        int length = right - left + 1;
        int k = log2[length];
        return compare(st[left][k], st[right - (1 << k) + 1][k]);
    }
    
    // 范围查询
    vector<int> rangeQuery(int left, int right) {
        vector<int> result;
        int length = right - left + 1;
        int k = log2[length];
        
        result.push_back(compare(st[left][k], st[right - (1 << k) + 1][k]));
        return result;
    }
    
    // 显示ST表
    void display() {
        cout << "Advanced Sparse Table:" << endl;
        cout << "====================" << endl;
        
        cout << "Query type: " << (isMinQuery ? "Minimum" : "Maximum") << endl;
        
        for (int i = 0; i < n; i++) {
            cout << "Row " << i << ": ";
            for (int j = 0; j < st[i].size(); j++) {
                cout << st[i][j] << " ";
            }
            cout << endl;
        }
    }
    
    // 显示统计信息
    void displayStats() {
        cout << "Advanced Sparse Table Statistics:" << endl;
        cout << "===============================" << endl;
        
        cout << "Array size: " << n << endl;
        cout << "Max log: " << log2[n] + 1 << endl;
        cout << "Query type: " << (isMinQuery ? "Minimum" : "Maximum") << endl;
        cout << "Space complexity: O(n log n)" << endl;
        cout << "Query time: O(1)" << endl;
    }
};
```

### RMQ工具类

```cpp
class RMQUtils {
public:
    // 性能测试
    static void performanceTest(SparseTable& st, vector<pair<int, int>>& queries) {
        cout << "RMQ Performance Test:" << endl;
        cout << "====================" << endl;
        
        // 查询测试
        auto start = chrono::high_resolution_clock::now();
        for (auto& query : queries) {
            st.query(query.first, query.second);
        }
        auto end = chrono::high_resolution_clock::now();
        auto queryTime = chrono::duration_cast<chrono::microseconds>(end - start);
        
        cout << "Query time: " << queryTime.count() << " microseconds" << endl;
        cout << "Number of queries: " << queries.size() << endl;
        cout << "Average query time: " << (double)queryTime.count() / queries.size() << " microseconds" << endl;
    }
    
    // 内存使用分析
    static void memoryAnalysis(SparseTable& st) {
        cout << "RMQ Memory Analysis:" << endl;
        cout << "==================" << endl;
        
        int totalElements = 0;
        for (int i = 0; i < st.st.size(); i++) {
            totalElements += st.st[i].size();
        }
        
        cout << "Total elements: " << totalElements << endl;
        cout << "Memory per element: " << sizeof(int) << " bytes" << endl;
        cout << "Total memory: " << totalElements * sizeof(int) << " bytes" << endl;
        cout << "Space complexity: O(n log n)" << endl;
    }
    
    // 查询分析
    static void queryAnalysis(SparseTable& st, vector<pair<int, int>>& queries) {
        cout << "RMQ Query Analysis:" << endl;
        cout << "=================" << endl;
        
        map<int, int> lengthCount;
        for (auto& query : queries) {
            int length = query.second - query.first + 1;
            lengthCount[length]++;
        }
        
        cout << "Query length distribution:" << endl;
        for (auto& pair : lengthCount) {
            cout << "Length " << pair.first << ": " << pair.second << " queries" << endl;
        }
    }
    
    // 显示RMQ可视化
    static void visualizeRMQ(SparseTable& st, vector<int>& arr) {
        cout << "RMQ Visualization:" << endl;
        cout << "================" << endl;
        
        cout << "Array: ";
        for (int i = 0; i < arr.size(); i++) {
            cout << arr[i] << " ";
        }
        cout << endl;
        
        cout << "Sparse Table:" << endl;
        st.display();
    }
    
    // 比较不同实现
    static void compareImplementations() {
        cout << "RMQ Implementation Comparison:" << endl;
        cout << "============================" << endl;
        
        cout << "1. Sparse Table:" << endl;
        cout << "   - Preprocessing: O(n log n)" << endl;
        cout << "   - Query: O(1)" << endl;
        cout << "   - Space: O(n log n)" << endl;
        cout << "   - Best for: Static arrays" << endl;
        cout << endl;
        
        cout << "2. Segment Tree:" << endl;
        cout << "   - Preprocessing: O(n)" << endl;
        cout << "   - Query: O(log n)" << endl;
        cout << "   - Space: O(n)" << endl;
        cout << "   - Best for: Dynamic arrays" << endl;
        cout << endl;
        
        cout << "3. Square Root Decomposition:" << endl;
        cout << "   - Preprocessing: O(n)" << endl;
        cout << "   - Query: O(sqrt n)" << endl;
        cout << "   - Space: O(sqrt n)" << endl;
        cout << "   - Best for: Simple queries" << endl;
    }
};
```

## 🎯 RMQ应用

### 实际应用场景

```cpp
class RMQApplications {
public:
    static void demonstrateApplications() {
        cout << "RMQ Applications:" << endl;
        cout << "===============" << endl;
        
        cout << "1. 数组查询:" << endl;
        cout << "   - 区间最小值查询" << endl;
        cout << "   - 区间最大值查询" << endl;
        cout << "   - 区间统计查询" << endl;
        
        cout << "2. 数据库优化:" << endl;
        cout << "   - 索引优化" << endl;
        cout << "   - 查询优化" << endl;
        cout << "   - 统计查询" << endl;
        
        cout << "3. 算法竞赛:" << endl;
        cout << "   - 区间查询问题" << endl;
        cout << "   - 动态规划优化" << endl;
        cout << "   - 数据结构问题" << endl;
        
        cout << "4. 系统优化:" << endl;
        cout << "   - 性能监控" << endl;
        cout << "   - 资源管理" << endl;
        cout << "   - 负载均衡" << endl;
    }
    
    static void analyzePerformance() {
        cout << "RMQ Performance Analysis:" << endl;
        cout << "=======================" << endl;
        
        cout << "1. 时间复杂度:" << endl;
        cout << "   - 预处理: O(n log n)" << endl;
        cout << "   - 查询: O(1)" << endl;
        cout << "   - 更新: 不支持" << endl;
        
        cout << "2. 空间复杂度:" << endl;
        cout << "   - 存储: O(n log n)" << endl;
        cout << "   - 辅助: O(n)" << endl;
        cout << "   - 总空间: O(n log n)" << endl;
        
        cout << "3. 优势:" << endl;
        cout << "   - 查询速度快" << endl;
        cout << "   - 实现简单" << endl;
        cout << "   - 适合静态数据" << endl;
    }
    
    static void selectRMQ(bool needsUpdates, bool needsRangeQueries, bool needsMemoryEfficiency) {
        cout << "RMQ Selection:" << endl;
        cout << "============" << endl;
        
        cout << "Needs updates: " << (needsUpdates ? "Yes" : "No") << endl;
        cout << "Needs range queries: " << (needsRangeQueries ? "Yes" : "No") << endl;
        cout << "Needs memory efficiency: " << (needsMemoryEfficiency ? "Yes" : "No") << endl;
        
        cout << "Recommendation:" << endl;
        
        if (needsUpdates) {
            cout << "Use Segment Tree (supports updates)" << endl;
        } else if (needsRangeQueries) {
            cout << "Use Sparse Table (fast range queries)" << endl;
        } else if (needsMemoryEfficiency) {
            cout << "Use Square Root Decomposition (memory efficient)" << endl;
        } else {
            cout << "Use Sparse Table (simple and fast)" << endl;
        }
    }
};
```

## 📊 RMQ分析

### 性能分析

```cpp
class RMQAnalysis {
public:
    static void analyzePerformance() {
        cout << "RMQ Performance Analysis:" << endl;
        cout << "=======================" << endl;
        
        cout << "1. 时间复杂度:" << endl;
        cout << "   - 预处理: O(n log n)" << endl;
        cout << "   - 查询: O(1)" << endl;
        cout << "   - 更新: 不支持" << endl;
        
        cout << "2. 空间复杂度:" << endl;
        cout << "   - 存储: O(n log n)" << endl;
        cout << "   - 辅助: O(n)" << endl;
        cout << "   - 总空间: O(n log n)" << endl;
        
        cout << "3. 算法特性:" << endl;
        cout << "   - 静态数据结构" << endl;
        cout << "   - 不支持更新" << endl;
        cout << "   - 查询速度快" << endl;
    }
    
    static void analyzeSpaceComplexity() {
        cout << "RMQ Space Complexity Analysis:" << endl;
        cout << "============================" << endl;
        
        cout << "1. 稀疏表:" << endl;
        cout << "   - 存储: O(n log n)" << endl;
        cout << "   - 对数表: O(n)" << endl;
        cout << "   - 总空间: O(n log n)" << endl;
        
        cout << "2. 空间优化:" << endl;
        cout << "   - 使用位运算" << endl;
        cout << "   - 压缩存储" << endl;
        cout << "   - 延迟计算" << endl;
        
        cout << "3. 内存效率:" << endl;
        cout << "   - 比线段树节省空间" << endl;
        cout << "   - 比平方根分解节省空间" << endl;
        cout << "   - 适合大数据集" << endl;
    }
    
    static void analyzeTimeComplexity() {
        cout << "RMQ Time Complexity Analysis:" << endl;
        cout << "============================" << endl;
        
        cout << "1. 预处理阶段:" << endl;
        cout << "   - 初始化: O(n)" << endl;
        cout << "   - 动态规划: O(n log n)" << endl;
        cout << "   - 对数计算: O(n)" << endl;
        
        cout << "2. 查询阶段:" << endl;
        cout << "   - 计算长度: O(1)" << endl;
        cout << "   - 查找对数: O(1)" << endl;
        cout << "   - 比较值: O(1)" << endl;
        
        cout << "3. 总体性能:" << endl;
        cout << "   - 预处理: O(n log n)" << endl;
        cout << "   - 查询: O(1)" << endl;
        cout << "   - 适合大量查询" << endl;
    }
};
```

## 🎮 RMQ测试

### 1. 基础功能测试

```cpp
class RMQTest {
public:
    static void testBasicSparseTable() {
        cout << "Testing Basic Sparse Table:" << endl;
        cout << "=========================" << endl;
        
        vector<int> arr = {1, 3, 2, 7, 9, 11, 4, 6, 8, 10};
        SparseTable st(arr);
        
        st.display();
        st.displayStats();
        
        // 查询测试
        cout << "Query [0, 4]: " << st.query(0, 4) << endl;
        cout << "Query [2, 7]: " << st.query(2, 7) << endl;
        cout << "Query [5, 9]: " << st.query(5, 9) << endl;
    }
    
    static void testAdvancedSparseTable() {
        cout << "Testing Advanced Sparse Table:" << endl;
        cout << "============================" << endl;
        
        vector<int> arr = {1, 3, 2, 7, 9, 11, 4, 6, 8, 10};
        
        // 最小值查询
        AdvancedSparseTable minSt(arr, true);
        cout << "Minimum query [0, 4]: " << minSt.query(0, 4) << endl;
        
        // 最大值查询
        AdvancedSparseTable maxSt(arr, false);
        cout << "Maximum query [0, 4]: " << maxSt.query(0, 4) << endl;
        
        minSt.display();
        maxSt.display();
    }
    
    static void testUtils() {
        cout << "Testing RMQ Utils:" << endl;
        cout << "================" << endl;
        
        vector<int> arr = {1, 3, 2, 7, 9, 11, 4, 6, 8, 10};
        SparseTable st(arr);
        
        vector<pair<int, int>> queries = {{0, 4}, {2, 7}, {5, 9}};
        
        // 性能测试
        RMQUtils::performanceTest(st, queries);
        
        // 内存分析
        RMQUtils::memoryAnalysis(st);
        
        // 查询分析
        RMQUtils::queryAnalysis(st, queries);
        
        // 可视化
        RMQUtils::visualizeRMQ(st, arr);
        
        // 实现比较
        RMQUtils::compareImplementations();
    }
    
    static void testApplications() {
        cout << "Testing Applications:" << endl;
        cout << "==================" << endl;
        
        RMQApplications::demonstrateApplications();
        RMQApplications::analyzePerformance();
        RMQApplications::selectRMQ(false, true, false);
    }
    
    static void testAnalysis() {
        cout << "Testing Analysis:" << endl;
        cout << "===============" << endl;
        
        RMQAnalysis::analyzePerformance();
        RMQAnalysis::analyzeSpaceComplexity();
        RMQAnalysis::analyzeTimeComplexity();
    }
};
```

## 🔗 相关链接

- [[01-特殊结构|特殊结构]]
- [[02-跳表详解|跳表详解]]
- [[03-字典树Trie|字典树Trie]]

## 💡 RMQ与ST表要点

1. **预处理**: O(n log n)时间构建稀疏表
2. **查询**: O(1)时间进行区间查询
3. **空间**: O(n log n)空间存储稀疏表
4. **应用**: 适合静态数组的区间查询

---

*📝 RMQ与ST表提示：ST表是解决RMQ问题的高效数据结构，通过预处理实现O(1)查询*
