"""Task 1: Fix typos and unify multi-form wikilinks across vault."""
import re
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')

# Replacement map: target → canonical
# Format: (old_pattern, new_pattern)
replacements = [
    # Lollapalooga (typo, missing z) → Lollapalooza
    ('[[Lollapalooga效应]]', '[[Lollapalooza效应]]'),
    ('[[Lollapalooga 效应]]', '[[Lollapalooza效应]]'),
    # Al Ries — unify to canonical 艾·里斯Al Ries (no space)
    ('[[艾·里斯 Al Ries]]', '[[艾·里斯Al Ries]]'),
    ('[[Al Ries]]', '[[艾·里斯Al Ries|Al Ries]]'),
    # Jack Trout — unify to 杰克·特劳特Jack Trout (no space)
    ('[[杰克·特劳特 Jack Trout]]', '[[杰克·特劳特Jack Trout]]'),
    ('[[Jack Trout]]', '[[杰克·特劳特Jack Trout|Jack Trout]]'),
]

# Scan all wiki and output md files
total_replaced = 0
files_changed = []

for d in [vault / 'wiki', vault / 'output']:
    if not d.exists():
        continue
    for p in d.rglob('*.md'):
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            count = sum(text.count(new) - original.count(new) for old, new in replacements)
            files_changed.append((p, count))
            total_replaced += count
            p.write_text(text, encoding='utf-8')

print(f'Files modified: {len(files_changed)}')
print(f'Total wikilink replacements: {total_replaced}')
print()
print('Sample files changed:')
for p, c in files_changed[:15]:
    rel = p.relative_to(vault)
    print(f'  {c}x  {rel}')
