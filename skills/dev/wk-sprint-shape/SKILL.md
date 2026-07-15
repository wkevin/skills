---
name: wk-sprint-shape
description: 从 backlog 通过「优先级 + 依赖图 + 主题聚类」三因子算法,挑选 10-20 个 UC/IF,塑形一个新 Sprint 段(代号 + 版本 + task 列表),或修改已有 Sprint。每次塑形或修改都仅修改 docs/sprint.md §1,读 docs/tasks.md §1.1/§1.2 取 UC/IF 完整定义(只读),绝不改 PRD/ADD/Tasks。算法核心:依赖链 scaffold 拓扑排序 + 跨任务交叉引用推断依赖 + Sprint/Milestone/Production 三层候选池过滤 + 主题聚类生成代号。**输出格式最小化**:段名带版本,不加 emoji / Version / 起止 / Goal 等冗余字段,三子节只在 ≥2 个非空时生成,否则平铺。触发词:"/sprint-shape"、"排个 sprint"、"塑个 sprint"、"开 v0.X"、"做下一版"、"规划下个 sprint"、"从 backlog 抽 10 个 task"。
---

# /sprint-shape — 从 backlog 塑形一个 Sprint

把当前轮用户描述的 sprint/version 规划意图,通过 **三因子塑形算法**(优先级 + 依赖图 + 主题聚类)落到 `docs/sprint.md §1` —— 仅修改 sprint.md,读 `tasks.md §1.1/§1.2` 取 UC/IF 完整定义。每次塑形或修改产出**一个 Sprint 段**(代号 + 版本 + task 列表)。

> **核心定位**:Sprint 塑形(agile Sprint Planning 的工程化版本)
>
> | ❌ 单向写入                            | ✅ 三因子塑形 + 联动校验                              |
> | -------------------------------------- | ----------------------------------------------------- |
> | 用户说"做 v0.5",AI 随手挑 10 个 task   | 用户给目标,AI 按 P 优先级 + 依赖链 scaffold + 主题聚类 |
> | 改了 Sprint 但跟 Active Sprint 重复    | 联动校验:不重复 + 依赖链完整 + UC/IF 都已定义         |
> | 输出臃肿(emoji + 4 字段 + 三子节)   | **输出最小化**:段名带版本,冗余字段只在 ≥2 子节时生成 |

## 接口

```sh
/wk-sprint-shape <塑形意图>
```

**例**:

```sh
/wk-sprint-shape 做 v0.5,主题是批量导入
/wk-sprint-shape 规划下一版,10 个 task
/wk-sprint-shape 修改 Sprint 2,加 UC-04-05
/wk-sprint-shape 给 Sprint 1 加个 bug fix IF-02-03
```

**塑形意图模式**:

| 模式 | 触发 | 行为 |
| --- | --- | --- |
| **新建 Sprint** | "做 vX.X"、"开新 sprint"、"从 backlog 抽 N 个 task" | 从 Product Backlog 挑 10-20 task,创建新 Sprint 段(最小化输出) |
| **修改 Sprint** | "改 Sprint N"、"Sprint 1 加 UC-XX-YY"、"Sprint 2 调一下" | 增删/调整指定 Sprint 段内的 task;状态语义不变 |
| **状态推进** | "激活 Sprint 1"、"Sprint 1 done" | 不动 sprint.md 文件;由用户手改文档(在段头加 `Active` 关键词)或走 task-dev(状态语义由用户最终负责) |

skill 内部根据意图自动选择模式,简单意图直接执行,模糊意图走 1-2 轮澄清。

## 算法核心(三因子)

| 因子 | 数据源 | 算法 | 用途 |
| --- | --- | --- | --- |
| **优先级 (Priority)** | `tasks.md §1.1/§1.2` 标 `[P0/P1/P2/P3]` + `sprint.md §2 Product Backlog` 的 `[P?]` 标签 | 映射到 3 级候选池 | 必选/应选/可选 |
| **依赖图 (Dependency)** | `tasks.md §1.1/§1.2` 显式"依赖"字段(如有)+ 实现细节里的 UC/IF 编号交叉引用 | 拓扑排序 → scaffold 序列 | 前驱 task 必须在同 Sprint 或已完成 |
| **主题聚类 (Theme)** | UC/IF 标题/描述文本(中文分词 + 同义词聚类) | 主导主题 = 该 sprint 的 Goal | 命名代号 + Goal |

**Sprint/Milestone/Production 三层候选池(内部 filter,不写文件)**:

| 候选池 | 入选条件 | 含义 |
| --- | --- | --- |
| **Sprint pool** | `[P0]` ∪ 强依赖当前 milestone | 必须做(sprint-shape 必选) |
| **Milestone pool** | `[P1]/[P2]` ∪ 当前 milestone 范围 | 应该做(优先纳入) |
| **Production pool** | `[P2]/[P3]` ∪ 无明确 milestone 归属 | 可选做(容量允许时纳入) |

完整算法见 [references/sprint-shape-algorithm.md](references/sprint-shape-algorithm.md)。

## 文档系统(本 skill 触及范围)

| 文档 | 读写 | 何时 |
| --- | --- | --- |
| `docs/sprint.md §1 Sprint` | **写**(新增 / 修改 Sprint 段) | 主战场 |
| `docs/sprint.md §2 Product Backlog` | 可选清理(被纳入新 Sprint 的 task 从 Backlog 移除) | 新建 Sprint 时联动 |
| `docs/tasks.md §1.1/§1.2` | **只读** | 取 UC/IF 完整定义 + 优先级 + 依赖 |
| `docs/prd.md` / `docs/add.md` | **不碰** | — |

**关键不变量**:
- Active Sprint ≤ 1(doc-align §1.4.1)—— 创建新 Sprint 时,若有 Active,提示用户先推进
- 输出最小化:不加 emoji / 独立 Version / 起止 / Goal 字段(段名带版本,任务列表自解释)
- 三子节(首次/升级/bug fix)**只在 ≥2 个非空时**生成;单子节情况直接平铺,避免无意义子节头
- 历史 Sprint 段(sprint01-04)保留 legacy 完整字段,doc-align 评估时区分 legacy / current 两种风格

## 何时使用

- 用户说"做下一版 / 开 v0.X / 排个 sprint / 从 backlog 抽 N 个 task"
- 用户要修改已有 Sprint 的内容(加 task / 改 Goal / 改代号)
- 用户要推进 Sprint 状态机(Planning → Active → Done)

## 何时不要使用

- ❌ 项目没有 `docs/sprint.md` 或 `docs/tasks.md`(先跑 `wk-doc-align` 建文档骨架)
- ❌ 文档结构跟 doc-align 不一致(先跑 `wk-doc-align` 的 `transform` 模式改齐)
- ❌ 用户要**加新需求/新 UC/IF**(用 `wk-idea-flesh`,不是 sprint-shape)
- ❌ 用户要**实现 Sprint 内的 task**(用 `wk-task-dev`,不是 sprint-shape)
- ❌ 用户要**评估文档质量**(用 `wk-doc-align`,不是 sprint-shape)

---

## 流程(8 步)

### Step 1:探测文档存在性

```bash
ls docs/sprint.md docs/tasks.md 2>&1
```

| 情况 | 处理 |
| --- | --- |
| 2 个都在 | 进 Step 2 |
| 只有部分 | **先停**——告诉用户缺哪个,按 doc-align 规范补建空模板 |
| 全都不在 | **拒绝执行**——本 skill 只增量更新,不从零搭文档 |

### Step 2:识别塑形模式 + 1-2 轮澄清

读 `sprint.md §1` 现有 Sprint 段列表 + `sprint.md §2` Product Backlog,用 `AskUserQuestion` 1-2 轮澄清意图:

```
Q1. 塑形模式:
   - 新建 Sprint(从 backlog 挑 10-20 task 塑形)
   - 修改 Sprint N(增删/调整 task 或改 Goal/代号)
   - 状态推进(把 Sprint N 从 Planning 推到 Active 或 Done)

Q2. (新建时)Version 归属 + 起止日期:
   - Version: v0.X(用户指定或 skill 建议下一递增版本)
   - 起止: YYYY-MM-DD → YYYY-MM-DD(默认今天 → +14 天,用户可覆盖)

Q3. (新建时)代号风格:
   - 用户给(直接用)
   - skill 建议(基于主题聚类生成,用户可覆盖)
```

澄清完后输出意图摘要:

```
意图摘要:
- 模式: 新建 Sprint
- Version: v0.5
- 代号: Bulk-Onboard
- 起止: 2026-07-14 → 2026-07-28
- Goal: 批量导入 repo 流程完整可用
```

### Step 3:读 backlog 全集 + 构建候选池

```bash
# 1. 读 tasks.md §1.1 UC 完整定义
awk '/^## §1\.1/,/^## §1\.2/' docs/tasks.md

# 2. 读 tasks.md §1.2 IF 完整定义
awk '/^## §1\.2/,/^## §2/' docs/tasks.md

# 3. 读 sprint.md §2 Product Backlog 当前条目
awk '/^## §2/,/^## §3/' docs/sprint.md

# 4. 读 sprint.md §1 现有 Sprint 段(避免重复)
awk '/^## §1/,/^## §2/' docs/sprint.md
```

**提取每个 UC/IF 的元数据**:

```
UC/IF ID | 优先级 | 依赖(scaffold) | 主题关键词 | 是否已在 Sprint
UC-05-01 | P3     | 无              | 批量导入    | 否
UC-04-05 | P1     | 依赖 UC-04-01   | 用户认证    | 否
IF-05-01 | P3     | 配套 UC-05-01   | 批量导入    | 否
...
```

### Step 4:3 级分类(内部 filter,不写文件)

按上表"优先级 + 依赖 + milestone 归属"分类,候选池:

```
Sprint pool(必选):
- UC-04-05 [P1] 依赖 UC-04-01(强依赖当前 milestone)

Milestone pool(应选):
- UC-04-01 [P1] 用户认证核心
- IF-04-02 [P1] 认证 IF

Production pool(可选):
- UC-05-01 [P3] 批量导入
- IF-05-01 [P3] CSV 解析批处理
```

### Step 5:依赖图拓扑排序 + 主题聚类

**5a. 依赖图构建**:

两个数据源(算法细节见 references/sprint-shape-algorithm.md §1):

1. **显式依赖**:`tasks.md §1.1/§1.2` 实现细节里的 "依赖:" 字段(如有)
2. **推断依赖**:扫描实现细节里提到的其他 UC/IF 编号,如:
   ```
   **实现细节**:
     - 复用 IF-03-02 的解析逻辑  ← 推断 UC-XX-YY 依赖 IF-03-02
   ```

**5b. 拓扑排序**:
- 对新 Sprint 内所有候选 task 做 topological sort
- 输出 scaffold 序列(前驱 → 后继)
- 检测:**前驱 task 不在新 Sprint 或未 Done** → 警告并提示用户确认

**5c. 主题聚类**:
- 中文分词 + 同义词聚类(参考 references/sprint-shape-algorithm.md §2)
- 主导主题 = 出现频次最高的关键词簇
- 同主题 task 排在一起,辅助后续 §1.2 拆"首次实现 / 升级 / bug fix"

### Step 6:挑 10-20 task + 拆三子节

**6a. 10-20 task 挑选启发式**:

1. **必选** Sprint pool 全部
2. **应选** Milestone pool 按 dependency scaffold 顺序往下游,直到接近 2 周工作量上限
3. **可选** Production pool 在剩余容量内按主题聚类补充
4. **硬约束**:10 ≤ task 数 ≤ 20(用户可在提议时覆盖)

**6b. 工作量预估**(粗估):
- 简单(半天):UC/IF 实现细节 ≤ 2 条
- 中等(1 天):3-5 条
- 复杂(2-3 天):>5 条或涉及架构变更
- 目标:总工作量 ≤ 2 周(10 工作日)

**6c. 拆三子节**(首次实现 / 升级 / bug fix):

| 子节 | 入选条件 | 示例 |
| --- | --- | --- |
| **首次实现** | UC/IF 之前未在任何 Sprint 出现过(历史 git log 也无) | UC-05-01, IF-05-01 |
| **升级** | 同 UC/IF 在历史 Sprint 出现过(增量改进) | "upgrade: UC-04-05 加密码强度校验" |
| **bug fix** | 已有 issue / 已知缺陷 / 用户报告 | "fix: IF-02-03 NPE on empty input" |

每条标注格式:`首次实现 / 升级 / bug fix` 前缀,doc-align §1.2.3 要求。

### Step 7:提议联动改动 + 写入 sprint.md §1

**7a. 提议预览**:

```
提议(新建 Sprint):

[sprint.md §1 新增段]

### Sprint 3 — Bulk-Onboard (v0.5)

- [ ] UC-04-05 [P1] 用户密码强度校验(作为 终端用户,我希望 注册时密码必须 ≥ 8 位 + 数字字母,以便 提升账号安全)
- [ ] UC-05-01 [P3] 批量导入 repo(作为 知识库管理员,我希望 上传 CSV 一次性导入多 repo,以便 不用逐个粘贴 URL)
- [ ] IF-05-01 [P3] CSV 解析批处理

(若 3 类 ≥ 2 个非空 才拆子节;此处仅"首次实现"非空,平铺)

联动一致性预检:
- Sprint 数:0 → 1,未超 doc-align §1.4.1 上限 ✓
- 引用 UC/IF 都在 tasks.md §1.1/§1.2 定义:✓ (3/3)
- 依赖 scaffold:UC-04-05 依赖 UC-04-01(已 Done 在 Sprint 1)✓
- 主题聚类:主导 = "批量导入"(3/3 task)✓
- 代号生成:Bulk-Onboard(主题聚类 + Ubuntu 风格小写连字符)✓

OK 就改?
```

**7b. 写入 sprint.md §1**:

```bash
# 在 ## §1 末尾追加新 Sprint 段(若 §1 已有 Sprint 1,2,新 Sprint 接续编号)
# 同时从 sprint.md §2 Product Backlog 移除被纳入的 task
```

**编号冲突检测**:

```bash
LAST_SPRINT=$(grep -oE "Sprint [0-9]+" docs/sprint.md | sort -V | tail -1 | awk '{print $2}')
NEXT_SPRINT=$((LAST_SPRINT + 1))
echo "$NEXT_SPRINT"
```

### Step 8:联动校验 + commit

```bash
# 1. Sprint 数量 ≤ 1 Active(doc-align §1.4.1)
# 用户手改时在段头加 'Active' 关键词
ACTIVE_COUNT=$(awk '/^### Sprint/{flag=1} flag && /Active/{count++; flag=0} END{print count}' docs/sprint.md)
[ "$ACTIVE_COUNT" -le 1 ] || echo "WARN: Active Sprint > 1"

# 2. 新 Sprint 引用 UC/IF 都在 tasks.md 定义?
NEW_REFS=$(grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/sprint.md | sort -u)
ALL_DEFINED=$(grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/tasks.md | sort -u)
comm -23 <(echo "$NEW_REFS") <(echo "$ALL_DEFINED")
# 应为空

# 3. 依赖 scaffold 完整?前驱 task 都在新 Sprint 或 Done
# (算法见 references/sprint-shape-algorithm.md §3)

# 4. 跨 sprint.md 一致性:被纳入的 task 已从 §2 Backlog 移除?
for ref in $NEW_REFS; do
  grep -c "^\- \[ \] $ref" docs/sprint.md  # §2 应 = 0
done
```

**提议 commit**(仅改 sprint.md):

```bash
git add docs/sprint.md
git commit -m "sprint: 加 Sprint 3 Bulk-Onboard v0.5 (10-20 task, 主题聚类)"
```

---

## 硬约束(含 WHY)

1. **仅修改 `docs/sprint.md`**(§1 + 可选 §2 Backlog 清理)—— WHY: 与 task-dev 写入边界对齐;PRD/ADD/Tasks 是 idea-flesh 的职责。
2. **每个新 Sprint 10-20 task**(默认)—— WHY: Scrum 团队典型 velocity;过多 = sprint 失控,过少 = 浪费迭代。
3. **Sprint 内三子节拆分只在 ≥2 个非空时生成**—— WHY: 单子类非空时拆子节是无意义冗余;硬约束保持 doc-align §1.2.1 的精神但放宽到按需拆分。
4. **新 Sprint 状态由用户手改**—— WHY: 状态机推进(Planning → Active → Done)是业务承诺,本 skill 不擅自激活;用户可在 commit 后手改段头加 `Active` 关键词。
5. **Active Sprint ≤ 1**—— WHY: doc-align §1.4.1;多 Active 并行会让 commit 节奏混乱。
6. **不创建任务本身**(只搬运已有 UC/IF)—— WHY: 新 UC/IF 由 idea-flesh 负责;本 skill 只做"从池子挑 task 入 Sprint"。
7. **不实现任务**—— WHY: 实现是 task-dev 的职责;本 skill 只塑形,不动代码。
8. **依赖 scaffold 完整**(前驱在新 Sprint 或 Done)—— WHY: 否则 Sprint 开始后才发现前置缺失,等于 Sprint 失败。
9. **Sprint 起止日期连贯**(不与历史 Sprint 重叠或大空隙)—— WHY: doc-align §6.2 nice-to-have;连贯的迭代节奏便于 retrospective。
10. **commit message subject ≤ 60 字 + sprint 前缀**—— WHY: git log 可读性 + 与 idea-flesh/task-dev 风格一致。
11. **不创建新 §X 章节**(§3 Milestone Backlog / §4 Production Backlog)—— WHY: doc-align §2 + sprint-checklist.md §2 评估基线按 §1/§2;改结构要同步 doc-align,成本高。
12. **主题聚类不强制**(用户可指定 Goal)—— WHY: 启发式是辅助,人最终拍板。

## 模板

### Sprint 段(最小化输出)

```markdown
### Sprint {N} — {代号} (v{X.Y})

- [ ] {UC-NN-NN | IF-MM-NN} [{P0|P1|P2|P3}] {标题}
- [ ] upgrade: {UC-NN-NN | IF-MM-NN} {标题}     (仅当存在 upgrade 类 task)
- [ ] fix: {UC-NN-NN | IF-MM-NN} {标题}         (仅当存在 bug fix 类 task)
- [ ] {UC-NN-NN | IF-MM-NN} [{P0|P1|P2|P3}] {标题}
...
```

**三子节规则**:仅当 ≥2 个子类(首次实现 / 升级 / bug fix)非空时,才拆 `#### 首次实现` / `#### 升级` / `#### bug fix` 子节。子类计数规则:
- `首次实现` = 历史 Sprint 未出现过的 UC/IF
- `升级` = 历史 Sprint 出现过,本次为增量改进(标 `upgrade:` 前缀)
- `bug fix` = 修已知 bug(标 `fix:` 前缀)

单子类非空情况(典型:`首次实现` 7 条,`升级` 0 条,`bug fix` 0 条)直接平铺,不要 2 个空子节占行。

### Sprint Backlog 清理(纳入新 Sprint 后,从 §2 移除)

```bash
# 旧(在 §2)
- [ ] UC-05-01 批量导入 repo

# 新(Sprint 3 已收,§2 删除该行)
```

## 联动反模式

- ❌ **跳过依赖检查** — Scaffold 残缺,Sprint 开始才发现前置缺失
- ❌ **task 数 < 10 或 > 20** — 不符合 Scrum velocity,doc-align 会标记(用户明确接受 < 10 时记录)
- ❌ **3 子类都强加**(即使子类空)— 输出臃肿,需用户手动删
- ❌ **新 Sprint 状态直接 Active** — 业务承诺过早
- ❌ **同时多 Active Sprint** — doc-align §1.4.1 违规
- ❌ **改动 PRD/ADD/Tasks** — 越权;那是 idea-flesh 的工作
- ❌ **不检查 §2 Backlog 联动清理** — 新 Sprint 收了 task 但 §2 还有同一行 = 重复
- ❌ **跳过主题聚类** — Sprint 没有代号/版本,只剩 task 列表,失去 Sprint 灵魂
- ❌ **代号风格不一致** — 有的 "Bulk Onboard" 有的 "bulk-onboard",与已有 Sprint 代号风格对齐

## Worked Example

**用户**:`/wk-sprint-shape 做 v0.5,主题批量导入,10 个 task`

**Step 2 意图识别**:

```
意图摘要:
- 模式: 新建 Sprint
- Version: v0.5
- 代号: Bulk-Onboard(skill 建议)
```

(默认起止 2 周 / Goal 隐含在段名 — 用户明确要求才生成)

**Step 3-6 三因子塑形**(摘要):

```
候选池:
- Sprint pool: (空,无 P0)
- Milestone pool: UC-04-05[P1](依赖 UC-04-01 Done), IF-04-02[P1]
- Production pool: UC-05-01[P3], IF-05-01[P3], UC-05-02[P3](批量导入 UI)

依赖图:
- UC-04-05 → UC-04-01(Done ✓)
- IF-05-01 → UC-05-01(scaffold)
- UC-05-02 → UC-05-01(推断,实现细节提到)

主题聚类:
- "批量导入":UC-05-01, IF-05-01, UC-05-02(3 个)
- "用户认证":UC-04-05, IF-04-02(2 个)
- 主导:Bulk Onboarding

挑选结果(10 个 task,工作量预估 9.5 天):
- 首次实现 7 条
- 升级 1 条(upgrade: UC-04-05 加密码强度)
- bug fix 2 条(fix: IF-02-03, fix: IF-03-05)
```

**Step 7 提议**(已在上面 §7a 给出)。

**Step 8 commit**:

```bash
git add docs/sprint.md
git commit -m "sprint: 加 Sprint 3 Bulk-Onboard v0.5 (10 task, 主题批量导入)"
```

---

## 不做的事

- ❌ 不创建 UC/IF(idea-flesh 的事)
- ❌ 不实现 task(task-dev 的事)
- ❌ 不修改 PRD/ADD/Tasks(只读)
- ❌ 不创建新 §X 章节(§3/§4 等)
- ❌ 不擅自激活 / 推进 Sprint 状态(用户手改或走 task-dev)
- ❌ 不评估文档质量(doc-align 的事)
- ❌ 不写代码或修改 `src/` 等实现文件
- ❌ 不处理"已实现的 task 但 sprint.md 未勾 [x]"的同步(那是 task-dev 或人工)

## 回滚

如果用户塑形后说「这条不要了」或「改错了」:

```bash
# 软回滚:撤销最后一次 docs/sprint.md 改动
git checkout HEAD~1 -- docs/sprint.md

# 或生成 revert commit(更安全,保留历史)
git revert <commit-hash>
```

回滚后建议跑 `wk-doc-align` 的 `evaluate` 模式确认 sprint.md 没破坏基线。

## 关联

- **上游**:
  - [`wk-idea-flesh`](../wk-idea-flesh/SKILL.md) — 把新 UC/IF 落到 tasks.md + sprint.md §2 Backlog,本 skill 从 §2 挑 task
  - [`wk-doc-align`](../wk-doc-align/SKILL.md) — 评估 sprint.md 是否对齐 §1 Sprint + §2 Backlog 范式;本 skill 输出必须 pass 评估
- **下游**:
  - [`wk-task-dev`](../wk-task-dev/SKILL.md) — 实现本 skill 塑形的 §1 Sprint 段内 [ ] task;Prd/Add/Tasks 只读
- **同族 pipeline**(塑形链):
  - `wk-idea-flesh` → 把模糊想法 flesh out 到设计文档
  - `wk-sprint-shape`(本 skill) → 把 backlog 塑形到 Sprint 段
  - `wk-task-dev` → 把 Sprint 段的 [ ] 实际开发成 [x]
- **配套**:本 skill 写完后若 Sprint 量大,建议跑 `wk-doc-align` 的 `evaluate` 模式做最终 sign-off