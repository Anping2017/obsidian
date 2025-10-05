# LR(1)分析表构造

## 🎯 LR(1)分析概述

**LR(1)分析**是最强大的LR分析方法，它使用向前看符号来精确控制归约动作。LR(1)能够处理所有LR文法，但分析表可能很大。

## 🔍 LR(1)项目

### 项目定义
LR(1)项目是带有圆点和向前看符号的产生式：

```c
struct LR1Item {
    TokenType left;        // 产生式左部
    string right;          // 产生式右部
    int dotPosition;       // 圆点位置
    TokenType lookahead;   // 向前看符号
    
    LR1Item(TokenType left, string right, int dotPosition, TokenType lookahead)
        : left(left), right(right), dotPosition(dotPosition), lookahead(lookahead) {}
    
    bool operator==(const LR1Item& other) const {
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

### 项目类型
- **移进项目**：圆点后面有符号
- **归约项目**：圆点在产生式末尾，有特定向前看符号
- **接受项目**：开始符号的归约项目

## 🔧 LR(1)项目集构造

### 项目集闭包
```c
class LR1ItemSet {
private:
    set<LR1Item> items;
    
public:
    void addItem(LR1Item item) {
        items.insert(item);
    }
    
    void closure() {
        bool changed = true;
        while (changed) {
            changed = false;
            set<LR1Item> newItems;
            
            for (auto& item : items) {
                TokenType nextSymbol = item.getNextSymbol();
                if (isNonTerminal(nextSymbol)) {
                    // 计算FIRST(βa)，其中β是圆点后的符号串，a是向前看符号
                    string beta = item.right.substr(item.dotPosition + 1);
                    set<TokenType> firstBetaA = computeFirst(beta + item.lookahead);
                    
                    // 添加所有以nextSymbol为左部的产生式
                    for (auto& production : productions) {
                        if (production.left == nextSymbol) {
                            for (TokenType lookahead : firstBetaA) {
                                LR1Item newItem(nextSymbol, production.right, 0, lookahead);
                                if (items.find(newItem) == items.end()) {
                                    newItems.insert(newItem);
                                    changed = true;
                                }
                            }
                        }
                    }
                }
            }
            
            items.insert(newItems.begin(), newItems.end());
        }
    }
    
    LR1ItemSet gotoSet(TokenType symbol) {
        LR1ItemSet newSet;
        
        for (auto& item : items) {
            if (item.getNextSymbol() == symbol) {
                LR1Item newItem(item.left, item.right, item.dotPosition + 1, item.lookahead);
                newSet.addItem(newItem);
            }
        }
        
        newSet.closure();
        return newSet;
    }
    
    bool isEmpty() const {
        return items.empty();
    }
    
    set<LR1Item> getItems() const {
        return items;
    }
};
```

### 项目集构造算法
```c
vector<LR1ItemSet> constructItemSets() {
    vector<LR1ItemSet> itemSets;
    LR1ItemSet initialSet;
    
    // 添加初始项目
    LR1Item initialItem(START_SYMBOL, "E", 0, END_OF_INPUT);
    initialSet.addItem(initialItem);
    initialSet.closure();
    
    itemSets.push_back(initialSet);
    
    // 构造所有项目集
    for (int i = 0; i < itemSets.size(); i++) {
        LR1ItemSet currentSet = itemSets[i];
        
        // 对每个符号计算GOTO
        for (TokenType symbol : allSymbols) {
            LR1ItemSet nextSet = currentSet.gotoSet(symbol);
            if (!nextSet.isEmpty()) {
                int nextIndex = findItemSetIndex(nextSet, itemSets);
                if (nextIndex == -1) {
                    itemSets.push_back(nextSet);
                }
            }
        }
    }
    
    return itemSets;
}

int findItemSetIndex(const LR1ItemSet& target, const vector<LR1ItemSet>& itemSets) {
    for (int i = 0; i < itemSets.size(); i++) {
        if (itemSets[i].getItems() == target.getItems()) {
            return i;
        }
    }
    return -1;
}
```

## 📊 LR(1)分析表构造

### 分析表结构
```c
class LR1ParseTable {
private:
    map<pair<int, TokenType>, Action> actionTable;
    map<pair<int, TokenType>, int> gotoTable;
    vector<LR1ItemSet> itemSets;
    
public:
    void constructParseTable() {
        itemSets = constructItemSets();
        
        // 构造ACTION表
        for (int i = 0; i < itemSets.size(); i++) {
            LR1ItemSet itemSet = itemSets[i];
            
            for (auto& item : itemSet.getItems()) {
                if (!item.isComplete()) {
                    // 移进项目
                    TokenType nextSymbol = item.getNextSymbol();
                    LR1ItemSet nextSet = itemSet.gotoSet(nextSymbol);
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
                        // 只对特定向前看符号添加归约动作
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

## 🔄 LR(1)分析器实现

### 分析器结构
```c
class LR1Parser {
private:
    LR1ParseTable parseTable;
    stack<int> stateStack;
    vector<Token> input;
    int position;
    
public:
    LR1Parser(LR1ParseTable table, vector<Token> input) 
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

## 📈 LR(1)分析表示例

### 简单文法
```c
// 文法：
// E → E + T | T
// T → T * F | F
// F → (E) | id

// LR(1)项目集示例：
// I0: E' → •E, $
//     E → •E + T, $
//     E → •E + T, +
//     E → •T, $
//     E → •T, +
//     T → •T * F, $
//     T → •T * F, +
//     T → •T * F, *
//     T → •F, $
//     T → •F, +
//     T → •F, *
//     F → •(E), $
//     F → •(E), +
//     F → •(E), *
//     F → •id, $
//     F → •id, +
//     F → •id, *
```

### 分析表
```c
// ACTION表（部分）：
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

## 🎯 LR(1)分析特点

### 优点
- **表达能力**：能够处理所有LR文法
- **精确控制**：使用向前看符号精确控制
- **无冲突**：理论上无冲突

### 缺点
- **状态爆炸**：分析表可能很大
- **实现复杂**：实现相对复杂
- **内存消耗**：内存消耗大

## 🔧 状态合并

### 核心项目
LR(1)项目的核心项目是去掉向前看符号的项目：

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
};
```

### 状态合并算法
```c
vector<LR1ItemSet> mergeStates(const vector<LR1ItemSet>& itemSets) {
    map<CoreItem, set<TokenType>> coreToLookaheads;
    
    // 收集所有核心项目的向前看符号
    for (auto& itemSet : itemSets) {
        for (auto& item : itemSet.getItems()) {
            CoreItem core(item.left, item.right, item.dotPosition);
            coreToLookaheads[core].insert(item.lookahead);
        }
    }
    
    // 构造合并后的项目集
    vector<LR1ItemSet> mergedSets;
    map<set<TokenType>, int> lookaheadToState;
    
    for (auto& itemSet : itemSets) {
        set<TokenType> lookaheads;
        for (auto& item : itemSet.getItems()) {
            lookaheads.insert(item.lookahead);
        }
        
        auto it = lookaheadToState.find(lookaheads);
        if (it != lookaheadToState.end()) {
            // 合并到现有状态
            int stateIndex = it->second;
            for (auto& item : itemSet.getItems()) {
                mergedSets[stateIndex].addItem(item);
            }
        } else {
            // 创建新状态
            lookaheadToState[lookaheads] = mergedSets.size();
            mergedSets.push_back(itemSet);
        }
    }
    
    return mergedSets;
}
```

## 📊 LR(1)与SLR(1)比较

| 特性 | SLR(1) | LR(1) |
|------|--------|-------|
| 向前看 | FOLLOW集合 | 精确向前看 |
| 状态数 | 较少 | 较多 |
| 表达能力 | 较强 | 最强 |
| 实现复杂度 | 中等 | 复杂 |
| 内存消耗 | 中等 | 大 |

## 🔗 相关链接
- [[SLR(1)分析技术]] - SLR(1)分析基础
- [[LALR(1)分析技术]] - LALR(1)分析技术
- [[语法分析概述]] - 语法分析基础
- [[语法分析错误处理]] - 错误处理策略

