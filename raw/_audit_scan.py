"""Vault audit scanner — read-only, produces JSON report."""
import re
import json
from pathlib import Path
from collections import defaultdict

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

files = {}  # stem -> Path
for p in wiki.rglob('*.md'):
    files[p.stem] = p

# Collect wikilinks
wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')

incoming = defaultdict(set)
outgoing = defaultdict(set)
broken = defaultdict(list)

for stem, path in files.items():
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    # Skip frontmatter
    if text.startswith('---'):
        end = text.find('---', 4)
        if end > 0:
            text = text[end+3:]
    for m in wikilink_re.finditer(text):
        target = m.group(1).strip()
        if not target:
            continue
        # Skip external/path-like
        if target.startswith(('http', '/')):
            continue
        if '/' in target or '.md' in target.lower():
            continue
        outgoing[stem].add(target)
        if target in files:
            incoming[target].add(stem)
        else:
            broken[target].append(stem)

# Output
out = {
    'total_files': len(files),
    'total_outgoing_links': sum(len(v) for v in outgoing.values()),
    'broken_links': {
        'count': len(broken),
        'top30_by_refcount': [
            {'target': t, 'ref_count': len(s), 'sources_sample': list(s)[:5]}
            for t, s in sorted(broken.items(), key=lambda x: -len(x[1]))[:30]
        ],
    },
    'orphans': {
        'count': sum(1 for s in files if s not in incoming and s not in ('INDEX', 'PROGRESS', 'SCHEMA')),
        'sample': sorted([s for s in files if s not in incoming and s not in ('INDEX', 'PROGRESS', 'SCHEMA')])[:50],
    },
    'top_incoming': [
        {'stem': s, 'incoming': len(incoming.get(s, set())), 'outgoing': len(outgoing.get(s, set()))}
        for s in sorted(files, key=lambda x: -len(incoming.get(x, set())))[:15]
    ],
}

# Write report
report_path = vault / 'raw' / '_audit_report.json'
report_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Report saved: {report_path}')
print(f'Total wiki files: {out["total_files"]}')
print(f'Total wikilinks: {out["total_outgoing_links"]}')
print(f'Broken link targets: {out["broken_links"]["count"]}')
print(f'Orphan files: {out["orphans"]["count"]}')
