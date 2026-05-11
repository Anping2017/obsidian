"""Task 6: Find long files with too few outgoing wikilinks."""
import re
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')

results = []
for p in wiki.rglob('*.md'):
    # Skip meta files
    if p.name in ('INDEX.md', 'PROGRESS.md', 'SCHEMA.md', 'CHANGELOG.md'):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    # Strip frontmatter
    body = text
    if body.startswith('---'):
        end = body.find('---', 4)
        if end > 0:
            body = body[end+3:]
    # Char count (rough Chinese-char count: total chars - whitespace)
    chinese_len = sum(1 for c in body if '一' <= c <= '鿿')
    # Outgoing wikilinks (deduplicated)
    targets = set()
    for m in wikilink_re.finditer(body):
        target = m.group(1).strip()
        if target and not target.startswith(('http', '/')):
            targets.add(target)
    out_count = len(targets)
    if chinese_len >= 1000 and out_count < 4:
        results.append((p, chinese_len, out_count))

# Sort by length desc
results.sort(key=lambda x: -x[1])

print(f'Found {len(results)} long files with < 4 outgoing wikilinks')
print()
print('Top 30 (longest first):')
for p, length, out in results[:30]:
    rel = p.relative_to(vault).as_posix()
    print(f'  {length:>5} chars | {out} links | {rel}')

# Save full list
out_lines = [f'# Task 6: 长文件(>=1000中文字)但 wikilink < 4 的清单', '',
             f'共 {len(results)} 个候选,展示前 50:', '']
for p, length, out in results[:50]:
    rel = p.relative_to(vault).as_posix()
    out_lines.append(f'- [{out} links, {length} chars] {rel}')
(vault / 'raw' / '_audit_task6_list.txt').write_text('\n'.join(out_lines), encoding='utf-8')
print(f'\nSaved: raw/_audit_task6_list.txt')
