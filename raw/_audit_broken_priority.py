"""Extract broken links prioritized by reference count + classify."""
import json
import re
from pathlib import Path
from collections import defaultdict

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
data = json.loads((vault / 'raw' / '_audit_report.json').read_text(encoding='utf-8'))

# Re-scan for full broken list (not just top30)
wiki = vault / 'wiki'
files = {p.stem for p in wiki.rglob('*.md')}
wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')

broken = defaultdict(lambda: {'count': 0, 'sources': set()})

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
            broken[target]['count'] += 1
            broken[target]['sources'].add(p.stem)

# Filter heuristics for "worth creating"
# Skip: looks like a person name (中·中, foreign person), already aliased forms, etc.
def is_person_likely(target: str) -> bool:
    # Chinese names often have ·
    if '·' in target and len(target) <= 8:
        return True
    # All-Latin single capitalized word like "Hinton", "Marx", "Aaker"
    if re.match(r'^[A-Z][a-z]+$', target) and len(target) < 10:
        return True
    return False

def is_skip(target: str) -> bool:
    # Skip obvious junk / template artifacts
    if target.startswith(('wiki', 'output', 'raw', 'http')):
        return True
    # Single character or very weird
    if len(target) < 2:
        return True
    return False

# Sort by count desc
items = sorted(broken.items(), key=lambda x: -x[1]['count'])

# Group by category
high_concept = []  # >= 4 refs, looks like concept
mid_concept = []   # 2-3 refs
person_likely = []
unsure = []

for target, info in items:
    if is_skip(target):
        continue
    if is_person_likely(target):
        person_likely.append((target, info['count']))
        continue
    if info['count'] >= 4:
        high_concept.append((target, info['count'], list(info['sources'])[:3]))
    elif info['count'] >= 2:
        mid_concept.append((target, info['count'], list(info['sources'])[:3]))
    else:
        unsure.append((target, info['count']))

out_lines = []
out_lines.append(f'# Broken Links Priority Triage\n')
out_lines.append(f'Total broken: {len(broken)}')
out_lines.append(f'  High-priority concepts (≥4 refs): {len(high_concept)}')
out_lines.append(f'  Mid-priority concepts (2-3 refs): {len(mid_concept)}')
out_lines.append(f'  Likely persons: {len(person_likely)}')
out_lines.append(f'  Singleton/uncertain (1 ref): {len(unsure)}')
out_lines.append('')
out_lines.append('## P1: High-priority (≥4 refs) — WRITE NOW')
out_lines.append('')
for t, c, srcs in high_concept:
    out_lines.append(f'- **{t}** ({c}x)  ← from {", ".join(srcs[:2])}')
out_lines.append('')
out_lines.append('## P2: Mid-priority (2-3 refs)')
out_lines.append('')
for t, c, srcs in mid_concept:
    out_lines.append(f'- {t} ({c}x)')
out_lines.append('')
out_lines.append('## P3: Likely persons (would need entity page, not concept)')
out_lines.append('')
for t, c in person_likely[:50]:
    out_lines.append(f'- {t} ({c}x)')

(vault / 'raw' / '_audit_priority.txt').write_text('\n'.join(out_lines), encoding='utf-8')
print(f'Total: {len(broken)} broken')
print(f'P1 (high-priority concept, ≥4 refs): {len(high_concept)}')
print(f'P2 (mid-priority concept, 2-3 refs): {len(mid_concept)}')
print(f'P3 (likely persons): {len(person_likely)}')
print(f'P4 (singleton, 1 ref): {len(unsure)}')
print(f'Saved: raw/_audit_priority.txt')
