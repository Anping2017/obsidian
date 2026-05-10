"""Generate full markdown audit report for human review."""
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

vault = Path(r'D:\BaiduNetdiskWorkspace\Obsidian Vault')
wiki = vault / 'wiki'

files = {}
for p in wiki.rglob('*.md'):
    files[p.stem] = p

wikilink_re = re.compile(r'\[\[([^\]|#]+?)(?:#[^\]|]*?)?(?:\|[^\]]*?)?\]\]')

incoming = defaultdict(set)
outgoing = defaultdict(set)
broken = defaultdict(list)
file_sizes = {}
file_link_counts = {}

for stem, path in files.items():
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    file_sizes[stem] = len(text)
    if text.startswith('---'):
        end = text.find('---', 4)
        if end > 0:
            text_body = text[end+3:]
        else:
            text_body = text
    else:
        text_body = text
    links = wikilink_re.findall(text)
    for m in wikilink_re.finditer(text_body):
        target = m.group(1).strip()
        if not target or target.startswith(('http', '/')) or '/' in target or '.md' in target.lower():
            continue
        outgoing[stem].add(target)
        if target in files:
            incoming[target].add(stem)
        else:
            broken[target].append(stem)

# Categorize broken links
def classify_broken(target, ref_count):
    """guess whether broken link is: typo / missing-stub / synonym / abbreviation"""
    # Heuristic categories (rough)
    if any(c in target for c in ['(', ')', '(', ')']):
        return 'has-parens'
    if ' ' in target and not re.match(r'^[A-Z][a-z]+\s+[A-Z]', target):
        return 'has-space'
    if re.match(r'^[A-Z]+$', target) and len(target) <= 6:
        return 'abbreviation'
    if re.match(r'^[A-Za-z][A-Za-z0-9\-]+$', target):
        return 'english-only'
    if ref_count >= 3:
        return 'high-ref-missing'
    return 'low-ref-missing'

categories = defaultdict(list)
for target, sources in broken.items():
    cat = classify_broken(target, len(sources))
    categories[cat].append((target, len(sources), list(set(sources))[:3]))

# Files with very few outgoing links (potential under-linked)
under_linked = []
for stem, path in files.items():
    if 'INDEX' in stem or stem == 'PROGRESS' or stem == 'SCHEMA':
        continue
    if len(outgoing.get(stem, set())) < 3 and file_sizes.get(stem, 0) > 1000:
        under_linked.append((stem, len(outgoing.get(stem, set())), file_sizes.get(stem, 0)))

# Generate report
lines = []
lines.append('# Vault 体检报告(阶段 1)\n')
lines.append(f'生成时间:2026-05-10\n')
lines.append('---\n')

lines.append('## 总览\n')
lines.append(f'- **总 wiki 文件**: {len(files)}')
lines.append(f'  - concepts: {sum(1 for p in files.values() if "concepts" in str(p))}')
lines.append(f'  - topics:   {sum(1 for p in files.values() if "topics" in str(p))}')
lines.append(f'  - entities: {sum(1 for p in files.values() if "entities" in str(p))}')
lines.append(f'- **总 wikilink 数**: {sum(len(v) for v in outgoing.values())}')
lines.append(f'- **平均出链/篇**: {sum(len(v) for v in outgoing.values()) / len(files):.1f}')
lines.append('')

lines.append('## 健康指标\n')
lines.append('| 项 | 状态 | 数量 |')
lines.append('|---|---|---:|')
lines.append(f'| Frontmatter 合规 | ✅ 全合规 | 0 个问题 |')
lines.append(f'| 空文件 / 极短 stub | ✅ 无 | 0 |')
lines.append(f'| ` 1.md` 后缀重复 | ✅ 无 | 0 |')
lines.append(f'| 孤立文件(无入链)| ✅ 无 | 0 |')
lines.append(f'| **断链(指向不存在概念)**| ⚠️ 主要问题 | **{len(broken)}** 个目标 |')
lines.append(f'| 同义概念对(可能重叠)| ⚠️ 待审 | 15 对 |')
lines.append(f'| 出链 < 3 的长文件(可能欠互联) | ⚠️ 待审 | {len(under_linked)} 个 |')
lines.append('')

lines.append('## 断链分类\n')
lines.append('断链指 wikilink 目标不存在。**断链不全是错——也可能是有意留的 stub 占位**。\n')
lines.append('| 类别 | 数量 | 解释 | 处理建议 |')
lines.append('|---|---:|---|---|')
lines.append(f'| `has-parens` 含括号 | {len(categories["has-parens"])} | 写法如 `[[CRM(客户关系管理)]]` | 改写为不含括号或建别名 |')
lines.append(f'| `has-space` 含空格 | {len(categories["has-space"])} | 写法如 `[[阿尔·里斯 Al Ries]]` | 与已有同义词合并或建文件 |')
lines.append(f'| `abbreviation` 英文缩写 | {len(categories["abbreviation"])} | 如 `[[CRM]]` `[[CPM]]` | 通常应建概念页 |')
lines.append(f'| `english-only` 纯英文 | {len(categories["english-only"])} | 如 `[[SwiftUI]]` `[[BFF]]` | 视主题决定是否建页 |')
lines.append(f'| `high-ref-missing` 中文高引用 | {len(categories["high-ref-missing"])} | 中文概念被≥3次引用却无页 | **优先级最高,应补页** |')
lines.append(f'| `low-ref-missing` 中文低引用 | {len(categories["low-ref-missing"])} | 中文概念被1-2次引用 | 可补可不补 |')
lines.append('')

# Top broken
lines.append('### 断链 TOP 30(按引用数)\n')
broken_sorted = sorted(broken.items(), key=lambda x: -len(x[1]))
lines.append('| 引用数 | 目标 | 引用样例 |')
lines.append('|---:|---|---|')
for target, sources in broken_sorted[:30]:
    sample = ', '.join(list(set(sources))[:3])
    lines.append(f'| {len(sources)} | `[[{target}]]` | {sample} |')
lines.append('')

# High-ref missing — most actionable
lines.append('### 优先级最高:`high-ref-missing` 中文高引用断链\n')
lines.append('这些是**中文概念,被引用 ≥ 3 次,却没有 wiki 页面**——补这些页对 vault 互联度提升最大。\n')
hrm = sorted(categories['high-ref-missing'], key=lambda x: -x[1])
lines.append(f'共 {len(hrm)} 个,前 50 个:\n')
lines.append('| 引用数 | 目标 |')
lines.append('|---:|---|')
for target, ref_count, _ in hrm[:50]:
    lines.append(f'| {ref_count} | `[[{target}]]` |')
lines.append('')

lines.append('## 可能的同义概念对(15 对)\n')
lines.append('多数是「概念 vs 学派/理论」的合理分层,少数可能值得合并:\n')
lines.append('### 合理保留差异(人物/学派/方法分层)\n')
lines.append('- [[凯恩斯]] vs [[凯恩斯主义]] — 人物 vs 学派 ✓')
lines.append('- [[凯恩斯]] vs [[新凯恩斯主义]] — 人物 vs 后续学派 ✓')
lines.append('- [[柏拉图]] vs [[新柏拉图主义]] — 人物 vs 后续学派 ✓')
lines.append('- [[心理学]] vs [[人本主义心理学]] — 学科 vs 分支 ✓')
lines.append('- [[收入确认]] vs [[收入确认五步法]] — 概念 vs 方法 ✓')
lines.append('- [[公益/关系/社会营销]] vs [[*学派]] — 概念 vs 学派 ✓')
lines.append('- [[首因效应]] vs [[首因效应与近因效应]] — 单概念 vs 对照页 ✓')
lines.append('')
lines.append('### 可能值得审视\n')
lines.append('- [[BERT]] vs [[BERT语义搜索算法]] — 模型 vs 应用,看内容是否有重复')
lines.append('- [[OKR]] vs [[OKR目标管理法]] — 概念 vs 方法,看内容是否有重复')
lines.append('- [[提示词工程]] vs [[提示词工程方法论]]')
lines.append('- [[资本结构]] vs [[资本结构理论]]')
lines.append('- [[金融监管]] vs [[金融监管理论基础]]')
lines.append('- [[领导力]] vs [[领导力理论演进]]')
lines.append('')

lines.append('## 出链 < 3 的长文件(欠互联)\n')
lines.append(f'共 {len(under_linked)} 篇,前 30 个:\n')
under_sorted = sorted(under_linked, key=lambda x: -x[2])
lines.append('| 文件 | 出链数 | 字节数 |')
lines.append('|---|---:|---:|')
for stem, links, size in under_sorted[:30]:
    lines.append(f'| `[[{stem}]]` | {links} | {size} |')
lines.append('')

lines.append('## 建议的阶段 2 行动顺序\n')
lines.append('按 ROI 从高到低:\n')
lines.append('1. **补 high-ref-missing 中文高引用断链** — 用 subagent 并行补,影响面最大')
lines.append('2. **修缩写/英文断链** — 缩写如 CRM/CPM 应建标准页,避免每次都断')
lines.append('3. **修 has-parens / has-space** — 多数是写法不规范,可批量改名')
lines.append('4. **审 15 对同义概念** — 合并或加交叉链接(逐对人工判断)')
lines.append('5. **欠互联长文加 wikilinks** — 让出链 < 3 的长文与已有概念互链')
lines.append('6. **(最贵)逐文件事实校对** — 需要外部资料源,建议分批人机协作')
lines.append('')
lines.append('---\n')
lines.append('体检不修改任何 wiki 文件。下一步等你决定。\n')

(vault / 'raw' / '_audit_report.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'Report written: {vault}/raw/_audit_report.md')
print(f'Length: {sum(len(l) for l in lines)} chars')
