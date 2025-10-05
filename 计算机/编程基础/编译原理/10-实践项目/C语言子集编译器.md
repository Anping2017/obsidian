# C语言子集编译器

## 🎯 项目概述

**C语言子集编译器**是一个更复杂的编译器实践项目，实现了一个能够编译C语言子集的编译器。该项目支持变量声明、函数定义、控制流语句等C语言的核心特性，是学习编译原理高级概念的重要实践。

## 🔍 项目目标

### 学习目标
- **掌握复杂语法**：理解C语言的复杂语法结构
- **实现语义分析**：处理类型检查、作用域分析等
- **代码生成**：生成汇编代码或中间代码
- **优化技术**：实现基本的代码优化

### 功能目标
- 支持基本数据类型（int、float、char）
- 支持变量声明和赋值
- 支持函数定义和调用
- 支持控制流语句（if、while、for）
- 支持数组和指针操作

## 📊 项目架构

### 编译器模块结构
```c
class CSubsetCompiler {
private:
    LexicalAnalyzer* lexer;
    SyntaxAnalyzer* parser;
    SemanticAnalyzer* semanticAnalyzer;
    CodeGenerator* codeGenerator;
    Optimizer* optimizer;
    ErrorHandler* errorHandler;
    
public:
    CSubsetCompiler() {
        initializeCompiler();
    }
    
    void initializeCompiler() {
        cout << "初始化C语言子集编译器" << endl;
        
        lexer = new LexicalAnalyzer();
        parser = new SyntaxAnalyzer();
        semanticAnalyzer = new SemanticAnalyzer();
        codeGenerator = new CodeGenerator();
        optimizer = new Optimizer();
        errorHandler = new ErrorHandler();
        
        // 初始化各个模块
        lexer->initialize();
        parser->initialize();
        semanticAnalyzer->initialize();
        codeGenerator->initialize();
        optimizer->initialize();
        errorHandler->initialize();
    }
    
    bool compile(const string& sourceCode) {
        cout << "开始编译C语言子集源代码" << endl;
        cout << "===========================================" << endl;
        
        try {
            // 词法分析
            vector<Token> tokens = lexer->analyze(sourceCode);
            if (tokens.empty()) {
                cout << "词法分析失败" << endl;
                return false;
            }
            
            // 语法分析
            ASTNode* ast = parser->parse(tokens);
            if (!ast) {
                cout << "语法分析失败" << endl;
                return false;
            }
            
            // 语义分析
            if (!semanticAnalyzer->analyze(ast)) {
                cout << "语义分析失败" << endl;
                return false;
            }
            
            // 代码优化
            ASTNode* optimizedAST = optimizer->optimize(ast);
            
            // 代码生成
            string targetCode = codeGenerator->generate(optimizedAST);
            if (targetCode.empty()) {
                cout << "代码生成失败" << endl;
                return false;
            }
            
            cout << "编译成功" << endl;
            cout << "生成的目标代码:" << endl;
            cout << targetCode << endl;
            
            return true;
            
        } catch (const exception& e) {
            errorHandler->reportError("编译错误: " + string(e.what()));
            return false;
        }
    }
    
    void cleanup() {
        cout << "清理C语言子集编译器" << endl;
        
        if (lexer) {
            delete lexer;
            lexer = nullptr;
        }
        
        if (parser) {
            delete parser;
            parser = nullptr;
        }
        
        if (semanticAnalyzer) {
            delete semanticAnalyzer;
            semanticAnalyzer = nullptr;
        }
        
        if (codeGenerator) {
            delete codeGenerator;
            codeGenerator = nullptr;
        }
        
        if (optimizer) {
            delete optimizer;
            optimizer = nullptr;
        }
        
        if (errorHandler) {
            delete errorHandler;
            errorHandler = nullptr;
        }
        
        cout << "C语言子集编译器清理完成" << endl;
    }
    
    ~CSubsetCompiler() {
        cleanup();
    }
};
```

## 🔧 扩展词法分析器

### 扩展词法分析器实现
```c
class LexicalAnalyzer {
private:
    string sourceCode;
    size_t currentPos;
    vector<Token> tokens;
    
public:
    LexicalAnalyzer() : currentPos(0) {}
    
    void initialize() {
        cout << "初始化C语言子集词法分析器" << endl;
    }
    
    vector<Token> analyze(const string& code) {
        cout << "开始C语言子集词法分析" << endl;
        cout << "-------------------------------------------" << endl;
        
        sourceCode = code;
        currentPos = 0;
        tokens.clear();
        
        while (currentPos < sourceCode.length()) {
            char currentChar = sourceCode[currentPos];
            
            if (isspace(currentChar)) {
                currentPos++;
                continue;
            }
            
            if (isdigit(currentChar)) {
                Token token = scanNumber();
                tokens.push_back(token);
            } else if (isalpha(currentChar) || currentChar == '_') {
                Token token = scanIdentifier();
                tokens.push_back(token);
            } else if (currentChar == '"') {
                Token token = scanString();
                tokens.push_back(token);
            } else if (currentChar == '\'') {
                Token token = scanCharacter();
                tokens.push_back(token);
            } else if (isOperator(currentChar)) {
                Token token = scanOperator();
                tokens.push_back(token);
            } else if (isDelimiter(currentChar)) {
                Token token = scanDelimiter();
                tokens.push_back(token);
            } else {
                cout << "未知字符: " << currentChar << endl;
                currentPos++;
            }
        }
        
        // 添加结束标记
        Token eofToken;
        eofToken.type = TOKEN_EOF;
        eofToken.value = "EOF";
        tokens.push_back(eofToken);
        
        cout << "C语言子集词法分析完成，共识别 " << tokens.size() << " 个词法单元" << endl;
        return tokens;
    }
    
    Token scanNumber() {
        string value;
        
        // 扫描整数部分
        while (currentPos < sourceCode.length() && isdigit(sourceCode[currentPos])) {
            value += sourceCode[currentPos];
            currentPos++;
        }
        
        // 扫描小数部分
        if (currentPos < sourceCode.length() && sourceCode[currentPos] == '.') {
            value += '.';
            currentPos++;
            
            while (currentPos < sourceCode.length() && isdigit(sourceCode[currentPos])) {
                value += sourceCode[currentPos];
                currentPos++;
            }
        }
        
        Token token;
        token.type = TOKEN_NUMBER;
        token.value = value;
        
        cout << "识别数字: " << value << endl;
        return token;
    }
    
    Token scanIdentifier() {
        string value;
        
        while (currentPos < sourceCode.length() && 
               (isalnum(sourceCode[currentPos]) || sourceCode[currentPos] == '_')) {
            value += sourceCode[currentPos];
            currentPos++;
        }
        
        Token token;
        token.type = getKeywordType(value);
        token.value = value;
        
        cout << "识别标识符/关键字: " << value << endl;
        return token;
    }
    
    Token scanString() {
        string value;
        currentPos++; // 跳过开始的引号
        
        while (currentPos < sourceCode.length() && sourceCode[currentPos] != '"') {
            if (sourceCode[currentPos] == '\\') {
                currentPos++;
                if (currentPos < sourceCode.length()) {
                    value += sourceCode[currentPos];
                    currentPos++;
                }
            } else {
                value += sourceCode[currentPos];
                currentPos++;
            }
        }
        
        if (currentPos < sourceCode.length()) {
            currentPos++; // 跳过结束的引号
        }
        
        Token token;
        token.type = TOKEN_STRING;
        token.value = value;
        
        cout << "识别字符串: " << value << endl;
        return token;
    }
    
    Token scanCharacter() {
        string value;
        currentPos++; // 跳过开始的单引号
        
        if (currentPos < sourceCode.length()) {
            if (sourceCode[currentPos] == '\\') {
                currentPos++;
                if (currentPos < sourceCode.length()) {
                    value += sourceCode[currentPos];
                    currentPos++;
                }
            } else {
                value += sourceCode[currentPos];
                currentPos++;
            }
        }
        
        if (currentPos < sourceCode.length()) {
            currentPos++; // 跳过结束的单引号
        }
        
        Token token;
        token.type = TOKEN_CHARACTER;
        token.value = value;
        
        cout << "识别字符: " << value << endl;
        return token;
    }
    
    Token scanOperator() {
        char op = sourceCode[currentPos];
        currentPos++;
        
        // 检查双字符操作符
        if (currentPos < sourceCode.length()) {
            char nextChar = sourceCode[currentPos];
            string doubleOp = string(1, op) + string(1, nextChar);
            
            if (isDoubleOperator(doubleOp)) {
                currentPos++;
                Token token;
                token.type = TOKEN_OPERATOR;
                token.value = doubleOp;
                
                cout << "识别双字符操作符: " << doubleOp << endl;
                return token;
            }
        }
        
        Token token;
        token.type = TOKEN_OPERATOR;
        token.value = string(1, op);
        
        cout << "识别操作符: " << op << endl;
        return token;
    }
    
    Token scanDelimiter() {
        char delim = sourceCode[currentPos];
        currentPos++;
        
        Token token;
        token.type = TOKEN_DELIMITER;
        token.value = string(1, delim);
        
        cout << "识别分隔符: " << delim << endl;
        return token;
    }
    
    bool isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || 
               c == '=' || c == '<' || c == '>' || c == '!' ||
               c == '&' || c == '|' || c == '^' || c == '~';
    }
    
    bool isDelimiter(char c) {
        return c == '(' || c == ')' || c == '{' || c == '}' ||
               c == '[' || c == ']' || c == ';' || c == ',' ||
               c == '.' || c == ':' || c == '?';
    }
    
    bool isDoubleOperator(const string& op) {
        return op == "==" || op == "!=" || op == "<=" || op == ">=" ||
               op == "&&" || op == "||" || op == "++" || op == "--" ||
               op == "+=" || op == "-=" || op == "*=" || op == "/=";
    }
    
    TokenType getKeywordType(const string& value) {
        if (value == "int" || value == "float" || value == "char" || value == "void") {
            return TOKEN_TYPE;
        } else if (value == "if" || value == "else" || value == "while" || value == "for") {
            return TOKEN_KEYWORD;
        } else if (value == "return" || value == "break" || value == "continue") {
            return TOKEN_KEYWORD;
        } else {
            return TOKEN_IDENTIFIER;
        }
    }
    
    void printTokens() {
        cout << "词法单元列表" << endl;
        cout << "-------------------------------------------" << endl;
        
        for (size_t i = 0; i < tokens.size(); i++) {
            const Token& token = tokens[i];
            cout << "[" << i << "] " << getTokenTypeName(token.type) 
                 << " -> " << token.value << endl;
        }
        
        cout << endl;
    }
    
    string getTokenTypeName(TokenType type) {
        switch (type) {
            case TOKEN_NUMBER: return "数字";
            case TOKEN_IDENTIFIER: return "标识符";
            case TOKEN_KEYWORD: return "关键字";
            case TOKEN_TYPE: return "类型";
            case TOKEN_OPERATOR: return "操作符";
            case TOKEN_DELIMITER: return "分隔符";
            case TOKEN_STRING: return "字符串";
            case TOKEN_CHARACTER: return "字符";
            case TOKEN_EOF: return "结束";
            default: return "未知";
        }
    }
};

enum TokenType {
    TOKEN_NUMBER,
    TOKEN_IDENTIFIER,
    TOKEN_KEYWORD,
    TOKEN_TYPE,
    TOKEN_OPERATOR,
    TOKEN_DELIMITER,
    TOKEN_STRING,
    TOKEN_CHARACTER,
    TOKEN_EOF
};

struct Token {
    TokenType type;
    string value;
};
```

## 🔧 语法分析器

### 语法分析器实现
```c
class SyntaxAnalyzer {
private:
    vector<Token> tokens;
    size_t currentTokenIndex;
    
public:
    SyntaxAnalyzer() : currentTokenIndex(0) {}
    
    void initialize() {
        cout << "初始化C语言子集语法分析器" << endl;
    }
    
    ASTNode* parse(const vector<Token>& tokenList) {
        cout << "开始C语言子集语法分析" << endl;
        cout << "-------------------------------------------" << endl;
        
        tokens = tokenList;
        currentTokenIndex = 0;
        
        ASTNode* ast = parseProgram();
        
        if (currentTokenIndex < tokens.size() - 1) {
            cout << "语法分析未完成" << endl;
            return nullptr;
        }
        
        cout << "C语言子集语法分析完成" << endl;
        return ast;
    }
    
    ASTNode* parseProgram() {
        cout << "解析程序" << endl;
        
        ASTNode* program = new ASTNode();
        program->type = AST_PROGRAM;
        program->children = vector<ASTNode*>();
        
        while (currentTokenIndex < tokens.size() - 1) {
            ASTNode* statement = parseStatement();
            if (statement) {
                program->children.push_back(statement);
            } else {
                break;
            }
        }
        
        return program;
    }
    
    ASTNode* parseStatement() {
        cout << "解析语句" << endl;
        
        Token current = getCurrentToken();
        
        if (current.type == TOKEN_TYPE) {
            return parseDeclaration();
        } else if (current.type == TOKEN_KEYWORD && current.value == "if") {
            return parseIfStatement();
        } else if (current.type == TOKEN_KEYWORD && current.value == "while") {
            return parseWhileStatement();
        } else if (current.type == TOKEN_KEYWORD && current.value == "for") {
            return parseForStatement();
        } else if (current.type == TOKEN_KEYWORD && current.value == "return") {
            return parseReturnStatement();
        } else if (current.type == TOKEN_IDENTIFIER) {
            return parseAssignment();
        } else if (current.type == TOKEN_DELIMITER && current.value == "{") {
            return parseBlock();
        } else {
            cout << "语法错误: 意外的词法单元 " << current.value << endl;
            return nullptr;
        }
    }
    
    ASTNode* parseDeclaration() {
        cout << "解析声明" << endl;
        
        Token typeToken = getCurrentToken();
        currentTokenIndex++;
        
        Token nameToken = getCurrentToken();
        currentTokenIndex++;
        
        ASTNode* node = new ASTNode();
        node->type = AST_DECLARATION;
        node->value = nameToken.value;
        node->typeName = typeToken.value;
        
        // 检查是否有初始化
        if (getCurrentToken().type == TOKEN_OPERATOR && getCurrentToken().value == "=") {
            currentTokenIndex++; // 跳过 '='
            node->children.push_back(parseExpression());
        }
        
        // 跳过分号
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ";") {
            currentTokenIndex++;
        }
        
        return node;
    }
    
    ASTNode* parseIfStatement() {
        cout << "解析if语句" << endl;
        
        currentTokenIndex++; // 跳过 'if'
        
        // 跳过 '('
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == "(") {
            currentTokenIndex++;
        }
        
        ASTNode* condition = parseExpression();
        
        // 跳过 ')'
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ")") {
            currentTokenIndex++;
        }
        
        ASTNode* thenStatement = parseStatement();
        
        ASTNode* node = new ASTNode();
        node->type = AST_IF_STATEMENT;
        node->children.push_back(condition);
        node->children.push_back(thenStatement);
        
        // 检查是否有else
        if (getCurrentToken().type == TOKEN_KEYWORD && getCurrentToken().value == "else") {
            currentTokenIndex++; // 跳过 'else'
            ASTNode* elseStatement = parseStatement();
            node->children.push_back(elseStatement);
        }
        
        return node;
    }
    
    ASTNode* parseWhileStatement() {
        cout << "解析while语句" << endl;
        
        currentTokenIndex++; // 跳过 'while'
        
        // 跳过 '('
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == "(") {
            currentTokenIndex++;
        }
        
        ASTNode* condition = parseExpression();
        
        // 跳过 ')'
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ")") {
            currentTokenIndex++;
        }
        
        ASTNode* body = parseStatement();
        
        ASTNode* node = new ASTNode();
        node->type = AST_WHILE_STATEMENT;
        node->children.push_back(condition);
        node->children.push_back(body);
        
        return node;
    }
    
    ASTNode* parseForStatement() {
        cout << "解析for语句" << endl;
        
        currentTokenIndex++; // 跳过 'for'
        
        // 跳过 '('
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == "(") {
            currentTokenIndex++;
        }
        
        ASTNode* init = parseStatement();
        ASTNode* condition = parseExpression();
        
        // 跳过 ';'
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ";") {
            currentTokenIndex++;
        }
        
        ASTNode* update = parseExpression();
        
        // 跳过 ')'
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ")") {
            currentTokenIndex++;
        }
        
        ASTNode* body = parseStatement();
        
        ASTNode* node = new ASTNode();
        node->type = AST_FOR_STATEMENT;
        node->children.push_back(init);
        node->children.push_back(condition);
        node->children.push_back(update);
        node->children.push_back(body);
        
        return node;
    }
    
    ASTNode* parseReturnStatement() {
        cout << "解析return语句" << endl;
        
        currentTokenIndex++; // 跳过 'return'
        
        ASTNode* node = new ASTNode();
        node->type = AST_RETURN_STATEMENT;
        
        if (getCurrentToken().type != TOKEN_DELIMITER || getCurrentToken().value != ";") {
            node->children.push_back(parseExpression());
        }
        
        // 跳过分号
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ";") {
            currentTokenIndex++;
        }
        
        return node;
    }
    
    ASTNode* parseAssignment() {
        cout << "解析赋值语句" << endl;
        
        Token nameToken = getCurrentToken();
        currentTokenIndex++;
        
        // 跳过 '='
        if (getCurrentToken().type == TOKEN_OPERATOR && getCurrentToken().value == "=") {
            currentTokenIndex++;
        }
        
        ASTNode* expression = parseExpression();
        
        ASTNode* node = new ASTNode();
        node->type = AST_ASSIGNMENT;
        node->value = nameToken.value;
        node->children.push_back(expression);
        
        // 跳过分号
        if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ";") {
            currentTokenIndex++;
        }
        
        return node;
    }
    
    ASTNode* parseBlock() {
        cout << "解析代码块" << endl;
        
        currentTokenIndex++; // 跳过 '{'
        
        ASTNode* node = new ASTNode();
        node->type = AST_BLOCK;
        node->children = vector<ASTNode*>();
        
        while (getCurrentToken().type != TOKEN_DELIMITER || getCurrentToken().value != "}") {
            ASTNode* statement = parseStatement();
            if (statement) {
                node->children.push_back(statement);
            } else {
                break;
            }
        }
        
        currentTokenIndex++; // 跳过 '}'
        
        return node;
    }
    
    ASTNode* parseExpression() {
        cout << "解析表达式" << endl;
        
        return parseLogicalOr();
    }
    
    ASTNode* parseLogicalOr() {
        ASTNode* left = parseLogicalAnd();
        
        while (getCurrentToken().type == TOKEN_OPERATOR && getCurrentToken().value == "||") {
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* right = parseLogicalAnd();
            
            ASTNode* node = new ASTNode();
            node->type = AST_BINARY_OP;
            node->value = op.value;
            node->left = left;
            node->right = right;
            
            left = node;
        }
        
        return left;
    }
    
    ASTNode* parseLogicalAnd() {
        ASTNode* left = parseEquality();
        
        while (getCurrentToken().type == TOKEN_OPERATOR && getCurrentToken().value == "&&") {
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* right = parseEquality();
            
            ASTNode* node = new ASTNode();
            node->type = AST_BINARY_OP;
            node->value = op.value;
            node->left = left;
            node->right = right;
            
            left = node;
        }
        
        return left;
    }
    
    ASTNode* parseEquality() {
        ASTNode* left = parseRelational();
        
        while (getCurrentToken().type == TOKEN_OPERATOR && 
               (getCurrentToken().value == "==" || getCurrentToken().value == "!=")) {
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* right = parseRelational();
            
            ASTNode* node = new ASTNode();
            node->type = AST_BINARY_OP;
            node->value = op.value;
            node->left = left;
            node->right = right;
            
            left = node;
        }
        
        return left;
    }
    
    ASTNode* parseRelational() {
        ASTNode* left = parseAdditive();
        
        while (getCurrentToken().type == TOKEN_OPERATOR && 
               (getCurrentToken().value == "<" || getCurrentToken().value == ">" ||
                getCurrentToken().value == "<=" || getCurrentToken().value == ">=")) {
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* right = parseAdditive();
            
            ASTNode* node = new ASTNode();
            node->type = AST_BINARY_OP;
            node->value = op.value;
            node->left = left;
            node->right = right;
            
            left = node;
        }
        
        return left;
    }
    
    ASTNode* parseAdditive() {
        ASTNode* left = parseMultiplicative();
        
        while (getCurrentToken().type == TOKEN_OPERATOR && 
               (getCurrentToken().value == "+" || getCurrentToken().value == "-")) {
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* right = parseMultiplicative();
            
            ASTNode* node = new ASTNode();
            node->type = AST_BINARY_OP;
            node->value = op.value;
            node->left = left;
            node->right = right;
            
            left = node;
        }
        
        return left;
    }
    
    ASTNode* parseMultiplicative() {
        ASTNode* left = parseUnary();
        
        while (getCurrentToken().type == TOKEN_OPERATOR && 
               (getCurrentToken().value == "*" || getCurrentToken().value == "/" ||
                getCurrentToken().value == "%")) {
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* right = parseUnary();
            
            ASTNode* node = new ASTNode();
            node->type = AST_BINARY_OP;
            node->value = op.value;
            node->left = left;
            node->right = right;
            
            left = node;
        }
        
        return left;
    }
    
    ASTNode* parseUnary() {
        if (getCurrentToken().type == TOKEN_OPERATOR && 
            (getCurrentToken().value == "+" || getCurrentToken().value == "-" ||
             getCurrentToken().value == "!" || getCurrentToken().value == "~")) {
            
            Token op = getCurrentToken();
            currentTokenIndex++;
            
            ASTNode* operand = parseUnary();
            
            ASTNode* node = new ASTNode();
            node->type = AST_UNARY_OP;
            node->value = op.value;
            node->left = operand;
            
            return node;
        }
        
        return parsePrimary();
    }
    
    ASTNode* parsePrimary() {
        Token current = getCurrentToken();
        
        if (current.type == TOKEN_NUMBER) {
            currentTokenIndex++;
            
            ASTNode* node = new ASTNode();
            node->type = AST_NUMBER;
            node->value = current.value;
            
            return node;
        } else if (current.type == TOKEN_IDENTIFIER) {
            currentTokenIndex++;
            
            ASTNode* node = new ASTNode();
            node->type = AST_IDENTIFIER;
            node->value = current.value;
            
            return node;
        } else if (current.type == TOKEN_STRING) {
            currentTokenIndex++;
            
            ASTNode* node = new ASTNode();
            node->type = AST_STRING;
            node->value = current.value;
            
            return node;
        } else if (current.type == TOKEN_CHARACTER) {
            currentTokenIndex++;
            
            ASTNode* node = new ASTNode();
            node->type = AST_CHARACTER;
            node->value = current.value;
            
            return node;
        } else if (current.type == TOKEN_DELIMITER && current.value == "(") {
            currentTokenIndex++; // 跳过 '('
            
            ASTNode* node = parseExpression();
            
            if (getCurrentToken().type == TOKEN_DELIMITER && getCurrentToken().value == ")") {
                currentTokenIndex++; // 跳过 ')'
                return node;
            } else {
                cout << "缺少右括号" << endl;
                return nullptr;
            }
        } else {
            cout << "语法错误: 意外的词法单元 " << current.value << endl;
            return nullptr;
        }
    }
    
    Token getCurrentToken() {
        if (currentTokenIndex < tokens.size()) {
            return tokens[currentTokenIndex];
        } else {
            Token eofToken;
            eofToken.type = TOKEN_EOF;
            eofToken.value = "EOF";
            return eofToken;
        }
    }
    
    void printAST(ASTNode* node, int depth = 0) {
        if (!node) return;
        
        string indent(depth * 2, ' ');
        cout << indent << "节点类型: " << getASTTypeName(node->type) 
             << ", 值: " << node->value << endl;
        
        if (node->left) {
            cout << indent << "左子树:" << endl;
            printAST(node->left, depth + 1);
        }
        
        if (node->right) {
            cout << indent << "右子树:" << endl;
            printAST(node->right, depth + 1);
        }
        
        for (size_t i = 0; i < node->children.size(); i++) {
            cout << indent << "子节点[" << i << "]:" << endl;
            printAST(node->children[i], depth + 1);
        }
    }
    
    string getASTTypeName(ASTType type) {
        switch (type) {
            case AST_PROGRAM: return "程序";
            case AST_DECLARATION: return "声明";
            case AST_ASSIGNMENT: return "赋值";
            case AST_IF_STATEMENT: return "if语句";
            case AST_WHILE_STATEMENT: return "while语句";
            case AST_FOR_STATEMENT: return "for语句";
            case AST_RETURN_STATEMENT: return "return语句";
            case AST_BLOCK: return "代码块";
            case AST_NUMBER: return "数字";
            case AST_IDENTIFIER: return "标识符";
            case AST_STRING: return "字符串";
            case AST_CHARACTER: return "字符";
            case AST_BINARY_OP: return "二元操作";
            case AST_UNARY_OP: return "一元操作";
            default: return "未知";
        }
    }
};

enum ASTType {
    AST_PROGRAM,
    AST_DECLARATION,
    AST_ASSIGNMENT,
    AST_IF_STATEMENT,
    AST_WHILE_STATEMENT,
    AST_FOR_STATEMENT,
    AST_RETURN_STATEMENT,
    AST_BLOCK,
    AST_NUMBER,
    AST_IDENTIFIER,
    AST_STRING,
    AST_CHARACTER,
    AST_BINARY_OP,
    AST_UNARY_OP
};

struct ASTNode {
    ASTType type;
    string value;
    string typeName;
    ASTNode* left;
    ASTNode* right;
    vector<ASTNode*> children;
    
    ASTNode() : left(nullptr), right(nullptr) {}
};
```

## 🔗 相关链接
- [[简单计算器编译器]] - 简单计算器编译器项目
- [[虚拟机实现]] - 虚拟机实现项目
- [[编译器工具链]] - 编译器工具链项目
- [[项目实现技巧]] - 项目实现技巧
- [[词法分析概述]] - 词法分析基础
- [[语法分析概述]] - 语法分析基础
- [[语义分析概述]] - 语义分析基础

