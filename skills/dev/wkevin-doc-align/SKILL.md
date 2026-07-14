---
name: wkevin-doc-align
description: 评估项目最重要的四件套文档——prd.md / add.md / tasks.md / sprint.md——是否符合方法论,并提供两种模式:evaluate(纯评估,出 issue+verdict)和 transform(评估+修复路线图+联动扫描+commit 编排)。检查 WHY 列是否具体、UC agile 三段式、Sprint 起止日期+Goal、Critical Lens ≥ 3 毛病等。Use when user asks to "评审 / 评估 / 检查 / audit / review / 评分" 已有 docs,或 "改造 / 修复 / 按评估意见修" 已有 docs,或 Sprint 收尾 sign-off,或接手别人文档先评估再决定是否按此规范继续。
---

# /doc-align — 三件套文档评估器 / 改造器

评估 `docs/prd.md` / `docs/add.md` / `docs/tasks.md` 是否符合 PRD + ADD + Tasks 三文档方法论。**两种模式**:

- **`evaluate`**(默认):只评估已有文档,输出 issue 列表 + verdict
- **`transform`**:评估 + 修复路线图 + 章节对位 + 联动扫描 + commit 编排 → 闭环到 PASS

> **新增 transform 模式的原因**:v1 仅做评估,用户拿到 issue 列表后还要自己写大量修复步骤(章节搬迁、跨文档联动、commit 编排),skill 没覆盖。v2 把"评估 + 修复"做成完整工作流。

## 何时使用

| 触发场景 | 模式 |
|---|---|
| 用户说"评估 / 评审 / 检查 / audit / 评分" | `evaluate` |
| 用户说"按评估意见改造 / 修复 / sign-off 没过要修" | `transform` |
| 用户说"写新 add.md"(从零) | `transform`(全章从零写) |
| sprint 收尾 sign-off | `evaluate` |
| 接手别人文档,先评估再决定是否按此规范继续 | `evaluate` |

## 何时**不要**使用

- ❌ 用户要**加新需求**(已有三件套上加新 UC/IF/ADR)→ 用 [`wkevin-idea-realize`](../wkevin-idea-realize/SKILL.md)(增量改动范式)
- ❌ 用户要**改代码实现**→ 用 `dev:code` / `dev:end-to-end`
- ❌ 项目没有 `docs/` 目录(先建文档骨架)
- ❌ 文档结构跟 doc-align 不一致但用户只想加需求 → 先跑 `evaluate` 评估,verdict 是 PASS 后才能用 `idea-realize`

---

## 文档依赖方向(核心原则 ⚠️)

四件套有**严格的依赖方向**——这是本 skill 的**硬约束**,不是建议:

```
   prd (上游)   ─→   add (上游)   ─→   tasks (上游)   ─→   sprint (下游)
  (产品契约)        (架构契约)         (执行 catalog)         (当前进度)
     │                 │                  │                     │
  不能引 ↓           不能引 ↓           不能引 ↓              (可任意引上游)
   add 内部          tasks 内部          sprint 内部
   tasks 内部        sprint 内部
   sprint 内部
```

**核心规则**:**上游文档不引用下游文档内的内容**。

| 上游           | 不能引用下游的(内容)                  | 允许引用下游的(file-level) |
| -------------- | ------------------------------------- | -------------------------- |
| `prd.md`       | `add.md §X` / `add.md DA-N` / `tasks.md UC-XX-NN` / `tasks.md IF-XX-NN` / `sprint.md §X` | `[add.md]` / `[tasks.md]` / `[sprint.md]` 链接 + 角色描述("X 是 Y 契约") |
| `add.md`       | `tasks.md UC-XX-NN` / `tasks.md IF-XX-NN` / `sprint.md` 任何内容 | 同上 |
| `tasks.md`     | `sprint.md §X` / `sprint.md #anchor` | `[sprint.md]` 链接 + 角色描述 |
| `sprint.md`    | (无下游,无约束)                       | 任意引用上游                |

**反例(违规)**:
- prd.md 写 "详见 add.md §DA-12" → 引用了下游 ADR ❌
- add.md 写 "UC-01-01 添加 repo 流程" → 引用了下游 UC ❌
- tasks.md 写 "见 sprint.md §3 当前状态" → 引用了下游章节 ❌
- prd.md 写 "sprint.md = Sprint 计划 + Product Backlog + 当前状态" → 展开下游文档内容 ❌

**正例(合规)**:
- prd.md 写 "详见架构文档(单用户本地决策)" → file-level 指引 ✅
- add.md 写 "AI 建议在 tag-editor 内以虚线 border + Sparkles 标记" → 描述语义,无下游 ID ✅
- tasks.md 写 "见 [`sprint.md`](./sprint.md)" → file-level 链接 ✅

**WHY**:
- 下游文档会被频繁迭代(sprint.md 每周变,tasks.md 加新 UC);上游文档若硬编码下游编号,下游一变上游就断链
- 维护责任清晰:下游定义什么编号 / 章节归下游管,上游不"占位"下游决策
- 重构时改下游不会"莫名其妙破坏上游"

**判定命令**(用于 Step 7 跨文档联动扫描):
```bash
# prd.md → 下游引用 (应为 0)
grep -nE 'add\.md §|add\.md#|tasks\.md (UC|IF)-[0-9]+-[0-9]+|sprint\.md §|sprint\.md#' docs/prd.md

# add.md → 下游引用 (应为 0)
grep -nE '(UC|IF)-[0-9]+-[0-9]+|sprint\.md' docs/add.md

# tasks.md → sprint.md 内部引用 (应为 0)
grep -nE 'sprint\.md §|sprint\.md#' docs/tasks.md
```

**反模式提醒**:本约束跟"是否需要下游信息"无关。**需要引用时,改用语义描述**("该字段由三文件拆分保护" 而非 "IF-01-02 三文件拆分"),而不是写"详见 tasks.md §1.1 UC-01-01"。

---

## Mode A:`evaluate`(纯评估)

适合:sprint 收尾 sign-off / 接手别人文档先看 / 文档健康度审计。

### Step 1:定位要评估的文件

用 Bash `find` / `ls` 找:

- `docs/prd.md` / `docs/PRD.md`
- `docs/add.md` / `docs/ADD.md`
- `docs/tasks.md`
- `docs/sprint.md`(Sprint 计划 + Product Backlog)

如果某些文件缺失 → 输出 `MISSING: filename` 并降低该文件 verdict。

### Step 2:按需加载清单

每个文档都有专属 checklist。**必须**读对应清单:

| 评估目标 | MANDATORY 读取                                                 | Do NOT 读取      |
| -------- | -------------------------------------------------------------- | ---------------- |
| PRD      | [references/prd-checklist.md](references/prd-checklist.md)     | add / tasks / sprint 清单 |
| ADD      | [references/add-checklist.md](references/add-checklist.md)     | prd / tasks / sprint 清单 |
| Tasks    | [references/tasks-checklist.md](references/tasks-checklist.md) | prd / add / sprint 清单   |
| Sprint   | [references/sprint-checklist.md](references/sprint-checklist.md) | prd / add / tasks 清单 |

**NEVER 一次性读三个清单**——按用户问哪个读哪个,避免上下文浪费。

### Step 3:跑清单

清单里的每个问题都要回答 **是 / 否 / 部分**。每个"否"或"部分"都会变成一个 issue。

### Step 4:分类 issue 严重度

| 严重度           | 含义                           | 触发条件举例                                                     |
| ---------------- | ------------------------------ | ---------------------------------------------------------------- |
| **critical**     | 文档失去方法论价值,不修不可用 | 缺 §3 非目标;ADD 无 WHY 列;Tasks §1 UC 带 `[x]`;Sprint 缺 Goal/起止日期;sprint.md §1 引用 tasks.md 未定义的 UC/IF;**上游文档引用下游文档内部内容(UC/IF/DA/§X 锚点)** |
| **important**    | 关键质量问题,修后明显提升     | WHY 列是空话;UC 不是 agile 三段式;Critical Lens < 3;Sprint 状态与 git log 脱节 |
| **nice-to-have** | 锦上添花                       | mermaid 解读文字短;Sprint 缺代号;Product Backlog 编号未对齐 sprint-checklist §6.5 |

### Step 5:输出评估报告

格式:

```markdown
## [filename] 评估报告

**Verdict**: PASS / FIX / REWRITE

### Critical issues
- [L42] §3 非目标缺失 → 补全"明确不做的事"清单
- [L120] ADD §1-§5 表格无 WHY 列 → 补具体替代方案对比

### Important issues
- [L88] WHY 列写"为了简单" → 改为具体替代方案

### Nice-to-have
- [L30] mermaid 图后只有 1 段解读 → 补"判断层"段落

## 综合
- critical: N / important: N / nice-to-have: N
- 推荐 verdict: ...
```

### Verdict 规则

- `critical = 0` 且 `important ≤ 2` → **PASS**
- `critical = 0` 且 `important ≥ 3` → **FIX**(修后重审)
- `critical ≥ 1` → **REWRITE**(先修 critical 再走一遍清单)

---

## Mode B:`transform`(评估 + 改造)

适合:"按上面意见改造文档" / "sign-off 没过要修" / "从零写 add.md"。

### 完整 10 步流程

```
Step 1-5: 同 evaluate(跑评估,出 issue + verdict)
  ↓
Step 6: 章节对位(把每个 issue 转成"内容搬迁路径")
Step 7: 跨文档联动扫描(扫三件套引用一致性)
Step 8: 修复路线图(优先级 + 工时估算 + 分批)
Step 9: commit 编排(中间状态保护 + 一次性 commit)
Step 10: 验证闭环(回到 evaluate 模式复评)
```

### Step 6:章节对位分析(Content Mapping)

针对每个 critical issue,产出一张"内容搬迁表":

| Issue | 旧位置 | 新位置 | 处理 | 字数变化 |
|---|---|---|---|---|
| §2 目标缺失 | 无 | 新 §2 | 从零写 5-7 条 SMART | +40 行 |
| §3 非目标缺失 | 无 | 新 §3 | 从零写"明确不做" | +30 行 |
| §4 UC 不是三段式 | 旧 §3 目标用户 | 新 §4 用户场景 | 拆分重写 | ±0 |
| §5 技术方案混入 PRD | 旧 §5(9 子节)| add.md §3-§5 | 整段挪 | -145 行 |
| §7 里程碑缺失 | 无 | 新 §7 | 引用 `sprint.md §1` Sprint 代号 | +15 行 |
| §8 成功指标缺失 | 旧 §2.5"已落地 vs 未接住"| 新 §8 | 重写为可量化 KPI | +20 行 |

**处理方式分类**:
- **平移**(改动 ≤ 20%):保留原文,只调位置
- **拆分**:一段拆到多章(如旧 §4 需求拆到 §2 / §4 / §6)
- **重写**:从零写(如 §2 SMART / §3 非目标)
- **整段挪**:跨文档搬迁(如旧 §5 技术方案 → add.md)
- **删除**:过时或冗余

### Step 7:跨文档联动扫描

扫三件套引用一致性,出"联动矩阵":

| 扫描项 | 命令 | 通过标准 |
|---|---|---|
| PRD 引用 ADD ADR | `grep 'ADR-[0-9]' docs/prd.md` | 每个引用都在 add.md 存在 |
| PRD 引用 tasks UC | `grep 'UC-[0-9]' docs/prd.md` | 每个引用都在 tasks.md 存在 |
| tasks IF 引用 ADD ADR | `grep 'ADR-[0-9]' docs/tasks.md` | 每个引用都在 add.md 存在 |
| add ADR 引用 commit hash | `git show <hash>` 对 N 条逐一 | 全部存在 |
| 死链 | 自查 | 0 |
| **上游→下游内容引用**(⚠️ v3 新增,核心约束) | 见下方"上游不引下游"专项扫描 | 全部 0 |
| **下游→上游引用一致性** | 反向核对下游 ID 是否在对应上游存在 | 全部存在 |

**⚠️ 上游不引下游 专项扫描(v3 必跑)**:

| 扫描项 | 命令 | 通过标准 |
|---|---|---|
| prd.md 引 add.md 内部 | `grep -nE 'add\.md §\|add\.md#\|DA-[0-9]+' docs/prd.md` | 0(允许裸文本提及"add.md"作角色描述) |
| prd.md 引 tasks.md UC/IF | `grep -nE 'tasks\.md (UC\|IF)-[0-9]+-[0-9]+\|(UC\|IF)-[0-9]+-[0-9]+' docs/prd.md` | 0 |
| prd.md 引 sprint.md 内部 | `grep -nE 'sprint\.md §\|sprint\.md#' docs/prd.md` | 0 |
| add.md 引 tasks.md UC/IF | `grep -nE '(UC\|IF)-[0-9]+-[0-9]+' docs/add.md` | 0 |
| add.md 引 sprint.md 任意 | `grep -nE 'sprint\.md' docs/add.md` | 0 |
| tasks.md 引 sprint.md 内部 | `grep -nE 'sprint\.md §\|sprint\.md#' docs/tasks.md` | 0 |

> **注意**:`add.md` 内部 `DA-N` 引用是**自引用**(add.md 是 ADR 的 owner),不算违规;`tasks.md` 内部 `UC/IF` 是**自身 catalog**,也不算违规。只检查**跨文档**引用。

**联动错位检测**(高频问题):
- PRD §4 UC 编号跟 tasks §1.1 UC 编号对不上(单数字 vs 双数字)
- tasks §5 commit hash 跟 git log 对不上
- add.md §7 ADR 引用的 commit hash 在 4ef9c68(squash)内 — 必须标注"(squash)"
- PRD §7 跟 `sprint.md §1` Sprint 代号不一致
- **上游文档出现下游 ID / 章节锚点**(v3 新增,见专项扫描)

### Step 8:修复路线图

按依赖关系 + 工时分批,出"B 模式批次表":

| Batch | 内容 | 工时 | 依赖 | 串/并行 |
|---|---|---|---|---|
| Batch 1 | add.md 骨架 / 新增(独立) | 2-3h | 无 | 与 PRD §1-§5 并行 |
| Batch 2 | add.md §7 18 ADR + §10 Critical Lens | 3-4h | 依赖 git log 完整扫 | 串行 |
| Batch 3 | PRD 章节对位 + 重写 | 2-3h | 依赖 add.md §0-§2 | 串行 |
| Batch 4 | tasks.md UC/IF 范式转换 | 3-4h | 依赖 PRD §4 UC 编号 + add.md §7 ADR | 串行 |
| Batch 5 | 交叉验证 + 一次性 commit | 1h | 必须串行 | — |
| **总计** | | **12-15h**(1.5-2 工作日) | | |

**字段引用一致性约束**:
- Batch 1 完成后,Batch 3 的 PRD 才能引用 ADR-X 编号
- Batch 2 完成后,Batch 4 的 tasks IF 才能引用 ADR-X 编号
- Batch 3 完成后,Batch 4 的 tasks UC 才能引用 prd §4.UC-NN

### Step 9:commit 编排

**中间状态保护**(避免半改入 git):
```
Step 9a: mkdir docs/_draft/ + .gitignore 加 docs/_draft/
Step 9b: 改造全程只在 docs/_draft/ 编辑
Step 9c: 中途被打断 → 直接 rm -rf docs/_draft/(不影响 git)
```

**一次性 commit**(避免增量 commit 噪音):
```
Step 9d: 验证通过后 mv docs/_draft/*.md docs/(原子操作)
Step 9e: git add + 一个 commit(commit message 见下方模板)
```

**commit message 模板**:
```
docs: rewrite PRD/ADD/Tasks to doc-align schema

- prd.md: 412 → N lines, restructure to §1-§9 schema
  - New §2 SMART goals, §3 non-goals, §4 user scenarios (agile 3-segment),
    §6 out-of-scope, §7 milestone/Sprint, §8 success KPIs
  - Moved old §5 tech architecture to ADD §3-§5
- add.md: 0 → N lines, new file
  - §0 Context + §1-§5 Five Views + §6 Scenarios + §7 Decision View (18 ADR)
  - §8 Behavior View + §9 Synthesis + §10 Critical Lens (strict 3)
- tasks.md: N → N lines, UC/IF paradigm
- sprint.md: 新建文件, Sprint 计划 + Product Backlog
  - Milestone/Sprint codes: Sprint 1 Joy / Sprint 2 Sadness / Sprint 3 Fear
  - N UC + N IF + N backlog
  - §N Commit Reference Appendix

Plan: /home/wkevin/.claude/plans/<plan-name>.md
```

### Step 10:验证闭环

回到 `evaluate` 模式复评:

| 验证项 | 命令 | 通过标准 |
|---|---|---|
| prd.md critical 数 | 跑 [prd-checklist.md](references/prd-checklist.md) | 0 |
| add.md critical 数 | 跑 [add-checklist.md](references/add-checklist.md) | 0 |
| tasks.md critical 数 | 跑 [tasks-checklist.md](references/tasks-checklist.md) | 0 |
| 任意 important 数 | | ≤ 2 |
| 交叉引用一致性 | Step 7 全跑 | 全过 |

**若复评仍 REWRITE**:回到 Step 6 重新做章节对位(可能上次分析漏了 issue)。

**若复评 PASS**:输出最终报告,包含改造前后行数对比 + 修复总耗时 + 残留 nice-to-have(可选下次迭代)。

### B 模式输出报告模板

```markdown
## 三件套 transform 报告

### 改造前状态
| 文件 | 行数 | verdict |
|---|---|---|
| prd.md | 412 | REWRITE (critical=4) |
| add.md | 0 (缺失) | REWRITE (critical=1) |
| tasks.md | 328 | REWRITE (critical=4) |

### 改造后状态
| 文件 | 行数 | verdict |
|---|---|---|
| prd.md | 271 | PASS |
| add.md | 1380 | PASS |
| tasks.md | 969 | PASS |

### 修复路线图(实际执行)
| Batch | 内容 | 工时 | commit |
|---|---|---|---|
| Batch 1 | add.md §0-§5 | 实际 | 内含 commit |
| Batch 2 | add.md §6-§10 | 实际 | |
| Batch 3 | PRD 重写 | 实际 | |
| Batch 4 | tasks UC/IF 化 | 实际 | |
| Batch 5 | 验证 + commit | 实际 | |
| **总计** | | **实际** | |

### 残留 nice-to-have(留给下次迭代)
- [ ] xxx
- [ ] yyy
```

---

## 反模式(两种模式通用)

### evaluate 模式反模式

- ❌ **只检查章节存在性**——"§3 在不在"是必要不充分,要看内容质量
- ❌ **接受空话 WHY**——"为了简单 / 性能 / 扩展性"全部记 critical
- ❌ **给未跑清单的文档打 PASS**——必须每个问题都回答
- ❌ **混用中英文术语**——评估报告里术语对齐(UC / IF / Sprint / Version 用英文,其余中文)

### transform 模式反模式

- ❌ **半改半新进 git** — 必须用 `docs/_draft/` 中间目录 + 一次性 commit
- ❌ **跨文档引用编号对不上就 commit** — PRD §4 UC-XX 必须跟 tasks.md §1.1 UC-XX-NN 一致(单数字 vs 双数字)
- ❌ **没有 commit 编排直接动手** — 不分 Batch 会导致依赖倒置(PRD 引用了不存在的 ADR)
- ❌ **跳过 Step 10 验证闭环** — 没有复评就 claim 完工,可能留 critical 不知道
- ❌ **上游引下游内容** — 在 prd.md / add.md / tasks.md 引用下游文档的 ID(UC/IF/DA-N)、章节锚点(§X / #anchor)、或具体描述。违反"上游不引下游"硬约束(v3 核心原则)

---

## 关联(更新)

| Skill | 关系 |
|---|---|
| [`wkevin-idea-realize`](../wkevin-idea-realize/SKILL.md) | 加新需求 → 用 idea-realize(增量联动,不变基线);transform 完成后才能用 idea-realize |
| `dev:code` / `dev:end-to-end` | 代码实现 → 本 skill 不动代码 |
| `wkevin-arch-decoder` | 架构分析 → 从代码反推 ADD;transform 改造 ADD 时可参考 |
| `skill-judge` | 通用 skill 评估 → 评估本 skill 自身用 |

**完整工作流**:
1. **基线评估**:`wkevin-doc-align --mode=evaluate`(确认现状 verdict)
2. **基线改造**:`wkevin-doc-align --mode=transform`(把 REWRITE → PASS)
3. **增量需求**:后续加需求 → `wkevin-idea-realize`(基于 PASS 基线做增量联动)
4. **回滚 / 退一步**:若 transform 失败,保留 `docs/_draft/` 作为 partial state,人工清理