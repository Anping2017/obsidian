# LL(1)文法与构造

## 🎯 LL(1)文法概述

**LL(1)文法**是一种特殊的上下文无关文法，能够用LL(1)分析器进行自顶向下的语法分析。其中LL(1)表示：
- **L**：从左到右扫描输入
- **L**：最左推导
- **1**：向前看1个符号

## 🔍 LL(1)文法条件

### 基本条件
LL(1)文法必须满足以下条件：
1. **无左递归**：不能有左递归产生式
2. **无左因子**：不能有左因子
3. **FIRST-FOLLOW不相交**：对于每个非终结符A，如果A → α|β，则FIRST(α) ∩ FIRST(β) = ∅

### 条件检查
```c
bool isLL1Grammar(Grammar grammar) {
    // 检查左递归
    if (hasLeftRecursion(grammar)) {
        return false;
    }
    
    // 检查左因子
    if (hasLeftFactoring(grammar)) {
        return false;
    }
    
    // 检查FIRST-FOLLOW不相交
    for (auto& nonTerminal : grammar.nonTerminals) {
        if (!checkFirstFollowDisjoint(nonTerminal)) {
            return false;
        }
    }
    
    return true;
}
```

## 📊 FIRST集合计算

### FIRST集合定义
FIRST(α)是能够从α推导出的所有字符串的第一个符号的集合。

### 计算规则
```c
set<TokenType> computeFirst(string production) {
    set<TokenType> first;
    
    if (production.empty()) {
        first.insert(EMPTY);
        return first;
    }
    
    TokenType firstSymbol = production[0];
    
    if (isTerminal(firstSymbol)) {
        first.insert(firstSymbol);
    } else {
        // 非终结符
        first = computeFirstForNonTerminal(firstSymbol);
        
        // 如果FIRST(firstSymbol)包含ε，继续计算后续符号
        if (first.count(EMPTY)) {
            first.erase(EMPTY);
            string rest = production.substr(1);
            set<TokenType> restFirst = computeFirst(rest);
            first.insert(restFirst.begin(), restFirst.end());
        }
    }
    
    return first;
}

set<TokenType> computeFirstForNonTerminal(TokenType nonTerminal) {
    set<TokenType> first;
    
    for (auto& production : productions) {
        if (production.left == nonTerminal) {
            set<TokenType> prodFirst = computeFirst(production.right);
            first.insert(prodFirst.begin(), prodFirst.end());
        }
    }
    
    return first;
}
```

### FIRST集合示例
```c
// 文法：
// E → T E'
// E' → + T E' | ε
// T → F T'
// T' → * F T' | ε
// F → (E) | id

// FIRST集合：
// FIRST(E) = {(, id}
// FIRST(E') = {+, ε}
// FIRST(T) = {(, id}
// FIRST(T') = {*, ε}
// FIRST(F) = {(, id}
```

## 📊 FOLLOW集合计算

### FOLLOW集合定义
FOLLOW(A)是可能出现在A后面的所有符号的集合。

### 计算规则
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

### FOLLOW集合示例
```c
// 文法：
// E → T E'
// E' → + T E' | ε
// T → F T'
// T' → * F T' | ε
// F → (E) | id

// FOLLOW集合：
// FOLLOW(E) = {$, )}
// FOLLOW(E') = {$, )}
// FOLLOW(T) = {+, $, )}
// FOLLOW(T') = {+, $, )}
// FOLLOW(F) = {*, +, $, )}
```

## 🔄 LL(1)分析表构造

### 分析表构造算法
```c
class LL1ParseTable {
private:
    map<pair<TokenType, TokenType>, string> parseTable;
    
public:
    void constructParseTable() {
        for (auto& production : productions) {
            TokenType left = production.left;
            string right = production.right;
            
            set<TokenType> first = computeFirst(right);
            
            // 对于FIRST(right)中的每个终结符a
            for (TokenType terminal : first) {
                if (terminal != EMPTY) {
                    parseTable[{left, terminal}] = right;
                }
            }
            
            // 如果FIRST(right)包含ε
            if (first.count(EMPTY)) {
                set<TokenType> follow = computeFollow(left);
                for (TokenType terminal : follow) {
                    parseTable[{left, terminal}] = right;
                }
            }
        }
    }
    
    string getProduction(TokenType nonTerminal, TokenType terminal) {
        return parseTable[{nonTerminal, terminal}];
    }
    
    bool hasProduction(TokenType nonTerminal, TokenType terminal) {
        return parseTable.find({nonTerminal, terminal}) != parseTable.end();
    }
};
```

### 分析表示例
```c
// 文法：
// E → T E'
// E' → + T E' | ε
// T → F T'
// T' → * F T' | ε
// F → (E) | id

// 分析表：
//      id    +    *    (    )    $
// E    TE'   -    -    TE'  -    -
// E'   -     +TE' -    -    ε    ε
// T    FT'   -    -    FT'  -    -
// T'   -     ε    *FT' -    ε    ε
// F    id    -    -    (E)  -    -
```

## 🔧 LL(1)分析器实现

### 分析器结构
```c
class LL1Parser {
private:
    LL1ParseTable parseTable;
    vector<Token> tokens;
    int position;
    
public:
    LL1Parser(Grammar grammar, vector<Token> tokens) 
        : parseTable(grammar), tokens(tokens), position(0) {}
    
    bool parse() {
        stack<TokenType> parseStack;
        parseStack.push(END_OF_INPUT);
        parseStack.push(START_SYMBOL);
        
        while (!parseStack.empty()) {
            TokenType top = parseStack.top();
            TokenType current = tokens[position].type;
            
            if (top == current) {
                // 匹配成功
                parseStack.pop();
                position++;
            } else if (isTerminal(top)) {
                // 终结符不匹配
                error("Expected " + tokenTypeToString(top) + 
                      ", found " + tokenTypeToString(current));
                return false;
            } else {
                // 非终结符，查找产生式
                string production = parseTable.getProduction(top, current);
                if (production.empty()) {
                    error("No production for " + tokenTypeToString(top) + 
                          " and " + tokenTypeToString(current));
                    return false;
                }
                
                parseStack.pop();
                // 将产生式右部逆序压入栈
                for (int i = production.length() - 1; i >= 0; i--) {
                    if (production[i] != EMPTY) {
                        parseStack.push(production[i]);
                    }
                }
            }
        }
        
        return true;
    }
    
    void error(string message) {
        cout << "Error: " << message << " at position " << position << endl;
    }
};
```

## 🎯 LL(1)文法特点

### 优点
- **确定性**：分析过程确定，无回溯
- **效率高**：分析效率高
- **实现简单**：实现相对简单

### 缺点
- **限制严格**：文法限制严格
- **表达能力**：表达能力有限
- **变换复杂**：文法变换复杂

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
- [[自顶向下分析]] - 自顶向下分析基础
- [[语法分析概述]] - 语法分析基础
- [[语法分析树]] - 语法树构建
- [[语法分析错误处理]] - 错误处理策略

