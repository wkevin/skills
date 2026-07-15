# Sprint 评估清单

对 `docs/sprint.md` 逐节评估。

## 0. 文件级

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 0.1 | 文件存在 | | critical |
| 0.2 | 顶部有 Sprint / Version 范式说明(术语定义) | | important |
| 0.3 | Sprint 状态机定义清楚(🟡 Planning / 🔵 Active / 🟢 Done / ⚫ Cancelled) | | important |
| 0.4 | Sprint 与 Version 关系说明(Sprint = 迭代周期,Version = 发布版本) | | important |

---

## 1. §1 Sprint

### 1.1 Sprint 基本约束

每个 Sprint 必须有:

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 1.1 | 编号(Sprint 1, Sprint 2, ... — 顺序递增) | | critical |
| 1.2 | **代号**(主题命名,类似 Ubuntu code name) | | important |
| 1.3 | **起止日期**(YYYY-MM-DD → YYYY-MM-DD) | | critical |
| 1.4 | **Goal**(一句话描述本次 Sprint 目标) | | critical |
| 1.5 | **Version 归属**(v0.1 / v0.5 / v1.0-rc 等) | | important |
| 1.6 | **状态**(🟡 Planning / 🔵 Active / 🟢 Done / ⚫ Cancelled) | | critical |

### 1.2 Sprint 拆解

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 2.1 | 每个 Sprint 拆**初次实现** + **优化 / bug fix** 两节 | | important |
| 2.2 | 同一 UC / IF 可在多个 Sprint 中**多次出现**(初次 + 优化 + fix) | | important |
| 2.3 | 优化 / fix 条目带说明("upgrade: ..." / "fix: ...") | | nice-to-have |
| 2.4 | Sprint 内 UC/IF 引用都用 `UC-NN-NN` / `IF-MM-NN` 编号(从 tasks.md §1.1/§1.2 引用) | | critical |

### 1.3 状态语义

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 3.1 | `[x]` 完成 · `[~]` 进行中 · `[ ]` 待办 · `[!]` 阻塞 定义明确 | | important |
| 3.2 | 没有 `[x]` 但 git log 显示已实现 = 文档与现实脱节 | | critical |
| 3.3 | 没有 `[ ]` 但实现未完成 = 虚报完成 | | critical |

### 1.4 Sprint 数量约束

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 4.1 | 当前 Active / Planning 中的 Sprint ≤ 1(避免多 Sprint 并行) | | important |
| 4.2 | 历史 Done / Cancelled Sprint 可保留多个(用作历史追溯) | | nice-to-have |

---

## 2. §2 Product Backlog

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 5.1 | Product Backlog 用 `[ ]` 标识(**未**排进任何 Sprint) | | important |
| 5.2 | 条目带优先级 `[P0]` / `[P1]` / `[P2]` / `[P3]`(Backlog 默认 `[P3]` 远期) | | important |
| 5.3 | 编号格式 `UC-NN-NN` / `IF-MM-NN`(同 tasks.md 编号空间) | | critical |
| 5.4 | Product Backlog 条目必须在 `tasks.md §1.1` / `§1.2` 有完整定义 | | critical |
| 5.5 | Product Backlog 与"已完成历史"**不重复**——已实现的合并到 Sprint | | important |
| 5.6 | 不使用 `UC-BL-NN` 自创格式(跟 tasks-checklist §6.10 保持一致) | | important |

---

## 3. Sprint ↔ Version 关系

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 6.1 | 每个 Version 覆盖明确 Sprint 范围(1+ 个 Sprint) | | important |
| 6.2 | Sprint 起止日期连贯(无重叠,无大空隙) | | nice-to-have |
| 6.3 | Version 字符串格式一致(`vMAJOR.MINOR` 或 `vMAJOR.MINOR-rc` 等) | | nice-to-have |

---

## 4. 跨文件一致性(cross-doc)

| # | 检查项 | 命令 / 方法 | 严重度 |
|---|---|---|---|
| 7.1 | **sprint.md §1 引用的 UC/IF 都在 `tasks.md §1.1/§1.2` 定义** | `comm -23 <(grep -oE "UC-[0-9]+-[0-9]+\|IF-[0-9]+-[0-9]+" docs/sprint.md \| sort -u) <(grep -oE "UC-[0-9]+-[0-9]+\|IF-[0-9]+-[0-9]+" docs/tasks.md \| sort -u)` 应为空 | critical |
| 7.2 | **tasks.md §1.1/§1.2 的 UC/IF 至少在 sprint.md 中有引用或在 Product Backlog** | 反向 `comm -23` 比对;列出"已定义但未引用"的 UC/IF(应为远期 Backlog,允许少量) | important |
| 7.3 | **Sprint 代号跟 PRD §7 里程碑表(如有)对齐** | 比对 `sprint.md §1` 与 `prd.md §7` | important |
| 7.4 | **sprint.md §1 Sprint N 状态跟 task-dev 实际进度一致** | `git log --oneline \| grep feat(UC-XX-YY)` 比对 [x] | critical |

---

## 5. Sprint 综合判定

| critical 数 | important 数 | verdict |
|---|---|---|
| 0 | ≤ 3 | **PASS** |
| 0 | ≥ 4 | **FIX** |
| ≥ 1 | 任意 | **REWRITE** |

**最常见的 3 个 Sprint 问题**:

1. **§1 Sprint 缺 Goal / 起止日期** —— 没有 Goal 的 Sprint 像没方向的迭代,无法评估成功
2. **sprint.md §1 引用了 tasks.md 未定义的 UC/IF** —— 跨文件失同步
3. **Sprint 状态跟实际脱节** —— [x] 但 git log 没对应 commit,或 git log 已有 commit 但 [ ]

---

## 6. Sprint 范式

> **Sprint** 是 agile 方法论中的迭代周期单位(典型 2 周),一个 Sprint 有一个明确的 Goal,产出可演示的功能增量。
>
> **Version** 是发布版本,由 1+ 个 Sprint 的累计产出形成。
>
> **Product Backlog** 是所有未排进 Sprint 的需求池,优先级动态调整。
>
> 评估时检查 sprint.md 是否对齐这些范式特征。**必须**采用某种明确范式,不强制跟某外部项目一致。

| # | 检查项 | 严重度 |
|---|---|---|
| 6.1 | **Sprint 标题三字段** — 代号 + 起止日期 + Goal | critical |
| 6.2 | **Sprint 状态机清晰** — 🟡/🔵/🟢/⚫ 四态定义完整 | important |
| 6.3 | **Sprint 拆"初次实现" + "优化与 bug fix"两节** | important |
| 6.4 | **Product Backlog 在 §2**(独立于 Sprint) | nice-to-have |
| 6.5 | **Product Backlog 编号 `UC-NN-NN` / `IF-MM-NN`(标 `[P3]`)** | important |
| 6.6 | **Sprint 引用 tasks.md §1.1/§1.2 的 UC/IF,不重定义** | critical |

---

## 加载指引

本文件仅在评估 sprint.md 时加载。如果用户问"评估 tasks.md"——不要读此文件,跳到 [tasks-checklist.md](tasks-checklist.md)。

本 skill 触发名:`/doc-align`。
---

## 7. sprint.md 可选章节清单(v3 经验)

> **核心规则**:`sprint.md` 应当 **lean + 灵活** — 不要强加"§1 Sprint / §2 Product Backlog / §3 当前状态 / §4 Commit Reference Appendix" 死板结构。**项目可自由组织**(gh-curio v3 实战 = `## MileStone 01` / `## MileStone 02` / `## Product Backlog` 扁平结构)。

| 章节 | 何时加 | 何时**不**加 | 失败案例 |
| --- | --- | --- | --- |
| **§1 Sprint 计划(Sprint N 列表)** | 项目有"短周期迭代"概念(2-4 周一个 Sprint) | 个人项目,无短周期迭代,只发"Milestone/Version" | — |
| **§2 Product Backlog** | 有"未来候选"独立于 Milestone | 候选都合并到 Milestone 描述里,无独立 backlog | — |
| **§3 当前状态(`[x]/[ ]` 列表)** | Sprint/Milestone 状态需显式追踪 | 状态用 commit message / git log 追踪,文档不重复 | — |
| **§4 Commit Reference Appendix** | 需要"commit hash → UC/IF 映射"做 milestone ↔ 代码双向追溯 | 默认不加;**git log + `git log --grep` 已能查** | v3 实施时自动加 50 行,用户**全部删除** |
| **§5+ 任何额外章节** | 真的需要 | 默认不加 | v3 反复栽跟头 |

**WHY 不加 §4 Commit Reference**:commit 历史已经在 git 里 (`git log` / `git blame`);文档里复制一份 = 信息重复 + git log 一变文档就过期。**用 commit message 本身的 `feat(UC-XX-YY): ...` 格式**就够了,比文档附录更好查。

**MileStone vs Sprint**:
- **Sprint** = 2-4 周短迭代(agile Scrum 概念);适合团队 / 有 review 节奏的项目
- **MileStone** = "v0.1 / v0.5 / v1.0" 长周期发布节点(gh-curio 用这个)
- v3 实战:gh-curio 用 **MileStone** 而非 Sprint,文档结构是 `## MileStone 01` / `## MileStone 02` 扁平
- **不要强加 Sprint 范式**:checklist §6 描述的是"短迭代"项目;单用户长期项目用 MileStone 更合适

**§X 编号灵活原则**:
- 不要强加 §1-§N;项目自创结构(MileStone 01/02)同样合规
- 章节标题用项目自己的命名,不用"§1 Sprint 计划 / §2 Product Backlog" 这种通用模板
