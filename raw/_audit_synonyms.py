"""Detect probable synonyms / name conflicts in vault."""
import json
import re
from pathlib import Path
from collections import defaultdict

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

files = []
for p in wiki.rglob('*.md'):
    files.append(p.stem)

# Look for prefix/suffix overlaps: A vs A+something
synonyms = []

# Strategy 1: stems where one is a substring of another, both >= 3 chars,
# and the longer is <= 1.5x the shorter (so 互惠 vs 互惠原则, but not 互惠 vs 互惠原则的应用)
for i, a in enumerate(files):
    if len(a) < 3:
        continue
    for b in files:
        if b == a:
            continue
        if len(b) < len(a) + 1 or len(b) > len(a) * 2 + 4:
            continue
        if a in b:
            # Common pattern: A 和 A+(原则|理论|效应|模型|思维|偏差|定律|法则|分析)
            suffix = b.replace(a, '', 1)
            common = ['原则', '理论', '效应', '模型', '思维', '偏差', '定律', '法则', '分析', '方法', '现象', '能力', '主义', '论', '学', '法', '流派', '家']
            if any(suffix.startswith(s) or suffix.endswith(s) or suffix == s for s in common):
                synonyms.append((a, b, suffix))

# Dedupe
seen = set()
unique = []
for a, b, s in synonyms:
    key = tuple(sorted([a, b]))
    if key not in seen:
        seen.add(key)
        unique.append((a, b, s))

# Output
out_lines = [f'# 可能同义/重叠的概念对(共 {len(unique)} 对)\n']
out_lines.append('每对都需要人工判断是否合并、保留差异、或交叉链接\n')
out_lines.append('---\n')
for a, b, suffix in unique:
    out_lines.append(f'- [[{a}]]  ↔  [[{b}]]')

(vault / 'raw' / '_audit_synonyms.txt').write_text('\n'.join(out_lines), encoding='utf-8')
print(f'Found {len(unique)} possible synonym pairs')
print('Saved to raw/_audit_synonyms.txt')
