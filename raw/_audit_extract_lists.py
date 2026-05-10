"""Extract precise lists for Task 2 (Chinese high-ref) and Task 3 (English abbreviations)."""
import json
import re
from pathlib import Path
from collections import defaultdict

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

files = {p.stem for p in wiki.rglob('*.md')}
wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')

broken = defaultdict(list)

for p in wiki.rglob('*.md'):
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    if text.startswith('---'):
        end = text.find('---', 4)
        if end > 0:
            text = text[end+3:]
    for m in wikilink_re.finditer(text):
        target = m.group(1).strip()
        if not target or target.startswith(('http', '/')) or '/' in target or '.md' in target.lower():
            continue
        if target not in files:
            broken[target].append(p.stem)

# Classify
chinese_high = []  # >= 3 refs, mostly Chinese
english_abbrev = []  # all-uppercase or mixed-case English, short
english_long = []  # English-only, longer
has_space = []
has_parens = []

for target, sources in broken.items():
    refs = len(sources)
    if any(c in target for c in ['(', ')', '(', ')']):
        has_parens.append((target, refs))
        continue
    if ' ' in target:
        has_space.append((target, refs))
        continue
    # Pure English
    if re.match(r'^[A-Za-z][A-Za-z0-9\-\.]+$', target):
        if len(target) <= 8 and re.match(r'^[A-Z]+', target):
            english_abbrev.append((target, refs))
        else:
            english_long.append((target, refs))
        continue
    # Chinese-mostly
    if refs >= 3:
        chinese_high.append((target, refs))

# Sort
chinese_high.sort(key=lambda x: -x[1])
english_abbrev.sort(key=lambda x: -x[1])

# Output as plain text lists
out = []
out.append('# Task 2: 中文高频断链清单\n')
out.append(f'共 {len(chinese_high)} 个,被引用 ≥ 3 次的中文概念,需要建 wiki/concepts/<名>.md\n')
for t, r in chinese_high:
    out.append(f'- {t}  ({r}x)')
out.append('')
out.append('---\n')
out.append('# Task 3: 英文缩写断链清单\n')
out.append(f'共 {len(english_abbrev)} 个,需要建 wiki/concepts/<缩写>.md\n')
for t, r in english_abbrev:
    out.append(f'- {t}  ({r}x)')

(vault / 'raw' / '_audit_task2_3_lists.txt').write_text('\n'.join(out), encoding='utf-8')
print(f'Task 2 (Chinese high-ref): {len(chinese_high)} items')
print(f'Task 3 (English abbreviations): {len(english_abbrev)} items')
print(f'Saved to raw/_audit_task2_3_lists.txt')
