#!/usr/bin/env python3
"""
wk-task-dev Step 0a: 扫 docs/tasks.md 列出待实现清单
- 段文父 bullet [ ] 状态 (UC/IF 段)
- 段文 优化升级 段 - [ ] 项

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
"""
import re
import sys
import os
from pathlib import Path


def resolve_doc_path() -> Path:
    """Step 0a 输入解析: 找 docs/tasks.md 路径。"""
    # 1. --doc <path>
    if '--doc' in sys.argv:
        idx = sys.argv.index('--doc')
        try:
            return Path(sys.argv[idx + 1]).expanduser().resolve()
        except IndexError:
            pass

    # 2. WK_TASK_DEV_DOC 环境变量
    env = os.environ.get('WK_TASK_DEV_DOC')
    if env:
        return Path(env).expanduser().resolve()

    # 3. $CWD/docs/tasks.md
    cwd_doc = (Path.cwd() / 'docs' / 'tasks.md').resolve()
    if cwd_doc.exists():
        return cwd_doc

    # 4. 向上找 docs/tasks.md
    cur = Path.cwd().resolve()
    while cur != cur.parent:
        cand = cur / 'docs' / 'tasks.md'
        if cand.exists():
            return cand
        cur = cur.parent

    # 5. fallback
    return cwd_doc


# 解析 args
raw_args = sys.argv[1:]
DOC = resolve_doc_path()
arg = None
i = 0
while i < len(raw_args):
    a = raw_args[i]
    if a == '--doc':
        i += 2  # skip --doc + value
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

# 1) 段文父 bullet (用 / 简述 优先; 缺则回退到「**我希望**」首句 30 字)
parent_pat = re.compile(r'^- \[([ x~!]*)\] \*\*([UI][CF]-[\d]+-\d+)\*\*\s*(?:\[P\d?\])\s*(?:/\s*(.+))?$')
parent_ids = {}  # id -> start_line for fallback lookup
for i, line in enumerate(lines):
    m = parent_pat.match(line)
    if m:
        parent_ids[m.group(2)] = i

parents = []
for i, line in enumerate(lines):
    m = parent_pat.match(line)
    if not m:
        continue
    state, id_, title = m.group(1), m.group(2), (m.group(3) or '').strip()
    if state.strip() != '':
        continue
    if arg and id_ != arg:
        continue
    # 回退:如 title 为空,读 我希望 / 特性描述 短标题
    if not title:
        for j in range(i + 1, min(i + 10, len(lines))):
            if '**我希望**' in lines[j]:
                tm = re.search(r'\*\*我希望\*\*\s*(.*)', lines[j])
                if tm:
                    # 取前 20 字符(更短更可读)
                    s = tm.group(1).strip()
                    # 取前一个完整句号/逗号前
                    short = re.split(r'(?<=[。.!?])\s*|[,，]', s, maxsplit=1)[0]
                    title = short[:20]
                break
            if '**特性描述**' in lines[j]:
                tm = re.search(r'\*\*特性描述\*\*\s*[:：]\s*(.*)', lines[j])
                if tm:
                    s = tm.group(1).strip()
                    # 取前 20 字符,以句号/逗号切断
                    short = re.split(r'(?<=[。.!?])\s*|[,，]', s, maxsplit=1)[0]
                    title = short[:20]
                break
    parents.append((id_, title))

# 2) 优化升级 - [ ] 项
opt_pat = re.compile(r'^\s+- \[ \] (.+)')
opt = []
seg_pat = re.compile(r'^- \[[ x~!]*\] \*\*([UI][CF]-[\d]+-\d+)\*\*')
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

# 3) 输出
N, M = len(parents), len(opt)
if arg:
    print(f'# 单段 {arg} 清单(Step 0a 限定查询)')
else:
    print(f'# 全局待实现清单(Step 0a)')
print(f'待实现清单(扫 docs/tasks.md):')
print()
if not arg:
    print(f'[段文父 bullet — {N} 项]')
    for id_, t in parents:
        print(f'  - {id_} [ ] / {t}')
    print()
    print(f'[优化升级 — {M} 项]')
    if opt:
        for sid, txt in opt:
            print(f'  - 段 {sid} > {txt}')
    else:
        print('  (无)')
    print()
    print(f'共 {N + M} 项待实现。')
else:
    # 单段模式
    p = [x for x in parents if x[0] == arg]
    o = [x for x in opt if x[0] == arg]
    if p or o:
        print(f'[段 {arg} 段文父 bullet]')
        for id_, t in p:
            print(f'  - {id_} [ ] / {t}')
        print(f'[段 {arg} 优化升级]')
        for sid, txt in o:
            print(f'  - 段 {sid} > {txt}')
    else:
        print('  (无待实现项,可能 [x] 已完成)')
