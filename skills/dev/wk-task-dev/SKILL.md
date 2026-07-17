---
name: wk-task-dev
description: 批量实现 docs/sprint.md §1 Sprint 段中指定 Version（v0.X）或单 task id（UC-XX-YY / IF-XX-YY）的所有 [ ] 项。读 sprint.md 取进度 → 读 tasks.md §1.1/§1.2 + prd.md + add.md 取 UC/IF 上下文 → 实现后**仅更新 sprint.md 勾 [x]**，prd/add/tasks 只读。触发词："/task-dev"、"实现 v0.X"、"实现 UC-XX-YY"、"批量开发"。适用于长时间、无人值守的批量 task 开发。
---

## 用法

**允许：**

```
/wk-task-dev UC-03-02         # 实现单 task
/wk-task-dev IF-04-01         # 实现单 task
/wk-task-dev v0.5             # 实现指定 version(Sprint 覆盖的 Version)的所有 [ ]
/wk-task-dev status           # 仅打印当前进度（不开发）
```

**禁止：**

```
/wk-task-dev Sprint-2         # 指定 Sprint id -- 危险、禁止
/wk-task-dev all              # 所有 [ ] -- 危险、禁止
```

`version` 必须精确匹配 `sprint.md §1` 中某个 Sprint 段标注的 Version 字符串（如 `v0.5`），否则输出 `VERSION_NOT_FOUND: <arg>` 并停止。

## 工作流程

### 1. 解析 + 过滤

- 解析 `$2` 为 task id 列表或 version
- 若是 version：扫描 `sprint.md §1` 该 Version 覆盖的所有 Sprint 段，**只看 `[ ]`**（已 `[x]` 视为历史已实现，跳过）
- 输出 `[version] 共 N 个 task，其中 [ ] = M 个待实现`
  - M = 0 → 输出 `VERSION_COMPLETE: <version>`，停下
  - M > 10 → 提示用户 "批量 N 个，按顺序还是指定子集？"，等回复
- 已 `[!]` 标记的任务 → 列入"需重提决策"清单（在 progress snapshot 里也带上）

### 2. 实现 + 提交

**默认顺序**：

1. BugFix 段（性能 / 正确性 bug，影响后续稳定性）
2. IF 段（基础设施；UC 通常依赖这些）
3. UC 段（用户可见功能）
4. 段内按 `sprint.md` 文档顺序
5. 发现 UC 依赖未实现的 IF → 临时插入该 IF（破坏顺序是 OK 的）

**对每个 task**：

1. 读相关上下文(`docs/tasks.md §1.1/§1.2` 取 UC/IF 完整定义,`docs/prd.md` 取场景/价值,`docs/add.md` 取架构/决策)
2. 实现
3. **跑 verification**（见下）
4. 改 `sprint.md`：`[ ] → [x]`（成功）或 `[ ] → [!]`（见"### 需要决策的任务"）
5. **`git add <本 task 改的代码文件> docs/sprint.md` + `git commit`**（带 `Co-Authored-By: Claude <noreply@anthropic.com>`）

> **sprint.md `[x]/[!]` 翻牌必须在同一个 commit 里**(per-task commit)。
>
> 一个 `[ ]` task = 一个 `[x]` flip = 一个 commit。理由:
>
> - `git blame docs/sprint.md` 应该精确到每个 task 何时收尾
> - `git log --grep='<UC-XX-YY>'` 与 sprint.md 状态天然对齐,**无需对照** commit body 与文档状态
> - 中途中断(切换到其他任务)时,已完成 task 的 `[x]` 不会再被误批量 rollback
> **prd.md / add.md / tasks.md 在本 skill 中只读** —— 只动 `sprint.md` 勾 [x] 状态,不动 UC/IF 定义或 Sprint 计划。

**Baseline 处理**：

- 已存在的失败测试（基线问题）不算本 task 引入 → commit body 里 cite baseline commit 即可
- 类型 / lint 报红但与本 task 无关 → 同上 cite baseline
- **新增的失败** 必须先修，commit 时明确说明根因

### 3. 进度汇报

- 每完成 **3 个 task**（或每完成一个 `[P3]`）输出一次 snapshot：

  ```
  ✓ 已完成 N/M：<task 列表>
  ⏭️ 已跳过 K：[!] 任务列表（需重提决策）
  ⏳ 剩余：<task 列表>
  ```

- batch 全部完成后给最终 summary：commit 列表 + 跳过的 `[!]` + 剩余 `[ ]`

## 边界协议

### Commit 节奏与全局 memory 互斥

本 skill workflow 自身定义批量 commit 节奏 —— 每个 task 完成一次 `git commit`,**正常情况下不需要逐条询问用户确认 'commit'**。

若全局 `git-requires-confirmation` memory 设了强约束（"严格等待用户确认才 commit"）,**以全局 memory 为准**,本 skill 的批量节奏失效,逐 task 停下来等用户确认。这是用户层面的硬护栏,本 skill 不绕开。

### 需要决策的任务（[P3] escape hatch）

不是所有 task 都能"无人干预"完成。判断标准：

- 库选型（Tiptap vs Lexical）
- 跨多个 schema / 多个文件类型的架构决策
- 用户偏好相关（默认主题色 / 默认 taxonomy）

→ **暂停 batch**：

1. 输出：决策问题 + 候选方案（每项优缺点）+ 推荐项
2. 用 `AskUserQuestion` 收集回复
3. 用户回复后继续

不要"猜测最佳默认"继续推进——`[P3]` 选错了重做成本高。用户决策 OK 之后再做不算违反"批量无人干预"。

### 中断与降级

用户中途切换到其他任务（如修 build error）：

- 当前 task → `[!]`，附一行 reason
- 已完成 task 的 `[x]` 不回滚
- 下次启动该 batch 时自动 surface `[!]`（参见"1. 解析 + 过滤"）
- batch 结束后给"已完成 + 跳过 + 剩余"清单

## git 提交规范

`<type>(<scope>): <subject>` 格式（来自 CONTRIBUTING.md §5）：

| Type       | 何时用                                      |
| ---------- | ------------------------------------------- |
| `feat`     | 新功能 / 新 UC / 新 IF                      |
| `fix`      | 修 bug（通常对应 `sprint.md §1` Sprint 内 "优化与 bug fix" 子节） |
| `refactor` | 重构（无新功能无 bug 修复）                 |
| `docs`     | 纯文档变更                                  |
| `test`     | 加 / 改测试                                 |
| `chore`    | 配置 / 依赖 / 杂事                          |

**scope 强制**用 `UC-XX-YY` 或 `IF-XX-YY`（**不写** `M*-T*` / `Sprint-N` / `v0.X`；Sprint-number / version 不出现在 commit scope）。Claude 生成的 commit **必须**带 `-m "Co-Authored-By: Claude <noreply@anthropic.com>"`。

**不做**的事（commit 之外）：不 push / 不 squash / 不 rebase / 不 amend 既有 commit / 不交互式 `git rebase -i`。

## 关联

- **上游**:
  - `wk-sprint-shape` — 把 backlog 塑形到 `sprint.md §1 Sprint` 段,本 skill 按 `[ ]` 顺序实现;**前提**:本 skill 看到的 [ ] 项必须先被 sprint-shape 塑形到 §1（§2 Backlog 项本 skill 不接）
  - `wk-idea-flesh` — 间接上游;idea-flesh 写 `tasks.md §1.1/§1.2` UC/IF 定义,本 skill 读这些定义
- **下游**:无;本 skill 是塑形链终点
- **同族塑形链**:
  - `wk-idea-flesh` → 把模糊想法 flesh out 到 PRD/ADD/Tasks + Backlog
  - `wk-sprint-shape` → 从 Backlog 挑 10-20 task 塑形到 §1 Sprint 段（代号 / Goal / Version）
  - `wk-task-dev`（本 skill）→ 把 §1 Sprint 段内 [ ] 实际开发成 [x]
