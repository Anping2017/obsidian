"""List all wiki files created 2026-05-10 or later (this session's work)."""
import re
from pathlib import Path

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

new_files = []
for p in wiki.rglob('*.md'):
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    m = re.search(r'created:\s*(2026-05-\d\d)', text)
    if m and m.group(1) >= '2026-05-10':
        # word count
        clen = sum(1 for c in text if '一' <= c <= '鿿')
        new_files.append((p.relative_to(wiki).as_posix(), m.group(1), clen))

new_files.sort()
lines = [f'# Files created 2026-05-10+ (this session): {len(new_files)}', '']
for rel, date, clen in new_files:
    lines.append(f'{rel}\t{date}\t{clen}ch')
(vault / 'raw' / '_audit_new_files.txt').write_text('\n'.join(lines), encoding='utf-8')
print(f'New files (created >= 2026-05-10): {len(new_files)}')
for rel, date, clen in new_files:
    print(f'  {clen:>5}ch  {rel}')
