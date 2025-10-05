# KMP算法

## 🎯 核心概念

**KMP算法(Knuth-Morris-Pratt)**是一种高效的字符串匹配算法，用于在文本中查找模式串的所有出现位置。KMP算法的核心思想是利用模式串的失败函数(也称为部分匹配表或next数组)来避免不必要的字符比较，从而将时间复杂度从O(mn)优化到O(m+n)。

## 🔍 算法原理

### 1. 基本思想
```python
def kmp_concept():
    """KMP算法基本思想"""
    # 1. 失败函数：记录模式串中每个位置的最长公共前后缀长度
    # 2. 匹配过程：利用失败函数跳过不必要的比较
    # 3. 时间复杂度：O(m+n)，其中m是模式串长度，n是文本长度
    # 4. 空间复杂度：O(m)
    
    pass

def kmp_properties():
    """KMP算法性质"""
    properties = {
        "时间复杂度": "O(m+n)",
        "空间复杂度": "O(m)",
        "预处理时间": "O(m)",
        "匹配时间": "O(n)",
        "失败函数": "记录最长公共前后缀长度",
        "应用场景": ["字符串匹配", "文本搜索", "模式识别"]
    }
    return properties
```

### 2. 失败函数构建
```python
def failure_function_construction():
    """失败函数构建"""
    
    def build_failure_function(pattern):
        """构建失败函数(部分匹配表)"""
        m = len(pattern)
        failure = [0] * m
        j = 0
        
        for i in range(1, m):
            # 如果字符不匹配，回退到前一个匹配位置
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            
            # 如果字符匹配，增加匹配长度
            if pattern[i] == pattern[j]:
                j += 1
            
            failure[i] = j
        
        return failure
    
    def build_failure_function_optimized(pattern):
        """优化的失败函数构建"""
        m = len(pattern)
        failure = [0] * m
        j = 0
        
        for i in range(1, m):
            # 回退到前一个匹配位置
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            
            # 增加匹配长度
            if pattern[i] == pattern[j]:
                j += 1
            
            failure[i] = j
        
        return failure
    
    def build_failure_function_with_explanation(pattern):
        """带解释的失败函数构建"""
        m = len(pattern)
        failure = [0] * m
        j = 0
        
        print(f"构建模式串 '{pattern}' 的失败函数:")
        print(f"位置 0: failure[0] = 0 (第一个字符)")
        
        for i in range(1, m):
            print(f"位置 {i}: 比较 pattern[{i}] = '{pattern[i]}' 和 pattern[{j}] = '{pattern[j]}'")
            
            # 回退到前一个匹配位置
            while j > 0 and pattern[i] != pattern[j]:
                print(f"  不匹配，回退到 failure[{j-1}] = {failure[j-1]}")
                j = failure[j - 1]
            
            # 增加匹配长度
            if pattern[i] == pattern[j]:
                j += 1
                print(f"  匹配，j = {j}")
            else:
                print(f"  不匹配，j = {j}")
            
            failure[i] = j
            print(f"  failure[{i}] = {failure[i]}")
        
        return failure
    
    return build_failure_function, build_failure_function_optimized, build_failure_function_with_explanation

def failure_function_examples():
    """失败函数示例"""
    
    def failure_example_1():
        """示例1: "ababaca" """
        pattern = "ababaca"
        failure = build_failure_function(pattern)
        print(f"模式串: {pattern}")
        print(f"失败函数: {failure}")
        return failure
    
    def failure_example_2():
        """示例2: "abcabc" """
        pattern = "abcabc"
        failure = build_failure_function(pattern)
        print(f"模式串: {pattern}")
        print(f"失败函数: {failure}")
        return failure
    
    def failure_example_3():
        """示例3: "aaaaaa" """
        pattern = "aaaaaa"
        failure = build_failure_function(pattern)
        print(f"模式串: {pattern}")
        print(f"失败函数: {failure}")
        return failure
    
    return failure_example_1, failure_example_2, failure_example_3
```

## 🎨 算法实现

### 1. 基本KMP算法
```python
def kmp_algorithm():
    """KMP算法实现"""
    
    def kmp_search(text, pattern):
        """KMP字符串匹配算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        # 构建失败函数
        failure = build_failure_function(pattern)
        
        # 匹配过程
        matches = []
        j = 0
        
        for i in range(n):
            # 如果字符不匹配，回退到前一个匹配位置
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            
            # 如果字符匹配，增加匹配长度
            if text[i] == pattern[j]:
                j += 1
            
            # 如果完全匹配，记录位置
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]  # 继续寻找下一个匹配
        
        return matches
    
    def kmp_search_with_count(text, pattern):
        """带计数器的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)], 0
        
        failure = build_failure_function(pattern)
        matches = []
        j = 0
        comparisons = 0
        
        for i in range(n):
            comparisons += 1
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
                comparisons += 1
            
            if text[i] == pattern[j]:
                j += 1
            
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]
        
        return matches, comparisons
    
    def kmp_search_with_explanation(text, pattern):
        """带解释的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        failure = build_failure_function(pattern)
        matches = []
        j = 0
        
        print(f"在文本 '{text}' 中搜索模式 '{pattern}'")
        print(f"失败函数: {failure}")
        print("匹配过程:")
        
        for i in range(n):
            print(f"位置 {i}: 比较 text[{i}] = '{text[i]}' 和 pattern[{j}] = '{pattern[j]}'")
            
            while j > 0 and text[i] != pattern[j]:
                print(f"  不匹配，回退到 failure[{j-1}] = {failure[j-1]}")
                j = failure[j - 1]
            
            if text[i] == pattern[j]:
                j += 1
                print(f"  匹配，j = {j}")
            else:
                print(f"  不匹配，j = {j}")
            
            if j == m:
                match_pos = i - m + 1
                matches.append(match_pos)
                print(f"  找到匹配，位置: {match_pos}")
                j = failure[j - 1]
        
        return matches
    
    return kmp_search, kmp_search_with_count, kmp_search_with_explanation

def kmp_examples():
    """KMP算法示例"""
    
    def kmp_example_1():
        """示例1: 基本匹配"""
        text = "ababcababa"
        pattern = "ababa"
        matches = kmp_search(text, pattern)
        print(f"文本: {text}")
        print(f"模式: {pattern}")
        print(f"匹配位置: {matches}")
        return matches
    
    def kmp_example_2():
        """示例2: 多个匹配"""
        text = "ababababab"
        pattern = "abab"
        matches = kmp_search(text, pattern)
        print(f"文本: {text}")
        print(f"模式: {pattern}")
        print(f"匹配位置: {matches}")
        return matches
    
    def kmp_example_3():
        """示例3: 无匹配"""
        text = "abcdefg"
        pattern = "xyz"
        matches = kmp_search(text, pattern)
        print(f"文本: {text}")
        print(f"模式: {pattern}")
        print(f"匹配位置: {matches}")
        return matches
    
    return kmp_example_1, kmp_example_2, kmp_example_3
```

### 2. 优化KMP算法
```python
def optimized_kmp_algorithm():
    """优化KMP算法实现"""
    
    def kmp_search_optimized(text, pattern):
        """优化的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        # 构建优化的失败函数
        failure = build_failure_function_optimized(pattern)
        
        # 优化的匹配过程
        matches = []
        j = 0
        
        for i in range(n):
            # 使用失败函数快速回退
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            
            if text[i] == pattern[j]:
                j += 1
            
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]
        
        return matches
    
    def kmp_search_with_early_termination(text, pattern):
        """带早期终止的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        failure = build_failure_function(pattern)
        matches = []
        j = 0
        
        for i in range(n):
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            
            if text[i] == pattern[j]:
                j += 1
            
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]
                
                # 早期终止：如果只需要第一个匹配
                if len(matches) == 1:
                    break
        
        return matches
    
    def kmp_search_with_memory_optimization(text, pattern):
        """内存优化的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        # 使用生成器减少内存使用
        def build_failure_generator(pattern):
            m = len(pattern)
            failure = [0] * m
            j = 0
            
            for i in range(1, m):
                while j > 0 and pattern[i] != pattern[j]:
                    j = failure[j - 1]
                
                if pattern[i] == pattern[j]:
                    j += 1
                
                failure[i] = j
                yield failure[i]
        
        failure = list(build_failure_generator(pattern))
        matches = []
        j = 0
        
        for i in range(n):
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            
            if text[i] == pattern[j]:
                j += 1
            
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]
        
        return matches
    
    return kmp_search_optimized, kmp_search_with_early_termination, kmp_search_with_memory_optimization
```

### 3. 高级KMP算法
```python
def advanced_kmp_algorithm():
    """高级KMP算法实现"""
    
    def kmp_search_with_wildcards(text, pattern):
        """支持通配符的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        # 构建失败函数，忽略通配符
        failure = [0] * m
        j = 0
        
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j] and pattern[i] != '?' and pattern[j] != '?':
                j = failure[j - 1]
            
            if pattern[i] == pattern[j] or pattern[i] == '?' or pattern[j] == '?':
                j += 1
            
            failure[i] = j
        
        # 匹配过程
        matches = []
        j = 0
        
        for i in range(n):
            while j > 0 and text[i] != pattern[j] and pattern[j] != '?':
                j = failure[j - 1]
            
            if text[i] == pattern[j] or pattern[j] == '?':
                j += 1
            
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]
        
        return matches
    
    def kmp_search_with_case_insensitive(text, pattern):
        """大小写不敏感的KMP算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        
        # 转换为小写
        text_lower = text.lower()
        pattern_lower = pattern.lower()
        
        # 构建失败函数
        failure = build_failure_function(pattern_lower)
        
        # 匹配过程
        matches = []
        j = 0
        
        for i in range(n):
            while j > 0 and text_lower[i] != pattern_lower[j]:
                j = failure[j - 1]
            
            if text_lower[i] == pattern_lower[j]:
                j += 1
            
            if j == m:
                matches.append(i - m + 1)
                j = failure[j - 1]
        
        return matches
    
    def kmp_search_with_multiple_patterns(text, patterns):
        """多模式串KMP算法"""
        results = {}
        
        for pattern in patterns:
            matches = kmp_search(text, pattern)
            results[pattern] = matches
        
        return results
    
    return kmp_search_with_wildcards, kmp_search_with_case_insensitive, kmp_search_with_multiple_patterns
```

## 🔧 高级应用

### 1. 文本搜索
```python
def text_search_applications():
    """文本搜索应用"""
    
    def document_search(documents, query):
        """文档搜索"""
        results = []
        
        for doc_id, document in documents.items():
            matches = kmp_search(document, query)
            if matches:
                results.append({
                    'document_id': doc_id,
                    'matches': matches,
                    'count': len(matches)
                })
        
        return results
    
    def log_analysis(logs, pattern):
        """日志分析"""
        results = []
        
        for log_entry in logs:
            matches = kmp_search(log_entry, pattern)
            if matches:
                results.append({
                    'log_entry': log_entry,
                    'matches': matches,
                    'count': len(matches)
                })
        
        return results
    
    def code_search(code_files, pattern):
        """代码搜索"""
        results = []
        
        for file_path, code in code_files.items():
            matches = kmp_search(code, pattern)
            if matches:
                results.append({
                    'file_path': file_path,
                    'matches': matches,
                    'count': len(matches)
                })
        
        return results
    
    return document_search, log_analysis, code_search
```

### 2. 模式识别
```python
def pattern_recognition_applications():
    """模式识别应用"""
    
    def dna_sequence_analysis(sequences, pattern):
        """DNA序列分析"""
        results = []
        
        for seq_id, sequence in sequences.items():
            matches = kmp_search(sequence, pattern)
            if matches:
                results.append({
                    'sequence_id': seq_id,
                    'matches': matches,
                    'count': len(matches)
                })
        
        return results
    
    def protein_sequence_analysis(sequences, pattern):
        """蛋白质序列分析"""
        results = []
        
        for protein_id, sequence in sequences.items():
            matches = kmp_search(sequence, pattern)
            if matches:
                results.append({
                    'protein_id': protein_id,
                    'matches': matches,
                    'count': len(matches)
                })
        
        return results
    
    def network_packet_analysis(packets, pattern):
        """网络包分析"""
        results = []
        
        for packet_id, packet_data in packets.items():
            matches = kmp_search(packet_data, pattern)
            if matches:
                results.append({
                    'packet_id': packet_id,
                    'matches': matches,
                    'count': len(matches)
                })
        
        return results
    
    return dna_sequence_analysis, protein_sequence_analysis, network_packet_analysis
```

### 3. 字符串处理
```python
def string_processing_applications():
    """字符串处理应用"""
    
    def string_replacement(text, pattern, replacement):
        """字符串替换"""
        matches = kmp_search(text, pattern)
        if not matches:
            return text
        
        result = []
        last_end = 0
        
        for match_pos in matches:
            result.append(text[last_end:match_pos])
            result.append(replacement)
            last_end = match_pos + len(pattern)
        
        result.append(text[last_end:])
        return ''.join(result)
    
    def string_validation(text, patterns):
        """字符串验证"""
        results = {}
        
        for pattern in patterns:
            matches = kmp_search(text, pattern)
            results[pattern] = {
                'found': len(matches) > 0,
                'count': len(matches),
                'positions': matches
            }
        
        return results
    
    def string_statistics(text, patterns):
        """字符串统计"""
        results = {}
        
        for pattern in patterns:
            matches = kmp_search(text, pattern)
            results[pattern] = {
                'count': len(matches),
                'positions': matches,
                'frequency': len(matches) / len(text) if len(text) > 0 else 0
            }
        
        return results
    
    return string_replacement, string_validation, string_statistics
```

## 📊 性能分析

### 1. 时间复杂度分析
```python
def time_complexity_analysis():
    """时间复杂度分析"""
    complexity_analysis = {
        "失败函数构建": {
            "时间复杂度": "O(m)",
            "说明": "每个字符最多被比较一次",
            "优势": "线性时间构建"
        },
        "匹配过程": {
            "时间复杂度": "O(n)",
            "说明": "每个文本字符最多被比较一次",
            "优势": "线性时间匹配"
        },
        "总体复杂度": {
            "时间复杂度": "O(m+n)",
            "说明": "预处理O(m) + 匹配O(n)",
            "优势": "比暴力算法O(mn)更高效"
        }
    }
    
    return complexity_analysis
```

### 2. 空间复杂度分析
```python
def space_complexity_analysis():
    """空间复杂度分析"""
    space_analysis = {
        "失败函数": {
            "空间复杂度": "O(m)",
            "说明": "存储模式串的失败函数",
            "影响因素": ["模式串长度"]
        },
        "匹配过程": {
            "空间复杂度": "O(1)",
            "说明": "只需要几个变量",
            "影响因素": ["算法实现"]
        },
        "总体复杂度": {
            "空间复杂度": "O(m)",
            "说明": "主要由失败函数决定",
            "优势": "空间效率高"
        }
    }
    
    return space_analysis
```

### 3. 算法选择指南
```python
def algorithm_selection_guide():
    """算法选择指南"""
    selection_guide = {
        "应用场景": {
            "文本搜索": "KMP算法",
            "模式识别": "KMP算法",
            "字符串匹配": "KMP算法",
            "DNA序列分析": "KMP算法"
        },
        "性能要求": {
            "时间优先": "KMP算法",
            "空间优先": "KMP算法",
            "实现简单": "暴力算法",
            "功能丰富": "KMP算法"
        },
        "数据特征": {
            "长文本": "KMP算法",
            "短模式": "KMP算法",
            "重复模式": "KMP算法",
            "随机文本": "KMP算法"
        }
    }
    
    return selection_guide
```

## 🔗 相关概念

### 字符串匹配
- **关系**：KMP是字符串匹配算法
- **链接**：[[02-字符串算法]]

### 动态规划
- **关系**：失败函数构建使用DP思想
- **链接**：[[02-理解层-核心思想/03-动态规划]]

### 字符串哈希
- **关系**：另一种字符串匹配方法
- **链接**：[[03-字符串哈希]]

### 后缀数组
- **关系**：另一种字符串处理技术
- **链接**：[[04-后缀数组]]

### AC自动机
- **关系**：多模式串匹配算法
- **链接**：[[05-AC自动机]]

## 📚 学习建议

### 费曼学习法
1. **选择概念**：KMP算法
2. **教授他人**：解释KMP算法的原理和实现
3. **回顾简化**：找出理解不足
4. **重新组织**：用更简单的方式表达

### 刻意练习
1. **实现练习**：实现KMP算法
2. **应用练习**：解决字符串匹配问题
3. **优化练习**：优化算法性能
4. **对比练习**：对比不同字符串匹配算法

## 🔗 相关链接
- [[02-字符串算法]] - 字符串算法
- [[02-理解层-核心思想/03-动态规划]] - 动态规划
- [[03-字符串哈希]] - 字符串哈希
- [[04-后缀数组]] - 后缀数组
- [[05-AC自动机]] - AC自动机
