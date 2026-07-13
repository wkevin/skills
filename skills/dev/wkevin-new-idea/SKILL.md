---
name: wkevin-new-idea
description: 把新需求作为「一次联动改动」,自动传播到 docs/prd.md + docs/add.md + docs/tasks.md 中所有受影响的文档,并做跨文档一致性校验。流程:探测文档 → 分类改动类型 → 联动预览 → 跨文档扫现状 → 提议联动方案 → 按依赖序编辑 → 联动校验 → 提议 commit。本 skill 写入的产物严格对齐 wkevin-vital-docs 的 PRD / ADD / Tasks 三件套评估基线。触发词:"/new-idea"、用户说"加需求 / 加个 task / 加个 UC / 加个 IF / 加个决策 / btw, ..."。
---

# /new-idea — 联动修改 PRD + ADD + Tasks

把当前轮用户描述的新需求作为**一次联动改动**,传播到所有受影响的文档,避免「改了 PRD 没改 Tasks」「改了 ADD §7 但 Tasks 没拆 task」这类单源失同步。

> **作用域**:本 skill **只**处理 `docs/prd.md` / `docs/add.md` / `docs/tasks.md` 三个文件 —— 这是 wkevin-vital-docs 评估基线。任何其他文件(如独立的 `design.md` / `decisions/000N-xxx.md` / `roadmap.md`)**不在本 skill 范围**。

## 核心理念:联动而非独立

| ❌ 错误的做法(doc-centric) | ✅ 正确的做法(change-centric) |
|---|---|
| 选文档 → 改文档 → 结束 | 选改动类型 → 看传播矩阵 → 联动预览 → 按依赖序编辑 → 跨文档校验 |
| 改了 PRD §2 目标但没拆 task | 改了 PRD 目标同步拆对应 Tasks UC |
| 改了 ADD §7 Decision 但 Tasks 没拆 task | 关键决策必同步 Tasks IF + Milestone |
| 改了 PRD §7 里程碑表但 tasks.md 里没新 M 段 | PRD 里程碑表 ↔ Tasks Milestone 段强一致 |

**联动传播矩阵**(改动类型 → 必须/应当/可选改哪些文档):

| Type | 含义 | PRD | ADD | Tasks |
|---|---|---|---|---|
| **[N]** | 新功能需求 | **MUST** §2/§4/§7 | maybe §1-§5 视图更新 | **MUST** UC + Milestone task |
| **[A]** | 新架构决策 | rare §3/§6 | **MUST** §7 Decision View | **MUST** UC/IF + Milestone task |
| **[M]** | 新里程碑 | **MUST** §7 加行 | maybe | **MUST** 新 M 段 |
| **[B]** | Bug fix | no | maybe §4 Runtime | **MUST** UC/IF + fix task |
| **[O]** | 性能优化 | no | **MUST** §4 Runtime | **MUST** UC/IF |
| **[S]** | 安全修复 | no | **MUST** §4 Runtime | **MUST** UC/IF |
| **[X]** | 非目标更新 | **MUST** §3 | no | no |
| **[V]** | v2 候选 | **MUST** §6 | no | **MUST** §2.4 Backlog [P3] |
| **[R]** | 重构 | no | **MUST** §1/§3 | **MUST** UC/IF |
| **[D]** | 文档补充(纯文本) | maybe | maybe | no |

**MUST** = 不改会出现双源失同步 · **maybe** = 视情况决定 · **rare** = 几乎不改 · **no** = 明确不改

## 与 wkevin-vital-docs 的对齐(3 文件严格对齐)

| 本 skill 写入 | vital-docs 评估清单 | 关键章节 |
|---|---|---|
| `docs/prd.md` | `prd-checklist.md` | §1-§9(§3 非目标 / §7 里程碑 / §9 风险是 critical) |
| `docs/add.md` | `add-checklist.md` | §0 Context / §1-§5 五视图 / §6 Scenarios / §7 Decision View / §10 Critical Lens |
| `docs/tasks.md` | `tasks-checklist.md` | §1.1 UC 三段式 / §1.2 IF / §2 Milestone ≤ 3 / §2.4 Backlog |

**承诺**:按本 skill 写入的文档,vital-docs 评估时 critical 数 ≤ 1;若超出,按下方"联动反模式"对照修。

**注意**:vital-docs **不评估**独立的 `design.md` / `roadmap.md` / `decisions/` 文件。本 skill 也不处理这些文件 —— 一切内容并入 add.md / tasks.md 内部章节。

## 何时使用

- 用户说「加需求 / 加个 task / 加个 UC / 加个 IF / 加个决策 / btw, ...」,或 `/new-idea ...`
- 项目任何阶段想增 / 改 / 删一条需求
- 增量更新 `docs/` 下的 PRD/ADD/Tasks 三件套(不是代码实现本身)

## 何时不要使用

- ❌ 项目没有 `docs/` 目录(先建文档骨架)
- ❌ 文档结构跟 vital-docs 不一致(先跑 `wkevin-vital-docs` 评估,按其 verdict 修复后再用)
- ❌ 用户要写代码实现(用 `dev:end-to-end` / `ultracode` / `dev:code` 模式)
- ❌ 改动只是代码(无 PRD/ADD/Tasks 联动需求)—— 本 skill 不动代码
- ❌ 要改 `design.md` / `roadmap.md` / `decisions/` 文件 —— 这些不在本 skill 范围,请先按 vital-docs 规范合并到 add.md / tasks.md

## 文档系统(严格 3 文件)

| 文档 | 职责 | 内容性质 |
|---|---|---|
| `docs/prd.md` | 产品需求文档(PRD) | 产品向(愿景 / 目标 / 非目标 / 场景 / 范围外 / 风险) |
| `docs/add.md` | 架构设计文档(ADD) | 技术向(Context + 5+1 view + Decision View + Critical Lens) |
| `docs/tasks.md` | 任务清单(Tasks) | 用户向 UC + 系统向 IF + Milestone 排期 |

**配套关系**:
- PRD = "做什么 + 为什么"
- ADD = "技术方案 + 为什么这么决定"
- Tasks = "谁 / 何时 / 怎么拆"

## 流程(联动版 8 步)

### Step 1:探测文档存在性

```bash
ls docs/prd.md docs/add.md docs/tasks.md 2>&1
```

| 情况 | 处理 |
|---|---|
| 3 个全在 | 进 Step 2 |
| 只有部分 | **先停**——告诉用户缺哪个,按 vital-docs 规范补建空模板 |
| 全都不在 | **拒绝执行**——本 skill 只增量更新,不从零搭文档 |

> 如果项目还有 `design.md` / `roadmap.md` / `decisions/` 等历史遗留文件,**提示用户先合并到 add.md / tasks.md** 再用本 skill。

### Step 2:分类改动类型

根据用户描述,确定本次改动的 [Type]:

| 用户说的 | Type |
|---|---|
| "加个功能 / 加个特性 / 用户能 X" | **[N]** |
| "改架构 / 改存储 / 用 X 不用 Y / 加个决策" | **[A]** |
| "开新里程碑 / 进入 v2 规划" | **[M]** |
| "修 bug / 修了 X 不工作" | **[B]** |
| "加速 / 优化性能 / 减少内存" | **[O]** |
| "安全 / 鉴权 / 防 XSS" | **[S]** |
| "明确不做 / 不支持 X" | **[X]** |
| "v2 再做 / 以后考虑" | **[V]** |
| "重构 X 模块 / 改设计" | **[R]** |
| "文档写错了 / 补一句说明" | **[D]** |

如果类型模糊(如「这个需求...」),用 **AskUserQuestion** 让用户选。

### Step 3:联动预览

根据 [Type] + 传播矩阵,**一次性列出本次要改的所有文档**:

```
[Type] 一句话
  → MUST: <文档列表>
  → MAYBE: <文档列表>(待 Step 4 扫现状后确认)
  → SKIP: <明确不动的文档>
```

例:`[N] 批量导入 repo → MUST: PRD+Tasks / MAYBE: ADD / SKIP: (无)`

### Step 4:扫现状(跨文档)

**按 PRD → ADD → Tasks 顺序扫**(产品向在前,技术方案在后,任务拆解在最后):

```bash
# PRD: 顶部 + 里程碑表 + 现有 §N
head -50 docs/prd.md
grep -nE "^\| M[0-9]+ " docs/prd.md        # §7 里程碑表行
grep -nE "^## §[0-9]+" docs/prd.md           # 章节位置

# ADD: 当前 §N + §7 Decision View
grep -nE "^## [0-9]+\." docs/add.md
grep -nE "^### 7\." docs/add.md             # Decision View

# Tasks: 最新 milestone + UC/IF 编号
grep -nE "^### M[0-9]+|^- \*\*UC-[0-9]+-[0-9]+|^- \*\*IF-[0-9]+-[0-9]+" docs/tasks.md
grep -oE "UC-[0-9]+-[0-9]+" docs/tasks.md | sort -u | tail -5   # 最近 5 个 UC
grep -oE "IF-[0-9]+-[0-9]+" docs/tasks.md | sort -u | tail -5   # 最近 5 个 IF
```

明确:
- **新 UC/IF 编号**(避免冲突;算法见下)
- **新 task 归到哪个 milestone**(沿用现有 Milestone,或开新 M{N+1} 代号)
- **是否需要修改 PRD §N**(按 epic 拆需求 → PRD;技术方案 → ADD;重要决策追加 ADD §7)

#### UC / IF 编号冲突解决

```bash
# 1. 列出所有已有 UC/IF
grep -oE "UC-[0-9]+-[0-9]+" docs/tasks.md | sort -u > /tmp/existing_uc.txt
grep -oE "IF-[0-9]+-[0-9]+" docs/tasks.md | sort -u > /tmp/existing_if.txt

# 2. 取最大号 +1;若已存在则 +2 直到无冲突
LAST_UC=$(grep -oE "UC-[0-9]+-[0-9]+" docs/tasks.md | sort -V | tail -1)
NEXT_UC="$LAST_UC"
while grep -q "^$NEXT_UC$" /tmp/existing_uc.txt; do
  NEXT_UC=$(echo "$NEXT_UC" | awk -F'-' '{printf "UC-%s-%d", $2, $3+1}')
done
echo "$NEXT_UC"

# IF 同理(替换 UC→IF)
```

- **用户给的 ID 已存在** → 提示冲突,给出算法算出的下一个空闲 ID,请用户重选

### Step 5:提议联动改动(关键步骤)

> **注意**:这是 change-centric 提案,不是 doc-centric。
>
> 提议(联动):
> **[N] 新功能「批量导入 repo(CSV → URL 列表)」**
>
> - `docs/prd.md`:
>   - §2 目标加 8. 批量导入 ≥ 10 个 repo < 30s
>   - §4 加场景:管理员上传 CSV 含 URL 列表
>   - §7 里程碑表加 M14 行(0% / ✗)
> - `docs/add.md`: 无改动(已有 CSV 解析章节复用)
> - `docs/tasks.md`:
>   - §1.1 加 **UC-04-08** [P2] 批量导入 repo(CSV → URL 列表)
>     - **作为** 知识库管理员
>     - **我希望** 上传一份 CSV 文件一次性导入多个 repo
>     - **以便** 不用逐个粘贴 URL
>     - **实现细节**:
>       - 解析 CSV 第一列为 GitHub URL
>       - 跳过格式不合法的行并记 warn 日志
>       - 加 e2e: 10 条 URL 全导入
>   - §2 M14 "Seedling" 段加 task 引用 UC-04-08
>
> **联动一致性预检**:
> - PRD §7「M14 — Seedling」 ↔ Tasks `### M14 — "Seedling"` 段名一致 ✓
> - 新 UC-04-08 与现有最大 UC ID UC-04-07 连续 ✓
>
> OK 就改?如要改文案请说。

### Step 6:联动编辑(按依赖序)

按 **PRD → ADD → Tasks** 顺序编辑(产品向在前,技术方案在后,任务拆解在最后):

| 顺序 | 文档 | 编辑要点 |
|---|---|---|
| 1 | PRD | §2/§4/§6/§7 按需;**先读 PRD 顶部目录**确认 §N 还叫这名 |
| 2 | ADD | §1-§5 视图按需;§7 Decision View 按 [A] 类型决策填 Context/Decision/Consequences |
| 3 | Tasks | UC agile 三段式(作为/我希望/以便)+ 实现细节;IF 特性描述 + 实现细节;Milestone 按代号 |

PRD 章节定位:**先读 PRD 顶部目录**确认 §N 是否还叫这名;vital-docs 视为已迁到 ADD 的内容(如数据模型、技术栈)不写回 PRD。

### Step 7:联动校验(关键步骤)

改完所有文档后,**重新扫描跨文档一致性**:

```bash
# 1. PRD §7 里程碑表 ↔ Tasks Milestone 段 一致?
grep -oE "\| M[0-9]+ \|" docs/prd.md | sort -u > /tmp/prd_ms.txt
grep -oE "^### M[0-9]+" docs/tasks.md | sort -u > /tmp/tasks_ms.txt
diff /tmp/prd_ms.txt /tmp/tasks_ms.txt   # 应为空

# 2. 新 UC/IF ID 唯一?
NEW_ID="UC-04-08"
grep -c "$NEW_ID" docs/tasks.md   # 应为 1

# 3. ADD §7 Decision View 内容 ↔ Tasks UC/IF 引用一致?
grep -nE "^### 7\." docs/add.md | wc -l   # 决策数
grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/add.md | sort -u   # ADD 引用的 UC/IF

# 4. PRD §2 目标 ↔ Tasks UC 对应?
grep -E "^- \*\*UC-[0-9]+-[0-9]+" docs/tasks.md | wc -l   # UC 总数
```

输出校验报告(给用户看):

> 联动校验结果:
> - PRD §7 里程碑表 ↔ Tasks Milestone 段:一致 ✓
> - 新 UC ID UC-04-08 唯一:是 ✓
> - ADD §7 决策数 ↔ Tasks UC/IF 引用:一致 ✓
> - PRD §2 目标 8 ↔ Tasks UC-04-08 对应:是 ✓
> - PRD §7 M14 行 ↔ Tasks M14 "Seedling" 段存在:是 ✓
>
> OK 提交?

### Step 8:提议 commit(联动版)

用 **AskUserQuestion** 让用户确认:

> 提议 commit:
> `idea: 加 UC-04-08 批量导入 repo (联动 prd+tasks)`
>
> OK 提交?

**commit message 风格**(按团队约定二选一):

| 团队风格 | 模板 | 例 |
|---|---|---|
| 中文主题 | `idea: 加 UC-{xx}-{yy} {一句话摘要} (联动 <文档列表>)` | `idea: 加 UC-04-08 批量导入 repo (联动 prd+tasks)` |
| 英文主题(Conventional Commits) | `idea(tasks): add UC-{xx}-{yy} {kebab} (sync prd)` | `idea(tasks): add UC-04-08 batch-import-repos (sync prd)` |

**联动 commit 策略**(让用户选):

| 策略 | 适用场景 | 优缺点 |
|---|---|---|
| **单 commit** | 改动小 / 一致性强 | 原子性强;但一个改动混多个文档 |
| **多 commit**(每文档一个) | 改动大 / 文档独立可 review | review 清晰;但中间状态文档可能失同步 |

**长度约束**:subject ≤ 60 字,超长用 body 分行。

用户确认后执行:

```bash
# 单 commit
git add docs/prd.md docs/add.md docs/tasks.md
git commit -m "<提议的 message>"

# 多 commit(每个文档一个)
git add docs/prd.md && git commit -m "docs(prd): ..."
git add docs/add.md && git commit -m "docs(add): ..."
git add docs/tasks.md && git commit -m "docs(tasks): ..."
```

## 硬约束(含 WHY)

1. **不修改代码** — WHY: 本 skill 只管文档;代码实应用 `dev:end-to-end` / `ultracode` 模式。
2. **每个 UC 至少 2-3 个子项(或 UC + IF 配套)** — WHY: 来自 tasks-checklist §1.1.3 实现细节嵌套规范;UC 没实现细节 = 占位。
3. **UC / IF / Milestone 编号避免冲突** — WHY: 编号冲突会让 git log 和检索定位失效。
4. **不修改 task 状态 `[ ]` → `[x]`** — WHY: 那是 commit 完成任务的工作流(用 `dev:end-to-end`);本 skill 不验证实现。
5. **commit message subject ≤ 60 字** — WHY: git log 可读性 + Conventional Commits 规范。
6. **PRD 瘦身** — WHY: 已迁到 ADD 的内容(数据模型 / 技术栈等)写回 PRD 会双源失同步。
7. **联动改动不拆 commit**(默认) — WHY: 单 commit 保证原子性,避免中间状态文档失同步;若用户明确要多 commit 才拆。
8. **不创建独立 `decisions/000N-xxx.md` 文件** — WHY: vital-docs 不评估该路径;ADD §7 Decision View 才是 ADR 内容的归宿。
9. **不创建 `design.md` / `roadmap.md` 文件** — WHY: vital-docs 不评估这两个文件;请改用 add.md / tasks.md。

## 模板(3 文件版)

### PRD §2 目标新增一条

```markdown
8. **{动词}** — {一句话描述}
```

### PRD §4 场景新增(联动 UC)

```markdown
- **{角色}** {动作}
  - {价值描述}
```

### PRD §7 里程碑表加一行(联动 Tasks Milestone)

```markdown
| M{段} | {段名} | 0% | ✗ | {一句话备注 / 子项摘要} |
```

### ADD §N 新视图章节

```markdown
## {N}. {新视图名}

{内容,带 WHY 列}
```

### ADD §7 Decision View 新决策(对应 [A] 类型)

```markdown
### 7.{N} {新决策标题}

**Status**: Accepted

**Context**: 当时面对什么问题、考虑了哪些备选方案

**Decision**: 最终选了什么 + 为什么

**Consequences**: 选了之后带来的正向 / 负向影响
```

### Tasks UC 三段式(agile,中文标签)

```markdown
- **UC-{xx}-{yy}** [{P0|P1|P2|P3}]
  - **作为** {具体角色 / 场景,不是 "user" 这种空泛词}
  - **我希望** {动作 + 对象}
  - **以便** {价值 / 动机}
  - **实现细节**:
    - {文件路径 / 函数名 / 配置值}
```

### Tasks IF 特性描述

```markdown
- **IF-{mm}-{nn}** [{P0|P1|P2|P3}]
  - **{特性一句话描述}**
  - **实现细节**:
    - {技术点 / 路径}
```

### Tasks §2 新 Milestone 段

```markdown
### M{段} — "{代号}" ({版本范围}, {时间范围}) 

#### 初次实现
- [ ] UC-{xx}-{yy} {user story 一句话}
- [ ] IF-{mm}-{nn} {特性一句话}
- [ ] UC-{xx}-{yy+1} ...

#### 优化与 bug fix(iterations during M{段})
- [ ] UC-{xx}-{yy} — fix: {bug 描述}
- [ ] UC-{xx}-{yy} — upgrade: {改进描述}
```

### Tasks §2.4 Backlog(对应 [V] v2 候选)

```markdown
- [ ] UC-{xx}-{yy} [P3] {v2 候选需求}
```

## 联动反模式(3 文件版)

- ❌ **改了 PRD §2 目标但 Tasks 没拆 UC** — 提了目标但没拆任务,下个 sprint 不知道做啥
- ❌ **改了 PRD §7 里程碑表但 Tasks 里没新 M 段** — 文档自相矛盾
- ❌ **改了 ADD §7 Decision 但 Tasks 没拆 UC/IF** — 决策失追溯
- ❌ **改了 Tasks UC 但 PRD §4 没加场景** — 实现细节有了,但产品向入口没同步
- ❌ **改了 PRD §6 v2 候选但 Tasks §2.4 Backlog 没加** — v2 计划失忆
- ❌ **改了 PRD §3 非目标但没明确「为什么不做的原因」** — 非目标无解释,下次还会被问
- ❌ **联动改动拆多个 commit 但中间没推** — 别人 pull 时中间状态文档失同步
- ❌ **UC 不是 agile 三段式(写了 "I want to" 没翻译成 "我希望")** — tasks-checklist §1.1.2 critical
- ❌ **UC 带 `[x]` 状态** — 状态归 Milestone(§2),不是 UC 本身;tasks-checklist §1.1.1 critical
- ❌ **Milestone > 3 个**(堆了十几个 M1~M14) — tasks-checklist §2 要求 ≤ 3,合并成代号化 Milestone

## Worked Example(3 文件联动版)

**用户**:「btw,加个需求:批量导入 repo,从 CSV 文件读 URL 列表。」

**Step 2 分类**:`[N]` 新功能

**Step 3 联动预览**:
> `[N] → MUST: PRD+Tasks / MAYBE: ADD / SKIP: (无)`

**Step 5 提议联动**:

> 提议(联动):
> **[N] 新功能「批量导入 repo(CSV → URL 列表)」**
>
> - `docs/prd.md`:
>   - §2 目标加 8. 批量导入 ≥ 10 个 repo < 30s
>   - §4 加场景:管理员上传 CSV 含 URL 列表
>   - §7 里程碑表加 M14 行(0% / ✗)
> - `docs/add.md`: 无改动(已有 CSV 解析章节复用)
> - `docs/tasks.md`:
>   - §1.1 加 **UC-04-08** [P2]
>     - **作为** 知识库管理员
>     - **我希望** 上传一份 CSV 文件一次性导入多个 repo
>     - **以便** 不用逐个粘贴 URL
>     - **实现细节**:
>       - 解析 CSV 第一列为 GitHub URL
>       - 跳过格式不合法的行并记 warn 日志
>       - 加 e2e: 10 条 URL 全导入
>   - §2 M14 "Seedling" 段加 task 引用 UC-04-08
>
> **联动一致性预检**:
> - PRD §7「M14 — Seedling」 ↔ Tasks `### M14 — "Seedling"` 段名一致 ✓
> - 新 UC-04-08 与现有最大 UC ID UC-04-07 连续 ✓
>
> OK 就改?

**Step 7 联动校验**:

> 联动校验结果:
> - PRD §7 里程碑表 ↔ Tasks Milestone 段:一致 ✓
> - 新 UC ID UC-04-08 唯一:是 ✓
> - PRD §2 目标 8 ↔ Tasks UC-04-08 对应:是 ✓
> - PRD §7 M14 行 ↔ Tasks M14 "Seedling" 段存在:是 ✓
>
> OK 提交?

**Step 8 commit**:

> 提议 commit:
> `idea: 加 UC-04-08 批量导入 repo (联动 prd+tasks)`
>
> OK 提交?

## 不做的事

- ❌ 不写代码实现
- ❌ 不改 `docs/` 之外的任何文件(README.md 等需同步的单独指示)
- ❌ **不创建 / 修改 `design.md`、`roadmap.md`、`decisions/` 等 vital-docs 不评估的文件** —— 这些是历史遗留,本 skill 强制 3 文件模型
- ❌ 不直接 commit(必须用户确认 message 后再 commit)
- ❌ 不创建 `idea.md` / `research.md`(旧版幽灵文件)
- ❌ 不重新创建 vital-docs 视为已迁出的 PRD 章节(数据模型 / 技术栈等应写 ADD)
- ❌ **不只改一个文档就结束**(除非 Type 是 [X]/[V]/[D] 这种明确单文档类型)

## 回滚

如果用户写完后说「这条不要了」或「改错了」:

```bash
# 软回滚:撤销最后一次 docs 改动
git checkout HEAD~1 -- docs/

# 或生成 revert commit(更安全,保留历史)
git revert <commit-hash>

# 联动多 commit 时,逐个 revert
git revert <commit1> <commit2> ...
```

回滚后建议跑一次 `wkevin-vital-docs` 确认没破坏文档质量基线。

## 关联

- **上游**:`wkevin-vital-docs` — 评估本 skill 写入的 PRD/ADD/Tasks 是否合规
- **下游**:`dev:end-to-end` / `dev:plan` / `dev:code` — 把 `tasks.md` 的 UC/IF 转为实现
- **配套**:写完后若改动显著(新增大模块 / 改 API),建议同步 `README.md` 的索引