"""Find broken targets that have an obvious alias candidate already in vault."""
import json
import re
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

# All file stems
files = {p.stem: p for p in wiki.rglob('*.md')}

# Broken targets and refcounts
import re
wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')

from collections import defaultdict
broken = defaultdict(int)
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
            broken[target] += 1

# For each broken, find candidate alias: a file whose stem contains the broken target
def find_alias(target):
    candidates = []
    for stem in files:
        if target == stem:
            continue
        # Substring match (target inside stem)
        if target in stem and len(stem) > len(target):
            candidates.append(stem)
    # Prefer shortest match (most similar in scope)
    candidates.sort(key=lambda s: len(s))
    return candidates[:3]

# Output aliasing plan
plan = []
no_alias = []
for target, count in sorted(broken.items(), key=lambda x: -x[1]):
    if count < 2:
        continue  # skip singletons
    candidates = find_alias(target)
    if candidates:
        plan.append((target, count, candidates[0], candidates))
    else:
        no_alias.append((target, count))

out = ['# Phase A: Auto-alias candidates\n']
out.append(f'Auto-alias possible: {len(plan)} broken targets')
out.append(f'Need to write fresh: {len(no_alias)} broken targets (no alias)\n')
out.append('## Alias plan (broken → existing file)\n')
for target, count, best, all_c in plan[:60]:
    others = f' (also: {", ".join(all_c[1:])})' if len(all_c) > 1 else ''
    out.append(f'- [[{target}]] ({count}x) → [[{best}|{target}]]{others}')
out.append('\n## No alias — must write fresh (top 60)\n')
for target, count in no_alias[:60]:
    out.append(f'- {target} ({count}x)')

(vault / 'raw' / '_audit_alias_plan.txt').write_text('\n'.join(out), encoding='utf-8')
print(f'With alias candidate (≥2 refs): {len(plan)}')
print(f'No alias, need fresh write (≥2 refs): {len(no_alias)}')

# Auto-apply aliases for unambiguous cases (only 1 candidate)
auto_apply = [(t, c, best) for t, c, best, all_c in plan if len(all_c) == 1]
print(f'\nAuto-apply candidates (single match): {len(auto_apply)}')
import json
(vault / 'raw' / '_audit_alias_plan.json').write_text(
    json.dumps([{'target': t, 'count': c, 'replacement': best, 'all_candidates': all_c}
                for t, c, best, all_c in plan], ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print('Saved: raw/_audit_alias_plan.txt + .json')
