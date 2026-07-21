"""Round 2 dedup: find near-duplicate filename pairs and content-similar files."""
import re
from pathlib import Path
from itertools import combinations

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
concepts = vault / 'wiki' / 'concepts'

files = list(concepts.glob('*.md'))
stems = {p.stem: p for p in files}

def normalize(s):
    """Strip common suffixes/spaces to find near-dups."""
    s = s.replace(' ', '').replace('-', '').lower()
    # strip common Chinese descriptive suffixes
    for suf in ['架构', '模型', '系统', '运营', '心理学', '定律', '原则', '融合', '学派', '方法', '框架']:
        if s.endswith(suf.lower()):
            s2 = s[:-len(suf)]
            if len(s2) >= 2:
                s = s2
    return s

# Group by normalized stem
groups = {}
for stem in stems:
    n = normalize(stem)
    groups.setdefault(n, []).append(stem)

# Known suspicious pairs (one stem is substring of another, or English vs Chinese)
print('=== Candidate duplicate groups (normalized collision) ===')
dup_groups = {n: g for n, g in groups.items() if len(g) > 1}
for n, g in sorted(dup_groups.items()):
    print(f'  [{n}] → {g}')

print()
print('=== Substring pairs (one name contains another, both concepts) ===')
# Specific known session dups
known = [
    ('Apache Kafka', 'Kafka'),
    ('Service Mesh', '服务网格'),
    ('量化宽松QE', '量化宽松'),
    ('Fintech 监管沙盒', 'Fintech监管沙盒'),
    ('订阅经济', '订阅商业模式'),
    ('Porter五力模型', '波特五力模型'),
    ('Tandem 语伴', 'Tandem语伴'),
    ('Apache Flink', 'Flink'),
    ('品牌资产', '品牌权益'),
    ('检索增强生成', 'RAG'),
]
for a, b in known:
    ea = 'Y' if a in stems else '-'
    eb = 'Y' if b in stems else '-'
    print(f'  [{ea}] {a}  vs  [{eb}] {b}')
