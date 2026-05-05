# LR(0)分析表构造

## 🎯 LR(0)分析概述

**LR(0)分析**是最简单的LR分析方法，它不需要向前看符号就能进行语法分析。LR(0)分析表构造是理解LR分析的基础。

## 🔍 LR(0)项目

### 项目定义
LR(0)项目是带有圆点的产生式，表示分析过程中的位置：

```c
struct LR0Item {
    TokenType left;        // 产生式左部
    string right;          // 产生式右部
    int dotPosition;       // 圆点位置
    
    LR0Item(TokenType left, string right, int dotPosition)
        : left(left), right(right), dotPosition(dotPosition) {}
    
    bool operator==(const LR0Item& other) const {
        return left == other.left && right == other.right && 
               dotPosition == other.dotPosition;
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
- **归约项目**：圆点在产生式末尾
- **接受项目**：开始符号的归约项目

## 🔧 项目集构造

### 项目集闭包
```c
class LR0ItemSet {
private:
    set<LR0Item> items;
    
public:
    void addItem(LR0Item item) {
        items.insert(item);
    }
    
    void closure() {
        bool changed = true;
        while (changed) {
            changed = false;
            set<LR0Item> newItems;
            
            for (auto& item : items) {
                TokenType nextSymbol = item.getNextSymbol();
                if (isNonTerminal(nextSymbol)) {
                    // 添加所有以nextSymbol为左部的产生式
                    for (auto& production : productions) {
                        if (production.left == nextSymbol) {
                            LR0Item newItem(nextSymbol, production.right, 0);
                            if (items.find(newItem) == items.end()) {
                                newItems.insert(newItem);
                                changed = true;
                            }
                        }
                    }
                }
            }
            
            items.insert(newItems.begin(), newItems.end());
        }
    }
    
    LR0ItemSet gotoSet(TokenType symbol) {
        LR0ItemSet newSet;
        
        for (auto& item : items) {
            if (item.getNextSymbol() == symbol) {
                LR0Item newItem(item.left, item.right, item.dotPosition + 1);
                newSet.addItem(newItem);
            }
        }
        
        newSet.closure();
        return newSet;
    }
    
    bool isEmpty() const {
        return items.empty();
    }
    
    set<LR0Item> getItems() const {
        return items;
    }
};
```

### 项目集构造算法
```c
vector<LR0ItemSet> constructItemSets() {
    vector<LR0ItemSet> itemSets;
    LR0ItemSet initialSet;
    
    // 添加初始项目
    LR0Item initialItem(START_SYMBOL, "E", 0);
    initialSet.addItem(initialItem);
    initialSet.closure();
    
    itemSets.push_back(initialSet);
    
    // 构造所有项目集
    for (int i = 0; i < itemSets.size(); i++) {
        LR0ItemSet currentSet = itemSets[i];
        
        // 对每个符号计算GOTO
        for (TokenType symbol : allSymbols) {
            LR0ItemSet nextSet = currentSet.gotoSet(symbol);
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

int findItemSetIndex(const LR0ItemSet& target, const vector<LR0ItemSet>& itemSets) {
    for (int i = 0; i < itemSets.size(); i++) {
        if (itemSets[i].getItems() == target.getItems()) {
            return i;
        }
    }
    return -1;
}
```

## 📊 LR(0)分析表构造

### 分析表结构
```c
struct Action {
    enum Type { SHIFT, REDUCE, ACCEPT, ERROR };
    Type type;
    int nextState;
    TokenType left;
    string right;
    
    Action(Type type, int nextState = -1, TokenType left = EMPTY, string right = "")
        : type(type), nextState(nextState), left(left), right(right) {}
};

class LR0ParseTable {
private:
    map<pair<int, TokenType>, Action> actionTable;
    map<pair<int, TokenType>, int> gotoTable;
    vector<LR0ItemSet> itemSets;
    
public:
    void constructParseTable() {
        itemSets = constructItemSets();
        
        // 构造ACTION表
        for (int i = 0; i < itemSets.size(); i++) {
            LR0ItemSet itemSet = itemSets[i];
            
            for (auto& item : itemSet.getItems()) {
                if (!item.isComplete()) {
                    // 移进项目
                    TokenType nextSymbol = item.getNextSymbol();
                    LR0ItemSet nextSet = itemSet.gotoSet(nextSymbol);
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
                        // 对所有终结符添加归约动作
                        for (TokenType terminal : terminals) {
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

## 🔄 LR(0)分析器实现

### 分析器结构
```c
class LR0Parser {
private:
    LR0ParseTable parseTable;
    stack<int> stateStack;
    vector<Token> input;
    int position;
    
public:
    LR0Parser(LR0ParseTable table, vector<Token> input) 
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

## 📈 分析表示例

### 简单文法
```c
// 文法：
// E → E + T | T
// T → T * F | F
// F → (E) | id

// 项目集：
// I0: E' → •E
//     E → •E + T
//     E → •T
//     T → •T * F
//     T → •F
//     F → •(E)
//     F → •id

// I1: E' → E•
//     E → E• + T

// I2: E → T•
//     T → T• * F

// I3: T → F•

// I4: F → (•E)
//     E → •E + T
//     E → •T
//     T → •T * F
//     T → •F
//     F → •(E)
//     F → •id

// I5: F → id•

// I6: E → E + •T
//     T → •T * F
//     T → •F
//     F → •(E)
//     F → •id

// I7: T → T * •F
//     F → •(E)
//     F → •id

// I8: F → (E•)
//     E → E• + T

// I9: E → E + T•

// I10: T → T * F•

// I11: F → (E)•
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

## 🎯 LR(0)分析特点

### 优点
- **简单直观**：算法简单，易于理解
- **无向前看**：不需要向前看符号
- **基础算法**：是其他LR分析的基础

### 缺点
- **冲突问题**：容易产生移进-归约冲突
- **表达能力**：表达能力有限
- **实用性问题**：实际应用较少

## 🔧 冲突处理

### 移进-归约冲突
当同一个状态既有移进项目又有归约项目时发生：

```c
// 冲突示例：
// I2: E → T•
//     T → T• * F
// 
// 当遇到*时，既可以归约E → T，也可以移进T → T * F
```

### 归约-归约冲突
当同一个状态有多个归约项目时发生：

```c
// 冲突示例：
// I3: T → F•
//     F → (E)•
// 
// 当遇到)时，既可以归约T → F，也可以归约F → (E)
```

## 🔗 相关链接
- [[自底向上分析]] - 自底向上分析基础
- [[SLR(1)分析技术]] - SLR(1)分析技术
- [[LR(1)分析表构造]] - LR(1)分析详细内容
- [[语法分析错误处理]] - 错误处理策略

