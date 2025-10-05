# SLR(1)分析技术

## 🎯 SLR(1)分析概述

**SLR(1)分析**是Simple LR(1)分析的简称，它在LR(0)分析的基础上使用FOLLOW集合来解决冲突问题。SLR(1)是LR分析中最实用的方法之一。

## 🔍 SLR(1)基本思想

### 核心思想
SLR(1)分析使用FOLLOW集合来限制归约动作，只有当向前看符号在FOLLOW集合中时才进行归约。

### 与LR(0)的区别
- **LR(0)**：对所有终结符都进行归约
- **SLR(1)**：只对FOLLOW集合中的终结符进行归约

## 🔧 SLR(1)项目

### 项目定义
SLR(1)项目与LR(0)项目相同，但归约动作的确定方式不同：

```c
struct SLR1Item {
    TokenType left;        // 产生式左部
    string right;          // 产生式右部
    int dotPosition;       // 圆点位置
    
    SLR1Item(TokenType left, string right, int dotPosition)
        : left(left), right(right), dotPosition(dotPosition) {}
    
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

## 📊 SLR(1)分析表构造

### 分析表构造算法
```c
class SLR1ParseTable {
private:
    map<pair<int, TokenType>, Action> actionTable;
    map<pair<int, TokenType>, int> gotoTable;
    vector<SLR1ItemSet> itemSets;
    
public:
    void constructParseTable() {
        itemSets = constructItemSets();
        
        // 构造ACTION表
        for (int i = 0; i < itemSets.size(); i++) {
            SLR1ItemSet itemSet = itemSets[i];
            
            for (auto& item : itemSet.getItems()) {
                if (!item.isComplete()) {
                    // 移进项目
                    TokenType nextSymbol = item.getNextSymbol();
                    SLR1ItemSet nextSet = itemSet.gotoSet(nextSymbol);
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
                        // 只对FOLLOW集合中的终结符添加归约动作
                        set<TokenType> follow = computeFollow(item.left);
                        for (TokenType terminal : follow) {
                            actionTable[{i, terminal}] = Action(Action::REDUCE, -1, item.left, item.right);
                        }
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

### FOLLOW集合计算
```c
set<TokenType> computeFollow(TokenType nonTerminal) {
    set<TokenType> follow;
    
    // 如果A是开始符号，添加$
    if (nonTerminal == START_SYMBOL) {
        follow.insert(END_OF_INPUT);
    }
    
    // 遍历所有产生式
    for (auto& production : productions) {
        string right = production.right;
        
        // 找到A在产生式右部的位置
        for (int i = 0; i < right.length(); i++) {
            if (right[i] == nonTerminal) {
                string afterA = right.substr(i + 1);
                
                if (afterA.empty()) {
                    // A是产生式右部的最后一个符号
                    if (production.left != nonTerminal) {
                        set<TokenType> leftFollow = computeFollow(production.left);
                        follow.insert(leftFollow.begin(), leftFollow.end());
                    }
                } else {
                    // 计算FIRST(afterA)
                    set<TokenType> firstAfterA = computeFirst(afterA);
                    follow.insert(firstAfterA.begin(), firstAfterA.end());
                    
                    // 如果FIRST(afterA)包含ε，添加FOLLOW(production.left)
                    if (firstAfterA.count(EMPTY)) {
                        follow.erase(EMPTY);
                        if (production.left != nonTerminal) {
                            set<TokenType> leftFollow = computeFollow(production.left);
                            follow.insert(leftFollow.begin(), leftFollow.end());
                        }
                    }
                }
            }
        }
    }
    
    return follow;
}
```

## 🔄 SLR(1)分析器实现

### 分析器结构
```c
class SLR1Parser {
private:
    SLR1ParseTable parseTable;
    stack<int> stateStack;
    vector<Token> input;
    int position;
    
public:
    SLR1Parser(SLR1ParseTable table, vector<Token> input) 
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

## 📈 SLR(1)分析表示例

### 简单文法
```c
// 文法：
// E → E + T | T
// T → T * F | F
// F → (E) | id

// FOLLOW集合：
// FOLLOW(E) = {$, )}
// FOLLOW(T) = {+, $, )}
// FOLLOW(F) = {*, +, $, )}
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

## 🎯 SLR(1)分析特点

### 优点
- **实用性强**：能够处理大多数实际文法
- **实现简单**：比LR(1)简单
- **效率高**：分析效率高
- **冲突解决**：能够解决大部分冲突

### 缺点
- **仍有冲突**：某些文法仍有冲突
- **表达能力**：表达能力有限
- **FOLLOW计算**：需要计算FOLLOW集合

## 🔧 冲突处理

### 移进-归约冲突
当同一个状态既有移进项目又有归约项目时：

```c
// 冲突示例：
// I2: E → T•
//     T → T• * F
// 
// 当遇到*时：
// - 可以归约E → T（因为*在FOLLOW(E)中）
// - 可以移进T → T * F
// 
// SLR(1)通过FOLLOW集合限制归约动作
```

### 归约-归约冲突
当同一个状态有多个归约项目时：

```c
// 冲突示例：
// I3: T → F•
//     F → (E)•
// 
// 当遇到)时：
// - 可以归约T → F（因为)在FOLLOW(T)中）
// - 可以归约F → (E)（因为)在FOLLOW(F)中）
// 
// 这种情况SLR(1)无法解决
```

## 📊 SLR(1)与LR(0)比较

| 特性 | LR(0) | SLR(1) |
|------|-------|--------|
| 向前看 | 无 | 1个符号 |
| 归约条件 | 所有终结符 | FOLLOW集合 |
| 冲突处理 | 容易冲突 | 减少冲突 |
| 实现复杂度 | 简单 | 中等 |
| 表达能力 | 有限 | 较强 |

## 🔧 文法变换

### 消除左递归
```c
// 原文法（左递归）
// A → Aα | β

// 变换后（右递归）
// A → βA'
// A' → αA' | ε
```

### 消除左因子
```c
// 原文法
// A → αβ | αγ

// 变换后
// A → αA'
// A' → β | γ
```

## 🔗 相关链接
- [[LR(0)分析表构造]] - LR(0)分析基础
- [[LR(1)分析表构造]] - LR(1)分析详细内容
- [[LALR(1)分析技术]] - LALR(1)分析技术
- [[语法分析错误处理]] - 错误处理策略

