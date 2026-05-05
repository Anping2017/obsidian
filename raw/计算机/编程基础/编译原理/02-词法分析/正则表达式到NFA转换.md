# 正则表达式到NFA转换

## 🎯 Thompson算法概述

**Thompson算法**是将正则表达式转换为NFA的经典算法。它通过递归构造的方式，为每个正则表达式操作符构造对应的NFA。

## 🔧 基本构造规则

### 1. 空字符串 ε
```c
// 构造NFA：ε
// 状态：0(初始), 1(接受)
// 转换：0 --ε--> 1

NFA epsilon() {
    NFA nfa;
    nfa.addState(0);
    nfa.addState(1);
    nfa.addTransition(0, 'ε', 1);
    nfa.setAcceptState(1);
    return nfa;
}
```

### 2. 单个字符 a
```c
// 构造NFA：a
// 状态：0(初始), 1(接受)
// 转换：0 --a--> 1

NFA character(char c) {
    NFA nfa;
    nfa.addState(0);
    nfa.addState(1);
    nfa.addTransition(0, c, 1);
    nfa.setAcceptState(1);
    return nfa;
}
```

### 3. 选择 r|s
```c
// 构造NFA：r|s
// 状态：0(初始), 1, 2, 3, 4(接受)
// 转换：0 --ε--> 1, 0 --ε--> 3
//       1 --r--> 2, 3 --s--> 4
//       2 --ε--> 4

NFA union(NFA r, NFA s) {
    NFA nfa;
    int start = nfa.addState();
    int end = nfa.addState();
    
    // 添加ε转换到r和s的开始状态
    nfa.addTransition(start, 'ε', r.getStartState());
    nfa.addTransition(start, 'ε', s.getStartState());
    
    // 添加从r和s的接受状态到结束状态的ε转换
    nfa.addTransition(r.getAcceptState(), 'ε', end);
    nfa.addTransition(s.getAcceptState(), 'ε', end);
    
    nfa.setAcceptState(end);
    return nfa;
}
```

### 4. 连接 rs
```c
// 构造NFA：rs
// 状态：r的开始, r的接受, s的开始, s的接受
// 转换：r的接受 --ε--> s的开始

NFA concatenation(NFA r, NFA s) {
    NFA nfa;
    
    // 添加r的所有状态和转换
    nfa.addStates(r.getStates());
    nfa.addTransitions(r.getTransitions());
    
    // 添加s的所有状态和转换
    nfa.addStates(s.getStates());
    nfa.addTransitions(s.getTransitions());
    
    // 添加从r的接受状态到s的开始状态的ε转换
    nfa.addTransition(r.getAcceptState(), 'ε', s.getStartState());
    
    nfa.setAcceptState(s.getAcceptState());
    return nfa;
}
```

### 5. 闭包 r*
```c
// 构造NFA：r*
// 状态：0(初始), 1, 2, 3(接受)
// 转换：0 --ε--> 1, 0 --ε--> 3
//       1 --r--> 2, 2 --ε--> 1
//       2 --ε--> 3

NFA closure(NFA r) {
    NFA nfa;
    int start = nfa.addState();
    int end = nfa.addState();
    
    // 添加ε转换到r的开始状态
    nfa.addTransition(start, 'ε', r.getStartState());
    
    // 添加从r的接受状态到结束状态的ε转换
    nfa.addTransition(r.getAcceptState(), 'ε', end);
    
    // 添加从r的接受状态回到r的开始状态的ε转换（循环）
    nfa.addTransition(r.getAcceptState(), 'ε', r.getStartState());
    
    // 添加从开始状态到结束状态的ε转换（零次匹配）
    nfa.addTransition(start, 'ε', end);
    
    nfa.setAcceptState(end);
    return nfa;
}
```

## 🔄 完整算法实现

### Thompson算法
```c
NFA thompson(string regex) {
    stack<NFA> operands;
    stack<char> operators;
    
    for (char c : regex) {
        if (isOperand(c)) {
            operands.push(character(c));
        } else if (c == '|') {
            operators.push(c);
        } else if (c == '*') {
            NFA r = operands.top();
            operands.pop();
            operands.push(closure(r));
        } else if (c == '(') {
            operators.push(c);
        } else if (c == ')') {
            while (operators.top() != '(') {
                char op = operators.top();
                operators.pop();
                
                if (op == '|') {
                    NFA s = operands.top();
                    operands.pop();
                    NFA r = operands.top();
                    operands.pop();
                    operands.push(union(r, s));
                }
            }
            operators.pop(); // 移除'('
        }
    }
    
    // 处理剩余的连接操作
    while (!operators.empty()) {
        char op = operators.top();
        operators.pop();
        
        if (op == '|') {
            NFA s = operands.top();
            operands.pop();
            NFA r = operands.top();
            operands.pop();
            operands.push(union(r, s));
        }
    }
    
    return operands.top();
}
```

## 📊 算法复杂度

### 时间复杂度
- **构造时间**：O(|r|)，其中|r|是正则表达式的长度
- **状态数**：O(|r|)
- **转换数**：O(|r|)

### 空间复杂度
- **状态空间**：O(|r|)
- **转换空间**：O(|r|)

## 🎯 算法特点

### 优点
- **简单直观**：算法逻辑清晰
- **正确性**：保证构造的NFA正确
- **效率**：构造时间线性

### 缺点
- **状态数多**：可能产生大量状态
- **ε转换多**：包含大量ε转换
- **需要优化**：通常需要后续优化

## 📈 应用示例

### 示例1：识别标识符
```c
// 正则表达式：[a-zA-Z][a-zA-Z0-9]*
// 构造过程：
// 1. 构造[a-zA-Z]
// 2. 构造[a-zA-Z0-9]*
// 3. 连接两个NFA
```

### 示例2：识别数字
```c
// 正则表达式：[0-9]+
// 构造过程：
// 1. 构造[0-9]
// 2. 应用闭包操作
```

## 🔗 相关链接
- [[有限自动机理论]] - 有限自动机基础
- [[NFA到DFA转换算法]] - 后续转换
- [[DFA最小化算法]] - 优化算法
- [[词法分析器实现]] - 实际应用

