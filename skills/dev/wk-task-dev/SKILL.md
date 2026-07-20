---
name: wk-task-dev
description: 批量实现 docs/tasks.md 段文父 bullet `[ ]` + 段文 **优化升级** 列表 `- [ ]` 项(同 commit 翻父 bullet inline `[~]`/`[!]` 状态)(按单 task id UC-XX-YY / IF-XX-YY 入口;`v0.X` 入口已废弃)。**Step 0 强制预检**:先扫待实现清单 + 用户确认 + 选定 commit 模式(per-commit 确认 / 无需确认 / dry-run)后才进 Step 1。读 tasks.md 取 UC/IF 完整定义 + 段文 **优化升级** 段 + prd.md 取场景/价值 + add.md 取架构/决策 → 实现后**仅更新 tasks.md 自身**(`- [ ]` 优化升级 → `- [x]`,同 commit 翻父 bullet `[ ]/[~]/[!]/[x]` 4 形态状态)。dev agent 自主决定实现路径,只对照 DOD 验收 + 段文 **优化升级** 项;prd/add 只读。tasks.md UC/IF 段文只含 4 子段:**方案参考(必选,prd/add 章节号指针)+ DOD(必选,可验收标准)+ 实现建议(可选,1-2 句方向)+ 优化升级(可选,仅描述目标/要求/DOD,不约束 dev 怎么实现)**;**不写 `**子任务**` 子段**;**不写 `**实现细节**` 段**;dev agent 自主决定实现路径,只对照 DOD 验收 + 优化升级;prd/add 只读。段文是 task-dev 输入约束,不是 task-dev 内部细节规约;**段文父 bullet(task 编号行)只含 `[state] **ID** [P?]`** — 绝不写任何描述 / 副标题 / 斜体补充(简注/状态附加归 4 子段)。状态机整体内聚到 tasks.md。触发词:"/task-dev"、"实现 UC-XX-YY"、"批量开发"。适用于长时间、无人值守的批量 task 开发。Step 0 的预检 + 确认 + commit 模式选择是该 skill 的安全护栏,不在用户未确认前动手。
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

**Step 0a — 扫待实现清单**(执行 `python3 scan-pending.py`(本 skill 同目录),~20ms 完成):
- **(a) 段文父 bullet `[ ]` 状态**:匹配 `^- \[ \] \*\*UC-XX-YY\*\*` / `^- \[ \] \*\*IF-XX-NN\*\*`(UC-XX-YY / IF-XX-NN 共 4 形态中的 `[ ]` 父 bullet,即 User Case / Inner Feature 段未开始任务)。简述优先取 `/` 后短语,无则回退到「**我希望**」首句 30 字
- **(b) 段文 **优化升级** 段 `- [ ]` 项**:每个段文末尾 `**优化升级**(可选):` 子节里的 `- [ ]` checkbox(本段积压的待开发点)
- **(c) 段文 **关联 IF** / **关联 UC** 字段 → 分组**(Step 2 默认顺序依赖此分组,见下方「分组规则」)
- 输出格式(必须按此格式给用户):
  ```
  待实现清单(扫 docs/tasks.md):
  [段文父 bullet — N 项]
  - UC-XX-YY 状态 [ ] / 标题(取第一句作为我希望)
  - IF-XX-NN 状态 [ ] / 标题

  [优化升级 — M 项]
  - 段 UC/IF-XX-YY > 优化升级#1: 简注
  - 段 IF-XX-NN > 优化升级#1: 简注

  [关联组 — K 组 / M 项](含跨段引用的 IF/UC)
  - 组 1(L 项:IF a + UC b):
    - IF-XX-NN [P?]: 标题
    - UC-YY-MM [P?]: 标题
    - 关联证据:IF-XX-NN↔UC-YY-MM; UC-YY-MM↔IF-XX-NN

  [独立组 — T 项](无任何 [ ] 引用 / 引用已 [x] 的段)
  - IF-AA-BB [P?]: 标题
  - UC-CC-DD [P?]: 标题

  [建议执行顺序](按 [!]>[~]>关联组>独立组 排列;组内 IF 优先 UC,P 优先 + 文档顺序):
   1. [!] 阻塞 ...(若有)
   2. [~] in-progress ...(若有)
   3. 关联组 1: IF-X → IF-Y → UC-Z
   4. 关联组 2: IF-A → UC-B
   5. 独立组: IF-C → UC-D

  共 N + M 项待实现。
  ```
- **分组规则**(脚本内部 union-find 实现):
  - 解析每个 [ ] 段的 `**关联 IF**` / `**关联 UC**` 字段,抽取所有 `IF-XX-NN` / `UC-XX-NN`(正则匹配,过滤掉 `(无)` / `(无新 IF;...)` 等文字段,过滤掉 ID 后的注释后缀如 `IF-08-01(回收站列表)`)
  - **只 union 当前段与 [ ] 状态的引用**(已 [x] 的引用不算依赖 —— 因为已经实现,目标段可独立做)
  - **关联组**:union-find 后 size ≥ 2 的组(至少 2 个段互相引用或链式可达)
  - **独立组**:size = 1 的段(无任何 [ ] 引用 / 无关联字段 / 全部引用都已 [x])
  - WHY 关联组单独列出:实现时若先做 UC 再做 IF,容易出现「UC 写到一半发现 IF 没底座 → 临时插入 IF → 中断上下文」;**先 IF 后 UC 让 dev agent 可一气呵成完成链路**。独立组没跨段依赖,IF 仍是基础设施先行,沿用旧规约。
- 扫不到任何条目 → 输出 `NO_PENDING: tasks.md 中无 [ ] 父 bullet 也无 优化升级 - [ ] 项`,停下
- 任务 ID 列表(如 `$2` 给了 UC-XX-YY):脚本用 `python3 scan-pending.py UC-XX-YY` 单段模式,只输出该 ID 对应的清单(段文父 bullet [ ] + 该段 优化升级 - [ ] 项);不扫全局
- **优化升级 段内容约束**(只描述目标 / 要求 / DOD):写法 `- [ ] <目标>;<DOD>;不约束 dev 选 <实现路径> 任一`,**不允许** `- [ ] 修改 lib/xxx.ts 改用 React Hook` / `- [ ] 加 max-h-` 这种技术细节(违反原则)

> 性能备注:`scan-pending.py` 单次扫 ~20ms(0.02s 范围内,文件 ~70KB)。不要内联 re.findall 在 skill 描述里 — 调脚本即可。

**Step 0b — 用户确认**(**必须先把 Step 0a 输出逐项** as 文本段**写在消息中**给用户,让用户清楚看到清单 + 建议顺序 + 简要解释,然后才 `AskUserQuestion`):
- 文本输出格式(必须按此 markdown code block 格式):
  ```
  === Step 0a 输出 ===
  共 N + M 项待实现([段文父 bullet N 项 / 优化升级 M 项]):

  [段文父 bullet — N 项]
   1. UC-XX-YY 状态 [ ] / 简述
   2. IF-XX-NN 状态 [ ] / 简述

  [优化升级 — M 项]
   1. 段 UC/IF-XX-YY > 优化升级#1: 简注
   2. 段 IF-XX-NN > 优化升级#1: 简注

  [关联组 — K 组 / M 项](段文 **关联 IF** / **关联 UC** 字段解析出的跨段引用)
   - 组 1(L 项:IF a + UC b):
     - IF-XX-NN [P?]: 简述
     - UC-YY-MM [P?]: 简述
     - 关联证据:IF-XX-NN↔UC-YY-MM; UC-YY-MM↔IF-XX-NN

  [独立组 — T 项](无任何 [ ] 引用 / 引用已 [x] 的段)
   - IF-AA-BB [P?]: 简述
   - UC-CC-DD [P?]: 简述

  建议执行顺序(按 [!]>[~]>关联组>独立组 排列;组内 IF 优先 UC;同类型按 [P0>P1>P2>P3] + 文档顺序):
   1. [!] 阻塞 ...(若有)
   2. [~] in-progress ...(若有)
   3. 关联组 1(IF→UC): IF-X → IF-Y → UC-Z
   4. 关联组 2(IF→UC): IF-A → UC-B
   5. 独立组(IF 优先 → UC 后): IF-C → UC-D

  解释:关联组内的 IF/UC 是同一特性的两端(IF 是底座 / 内部能力,UC 是用户可见入口),先把底座做掉再做入口,避免 UC 写一半发现 IF 没兜底而中断上下文;独立组无跨段依赖,IF 仍是基础设施先行,沿用旧规约。

  ```
- 文本段输出后**才** `AskUserQuestion`:
  - 提示:"上面是本次待实现清单(共 N+M 项),关联组 K 组 / 独立组 T 项 / 优化升级 M 项,是否按建议顺序全部实现?若想调整顺序可指定子集"
  - 选项:
    - "全部实现(按建议顺序)" — 进入 Step 1 全跑,严格按 [!]>[~]>关联组>独立组 走,组内 IF→UC
    - "部分实现(指定)" — 用户给子集(回 `UC-XX-YY IF-XX-NN ...` 或段名),保持建议的子集内顺序
    - "取消" — 输出 `ABORTED`,停下
- 用户给"部分实现"时:把子集作为新的待实现清单,**保持建议的子集内顺序**(用户挑的子集按原建议顺序排列),不需要重新扫
- **关键**:AskUserQuestion 选项"全部实现"前必须展示清单 + 建议顺序 + 简要解释;不能只 ask "yes/no" 而不显示清单

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

**默认顺序**(由 `scan-pending.py` 在 Step 0a 已产出,Step 2 严格按此执行):

1. `[!]` 阻塞优先(先解锁)
2. `[~]` in-progress(避免上下文丢失)
3. **关联组**(段文 **关联 IF** / **关联 UC** 字段 union-find 出组,size ≥ 2):
   - 组内 **IF 优先于 UC**(先做底座 / 内部能力,再做用户可见入口 —— 避免 UC 写一半发现 IF 没兜底而中断上下文)
   - 同类型内按 `[P0] > [P1] > [P2] > [P3]` 排
   - 同优先级按 `docs/tasks.md` 文档顺序
4. **独立组**(size = 1,无任何 [ ] 引用 / 引用已 [x]):
   - 先 IF 后 UC(基础设施先行,沿用旧规约)
   - 同类型内按 `[P0] > [P1] > [P2] > [P3]` 排
   - 同优先级按 `docs/tasks.md` 文档顺序
5. 关联组之间 / 独立组之间:按组内首段(最小 line_no)的 P + 文档顺序
6. 发现 UC 实际实现时依赖未实现的 IF(没在关联字段里)→ 临时插入该 IF(破坏顺序是 OK 的)

**对每个 task**:

1. 读相关上下文(`docs/tasks.md User Case / Inner Feature` 取 UC/IF 完整定义,`docs/prd.md` 取场景/价值,`docs/add.md` 取架构/决策)
2. 实现
3. **跑 verification**(通过标准见下,**三条全过才算 verification OK**):
   - **(a) 新增测试通过**:本 task 新加的测试(如有)必须跑过;无新测试的纯 refactor / docs task 跳过此项
   - **(b) 既有测试不 regress**:相关测试套件全绿;如有 baseline 失败需 cite baseline commit
   - **(c) 类型 / lint 通过**:与本 task 改动的文件相关的类型检查 + lint 通过;无关报错 cite baseline
4. 段文结构(必含 4 子段):**方案参考**(必选,prd/add 章节号指针)+ **DOD**(必选,可验收标准)+ **实现建议**(可选,1-2 句方向)+ **优化升级**(可选,目标/DOD 形式);改 `docs/tasks.md`(同 commit):
   - **优化升级** 段 `- [ ]` → `- [x]`(只翻 优化升级 段 checkbox;**不动 方案参考 / 实现建议 / DOD 子段**)
   - 特殊情况:父 bullet `[ ] → [!]`(需决策)/ `[ ] → [~]`(中断);inline 状态同 commit 翻
5. **`git add <本 task 改的代码文件> docs/tasks.md` + `git commit`**(带 `Co-Authored-By: Claude <noreply@anthropic.com>`)

> **tasks.md `[x]/[!]` 翻牌必须在同一个 commit 里**(per-task commit)。
>
> 一个 `[ ]` task = 一个 `[x]` flip = 一个 commit。理由:
>
> - `git blame docs/tasks.md` 应该精确到每个 task 何时收尾
> - `git log --grep='<UC-XX-YY>'` 与 tasks.md 状态天然对齐,**无需对照** commit body 与文档状态
> - 中途中断(切换到其他任务)时,已完成 task 的 [x] 不会再被误批量 rollback
>   **prd.md / add.md 在本 skill 中只读** —— 只动 `tasks.md` **优化升级** 段 `[-]` ↔ `[x]` + 父 bullet 状态 4 形态翻牌,不动 UC/IF 定义(Version 概念已废弃)。
>   **段文不写 子任务 / 不写 实现细节** — 段文是 dev 输入约束(描述"做什么 / 怎么算成功"),不约束 dev 怎么实现。dev agent 自主决定实现路径 + 内部子段拆解,只对照 DOD 验收。

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
