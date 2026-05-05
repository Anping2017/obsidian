# LALR(1)分析技术

## 🎯 LALR(1)分析概述

**LALR(1)分析**是Look-Ahead LR(1)分析的简称，它在LR(1)分析的基础上通过合并具有相同核心项目的状态来减少状态数量。LALR(1)是实际编译器中最常用的LR分析方法。

## 🔍 LALR(1)基本思想

### 核心思想
LALR(1)分析通过合并具有相同核心项目但不同向前看符号的状态来减少状态数量，同时保持LR(1)的分析能力。

### 与LR(1)的区别
- **LR(1)**：每个状态都有唯一的向前看符号集合
- **LALR(1)**：合并具有相同核心项目的状态

## 🔧 LALR(1)项目

### 项目定义
LALR(1)项目与LR(1)项目相同，但状态合并方式不同：

```c
struct LALR1Item {
    TokenType left;        // 产生式左部
    string right;          // 产生式右部
    int dotPosition;       // 圆点位置
    TokenType lookahead;   // 向前看符号
    
    LALR1Item(TokenType left, string right, int dotPosition, TokenType lookahead)
        : left(left), right(right), dotPosition(dotPosition), lookahead(lookahead) {}
    
    bool operator==(const LALR1Item& other) const {
        return left == other.left && right == other.right && 
               dotPosition == other.dotPosition && lookahead == other.lookahead;
    }
    
    bool isComplete() const {
        return dotPosition >= right.length();
    }
    
    TokenType getNextSymbol() const {
        if (dotPosition < right.length()) {
            return right[dotPosition];
        }
        return EMPTY;
    }
};
```

## 🔄 LALR(1)状态合并

### 核心项目
核心项目是去掉向前看符号的项目：

```c
struct CoreItem {
    TokenType left;
    string right;
    int dotPosition;
    
    CoreItem(TokenType left, string right, int dotPosition)
        : left(left), right(right), dotPosition(dotPosition) {}
    
    bool operator==(const CoreItem& other) const {
        return left == other.left && right == other.right && 
               dotPosition == other.dotPosition;
    }
    
    bool operator<(const CoreItem& other) const {
        if (left != other.left) return left < other.left;
        if (right != other.right) return right < other.right;
        return dotPosition < other.dotPosition;
    }
};
```

### 状态合并算法
```c
vector<LALR1ItemSet> constructLALR1ItemSets(const vector<LR1ItemSet>& lr1ItemSets) {
    // 第一步：收集所有核心项目及其向前看符号
    map<CoreItem, set<TokenType>> coreToLookaheads;
    
    for (auto& itemSet : lr1ItemSets) {
        for (auto& item : itemSet.getItems()) {
            CoreItem core(item.left, item.right, item.dotPosition);
            coreToLookaheads[core].insert(item.lookahead);
        }
    }
    
    // 第二步：构造LALR(1)项目集
    vector<LALR1ItemSet> lalr1ItemSets;
    map<CoreItem, int> coreToState;
    
    for (auto& itemSet : lr1ItemSets) {
        LALR1ItemSet newSet;
        
        for (auto& item : itemSet.getItems()) {
            CoreItem core(item.left, item.right, item.dotPosition);
            set<TokenType> lookaheads = coreToLookaheads[core];
            
            for (TokenType lookahead : lookaheads) {
                LALR1Item newItem(item.left, item.right, item.dotPosition, lookahead);
                newSet.addItem(newItem);
            }
        }
        
        lalr1ItemSets.push_back(newSet);
    }
    
    return lalr1ItemSets;
}
```

### 向前看符号传播
```c
void propagateLookaheads(vector<LALR1ItemSet>& itemSets) {
    bool changed = true;
    while (changed) {
        changed = false;
        
        for (int i = 0; i < itemSets.size(); i++) {
            LALR1ItemSet& itemSet = itemSets[i];
            
            for (auto& item : itemSet.getItems()) {
                if (!item.isComplete()) {
                    TokenType nextSymbol = item.getNextSymbol();
                    if (isNonTerminal(nextSymbol)) {
                        // 计算FIRST(βa)
                        string beta = item.right.substr(item.dotPosition + 1);
                        set<TokenType> firstBetaA = computeFirst(beta + item.lookahead);
                        
                        // 传播向前看符号
                        for (auto& targetItem : itemSet.getItems()) {
                            if (targetItem.left == nextSymbol && targetItem.dotPosition == 0) {
                                for (TokenType lookahead : firstBetaA) {
                                    if (targetItem.lookahead != lookahead) {
                                        targetItem.lookahead = lookahead;
                                        changed = true;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

## 📊 LALR(1)分析表构造

### 分析表结构
```c
class LALR1ParseTable {
private:
    map<pair<int, TokenType>, Action> actionTable;
    map<pair<int, TokenType>, int> gotoTable;
    vector<LALR1ItemSet> itemSets;
    
public:
    void constructParseTable() {
        // 构造LR(1)项目集
        vector<LR1ItemSet> lr1ItemSets = constructLR1ItemSets();
        
        // 合并为LALR(1)项目集
        itemSets = constructLALR1ItemSets(lr1ItemSets);
        
        // 传播向前看符号
        propagateLookaheads(itemSets);
        
        // 构造ACTION表
        for (int i = 0; i < itemSets.size(); i++) {
            LALR1ItemSet itemSet = itemSets[i];
            
            for (auto& item : itemSet.getItems()) {
                if (!item.isComplete()) {
                    // 移进项目
                    TokenType nextSymbol = item.getNextSymbol();
                    LALR1ItemSet nextSet = itemSet.gotoSet(nextSymbol);
                    int nextState = findItemSetIndex(nextSet, itemSets);
                    
                    if (isTerminal(nextSymbol)) {
                        actionTable[{i, nextSymbol}] = Action(Action::SHIFT, nextState);
                    } else {
                        gotoTable[{i, nextSymbol}] = nextState;
                    }
                } else {
                    // 归约项目
                    if (item.left == START_SYMBOL) {
                        actionTable[{i, END_OF_INPUT}] = Action(Action::ACCEPT);
                    } else {
                        actionTable[{i, item.lookahead}] = Action(Action::REDUCE, -1, item.left, item.right);
                    }
                }
            }
        }
    }
    
    Action getAction(int state, TokenType symbol) {
        auto it = actionTable.find({state, symbol});
        if (it != actionTable.end()) {
            return it->second;
        }
        return Action(Action::ERROR);
    }
    
    int getGoto(int state, TokenType symbol) {
        auto it = gotoTable.find({state, symbol});
        if (it != gotoTable.end()) {
            return it->second;
        }
        return -1;
    }
};
```

## 🔄 LALR(1)分析器实现

### 分析器结构
```c
class LALR1Parser {
private:
    LALR1ParseTable parseTable;
    stack<int> stateStack;
    vector<Token> input;
    int position;
    
public:
    LALR1Parser(LALR1ParseTable table, vector<Token> input) 
        : parseTable(table), input(input), position(0) {}
    
    bool parse() {
        stateStack.push(0); // 初始状态
        
        while (position < input.size()) {
            int currentState = stateStack.top();
            Token currentToken = input[position];
            
            Action action = parseTable.getAction(currentState, currentToken.type);
            
            switch (action.type) {
                case Action::SHIFT:
                    shift(action.nextState);
                    break;
                case Action::REDUCE:
                    reduce(action.left, action.right);
                    break;
                case Action::ACCEPT:
                    return true;
                case Action::ERROR:
                    error("Parse error");
                    return false;
            }
        }
        
        return false;
    }
    
    void shift(int nextState) {
        stateStack.push(nextState);
        position++;
    }
    
    void reduce(TokenType left, string right) {
        // 从栈中弹出产生式右部的状态
        for (int i = 0; i < right.length(); i++) {
            stateStack.pop();
        }
        
        // 获取归约后的状态
        int currentState = stateStack.top();
        int nextState = parseTable.getGoto(currentState, left);
        stateStack.push(nextState);
    }
    
    void error(string message) {
        cout << "Error: " << message << " at position " << position << endl;
    }
};
```

## 📈 LALR(1)分析表示例

### 简单文法
```c
// 文法：
// E → E + T | T
// T → T * F | F
// F → (E) | id

// LALR(1)项目集示例：
// I0: E' → •E, $
//     E → •E + T, $+
//     E → •T, $+
//     T → •T * F, $+*
//     T → •F, $+*
//     F → •(E), $+*
//     F → •id, $+*

// I1: E' → E•, $
//     E → E• + T, $+

// I2: E → T•, $+
//     T → T• * F, $+*
```

### 分析表
```c
// ACTION表：
//      id    +    *    (    )    $
// I0   s5    -    -    s4   -    -
// I1   -     s6   -    -    -    acc
// I2   -     r2   s7   -    r2   r2
// I3   -     r4   r4   -    r4   r4
// I4   s5    -    -    s4   -    -
// I5   -     r6   r6   -    r6   r6
// I6   s5    -    -    s4   -    -
// I7   s5    -    -    s4   -    -
// I8   -     s6   -    -    s11  -
// I9   -     r1   s7   -    r1   r1
// I10  -     r3   r3   -    r3   r3
// I11  -     r5   r5   -    r5   r5

// GOTO表：
//      E    T    F
// I0   I1   I2   I3
// I4   I8   I2   I3
// I6   -    I9   I3
// I7   -    -    I10
```

## 🎯 LALR(1)分析特点

### 优点
- **状态数量**：比LR(1)少得多
- **表达能力**：与LR(1)相同
- **实用性强**：实际编译器广泛使用
- **效率高**：分析效率高

### 缺点
- **实现复杂**：实现相对复杂
- **向前看传播**：需要传播向前看符号
- **冲突检测**：需要检测合并冲突

## 🔧 冲突检测

### 合并冲突
当合并状态时可能产生冲突：

```c
bool hasMergeConflict(const LALR1ItemSet& itemSet) {
    map<TokenType, Action> actions;
    
    for (auto& item : itemSet.getItems()) {
        if (item.isComplete()) {
            TokenType lookahead = item.lookahead;
            Action action(Action::REDUCE, -1, item.left, item.right);
            
            if (actions.find(lookahead) != actions.end()) {
                // 发现冲突
                return true;
            }
            actions[lookahead] = action;
        }
    }
    
    return false;
}
```

### 冲突解决
```c
void resolveConflicts(vector<LALR1ItemSet>& itemSets) {
    for (auto& itemSet : itemSets) {
        if (hasMergeConflict(itemSet)) {
            // 分离冲突状态
            separateConflictingStates(itemSet);
        }
    }
}
```

## 📊 LALR(1)与其他方法比较

| 特性 | SLR(1) | LR(1) | LALR(1) |
|------|--------|-------|---------|
| 状态数 | 少 | 多 | 中等 |
| 表达能力 | 较强 | 最强 | 最强 |
| 实现复杂度 | 中等 | 复杂 | 复杂 |
| 内存消耗 | 少 | 多 | 中等 |
| 实用价值 | 高 | 低 | 最高 |

## 🔧 优化技术

### 状态压缩
```c
void compressStates(vector<LALR1ItemSet>& itemSets) {
    // 移除空状态
    itemSets.erase(
        remove_if(itemSets.begin(), itemSets.end(), 
                  [](const LALR1ItemSet& set) { return set.isEmpty(); }),
        itemSets.end()
    );
    
    // 重新编号状态
    map<int, int> oldToNew;
    for (int i = 0; i < itemSets.size(); i++) {
        oldToNew[i] = i;
    }
}
```

### 表压缩
```c
void compressParseTable(LALR1ParseTable& table) {
    // 使用稀疏矩阵存储
    // 使用位图压缩
    // 使用哈希表优化查找
}
```

## 🔗 相关链接
- [[LR(1)分析表构造]] - LR(1)分析基础
- [[SLR(1)分析技术]] - SLR(1)分析技术
- [[语法分析概述]] - 语法分析基础
- [[语法分析错误处理]] - 错误处理策略

