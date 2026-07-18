---
name: wk-task-dev
description: 批量实现 docs/tasks.md 段文父 bullet `[ ]` + 段文 **优化升级** 列表 `- [ ]` 项(同 commit 翻父 bullet inline `[~]`/`[!]` 状态)(按单 task id UC-XX-YY / IF-XX-YY 入口;`v0.X` 入口已废弃)。**Step 0 强制预检**:先扫待实现清单 + 用户确认 + 选定 commit 模式(per-commit 确认 / 无需确认 / dry-run)后才进 Step 1。读 tasks.md 取 UC/IF 完整定义 + 段文 **优化升级** 段 + prd.md 取场景/价值 + add.md 取架构/决策 → 实现后**仅更新 tasks.md 自身**(`- [ ]` 优化升级 → `- [x]`,同 commit 翻父 bullet `[ ]/[~]/[!]/[x]` 4 形态状态)。dev agent 自主决定实现路径,只对照 DOD 验收 + 段文 **优化升级** 项;prd/add 只读。tasks.md UC/IF 段文只含**方案参考(prd/add 章节号指针)+ 实现建议(可选,简短)+ DOD(可选)+ 优化升级(可选,本段积压的待开发点)**,**不写实现细节**;dev agent 自主决定实现路径,只对照 DOD 验收 + 优化升级;prd/add 只读。状态机整体内聚到 tasks.md。触发词:"/task-dev"、"实现 UC-XX-YY"、"批量开发"。适用于长时间、无人值守的批量 task 开发。Step 0 的预检 + 确认 + commit 模式选择是该 skill 的安全护栏,不在用户未确认前动手。
---

## 用法

**允许：**

```
/wk-task-dev UC-03-02         # 实现单 task
/wk-task-dev IF-04-01         # 实现单 task
# /wk-task-dev v0.X 已禁用(tasks.md 无 Version 段;用 UC-XX-YY / IF-XX-NN 单 task 入口)
/wk-task-dev status           # 仅打印当前进度(不开发)
```

**禁止：**

```
/wk-task-dev all              # 所有 [ ] -- 危险、禁止
/wk-task-dev Sprint-N         # sprint 概念已废弃
```

> 注:旧 `version` 入口已删除。Version 不在 tasks.md 自包含;以单 task id 入口为准。

## 工作流程

### 0. 预检:列出待实现清单 + 确认 + commit 模式选择(强制)

进入开发前,**必须**先扫描 `docs/tasks.md` 列出所有待实现条目,经用户确认 + 选定 commit 模式后才进入 Step 1:

**Step 0a — 扫待实现清单**(扫描 `docs/tasks.md`):
- **(a) 段文父 bullet `[ ]` 状态**:匹配 `^- \[ \] \*\*UC-XX-YY\*\*` / `^- \[ \] \*\*IF-XX-NN\*\*`(UC-XX-YY / IF-XX-NN 共 4 形态中的 `[ ]` 父 bullet,即 User Case / Inner Feature 段未开始任务)
- **(b) 段文 **优化升级** 段 `- [ ]` 项**:每个段文末尾 `**优化升级**(可选):` 子节里的 `- [ ]` checkbox(本段积压的待开发点)
- 输出格式(必须按此格式给用户):
  ```
  待实现清单(扫 docs/tasks.md):
  [段文父 bullet — N 项]
  - UC-XX-YY 状态 [ ] / 标题(取第一句作为我希望)
  - IF-XX-NN 状态 [ ] / 标题
  
  [优化升级 — M 项]
  - 段 UC/IF-XX-YY > 优化升级#1: 简注
  - 段 IF-XX-NN > 优化升级#1: 简注
  
  共 N + M 项待实现。
  ```
- 扫不到任何条目 → 输出 `NO_PENDING: tasks.md 中无 [ ] 父 bullet 也无 优化升级 - [ ] 项`,停下
- 任务 ID 列表(如 `$2` 给了 UC-XX-YY):只输出该 ID 对应的清单(段文父 bullet [ ] + 该段 优化升级 - [ ] 项);不扫全局

**Step 0b — 用户确认**(`AskUserQuestion`):
- 提示:"上面是本次待实现清单, 是否全部实现?"
- 选项:
  - "全部实现" — 进入 Step 1 全跑
  - "部分实现(指定)" — 用户给子集(回 `UC-XX-YY IF-XX-NN ...` 或段名)
  - "取消" — 输出 `ABORTED`,停下
- 用户给"部分实现"时:把子集作为新的待实现清单,不需要重新扫

**Step 0c — commit 模式选择**(`AskUserQuestion`,**只问一次**,本 session 后续 task 沿用):
- 选项:
  - **per-commit 确认**(推荐) — 每 task / 每 优化升级完成后,**暂停**等待用户回复 "ok / 改 X / 取消" 再继续;不阻塞但每个 commit 都 human-in-the-loop
  - **无需确认** — 自动连跑 N 项,仅在 Step 3 进度汇报里给汇总;全程 0 中断
  - **只读 dry-run**(用于查看未来要做的清单) — 不实现,只输出清单 + 退出
- 用户在后续若改主意:用 `/task-dev <id> --mode=confirm` 或 `--mode=auto` 临时覆盖本次单条
- 模式选择后**进入 Step 1**

```
注:本步骤(Step 0)是 gate,跳过会直接进入实现;但**没有用户确认不得 commit**(即使选 无需确认 模式,Step 0 的清单展示 + commit 模式问询也必走)。
```

### 1. 解析 + 过滤

- 解析 `$2` 为 task id 列表(已被 Step 0 锁定)
- 若是 task id(UC-XX-YY / IF-XX-NN):读该 task 的 User Case / Inner Feature 段文 + **优化升级** 列表(`- [ ]`),**只看 `[ ]`**(已 `[x]` 视为历史已实现,跳过)
- 若是 `/status`:仅打印当前进度(不开发);聚合 `[ ]/[x]/[~]/[!]` 状态分布 + 优化升级 数量
- 若是其他字符串(包括 `v0.X` 旧入口):输出 `TASK_NOT_FOUND: <arg>`,停下
- 已 `[!]` 标记的任务 → 列入"需重提决策"清单(在 progress snapshot 里也带上)
- M > 10 → 提示用户 "批量 N 个,按顺序还是指定子集?",等回复

### 2. 实现 + 提交

**默认顺序**:

1. `[!]` 阻塞优先(先解锁)
2. `[~]` in-progress(避免上下文丢失)
3. `[P0] > [P1] > [P2] > [P3]`
4. 同优先级内,IF 优先于 UC(基础设施先行)
5. 段内按 `docs/tasks.md` 文档顺序
6. 发现 UC 依赖未实现的 IF → 临时插入该 IF(破坏顺序是 OK 的)

**对每个 task**:

1. 读相关上下文(`docs/tasks.md User Case / Inner Feature` 取 UC/IF 完整定义,`docs/prd.md` 取场景/价值,`docs/add.md` 取架构/决策)
2. 实现
3. **跑 verification**(通过标准见下,**三条全过才算 verification OK**):
   - **(a) 新增测试通过**:本 task 新加的测试(如有)必须跑过;无新测试的纯 refactor / docs task 跳过此项
   - **(b) 既有测试不 regress**:相关测试套件全绿;如有 baseline 失败需 cite baseline commit
   - **(c) 类型 / lint 通过**:与本 task 改动的文件相关的类型检查 + lint 通过;无关报错 cite baseline
4. 改 `docs/tasks.md`(同 commit):
   - **优化升级** 段 `- [ ]` → `- [x]`
   - 特殊情况:`[ ] → [!]`(需决策)/ `[ ] → [~]`(中断);父 bullet inline 状态同 commit 翻
5. **`git add <本 task 改的代码文件> docs/tasks.md` + `git commit`**(带 `Co-Authored-By: Claude <noreply@anthropic.com>`)

> **tasks.md `[x]/[!]` 翻牌必须在同一个 commit 里**(per-task commit)。
>
> 一个 `[ ]` task = 一个 `[x]` flip = 一个 commit。理由:
>
> - `git blame docs/tasks.md` 应该精确到每个 task 何时收尾
> - `git log --grep='<UC-XX-YY>'` 与 tasks.md 状态天然对齐,**无需对照** commit body 与文档状态
> - 中途中断(切换到其他任务)时,已完成 task 的 [x] 不会再被误批量 rollback
>   **prd.md / add.md 在本 skill 中只读** —— 只动 `tasks.md` **优化升级** 段 `[-]` ↔ `[x]` + 父 bullet 状态 4 形态翻牌,不动 UC/IF 定义(Version 概念已废弃)。

**Baseline 处理**:

- 已存在的失败测试(基线问题)不算本 task 引入 → commit body 里 cite baseline commit 即可
- 类型 / lint 报红但与本 task 无关 → 同上 cite baseline
- **新增的失败** 必须先修,commit 时明确说明根因

### 3. 进度汇报

每完成 **3 个 task**(或每完成一个 `[P3]`)输出一次 snapshot:

```
✓ 已完成 N/M:<task 列表>
⏭️ 已跳过 K:[!] 任务列表(需重提决策)
⏳ 剩余:<task 列表>
```

batch 全部完成后给最终 summary:commit 列表 + 跳过的 `[!]` + 剩余 `[ ]`

## 边界协议

### Commit 节奏(由 Step 0c 选择)

本 skill 启动时 Step 0c 让用户选 commit 模式,本 session 后续沿用:

- **`per-commit 确认`**:每个 task / 每 优化升级项完成后,`git commit` 写入前**暂停**等待用户回复 "ok / 改 X / 取消" 再继续(推荐模式,每个 commit 都有 human-in-the-loop)
- **`无需确认`**:自动连跑全清单,每完成 N 项打印 Step 3 进度汇报,**全程 0 中断**(适合大批量 polish / 凌晨跑)
- **临时覆盖**:用户后续可用 `/task-dev <id> --mode=confirm|auto` 单条覆盖本 session 默认

若全局 `git-requires-confirmation` memory 设了强约束("严格等待用户确认才 commit"),**以全局 memory 为准**,任何模式都被强制 confirm。本 skill 不绕开用户硬护栏。

### 需要决策的任务([P3] escape hatch)

不是所有 task 都能"无人干预"完成。判断标准:

- 库选型(Tiptap vs Lexical)
- 跨多个 schema / 多个文件类型的架构决策
- 用户偏好相关(默认主题色 / 默认 taxonomy)

→ **暂停 batch**:

1. 输出:决策问题 + 候选方案(每项优缺点)+ 推荐项
2. 用 `AskUserQuestion` 收集回复
3. 用户回复后继续

不要"猜测最佳默认"继续推进——`[P3]` 选错了重做成本高。用户决策 OK 之后再做不算违反"批量无人干预"。

### 中断与降级

用户中途切换到其他任务(如修 build error):

- 当前 task → `[~]`,附一行 reason(中断 / 等用户)
- 已完成 task 的 `- [x]` 不回滚
- 下次启动该 batch 时自动 surface `[!]` / `[~]`(参见"1. 解析 + 过滤")
- batch 结束后给"已完成 + 跳过 + 剩余"清单

### Backlog 不接(历史 §2 不接的迁移)

`docs/tasks.md Backlog` 桶 1 / 桶 2 raw 行**本 skill 不接** —— 必须先由 `wk-idea-flesh` 升级到 User Case / Inner Feature(完整 UC/IF 三段式定义 + **优化升级** 段 `[ ]`)才能接。任务提交流程:`Backlog 桶 1/2 raw → flesh → User Case / Inner Feature 段文(+ **优化升级** [ ]) → task-dev` 三步链。Backlog 桶 3(`已方案设计/有 Task ID`)也不接,直接由对应 User Case / Inner Feature 段文读,不通过 Backlog 间接找。

## git 提交规范

`<type>(<scope>): <subject>` 格式(来自 CONTRIBUTING.md §5):

| Type       | 何时用                                                 |
| ---------- | ------------------------------------------------------ |
| `feat`     | 新功能 / 新 UC / 新 IF                                 |
| `fix`      | 修 bug(对应 User Case / Inner Feature UC 段文"方案参考 / 实现建议 / DOD"提到的问题) |
| `refactor` | 重构(无新功能无 bug 修复)                              |
| `docs`     | 纯文档变更                                             |
| `test`     | 加 / 改测试                                            |
| `chore`    | 配置 / 依赖 / 杂事                                     |

**scope 强制**用 `UC-XX-YY` 或 `IF-XX-YY`(**不写** `v0.X` / `Sprint-N` / 老的 `M*-T*`;Version / Sprint 概念不进 commit scope,历史的 sprint-shape 塑形链路已合并到本 skill)。Claude 生成的 commit **必须**带 `-m "Co-Authored-By: Claude <noreply@anthropic.com>"`。

**不做**的事(commit 之外):不 push / 不 squash / 不 rebase / 不 amend 既有 commit / 不交互式 `git rebase -i`。

## 关联

- **上游**:
  - `wk-idea-flesh` — 写 `tasks.md Backlog` raw / `User Case / Inner Feature 段` UC/IF 定义 + **优化升级** 段;**前提**:本 skill 接的 `[ ]` 优化升级必须已在 User Case / Inner Feature 段文(Backlog raw 行不接,需 flesh 升级后才接)
  - `wk-task-dev`(本 skill)→ 把 User Case / Inner Feature 段 **优化升级** `[ ]` 翻成 `[x]`(同 commit,父 bullet inline `[~]`/`[!]` 状态也可翻)
- **下游**:无;本 skill 是塑形链终点
