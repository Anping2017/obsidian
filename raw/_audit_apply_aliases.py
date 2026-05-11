"""Phase A: Apply safe alias replacements vault-wide."""
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')

# (broken_target, replacement_file_stem) — only semantically safe ones
safe_aliases = [
    ('CRM', 'CRM客户关系管理'),
    ('SwiftUI', 'SwiftUI与UIKit'),
    ('MUM', 'MUM多任务统一模型'),
    ('Java', 'Java JVM'),
    ('Gemini', 'Gemini系列模型'),
    ('Hinton', 'Geoffrey Hinton'),
    ('Local Pack', 'Local Pack本地包'),
    ('JavaScript', 'JavaScript原型链'),
    ('阿奎那', '托马斯·阿奎那'),
    ('ROI', '营销ROI'),
    ('KPI体系', '销售KPI体系'),
    ('KOL', 'KOL营销'),
    ('JVM', 'Java JVM'),
    ('HumanEval', 'HumanEval基准'),
    ('新零售', '新零售融合'),
    ('抖音算法', '抖音算法分发'),
    ('现金流', '现金流量表'),
    ('Apple生态', 'Apple生态系统'),
    ('推荐系统', '个性化推荐系统'),
    ('存货', '存货计价方法'),
    ('TypeScript', 'TypeScript类型系统'),
]

# Verify all replacements exist as files
wiki = vault / 'wiki'
existing = {p.stem for p in wiki.rglob('*.md')}
for target, repl in safe_aliases:
    if repl not in existing:
        print(f'WARN: replacement {repl} does not exist as file')

total_replaced = 0
files_changed = set()

for delete_target, keep_stem in safe_aliases:
    pattern = f'[[{delete_target}]]'
    replacement = f'[[{keep_stem}|{delete_target}]]'

    for d in [vault / 'wiki', vault / 'output']:
        if not d.exists():
            continue
        for p in d.rglob('*.md'):
            try:
                text = p.read_text(encoding='utf-8')
            except Exception:
                continue
            if pattern in text:
                count = text.count(pattern)
                new_text = text.replace(pattern, replacement)
                p.write_text(new_text, encoding='utf-8')
                total_replaced += count
                files_changed.add(str(p.relative_to(vault)))

print(f'\nAliases applied: {len(safe_aliases)}')
print(f'Wikilink occurrences replaced: {total_replaced}')
print(f'Files changed: {len(files_changed)}')
