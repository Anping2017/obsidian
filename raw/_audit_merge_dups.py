"""Task 5a: Merge confirmed duplicate pairs.

Strategy:
1. Delete the shorter file (less detailed)
2. Replace [[shorter]] with [[longer|shorter]] across vault to preserve display
"""
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')

# (delete_this, replace_with) pairs
merges = [
    ('NPS', 'NPS净推荐值'),
    ('Transformer', 'Transformer架构'),
    ('儿童发展', '儿童发展心理学'),
]

# For each merge, do the replacement vault-wide
total_replaced = 0
files_changed = set()

for delete_stem, keep_stem in merges:
    delete_path = vault / 'wiki' / 'concepts' / f'{delete_stem}.md'
    keep_path = vault / 'wiki' / 'concepts' / f'{keep_stem}.md'
    if not delete_path.exists() or not keep_path.exists():
        print(f'SKIP {delete_stem} → {keep_stem}: missing file')
        continue

    # Replace [[delete_stem]] (without alias) with [[keep_stem|delete_stem]] across vault
    # Note: must be careful not to change [[delete_stem|alias]] or [[other_stem delete_stem]]
    pattern = f'[[{delete_stem}]]'
    replacement = f'[[{keep_stem}|{delete_stem}]]'

    for d in [vault / 'wiki', vault / 'output']:
        if not d.exists():
            continue
        for p in d.rglob('*.md'):
            # Skip the file we're about to delete
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
                total_replaced += count
                files_changed.add(str(p.relative_to(vault)))

    # Now delete the duplicate file
    delete_path.unlink()
    print(f'Merged: deleted {delete_stem}.md, kept {keep_stem}.md')

print(f'\nTotal wikilink replacements: {total_replaced}')
print(f'Files changed: {len(files_changed)}')
