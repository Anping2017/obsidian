"""Round 2 merges: 7 duplicate pairs."""
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')

# (delete_this_stem, keep_this_stem) — keep the larger / more standard one
merges = [
    ('Kafka', 'Apache Kafka'),
    ('Service Mesh', '服务网格'),
    ('量化宽松QE', '量化宽松'),
    ('Fintech 监管沙盒', 'Fintech监管沙盒'),
    ('订阅经济', '订阅商业模式'),
    ('波特五力模型', 'Porter五力模型'),
    ('Tandem 语伴', 'Tandem语伴'),
]

total_replaced = 0
files_changed = set()
deleted = []
skipped = []

for delete_stem, keep_stem in merges:
    delete_path = vault / 'wiki' / 'concepts' / f'{delete_stem}.md'
    keep_path = vault / 'wiki' / 'concepts' / f'{keep_stem}.md'
    if not delete_path.exists():
        skipped.append(f'{delete_stem}.md (delete path missing)')
        continue
    if not keep_path.exists():
        skipped.append(f'{keep_stem}.md (keep path missing)')
        continue

    pattern = f'[[{delete_stem}]]'
    replacement = f'[[{keep_stem}|{delete_stem}]]'
    pair_replaced = 0

    for d in [vault / 'wiki', vault / 'output']:
        if not d.exists():
            continue
        for p in d.rglob('*.md'):
            if p == delete_path:
                continue
            try:
                text = p.read_text(encoding='utf-8')
            except Exception:
                continue
            if pattern in text:
                count = text.count(pattern)
                new_text = text.replace(pattern, replacement)
                p.write_text(new_text, encoding='utf-8')
                pair_replaced += count
                files_changed.add(str(p.relative_to(vault)))

    delete_path.unlink()
    deleted.append((delete_stem, keep_stem, pair_replaced))
    total_replaced += pair_replaced

print('Merged pairs (delete → keep, [refs updated]):')
for d, k, c in deleted:
    print(f'  {d}.md → {k}.md  ({c} refs)')
if skipped:
    print(f'\nSkipped: {skipped}')
print(f'\nTotal: {len(deleted)} files deleted, {total_replaced} wikilinks updated, {len(files_changed)} files touched')
