#!/usr/bin/env python3
"""
wk-task-dev Step 0a: 扫 docs/tasks.md 列出待实现清单
- 段文父 bullet [ ] 状态 (UC/IF 段)
- 段文 优化升级 段 - [ ] 项
- 段文 **关联 IF** / **关联 UC** 字段 → 分组(关联组 / 独立组)

用法:
  python3 scan-pending.py                          # 全局扫
  python3 scan-pending.py UC-01-06               # 限定单段
  python3 scan-pending.py --doc /path/to/tasks.md  # 显式指定文档

DOC 路径解析顺序(命中即停):
  1. --doc <path> CLI 参数
  2. WK_TASK_DEV_DOC 环境变量
  3. $CWD/docs/tasks.md(项目级默认)
  4. 向父目录递归找 docs/tasks.md(支持 monorepo / 嵌套 cwd)
  5. fallback: $CWD/docs/tasks.md(可能不存在 → 报错)

分组规则(只对 [ ] 状态的段建组):
  - 解析每个 [ ] 段的 **关联 IF** / **关联 UC** 字段,提取 IF-XX-NN / UC-XX-NN
  - 过滤掉文本(如"(无新 IF;...)"、"(无)"、空),保留纯 ID
  - 过滤掉本身已 [x] 的引用(已实现的引用不算依赖组)
  - 用 union-find: 当前段与每个 [ ] 引用段 union
  - 关联组:size ≥ 2 的组
  - 独立组:size = 1 的段(无任何 [ ] 引用 / 无引用 / 引用全部已 [x])

排序规则(Step 2 默认顺序 → Step 0a 输出建议顺序):
  1. [!] 阻塞优先
  2. [~] in-progress
  3. 关联组(组内 IF 优先 UC,同类型按 [P0>P1>P2>P3]+ 文档顺序)
  4. 独立组(IF 优先 UC,同类型按 [P0>P1>P2>P3]+ 文档顺序)
"""
import re
import sys
import os
from pathlib import Path


def resolve_doc_path() -> Path:
    """Step 0a 输入解析: 找 docs/tasks.md 路径。"""
    if '--doc' in sys.argv:
        idx = sys.argv.index('--doc')
        try:
            return Path(sys.argv[idx + 1]).expanduser().resolve()
        except IndexError:
            pass

    env = os.environ.get('WK_TASK_DEV_DOC')
    if env:
        return Path(env).expanduser().resolve()

    cwd_doc = (Path.cwd() / 'docs' / 'tasks.md').resolve()
    if cwd_doc.exists():
        return cwd_doc

    cur = Path.cwd().resolve()
    while cur != cur.parent:
        cand = cur / 'docs' / 'tasks.md'
        if cand.exists():
            return cand
        cur = cur.parent

    return cwd_doc


# 解析 args
raw_args = sys.argv[1:]
DOC = resolve_doc_path()
arg = None
i = 0
while i < len(raw_args):
    a = raw_args[i]
    if a == '--doc':
        i += 2
        continue
    arg = a
    i += 1

if not DOC.exists():
    print('# ERROR: docs/tasks.md not found')
    print(f'# CWD = {Path.cwd()}')
    print('# tried:')
    print('#   --doc <path>            (CLI arg)')
    print('#   $WK_TASK_DEV_DOC        (env var)')
    print('#   $CWD/docs/tasks.md      (project default)')
    print('#   walk-up to parent dirs  (monorepo / nested cwd)')
    sys.exit(1)

text = DOC.read_text()
lines = text.split('\n')

# -----------------------------------------------------------------------------
# 1) 解析所有段文父 bullet + 关联字段
# -----------------------------------------------------------------------------
# 父 bullet 行匹配:  - [state] **UC-XX-YY** [P?] [/ 简述]
parent_pat = re.compile(
    r'^- \[([ x~!]*)\] \*\*([UI][CF]-(\d+)-(\d+))\*\*\s*(?:\[P(\d)\])?\s*(?:/\s*(.+))?$'
)
# 关联字段行匹配:  - **关联 IF**: ...  或  - **关联 UC**: ...
rel_pat = re.compile(r'^\s*-\s*\*\*(关联 IF|关联 UC)\*\*\s*[::]\s*(.+?)\s*$')
# 段内 ID 抽取(纯 ID,过滤掉文字/后缀)
id_in_text_pat = re.compile(r'\b([UI][CF]-(\d+)-(\d+))\b')


def parse_short_title(start_idx: int) -> str:
    """回退:段文第一句「我希望」/「特性描述」取前 20 字。"""
    for j in range(start_idx + 1, min(start_idx + 10, len(lines))):
        if '**我希望**' in lines[j]:
            tm = re.search(r'\*\*我希望\*\*\s*(.*)', lines[j])
            if tm:
                s = tm.group(1).strip()
                short = re.split(r'(?<=[。.!?])\s*|[,，]', s, maxsplit=1)[0]
                return short[:20]
        if '**特性描述**' in lines[j]:
            tm = re.search(r'\*\*特性描述\*\*\s*[:：]\s*(.*)', lines[j])
            if tm:
                s = tm.group(1).strip()
                short = re.split(r'(?<=[。.!?])\s*|[,，]', s, maxsplit=1)[0]
                return short[:20]
    return ''


# 收集所有段(无论状态)+ 段范围
all_segs = {}   # id -> {state, prio, title, line_no, end_line}
rel_field = {}  # id -> [(ref_kind, [ref_ids])]
seg_order = []  # 按文档顺序的 id 列表

next_parent_pat = re.compile(r'^- \[[ x~!]*\] \*\*([UI][CF]-\d+-\d+)\*\*')

for i, line in enumerate(lines):
    m = parent_pat.match(line)
    if m:
        state, full_id, _, _, prio, title = (
            m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), (m.group(6) or '').strip()
        )
        if not title:
            title = parse_short_title(i)
        # 段范围:到下一个父 bullet / 文件尾
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if next_parent_pat.match(lines[j]):
                end = j
                break
        all_segs[full_id] = {
            'state': state.strip(),
            'prio': int(prio) if prio else 9,  # 无 P 默认最低
            'title': title,
            'line_no': i,
            'end_line': end,
        }
        seg_order.append(full_id)
        # 扫描该段内的 **关联 IF** / **关联 UC** 字段
        rels = []
        for j in range(i + 1, end):
            rm = rel_pat.match(lines[j])
            if rm:
                kind, body = rm.group(1), rm.group(2)
                # 抽取所有 IF/UC ID,跳过文字
                ids = id_in_text_pat.findall(body)
                ref_ids = []
                for hit in ids:
                    ref_ids.append(hit[0])
                if ref_ids:
                    rels.append((kind, ref_ids))
        if rels:
            rel_field[full_id] = rels

# -----------------------------------------------------------------------------
# 2) 优化升级 - [ ] 项(每个段末尾 优化升级 子节的 checkbox)
# -----------------------------------------------------------------------------
opt_pat = re.compile(r'^\s+- \[ \] (.+)')
seg_pat = re.compile(r'^- \[[ x~!]*\] \*\*([UI][CF]-[\d]+-\d+)\*\*')

opt = []  # [(seg_id, 简注), ...]
in_opt_section = False
cur_seg = None
for i, line in enumerate(lines):
    sm = seg_pat.match(line)
    if sm:
        cur_seg = sm.group(1)
        in_opt_section = False
        continue
    if line.strip().startswith('- **优化升级**') or line.strip().startswith('  - **优化升级**'):
        in_opt_section = True
        continue
    if in_opt_section:
        if line.strip().startswith('- **') and not line.strip().startswith('- [ ]'):
            in_opt_section = False
            continue
        om = opt_pat.match(line)
        if om:
            opt.append((cur_seg, om.group(1).strip()[:80]))

# -----------------------------------------------------------------------------
# 3) union-find 建组(只对 [ ] 段 + 引用 [ ] 段)
# -----------------------------------------------------------------------------
class UF:
    def __init__(self):
        self.p = {}

    def add(self, x):
        if x not in self.p:
            self.p[x] = x

    def find(self, x):
        self.add(x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


uf = UF()
# 只对 [ ] 状态段建组
pending_ids = [sid for sid in seg_order if all_segs[sid]['state'] == '']
for sid in pending_ids:
    uf.add(sid)
    if sid in rel_field:
        for _kind, ref_ids in rel_field[sid]:
            for ref in ref_ids:
                if ref in all_segs and all_segs[ref]['state'] == '':
                    uf.union(sid, ref)

# -----------------------------------------------------------------------------
# 4) 排序:关联组 / 独立组
# -----------------------------------------------------------------------------
def sort_key(seg_id):
    """同组/独立组内排序:(is_UC, prio, line_no) — IF 先 UC 后,P 小先,文档先。"""
    seg = all_segs[seg_id]
    is_uc = 0 if seg_id.startswith('IF') else 1
    return (is_uc, seg['prio'], seg['line_no'])


def sort_key_with_block(seg_id):
    """Step 2 全局排序(含 [!] / [~]):block 优先级、组内 is_uc、prio、line_no。"""
    seg = all_segs[seg_id]
    state = seg['state']
    if state == '!':
        block = 0
    elif state == '~':
        block = 1
    else:
        # 关联组 vs 独立组:先按组大小降序(大组先),同大小按 is_uc、prio、line_no
        root = uf.find(seg_id)
        group_size = sum(1 for x in pending_ids if uf.find(x) == root)
        # 关联组(size>=2)→ block=2;独立组(size=1)→ block=3
        block = 2 if group_size >= 2 else 3
    is_uc = 0 if seg_id.startswith('IF') else 1
    return (block, is_uc, seg['prio'], seg['line_no'])


groups = {}  # root -> [seg_id, ...]
for sid in pending_ids:
    root = uf.find(sid)
    groups.setdefault(root, []).append(sid)

related_groups = []  # [(root, [seg_id, ...])] size>=2
solo_groups = []    # [seg_id] size=1
for root, members in groups.items():
    members_sorted = sorted(members, key=sort_key)
    if len(members_sorted) >= 2:
        related_groups.append((root, members_sorted))
    else:
        solo_groups.extend(members_sorted)
solo_groups.sort(key=sort_key)

# 关联组之间排序:组内 IF 最小 line_no 优先(P 优先 + 文档顺序)
related_groups.sort(key=lambda rg: min(all_segs[sid]['line_no'] for sid in rg[1]))


# -----------------------------------------------------------------------------
# 5) 输出
# -----------------------------------------------------------------------------
N = len(pending_ids)
M = len(opt)
all_ids_in_order = sorted(pending_ids, key=sort_key_with_block)


def title_for(sid):
    return all_segs[sid]['title']


def state_for(sid):
    return all_segs[sid]['state'] or ' '


def prio_for(sid):
    p = all_segs[sid]['prio']
    return f'[P{p}]' if p != 9 else '[P-]'


if arg:
    print(f'# 单段 {arg} 清单(Step 0a 限定查询)')
else:
    print(f'# 全局待实现清单(Step 0a — 含关联分组 + 建议顺序)')
print(f'待实现清单(扫 docs/tasks.md):')
print()

if arg:
    # 单段模式(原行为)
    p = [(sid, title_for(sid)) for sid in pending_ids if sid == arg]
    o = [x for x in opt if x[0] == arg]
    if p or o:
        print(f'[段 {arg} 段文父 bullet]')
        for sid, t in p:
            print(f'  - {sid} [ ] / {t}')
        print(f'[段 {arg} 优化升级]')
        for sid, txt in o:
            print(f'  - 段 {sid} > {txt}')
    else:
        print('  (无待实现项,可能 [x] 已完成)')
    sys.exit(0)

# ---- 全局输出 ----
print(f'[段文父 bullet — {N} 项]')
for sid in seg_order:
    if all_segs[sid]['state'] == '':
        print(f'  - {sid} [ ] / {title_for(sid)}')
print()
print(f'[优化升级 — {M} 项]')
if opt:
    for sid, txt in opt:
        print(f'  - 段 {sid} > {txt}')
else:
    print('  (无)')
print()

# 关联组
related_count = sum(len(m) for _, m in related_groups)
solo_count = len(solo_groups)
print(f'[关联组 — {len(related_groups)} 组 / {related_count} 项]')
if related_groups:
    for gi, (root, members) in enumerate(related_groups, 1):
        ifs = [m for m in members if m.startswith('IF')]
        ucs = [m for m in members if m.startswith('UC')]
        # 解释:每个段引用了谁 → 印证分组
        explain = []
        for m in members:
            if m in rel_field:
                for kind, refs in rel_field[m]:
                    hit = [r for r in refs if r in all_segs and all_segs[r]['state'] == '']
                    if hit:
                        explain.append(f'{m}↔{"/".join(hit)}')
        print(f'  组 {gi}({len(members)} 项:IF {len(ifs)} + UC {len(ucs)}):')
        for m in members:
            print(f'    - {m} {prio_for(m)}: {title_for(m)}')
        if explain:
            print(f'    关联证据:{"; ".join(explain)}')
else:
    print('  (无)')
print()

# 独立组
print(f'[独立组 — {solo_count} 项]')
if solo_groups:
    for sid in solo_groups:
        print(f'  - {sid} {prio_for(sid)}: {title_for(sid)}')
else:
    print('  (无)')
print()

# 建议执行顺序
print('[建议执行顺序](Step 2 默认顺序)')
ordered = []
# a) [!]
bang = [s for s in pending_ids if all_segs[s]['state'] == '!']
if bang:
    bang.sort(key=sort_key)
    print(f'  1. [! 阻塞 — {len(bang)} 项](先解锁):')
    for s in bang:
        print(f'     - {s} {prio_for(s)}: {title_for(s)}')
    ordered.extend(bang)
# b) [~]
tilde = [s for s in pending_ids if all_segs[s]['state'] == '~']
if tilde:
    tilde.sort(key=sort_key)
    print(f'  2. [~ in-progress — {len(tilde)} 项](避免上下文丢失):')
    for s in tilde:
        print(f'     - {s} {prio_for(s)}: {title_for(s)}')
    ordered.extend(tilde)
# c) 关联组
gi_offset = 3
for gi, (root, members) in enumerate(related_groups, 1):
    print(f'  {gi_offset}. 关联组 {gi}({len(members)} 项,IF 优先 → UC 殿后;同类型按 P + 文档顺序):')
    for m in members:
        kind = 'IF' if m.startswith('IF') else 'UC'
        print(f'     - {m} {prio_for(m)} ({kind}): {title_for(m)}')
    ordered.extend(members)
    gi_offset += 1
# d) 独立组
if solo_groups:
    print(f'  {gi_offset}. 独立组({len(solo_groups)} 项,IF 优先 → UC 殿后;同类型按 P + 文档顺序):')
    for s in solo_groups:
        kind = 'IF' if s.startswith('IF') else 'UC'
        print(f'     - {s} {prio_for(s)} ({kind}): {title_for(s)}')
    ordered.extend(solo_groups)
print()
print(f'共 {N + M} 项待实现(段文父 bullet {N} + 优化升级 {M});建议按上述顺序逐 task 实现。')
