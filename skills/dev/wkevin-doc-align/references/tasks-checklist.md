# Tasks 评估清单

对 `docs/tasks.md` 逐节评估。本文件评估 **UC/IF 定义**(产品 catalog),Sprint 计划与进度请跳到 [sprint-checklist.md](sprint-checklist.md)。

## 0. 文件级检查

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 0.1 | 文件存在 | | critical |
| 0.2 | 顶部有文档范式说明(UC / IF 含义 + 与 sprint.md 的分工) | | important |
| 0.3 | 优先级定义明确(P0 / P1 / P2 / P3) | | nice-to-have |
| 0.4 | 文件边界说明:UC/IF 完整定义在本文件;Sprint / Backlog / 状态在 `sprint.md` | | important |

---

## 1. §1.1 User Case(用户视角)

### 1.1.1 编号规则

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 1.1 | UC 编号格式 `UC-xx-yy`(xx 分组,yy 流水号) | | important |
| 1.2 | UC **不带 `[x]` / `[ ]` 状态**——状态归 sprint.md | | critical |
| 1.3 | UC **不带实现细节以外的内容**(不混 IF 职责) | | important |

### 1.1.2 agile 三段式格式

每条 UC 必须有 **作为 / 我希望 / 以便** 三个标签(中文)。

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 2.1 | **作为** 标签存在 | | important |
| 2.2 | **我希望** 标签存在 | | important |
| 2.3 | **以便** 标签存在 | | important |
| 2.4 | "作为" 后跟具体角色 / 场景,不是 "user" 这种空泛词 | | important |
| 2.5 | "我希望" 是动作 + 对象,不是 "to do something" 的机翻 | | important |
| 2.6 | "以便" 是价值 / 动机,不是 "so that I can" 的字面翻译 | | important |

**反模式**:

```
❌ - **UC-01-01** [P1]
   - **As a** developer
   - **I want** to do something
   - **So that** I can achieve something
   → 机翻:所有关键词都是英文,没翻译
   → 标签不规范:作为 / 我希望 / 以便 不写出来

❌ - **UC-01-01** [x] 添加 repo
   → 状态 [x] 错放位置(应在 sprint.md Sprint)
```

### 1.1.3 实现细节嵌套

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 3.1 | **实现细节** 子标题存在 | | important |
| 3.2 | 实现细节列在 **agile 三段式之后**(不是同级) | | critical |
| 3.3 | 实现细节写**关键技术点**(文件路径 / 函数名 / 配置值) | | important |
| 3.4 | 实现细节不重复 UC 故事(不再讲一遍"作为...") | | nice-to-have |

**结构示意**:

```markdown
✅ - **UC-01-01** [P1]
   - **作为** ...
   - **我希望** ...
   - **以便** ...
   - **实现细节**:
     - 文件路径 / 函数名
     - 配置值 / 子步骤
```

### 1.1.4 UC 内容质量

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 4.1 | UC 至少 5 条(更少 = 文档没认真列) | | important |
| 4.2 | UC 业务分组合理(按业务域 / 模块 / 用户场景分) | | nice-to-have |
| 4.3 | UC 优先级 `[P0-P3]` 都标 | | nice-to-have |

---

## 2. §1.2 Inner Feature(系统内在)

### 2.1 编号规则

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 5.1 | IF 编号格式 `IF-mm-nn` | | important |
| 5.2 | IF 同样**不带状态**(状态归 sprint.md) | | critical |

### 2.2 IF 格式

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 6.1 | IF 用 **特性描述 + 实现细节** 拆分 | | important |
| 6.2 | **特性描述** 一句中文说清"这个功能干什么、解决什么问题" | | critical |
| 6.3 | 实现细节同 UC(技术点 + 路径) | | important |

**IF vs UC 的区分**:

| | UC | IF |
|---|---|---|
| 视角 | 用户能做什么 | 系统如何实现 |
| Persona | "作为 X 开发者" | 无 persona |
| 故事 | 作为 / 我希望 / 以便 | 特性描述 |
| 例 | "添加 repo" | "Octokit 抓取元数据" |

---

## 3. 附录:UC/IF ↔ 历史编号映射(可选)

> **v3 经验**:这些是 optional 章节,transform 模式**默认不加**,按项目需要决定。如果 v1 拆分前用 M*-T* 编号,确实需要追溯时再加;不需要就完全跳过。

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 8.1 | 历史 M*-T* / 其他旧编号映射到 UC / IF(追溯用) | | nice-to-have |
| 8.2 | 旧 milestone 不在正文中展开(仅在附录列映射) | | important |

> 注:历史 M*-T* 编号指拆分前的 Milestone / Task 编号,保留作为可追溯性。

## 3.5 tasks.md 可选章节清单(v3 经验)

> **核心规则**:`tasks.md` 应当 **lean** — 主要内容是 §1 UC/IF catalog。**下面这些章节都是 optional**,**默认不加**;除非项目明确需要,否则不写。

| 章节 | 何时加 | 何时**不**加 | 失败案例 |
| --- | --- | --- | --- |
| **§3 决策依赖 (D-1 ~ D-N)** | 跨 UC/IF 的关键决策确实需要独立解释(如 D-1: 写路径必走 Server Action),且在 UC/IF 各自特性描述里说不清楚 | UC/IF 自身的"实现细节"已能解释 | v3 实施时自动加 70 行,用户**全部删除**(决策已分散在 UC/IF + add.md §7 ADR) |
| **§4 历史 M*-T* 映射附录** | 项目从 M*-T* 编号体系迁移过来,git log / 旧 issue 还在用旧编号 | 没有 v1 拆分前的 M*-T* 编号 | v3 实施时自动加 25 行,用户**全部删除**(项目已经定型 1 年,旧编号无价值) |
| **§5+ 任何额外章节** | 真的需要 | 默认不加 | v3 反复栽跟头 |

**WHY 不加**:tasks.md 主要价值是"UC/IF 单一来源",决策、历史、未来 — 都有更适合的地方(决策 → add.md §7 ADR;历史 → git log;sprint → sprint.md)。**额外章节让 catalog 文件变成杂烩**。

---

## Tasks 综合判定

| critical 数 | important 数 | verdict |
|---|---|---|
| 0 | ≤ 3 | **PASS** |
| 0 | ≥ 4 | **FIX** |
| ≥ 1 | 任意 | **REWRITE** |

**最常见的 3 个 Tasks 问题**:

1. **§1 UC 带 `[x]` / `[ ]`**——状态错放位置,应该是 `sprint.md` Sprint 段
2. **UC 不是 agile 三段式**——直接写"作为 dev / I want to" 没翻译成中文
3. **UC 没在 sprint.md §1 Sprint 或 §2 Product Backlog 引用**——定义孤岛,没人排期

---

## 4. 范式对标(tasks.md 自包含范式)

> 评估时检查 tasks.md 是否对齐这些范式特征。**必须**采用某种明确范式,不强制跟某外部项目一致。

| # | 检查项 | 严重度 |
|---|---|---|
| 4.1 | **顶部有"文档范式"声明** — UC / IF / P0-P3 优先级定义齐全 | important |
| 4.2 | **有"文档导航"表** — §1 / §3 章节指向链接 | nice-to-have |
| 4.3 | **UC 编号 `UC-mm-nn`(双数字,业务分组)** — 不是单数字如 `UC-01` | important |
| 4.4 | **IF 编号 `IF-mm-nn`(双数字,工程分组)** — 不是 `IF-XX.YY` 带点格式 | important |
| 4.5 | **每条 UC/IF 标题行带 `[P0]` / `[P1]` / `[P2]` / `[P3]` 优先级标** | important |
| 4.6 | **UC agile 三段式用中文标签**(作为 / 我希望 / 以便)— 不混英文 `As a/I want/So that` | critical |
| 4.7 | **UC/IF 不带状态** — 状态全部归 `sprint.md` | critical |
| 4.8 | **本文件不含 Sprint / Backlog / Milestone 章节** — 那些在 `sprint.md` | critical |

**为什么强制范式**:无范式 = 各项目各写各的,读者跨项目读 5 个 tasks.md 会迷惑。明确范式 = 跨项目可读性。

> Sprint / Backlog 范式请参考 [sprint-checklist.md §6](sprint-checklist.md)。

---

## 5. 跨文档引用一致性(cross-doc)

> **依赖方向(核心原则)**:prd → add → tasks → sprint。**tasks 是 sprint 的上游**,**上游文档不引用下游文档内的内容**(sprint 章节锚点 / 具体状态符号)。允许 file-level 链接(`[sprint.md]` 形式)与角色描述("sprint.md = 当前进度")。
>
> **注意**:`tasks.md` 内部 `UC-XX-NN` / `IF-XX-NN` 是**自身 catalog**,**不算违规**;`add.md` 内部 `DA-N` 是 ADR 的 owner 自引用,也不违规。只检查**跨文档**引用 + 下游内容展开。

| # | 检查项 | 命令 / 方法 | 严重度 |
|---|---|---|---|
| 5.1 | **tasks §1.1 UC 编号跟 PRD §4 UC 编号一致**(都用 `UC-mm-nn` 双数字) | `grep '^### UC-' docs/tasks.md` 跟 `docs/prd.md §4` 比对 | critical |
| 5.2 | **tasks §1.2 IF 引用的 ADR 编号在 `docs/add.md` §7 存在** | `grep 'ADR-[0-9]' docs/tasks.md` 验证每个引用 | critical |
| 5.3 | **tasks §3 决策依赖(D-1~D-N)跟 PRD §1.2 / §3 一致** | 比对决策表 | important |
| 5.4 | **tasks agile 三段式跟 PRD §4 用同一种语言** | 人工抽检 2-3 条 | important |
| 5.5 | **sprint.md §1 引用的 UC/IF 都在本文件 §1.1/§1.2 定义** | `comm -23 <(grep -oE "UC-[0-9]+-[0-9]+\|IF-[0-9]+-[0-9]+" docs/sprint.md \| sort -u) <(grep -oE "UC-[0-9]+-[0-9]+\|IF-[0-9]+-[0-9]+" docs/tasks.md \| sort -u)` 应为空 | critical |
| **5.6** | **⚠️ 上游不引下游 — tasks 不引 sprint.md 章节锚点** | `grep -nE 'sprint\.md §\|sprint\.md#' docs/tasks.md` | **critical**(v3 新增) |
| **5.7** | **⚠️ 上游不引下游 — tasks 不展开 sprint.md 章节内容**(如"见 sprint.md §3 当前状态"应改为"详见 sprint.md"file-level 链接) | 人工抽检:`[sprint.md]` 链接 + 角色描述 vs 具体章节锚点 | **important**(v3 新增) |
| 5.6 | **sprint.md §2 Product Backlog 引用的 UC/IF 都在本文件 §1.1/§1.2 定义** | 同上(覆盖 sprint.md 全文) | critical |

---

## 6. 加载指引

本文件仅在评估 tasks.md 时加载。如果用户问"评估 sprint.md"——不要读此文件,跳到 [sprint-checklist.md](sprint-checklist.md)。

本 skill 触发名:`/doc-align`。