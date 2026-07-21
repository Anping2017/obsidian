"""Round 2 dedup: write clean report of duplicate pairs with sizes and refcounts."""
import re
from pathlib import Path
from collections import defaultdict

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'
concepts = wiki / 'concepts'
stems = {p.stem: p for p in concepts.glob('*.md')}

# Refcount for each stem across vault
wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')
refs = defaultdict(int)
for p in wiki.rglob('*.md'):
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    for m in wikilink_re.finditer(text):
        t = m.group(1).strip()
        refs[t] += 1

# Candidate dup pairs (verified both exist)
candidate_pairs = [
    ('Apache Kafka', 'Kafka'),
    ('Kafka', 'Kafka Streams与Flink'),
    ('Apache Flink', 'Flink'),
    ('Service Mesh', '服务网格'),
    ('量化宽松QE', '量化宽松'),
    ('Fintech 监管沙盒', 'Fintech监管沙盒'),
    ('订阅经济', '订阅商业模式'),
    ('Porter五力模型', '波特五力模型'),
    ('Tandem 语伴', 'Tandem语伴'),
    ('品牌资产', '品牌权益'),
    ('检索增强生成', 'RAG'),
    ('多模态学习', '多模态AI'),
    ('儿童发展心理学', '儿童发展'),  # already merged, check gone
    ('AI Agent', 'AI Agent框架'),
    ('Express', 'Express框架'),
    ('财务会计', '财务会计学'),
    ('关系营销', '关系营销学派'),
    ('私域流量', '私域流量运营'),
    ('手机店', '手机店运营'),
    ('投资决策', '投资决策框架'),
    ('内容SEO', '内容SEO学派'),
]

lines = ['# Round 2 Dedup Report', '']
lines.append('Format: [name] exists? | size(bytes) | refcount')
lines.append('')
for a, b in candidate_pairs:
    pa = stems.get(a)
    pb = stems.get(b)
    if pa and pb:
        sa = pa.stat().st_size
        sb = pb.stat().st_size
        lines.append(f'## {a}  vs  {b}')
        lines.append(f'  - "{a}": {sa} bytes, {refs.get(a,0)} refs')
        lines.append(f'  - "{b}": {sb} bytes, {refs.get(b,0)} refs')
        lines.append('')

(vault / 'raw' / '_audit_dup_report.txt').write_text('\n'.join(lines), encoding='utf-8')
print('Both-exist duplicate pairs:')
for a, b in candidate_pairs:
    if a in stems and b in stems:
        print(f'  {a}  <->  {b}')
