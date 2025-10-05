# Rabin-Karp算法

## 🎯 核心概念

**Rabin-Karp算法**是一种基于哈希的字符串匹配算法，通过计算模式串和文本子串的哈希值来进行快速匹配。该算法的核心思想是利用滚动哈希技术，在O(1)时间内计算相邻子串的哈希值，从而将时间复杂度优化到O(m+n)。

## 🔍 算法原理

### 1. 基本思想
```python
def rabin_karp_concept():
    """Rabin-Karp算法基本思想"""
    # 1. 哈希函数：将字符串映射为数值
    # 2. 滚动哈希：利用前一个哈希值计算下一个
    # 3. 哈希冲突：使用双重哈希或重新验证
    # 4. 时间复杂度：O(m+n)，最坏情况O(mn)
    
    pass

def rabin_karp_properties():
    """Rabin-Karp算法性质"""
    properties = {
        "时间复杂度": "O(m+n) 平均，O(mn) 最坏",
        "空间复杂度": "O(1)",
        "哈希函数": "多项式哈希",
        "滚动哈希": "O(1)时间计算相邻子串哈希",
        "冲突处理": "双重哈希或重新验证",
        "应用场景": ["字符串匹配", "模式识别", "文本搜索"]
    }
    return properties
```

### 2. 哈希函数设计
```python
def hash_function_design():
    """哈希函数设计"""
    
    def polynomial_hash(text, base=256, mod=1000000007):
        """多项式哈希函数"""
        hash_value = 0
        for char in text:
            hash_value = (hash_value * base + ord(char)) % mod
        return hash_value
    
    def rolling_hash(text, pattern_length, base=256, mod=1000000007):
        """滚动哈希函数"""
        n = len(text)
        m = pattern_length
        
        if n < m:
            return []
        
        # 计算base^(m-1) mod mod
        base_power = pow(base, m - 1, mod)
        
        # 计算第一个子串的哈希值
        pattern_hash = 0
        for i in range(m):
            pattern_hash = (pattern_hash * base + ord(text[i])) % mod
        
        # 计算文本的滚动哈希
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text[i])) % mod
        
        # 滚动计算
        hashes = [text_hash]
        for i in range(m, n):
            # 移除最左边的字符
            text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            # 添加最右边的字符
            text_hash = (text_hash * base + ord(text[i])) % mod
            hashes.append(text_hash)
        
        return hashes
    
    def double_hash(text, pattern_length, base1=256, mod1=1000000007, base2=257, mod2=1000000009):
        """双重哈希函数"""
        n = len(text)
        m = pattern_length
        
        if n < m:
            return []
        
        # 计算base1^(m-1) mod mod1
        base1_power = pow(base1, m - 1, mod1)
        base2_power = pow(base2, m - 1, mod2)
        
        # 计算第一个子串的双重哈希值
        hash1 = 0
        hash2 = 0
        for i in range(m):
            hash1 = (hash1 * base1 + ord(text[i])) % mod1
            hash2 = (hash2 * base2 + ord(text[i])) % mod2
        
        # 滚动计算
        hashes = [(hash1, hash2)]
        for i in range(m, n):
            # 移除最左边的字符
            hash1 = (hash1 - ord(text[i - m]) * base1_power) % mod1
            hash2 = (hash2 - ord(text[i - m]) * base2_power) % mod2
            # 添加最右边的字符
            hash1 = (hash1 * base1 + ord(text[i])) % mod1
            hash2 = (hash2 * base2 + ord(text[i])) % mod2
            hashes.append((hash1, hash2))
        
        return hashes
    
    return polynomial_hash, rolling_hash, double_hash

def hash_function_examples():
    """哈希函数示例"""
    
    def hash_example_1():
        """示例1: 基本哈希"""
        text = "hello"
        hash_value = polynomial_hash(text)
        print(f"文本: {text}")
        print(f"哈希值: {hash_value}")
        return hash_value
    
    def hash_example_2():
        """示例2: 滚动哈希"""
        text = "ababcababa"
        pattern_length = 3
        hashes = rolling_hash(text, pattern_length)
        print(f"文本: {text}")
        print(f"模式长度: {pattern_length}")
        print(f"滚动哈希: {hashes}")
        return hashes
    
    def hash_example_3():
        """示例3: 双重哈希"""
        text = "ababcababa"
        pattern_length = 3
        hashes = double_hash(text, pattern_length)
        print(f"文本: {text}")
        print(f"模式长度: {pattern_length}")
        print(f"双重哈希: {hashes}")
        return hashes
    
    return hash_example_1, hash_example_2, hash_example_3
```

## 🎨 算法实现

### 1. 基本Rabin-Karp算法
```python
def rabin_karp_algorithm():
    """Rabin-Karp算法实现"""
    
    def rabin_karp_search(text, pattern):
        """Rabin-Karp字符串匹配算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        base = 256
        mod = 1000000007
        
        # 计算base^(m-1) mod mod
        base_power = pow(base, m - 1, mod)
        
        # 计算模式串的哈希值
        pattern_hash = 0
        for char in pattern:
            pattern_hash = (pattern_hash * base + ord(char)) % mod
        
        # 计算第一个文本子串的哈希值
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text[i])) % mod
        
        # 匹配过程
        matches = []
        
        # 检查第一个子串
        if text_hash == pattern_hash:
            if text[:m] == pattern:
                matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            # 移除最左边的字符
            text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            # 添加最右边的字符
            text_hash = (text_hash * base + ord(text[i])) % mod
            
            # 检查哈希值是否匹配
            if text_hash == pattern_hash:
                if text[i - m + 1:i + 1] == pattern:
                    matches.append(i - m + 1)
        
        return matches
    
    def rabin_karp_search_with_count(text, pattern):
        """带计数器的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)], 0
        if n < m:
            return [], 0
        
        base = 256
        mod = 1000000007
        base_power = pow(base, m - 1, mod)
        
        # 计算模式串哈希值
        pattern_hash = 0
        for char in pattern:
            pattern_hash = (pattern_hash * base + ord(char)) % mod
        
        # 计算第一个文本子串哈希值
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text[i])) % mod
        
        matches = []
        hash_comparisons = 0
        string_comparisons = 0
        
        # 检查第一个子串
        hash_comparisons += 1
        if text_hash == pattern_hash:
            string_comparisons += 1
            if text[:m] == pattern:
                matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            text_hash = (text_hash * base + ord(text[i])) % mod
            
            hash_comparisons += 1
            if text_hash == pattern_hash:
                string_comparisons += 1
                if text[i - m + 1:i + 1] == pattern:
                    matches.append(i - m + 1)
        
        return matches, hash_comparisons + string_comparisons
    
    def rabin_karp_search_with_explanation(text, pattern):
        """带解释的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        base = 256
        mod = 1000000007
        base_power = pow(base, m - 1, mod)
        
        print(f"在文本 '{text}' 中搜索模式 '{pattern}'")
        print(f"基数: {base}, 模数: {mod}")
        
        # 计算模式串哈希值
        pattern_hash = 0
        for char in pattern:
            pattern_hash = (pattern_hash * base + ord(char)) % mod
        print(f"模式串哈希值: {pattern_hash}")
        
        # 计算第一个文本子串哈希值
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text[i])) % mod
        print(f"第一个子串哈希值: {text_hash}")
        
        matches = []
        
        # 检查第一个子串
        if text_hash == pattern_hash:
            print(f"哈希值匹配，验证字符串: '{text[:m]}' == '{pattern}'")
            if text[:m] == pattern:
                matches.append(0)
                print(f"找到匹配，位置: 0")
        
        # 滚动匹配
        for i in range(m, n):
            old_char = text[i - m]
            new_char = text[i]
            text_hash = (text_hash - ord(old_char) * base_power) % mod
            text_hash = (text_hash * base + ord(new_char)) % mod
            
            print(f"位置 {i}: 移除 '{old_char}', 添加 '{new_char}', 新哈希值: {text_hash}")
            
            if text_hash == pattern_hash:
                substring = text[i - m + 1:i + 1]
                print(f"哈希值匹配，验证字符串: '{substring}' == '{pattern}'")
                if substring == pattern:
                    matches.append(i - m + 1)
                    print(f"找到匹配，位置: {i - m + 1}")
        
        return matches
    
    return rabin_karp_search, rabin_karp_search_with_count, rabin_karp_search_with_explanation

def rabin_karp_examples():
    """Rabin-Karp算法示例"""
    
    def rabin_karp_example_1():
        """示例1: 基本匹配"""
        text = "ababcababa"
        pattern = "aba"
        matches = rabin_karp_search(text, pattern)
        print(f"文本: {text}")
        print(f"模式: {pattern}")
        print(f"匹配位置: {matches}")
        return matches
    
    def rabin_karp_example_2():
        """示例2: 多个匹配"""
        text = "ababababab"
        pattern = "abab"
        matches = rabin_karp_search(text, pattern)
        print(f"文本: {text}")
        print(f"模式: {pattern}")
        print(f"匹配位置: {matches}")
        return matches
    
    def rabin_karp_example_3():
        """示例3: 无匹配"""
        text = "abcdefg"
        pattern = "xyz"
        matches = rabin_karp_search(text, pattern)
        print(f"文本: {text}")
        print(f"模式: {pattern}")
        print(f"匹配位置: {matches}")
        return matches
    
    return rabin_karp_example_1, rabin_karp_example_2, rabin_karp_example_3
```

### 2. 优化Rabin-Karp算法
```python
def optimized_rabin_karp_algorithm():
    """优化Rabin-Karp算法实现"""
    
    def rabin_karp_search_optimized(text, pattern):
        """优化的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        # 使用更大的基数和模数
        base = 256
        mod = 1000000007
        
        base_power = pow(base, m - 1, mod)
        
        # 计算模式串哈希值
        pattern_hash = 0
        for char in pattern:
            pattern_hash = (pattern_hash * base + ord(char)) % mod
        
        # 计算第一个文本子串哈希值
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text[i])) % mod
        
        matches = []
        
        # 检查第一个子串
        if text_hash == pattern_hash and text[:m] == pattern:
            matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            text_hash = (text_hash * base + ord(text[i])) % mod
            
            if text_hash == pattern_hash and text[i - m + 1:i + 1] == pattern:
                matches.append(i - m + 1)
        
        return matches
    
    def rabin_karp_search_with_double_hash(text, pattern):
        """使用双重哈希的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        base1, mod1 = 256, 1000000007
        base2, mod2 = 257, 1000000009
        
        base1_power = pow(base1, m - 1, mod1)
        base2_power = pow(base2, m - 1, mod2)
        
        # 计算模式串双重哈希值
        pattern_hash1 = 0
        pattern_hash2 = 0
        for char in pattern:
            pattern_hash1 = (pattern_hash1 * base1 + ord(char)) % mod1
            pattern_hash2 = (pattern_hash2 * base2 + ord(char)) % mod2
        
        # 计算第一个文本子串双重哈希值
        text_hash1 = 0
        text_hash2 = 0
        for i in range(m):
            text_hash1 = (text_hash1 * base1 + ord(text[i])) % mod1
            text_hash2 = (text_hash2 * base2 + ord(text[i])) % mod2
        
        matches = []
        
        # 检查第一个子串
        if text_hash1 == pattern_hash1 and text_hash2 == pattern_hash2:
            if text[:m] == pattern:
                matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            text_hash1 = (text_hash1 - ord(text[i - m]) * base1_power) % mod1
            text_hash2 = (text_hash2 - ord(text[i - m]) * base2_power) % mod2
            text_hash1 = (text_hash1 * base1 + ord(text[i])) % mod1
            text_hash2 = (text_hash2 * base2 + ord(text[i])) % mod2
            
            if text_hash1 == pattern_hash1 and text_hash2 == pattern_hash2:
                if text[i - m + 1:i + 1] == pattern:
                    matches.append(i - m + 1)
        
        return matches
    
    def rabin_karp_search_with_early_termination(text, pattern):
        """带早期终止的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        base = 256
        mod = 1000000007
        base_power = pow(base, m - 1, mod)
        
        pattern_hash = 0
        for char in pattern:
            pattern_hash = (pattern_hash * base + ord(char)) % mod
        
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text[i])) % mod
        
        matches = []
        
        # 检查第一个子串
        if text_hash == pattern_hash and text[:m] == pattern:
            matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            text_hash = (text_hash * base + ord(text[i])) % mod
            
            if text_hash == pattern_hash and text[i - m + 1:i + 1] == pattern:
                matches.append(i - m + 1)
                
                # 早期终止：如果只需要第一个匹配
                if len(matches) == 1:
                    break
        
        return matches
    
    return rabin_karp_search_optimized, rabin_karp_search_with_double_hash, rabin_karp_search_with_early_termination
```

### 3. 高级Rabin-Karp算法
```python
def advanced_rabin_karp_algorithm():
    """高级Rabin-Karp算法实现"""
    
    def rabin_karp_search_with_wildcards(text, pattern):
        """支持通配符的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        base = 256
        mod = 1000000007
        base_power = pow(base, m - 1, mod)
        
        # 计算模式串哈希值，忽略通配符
        pattern_hash = 0
        for char in pattern:
            if char != '?':
                pattern_hash = (pattern_hash * base + ord(char)) % mod
        
        # 计算第一个文本子串哈希值
        text_hash = 0
        for i in range(m):
            if pattern[i] != '?':
                text_hash = (text_hash * base + ord(text[i])) % mod
        
        matches = []
        
        # 检查第一个子串
        if text_hash == pattern_hash:
            if text[:m] == pattern or all(pattern[j] == '?' or text[j] == pattern[j] for j in range(m)):
                matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            if pattern[0] != '?':
                text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            if pattern[i - m] != '?':
                text_hash = (text_hash - ord(text[i - m]) * base_power) % mod
            if pattern[i] != '?':
                text_hash = (text_hash * base + ord(text[i])) % mod
            
            if text_hash == pattern_hash:
                if all(pattern[j] == '?' or text[i - m + 1 + j] == pattern[j] for j in range(m)):
                    matches.append(i - m + 1)
        
        return matches
    
    def rabin_karp_search_with_case_insensitive(text, pattern):
        """大小写不敏感的Rabin-Karp算法"""
        n, m = len(text), len(pattern)
        if m == 0:
            return [i for i in range(n + 1)]
        if n < m:
            return []
        
        # 转换为小写
        text_lower = text.lower()
        pattern_lower = pattern.lower()
        
        base = 256
        mod = 1000000007
        base_power = pow(base, m - 1, mod)
        
        # 计算模式串哈希值
        pattern_hash = 0
        for char in pattern_lower:
            pattern_hash = (pattern_hash * base + ord(char)) % mod
        
        # 计算第一个文本子串哈希值
        text_hash = 0
        for i in range(m):
            text_hash = (text_hash * base + ord(text_lower[i])) % mod
        
        matches = []
        
        # 检查第一个子串
        if text_hash == pattern_hash:
            if text_lower[:m] == pattern_lower:
                matches.append(0)
        
        # 滚动匹配
        for i in range(m, n):
            text_hash = (text_hash - ord(text_lower[i - m]) * base_power) % mod
            text_hash = (text_hash * base + ord(text_lower[i])) % mod
            
            if text_hash == pattern_hash:
                if text_lower[i - m + 1:i + 1] == pattern_lower:
                    matches.append(i - m + 1)
        
        return matches
    
    def rabin_karp_search_with_multiple_patterns(text, patterns):
        """多模式串Rabin-Karp算法"""
        results = {}
        
        for pattern in patterns:
            matches = rabin_karp_search(text, pattern)
            results[pattern] = matches
        
        return results
    
    return rabin_karp_search_with_wildcards, rabin_karp_search_with_case_insensitive, rabin_karp_search_with_multiple_patterns
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
            matches = rabin_karp_search(document, query)
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
            matches = rabin_karp_search(log_entry, pattern)
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
            matches = rabin_karp_search(code, pattern)
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
            matches = rabin_karp_search(sequence, pattern)
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
            matches = rabin_karp_search(sequence, pattern)
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
            matches = rabin_karp_search(packet_data, pattern)
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
        matches = rabin_karp_search(text, pattern)
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
            matches = rabin_karp_search(text, pattern)
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
            matches = rabin_karp_search(text, pattern)
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
        "哈希计算": {
            "时间复杂度": "O(m)",
            "说明": "计算模式串和第一个子串的哈希值",
            "优势": "线性时间计算"
        },
        "滚动哈希": {
            "时间复杂度": "O(1)",
            "说明": "每个子串的哈希值在O(1)时间内计算",
            "优势": "常数时间更新"
        },
        "总体复杂度": {
            "时间复杂度": "O(m+n) 平均，O(mn) 最坏",
            "说明": "预处理O(m) + 匹配O(n) + 冲突处理",
            "优势": "平均情况下比暴力算法更高效"
        }
    }
    
    return complexity_analysis
```

### 2. 空间复杂度分析
```python
def space_complexity_analysis():
    """空间复杂度分析"""
    space_analysis = {
        "哈希值存储": {
            "空间复杂度": "O(1)",
            "说明": "只需要存储几个哈希值变量",
            "影响因素": ["算法实现"]
        },
        "匹配结果": {
            "空间复杂度": "O(k)",
            "说明": "存储匹配位置，k为匹配数量",
            "影响因素": ["匹配数量"]
        },
        "总体复杂度": {
            "空间复杂度": "O(1)",
            "说明": "主要由哈希值变量决定",
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
            "文本搜索": "Rabin-Karp算法",
            "模式识别": "Rabin-Karp算法",
            "字符串匹配": "Rabin-Karp算法",
            "DNA序列分析": "Rabin-Karp算法"
        },
        "性能要求": {
            "时间优先": "Rabin-Karp算法",
            "空间优先": "Rabin-Karp算法",
            "实现简单": "暴力算法",
            "功能丰富": "Rabin-Karp算法"
        },
        "数据特征": {
            "长文本": "Rabin-Karp算法",
            "短模式": "Rabin-Karp算法",
            "重复模式": "Rabin-Karp算法",
            "随机文本": "Rabin-Karp算法"
        }
    }
    
    return selection_guide
```

## 🔗 相关概念

### 字符串匹配
- **关系**：Rabin-Karp是字符串匹配算法
- **链接**：[[02-字符串算法]]

### 哈希函数
- **关系**：Rabin-Karp使用哈希函数
- **链接**：[[03-字符串哈希]]

### 滚动哈希
- **关系**：Rabin-Karp的核心技术
- **链接**：[[03-字符串哈希]]

### KMP算法
- **关系**：另一种字符串匹配算法
- **链接**：[[01-KMP算法]]

### AC自动机
- **关系**：多模式串匹配算法
- **链接**：[[05-AC自动机]]

## 📚 学习建议

### 费曼学习法
1. **选择概念**：Rabin-Karp算法
2. **教授他人**：解释Rabin-Karp算法的原理和实现
3. **回顾简化**：找出理解不足
4. **重新组织**：用更简单的方式表达

### 刻意练习
1. **实现练习**：实现Rabin-Karp算法
2. **应用练习**：解决字符串匹配问题
3. **优化练习**：优化算法性能
4. **对比练习**：对比不同字符串匹配算法

## 🔗 相关链接
- [[02-字符串算法]] - 字符串算法
- [[03-字符串哈希]] - 字符串哈希
- [[01-KMP算法]] - KMP算法
- [[05-AC自动机]] - AC自动机
