# Tasks 评估清单

对 `docs/tasks.md` 逐节评估。

## 0. 文件级检查

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 0.1 | 文件存在 | | critical |
| 0.2 | 顶部有文档范式说明（UC / IF / Milestone 含义） | | important |
| 0.3 | 优先级定义明确（P0 / P1 / P2 / P3） | | nice-to-have |

---

## 1. §1.1 User Case（用户视角）

### 1.1.1 编号规则

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 1.1 | UC 编号格式 `UC-xx-yy`（xx 分组，yy 流水号） | | important |
| 1.2 | UC **不带 `[x]` / `[ ]` 状态**——状态归 §2 | | critical |
| 1.3 | UC **不带实现细节以外的内容**（不混 IF 职责） | | important |

### 1.1.2 agile 三段式格式

每条 UC 必须有 **作为 / 我希望 / 以便** 三个标签（中文）。

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 2.1 | **作为** 标签存在 | | important |
| 2.2 | **我希望** 标签存在 | | important |
| 2.3 | **以便** 标签存在 | | important |
| 2.4 | "作为" 后跟具体角色 / 场景，不是 "user" 这种空泛词 | | important |
| 2.5 | "我希望" 是动作 + 对象，不是 "to do something" 的机翻 | | important |
| 2.6 | "以便" 是价值 / 动机，不是 "so that I can" 的字面翻译 | | important |

**反模式**：

```
❌ - **UC-01-01** [P1]
   - **As a** developer
   - **I want** to do something
   - **So that** I can achieve something
   → 机翻：所有关键词都是英文，没翻译
   → 标签不规范：作为 / 我希望 / 以便 不写出来

❌ - **UC-01-01** [x] 添加 repo
   → 状态 [x] 错放位置（应在 §2 Milestone）
```

### 1.1.3 实现细节嵌套

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 3.1 | **实现细节** 子标题存在 | | important |
| 3.2 | 实现细节列在 **agile 三段式之后**（不是同级） | | critical |
| 3.3 | 实现细节写**关键技术点**（文件路径 / 函数名 / 配置值） | | important |
| 3.4 | 实现细节不重复 UC 故事（不再讲一遍"作为..."） | | nice-to-have |

**结构示意**：

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
| 4.1 | UC 至少 5 条（更少 = 文档没认真列） | | important |
| 4.2 | UC 业务分组合理（按业务域 / 模块 / 用户场景分） | | nice-to-have |
| 4.3 | UC 优先级 `[P0-P3]` 都标 | | nice-to-have |

---

## 2. §1.2 Inner Feature（系统内在）

### 2.1 编号规则

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 5.1 | IF 编号格式 `IF-mm-nn` | | important |
| 5.2 | IF 同样**不带状态**（状态归 §2） | | critical |

### 2.2 IF 格式

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 6.1 | IF 用 **特性描述 + 实现细节** 拆分 | | important |
| 6.2 | **特性描述** 一句中文说清"这个功能干什么、解决什么问题" | | critical |
| 6.3 | 实现细节同 UC（技术点 + 路径） | | important |

**IF vs UC 的区分**：

| | UC | IF |
|---|---|---|
| 视角 | 用户能做什么 | 系统如何实现 |
| Persona | "作为 X 开发者" | 无 persona |
| 故事 | 作为 / 我希望 / 以便 | 特性描述 |
| 例 | "添加 repo" | "Octokit 抓取元数据" |

---

## 3. §2 Milestone

### 3.1 基本约束

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 7.2 | 每个 Milestone 有 **代号**（Ubuntu-style code name） | | important |
| 7.3 | 每个 Milestone 有 **Versions** 列表（可多个） | | nice-to-have |
| 7.4 | 每个 Milestone 有 **主题一句话描述** | | important |

### 3.2 迭代条目

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 8.1 | 每个 Milestone 拆**初次实现** + **优化 / bug fix** 两节 | | important |
| 8.2 | 同一 UC / IF 可在多个 Milestone 中**多次出现**（初次 + 优化 + fix） | | important |
| 8.3 | 优化 / fix 条目带说明（"upgrade: ..." / "fix: ..."） | | nice-to-have |

**示例**：

```markdown
### M1 — "Seedling" (v0.x → v1.0-rc, 2026-04 → 2026-07) ✅ DONE
   #### 初次实现
   - [x] UC-01-01 粘贴 URL 添加 repo
   - [x] UC-01-02 查看 repo 列表
   ...
   #### 优化与 bug fix（iterations during M1）
   - [x] UC-03-02 — fix: "Saving…" 状态卡死不消失的 bug
   - [x] UC-04-02 — upgrade: readme 输入从 <2KB seed 改为 readme.md 完整内容
```

### 3.3 状态语义

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 9.1 | `[x]` 完成 · `[~]` 进行中 · `[ ]` 待办 · `[!]` 阻塞 定义明确 | | important |
| 9.2 | 没有 `[x]` 但 git log 显示已实现 = 文档与现实脱节 | | critical |
| 9.3 | 没有 `[ ]` 但实现未完成 = 虚报完成 | | critical |

---

## 4. §2.4 Backlog（可选）

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 10.1 | Backlog 用 `[ ]` 标识（**未**排进任何 Milestone） | | important |
| 10.2 | Backlog 条目带优先级 `[P3]`（应是远期 / nice-to-have） | | important |
| 10.3 | Backlog 与"已完成历史"**不重复**——已实现的合并到 Milestone | | important |

---

## 5. 附录：UC/IF ↔ 历史 M*-T* 映射（可选）

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 11.1 | 历史 M*-T* 编号映射到 UC / IF（追溯用） | | nice-to-have |
| 11.2 | 旧 milestone 不在正文中展开（仅在附录列映射） | | important |

---

## Tasks 综合判定

| critical 数 | important 数 | verdict |
|---|---|---|
| 0 | ≤ 3 | **PASS** |
| 0 | ≥ 4 | **FIX** |
| ≥ 1 | 任意 | **REWRITE** |

**最常见的 3 个 Tasks 问题**：

1. **§1 UC 带 `[x]` / `[ ]`**——状态错放位置，应该是 §2 Milestone
2. **Milestone > 3**——堆了十几个 M1-T1 ~ M14-T5，应该压缩成 3 个代号化 Milestone
3. **UC 不是 agile 三段式**——直接写"作为 dev / I want to" 没翻译成中文

---

## 6. 范式对标(gh-curio reference)

> 参考范式:[gh-curio](https://github.com/wkevin/gh-curio) 的 tasks.md 结构。
> 评估时检查 tasks.md 是否对齐这些范式特征(不是 gh-curio 也行,但**必须**采用某一种明确范式)。

| # | 检查项 | 严重度 |
|---|---|---|
| 6.1 | **顶部有"文档范式"声明** — UC / IF / Milestone / P0-P3 优先级 / [x] 状态定义齐全 | important |
| 6.2 | **有"文档导航"表** — §1 / §2 / §3 / §4 章节指向链接 | nice-to-have |
| 6.3 | **UC 编号 `UC-mm-nn`(4 段,业务分组)** — 不是单数字如 `UC-01` | important |
| 6.4 | **IF 编号 `IF-mm-nn`(4 段,工程分组)** — 不是 `IF-XX.YY` 带点格式 | important |
| 6.5 | **每条 UC/IF 标题行带 `[P0]`/`[P1]`/`[P2]`/`[P3]` 优先级标** | important |
| 6.6 | **UC agile 三段式用中文标签**(作为 / 我希望 / 以便)— 不混英文 `As a/I want/So that` | critical |
| 6.7 | **§2 Milestone 标题三字段** — 代号 + 主题 + Versions | important |
| 6.8 | **§2 Milestone 拆"初次实现" + "优化与 bug fix"两节** — checkbox 走状态 | important |
| 6.9 | **Backlog 在 §2.4**(在 Milestone 章节内)— 不在单独 §6 | nice-to-have |
| 6.10 | **Backlog 编号 `UC-NN-NN` 或 `TB.N`** — 不是 `UC-BL-NN` 自创格式 | nice-to-have |

**为什么强制范式**:无范式 = 各项目各写各的,读者跨项目读 5 个 tasks.md 会迷惑。明确范式 = 跨项目可读性。

---

## 7. 跨文档引用一致性(cross-doc)

| # | 检查项 | 命令 / 方法 | 严重度 |
|---|---|---|---|
| 7.1 | **tasks §1.1 UC 编号跟 PRD §4 UC 编号一致**(都用 `UC-mm-nn` 双数字) | `grep '^### UC-' docs/tasks.md` 跟 `docs/prd.md §4` 比对 | critical |
| 7.2 | **tasks §2 Milestone 代号跟 PRD §7 Milestone 代号一致** | 比对 §2 与 PRD §7 | critical |
| 7.3 | **tasks §2.4 Backlog TB 编号跟 PRD §6 范围外 TB 引用一致** | `grep 'TB\.' docs/tasks.md` 跟 `docs/prd.md §6` 比对 | important |
| 7.4 | **tasks §1.2 IF 引用的 ADR 编号在 `docs/add.md` §7 存在** | `grep 'ADR-[0-9]' docs/tasks.md` 验证每个引用 | critical |
| 7.5 | **tasks §3 决策依赖(D-1~D-N)跟 PRD §1.2 / §3 一致** | 比对决策表 | important |
| 7.6 | **tasks agile 三段式跟 PRD §4 用同一种语言** | 人工抽检 2-3 条 | important |
| 7.7 | **tasks §5 Commit Reference Appendix 列出所有 commit hash + `git show` 能验证存在** | 对 N 条 commit 逐一 `git show <hash>` | important |

---

## 8. 状态语义与现实一致性

> tasks 的 [x]/[~]/[ ]/[!] 状态必须跟 git log / 代码现实一致,否则是虚假完成。

| # | 检查项 | 命令 / 方法 | 严重度 |
|---|---|---|---|
| 8.1 | **没有 [x] 但 git log 显示已实现 = 文档失同步** | `git log --since=...` 跟 [x] 比对 | critical |
| 8.2 | **没有 [ ] 但实现未完成 = 虚报完成** | 跑代码验证 | critical |
| 8.3 | **commit hash 必须 7 位短 hash 或完整 hash,跟 `git log` 完全一致** | `git log --oneline \| grep <hash>` | important |
| 8.4 | **squash commit(如 `4ef9c68`)必须明确标注 "(squash)" 或 "(内含 R-rename-1, R-merge-1 等 N commits)"** — 否则读者查不到 | 人工抽检 | important |

---

## 加载指引

本文件仅在评估 tasks.md 时加载。如果用户问"评估 add.md"——不要读此文件，跳到 [add-checklist.md](add-checklist.md)。

本 skill 触发名：`/vital-docs`。