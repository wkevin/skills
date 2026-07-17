---
name: wk-idea-flesh
description: 把新想法通过 3 维度头脑风暴(需求 / 方案 / 任务)落到文档系统,**3 个文档**(prd/add/tasks)**每个独立按需修改,没有"必动"**。每个文档有自己的触发原则:prd.md 看产品定位/需求变更,add.md 看架构/方案/决策变更,tasks.md User Case / Inner Feature / Backlog 看 UC/IF 定义(新/升级/删除)+ 状态(父 bullet `[ ]/[x]/[~]/[!]` 4 形态前置 markdown checkbox + 子任务列表 `- [ ]` / `- [x]`)+ Backlog(3 桶「未方案设计/无 Task ID」「已方案设计/无 Task ID」「已方案设计/有 Task ID」按设计成熟度)。状态机整体内聚到 tasks.md 自包含;Backlog 是新的"待办池";wk-sprint-shape 已删除(并入 wk-task-dev)。支持「迭代升级」:如果新想法是修改已有 UC/IF 的 behavior,直接改 User Case / Inner Feature 既有条目而不是另开新 ID。**核心因果**:idea 落地后 prd/add/tasks 任一处增加新待办工作(新 UC/IF / 已有 IF 段文扩展 / 已有 UC 行为升级),都必须在 tasks.md Backlog 同步留一条 raw 行(或 User Case / Inner Feature 段文内对应 polish 子任务) — Backlog 是"待办池"角色,任何地方出现新工作必须回流到 Backlog,否则后续 task-dev 会漏。所有产物严格对齐 wk-doc-align 评估基线。触发词:"/idea-flesh"、用户说"加需求 / 加个 task / 加个 UC / 加个 IF / 加个决策 / 已有 IF 加新步骤 / btw, ..."、或任何模糊想法描述。
---

# /idea-flesh — 3 维度头脑风暴驱动的想法落地

把当前轮用户描述的想法,通过 **3 维度头脑风暴** 落到文档系统。**3 个文档每个独立按需修改,没有"必动"**:

| 文档                                                            | 改它的触发原则                                          |
| --------------------------------------------------------------- | --------------------------------------------------- |
| `docs/prd.md`                                                   | 想法动了**产品定位 / 需求 / 场景 / 用户 / 范围**            |
| `docs/add.md`                                                   | 想法动了**技术方案 / 架构 / 组件 / 接口 / 决策(§7 ADR)**    |
| `docs/tasks.md` (`User Case` / `Inner Feature` / `Backlog`)    | 想法动了**UC/IF 定义**(新增 / 升级 / 删除 / 详设微调)或**状态/Backlog** |

每一类的判断独立,任一文档都可能"不动":

- "我们调整下产品定位"-改 PRD,**不动其他二**
- "用 GraphQL 替代 REST"-改 ADD §7 + tasks.md (理由:改了实现方式,现存 UC 备注变),不动 PRD
- "对 UC-04-02 re-suggest 行为升级"-改 tasks.md User Case,**不动其他二**
- "Backlog 里有 task 想优先做"-改 tasks.md Backlog → User Case / Inner Feature 段文,不属 flesh(属于 wk-task-dev 入口),不改 PRD / 不改 add

**核心口径**:**没有"必动"**。flesh 的产物 = 这 3 个文档各自的 "改 / 不动" 判断结果。

新产生的 UC/IF 进入 `tasks.md User Case / Inner Feature`(完整定义 + 子任务列表 `[ ]`)+ 从 `tasks.md Backlog` 移除对应 raw 行(flesh 闭环)——但**仅当**这条想法真的产出了新的 UC/IF ID。如果想法是纯 polish 或 PRD/ADD 改动,这两条规则不适用。状态机整体留 tasks.md 自包含。

**迭代升级**:如果新想法是已有 UC/IF 的 behavior 升级 / re-scope,**改原条目**而不是开新 ID。

> **核心理念**:头脑风暴 + 直接联动
>
> | ❌ 单向写入                 | ✅ 3 维度头脑风暴 + 直接落地              |
> | --------------------------- | ----------------------------------------- |
> | 用户给一句话,AI 直接拆 UC   | 用户给模糊想法,AI 多轮反问把 3 维度清晰化 |
> | 改完 PRD 但 Tasks 没拆 task | 3 维度讨论完,prd/add/tasks 一次性联动改   |

## 接口

```sh
/wk-idea-flesh <任意模糊想法>
```

**例**:

```sh
/wk-idea-flesh 我要赚到一个小目标
/wk-idea-flesh btw 能不能批量导入 repo
/wk-idea-flesh 加个暗色主题
```

skill 内部自动决定 3 维度的讨论深度(简单想法 3 轮,复杂想法 6 轮)。

## 3 维度头脑风暴

| 维度     | 讨论什么                                 | 落到哪个文档                                                                                                |
| -------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **需求** | persona / 场景 / 价值 / 优先级 / UC 拆分 | `docs/prd.md`(§2 目标 / §4 场景)+ `docs/tasks.md` User Case                                                  |
| **方案** | 架构影响 / 决策点 / IF 拆分 / 视图更新   | `docs/add.md`(§1-§5 视图 / §7 Decision)+ `docs/tasks.md` Inner Feature                                      |
| **任务** | 排期意向 / 依赖 / 粒度                   | `docs/tasks.md` Backlog(raw 想法暂存,3 桶)/ User Case & Inner Feature 子任务列表(`[ ]` 拆解)  |

**核心规则**:

- **3 个维度必谈**(每维度至少 1 轮澄清,共 3-6 轮)
- **讨论完才动手** —— 不要边聊边写,避免来回返工
- **3 文档独立按需** —— 任一文档都可能"不动"。每个文档有自己的触发原则(见顶部表)。
- **迭代升级优先** —— 3 维度头脑风暴完先问 "这是新建 ID,还是**升级已有 UC/IF**?",后者改原条目(User Case / Inner Feature 改文+加新 `[ ]` 子任务)而不是加新 ID
- **已有 ID 不要复制行为** —— 重复 ID 加 UC 是反模式;真需要新 UC 走新 ID(避免历史重叠)
- **新 UC/IF 进 tasks.md(User Case / Inner Feature 段文)+ 从 tasks.md Backlog 移除 raw 行(flesh 闭环)** —— **仅当这条想法真的产出了新的 UC/IF ID**;纯 polish / 纯 PRD 改动不适用这条

## 文档系统(3 文件,自包含 catalog + 状态 + Backlog)

> 历史 **4 文件**(`prd/add/tasks/sprint`)于 2026-07-17 合并为 3 文件,状态机整体内聚进 `tasks.md`。

每个文档有**独立的触发原则**(任一原则成立 → 改;不成立 → 跳)。详细见顶部表。

| 文档                                                       | 职责                                                                         | 触发原则(各自独立)                                                                   |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `docs/prd.md`                                              | 产品需求文档(PRD)— 产品向:愿景 / 目标 / 非目标 / 场景 / 范围外 / 风险        | 想法动了**产品定位 / 需求 / 场景**则改                                               |
| `docs/add.md`                                              | 架构设计文档(ADD)— 技术向:Context + 5+1 view + Decision View + Critical Lens | 想法动了**架构 / 方案 / 决策**则改                                                   |
| `docs/tasks.md`(`User Case` + `Inner Feature` + `Backlog`) | UC/IF 定义(骨架+状态) — 自包含 catalog + 子任务列表 + Backlog | 想法动了**UC/IF 定义**(新增 / 升级 / 删除 / 详设微调)或**状态/Backlog** 则改 |

**关键**: 这 3 个**可写**文档**互相不可替代** —— PRD §2 目标 ≠ tasks.md UC 实现细节;ADD §5 组件图 ≠ tasks.md Inner Feature 描述。**没有"必动"**,每条想法 3 文档独立判断改 / 不改。

**反过来**: 想法是升级已有 UC/IF 时,改的是 `tasks.md User Case / Inner Feature 既有段文`(加新 `[ ]` 子任务或改文);可能 `prd/add`(平级影响)。 —— 状态翻 `[~]` 不在 flesh 职责内(那是 wk-task-dev)。

> **作用域**:本 skill **只**处理 `docs/prd.md` / `docs/add.md` / `docs/tasks.md` 三个可写文档—— 这是 wk-doc-align 评估基线。任何其他文件(如独立的 `design.md` / `decisions/000N-xxx.md` / `roadmap.md`)**不在本 skill 范围**。

## 何时使用

- 用户描述新想法 / 新需求 / 新决策 / 新技术债
- 任何模糊想法 → 头脑风暴 → 落地

## 何时不要使用

- ❌ 项目没有 `docs/` 目录(先建文档骨架)
- ❌ 文档结构跟 doc-align 不一致(先跑 `wk-doc-align` 评估,按其 verdict 修复后再用)
- ❌ 用户要写代码实现(用 `dev:end-to-end` / `ultracode` / `dev:code` 模式)
- ❌ 改动只是代码(无 PRD/ADD/Tasks 联动需求)—— 本 skill 不动代码
- ❌ 要改 `design.md` / `roadmap.md` / `decisions/` 文件 —— 这些不在本 skill 范围
- ❌ 用户已经规划好要做什么(如"做下个 task / 从 backlog 抓 N 个 task") —— `wk-sprint-shape` 已废弃(2026-07-17),无版本塑形概念;简单"做 task"走 `/wk-task-dev UC-XX-YY` 或 `/wk-task-dev IF-XX-NN` 入口,不是新想法,flesh 不接

---

## 流程(7 步)

### Step 1:探测文档存在性

```bash
ls docs/prd.md docs/add.md docs/tasks.md 2>&1
```

| 情况     | 处理                                                 |
| -------- | ---------------------------------------------------- |
| 3 个全在 | 进 Step 2                                            |
| 只有部分 | **先停**——告诉用户缺哪个,按 doc-align 规范补建空模板 |
| 全都不在 | **拒绝执行**——本 skill 只增量更新,不从零搭文档       |

### Step 2:3 维度头脑风暴(多轮澄清)

**澄清流程**:按 **需求维度 → 方案维度 → 任务维度** 顺序,每维度 1-2 轮澄清,共 3-6 轮。每轮用 `AskUserQuestion` 提问,根据回答更新维度结论。

#### 需求维度(必谈,1-2 轮)

提问清单:

0. **新建 vs 迭代升级**(首问 — 决定整个产物的形态):
   - "这个想法是**全新功能**(开新 UC/IF),还是**已有 UC/IF 的 behavior 升级**?(如『UC-04-02 重新建议按钮:以前只更新 llmSuggestedTags,现在直接覆写 doc.tags』)"
   - **后续**:新建走 Step 4 新增路径(产出 `tasks.md User Case / Inner Feature` 新段文 + 从 `tasks.md Backlog` 移除对应 raw 行)。**升级走 Step 4 升级路径**(产物:改 `tasks.md User Case / Inner Feature` 既有段文 + 加新 `[ ]` 子任务;状态机内聚在 tasks.md,无需另写状态文档)
1. **Persona / 场景** — "谁会用这个功能?在什么场景?"(必问)
2. **价值 / 动机** — "解决了什么问题?不做会怎样?"(必问)
3. **优先级** — P0(必须)/P1(重要)/P2(可选)/P3(远期)
4. **UC 拆分** — "拆成 1 个 UC 还是多个?是否需要配套 IF?"

每轮后形成 **需求摘要**(只在对话里,不写入文件):

```
需求摘要:
- 形态: {new UC/IF | upgrade 已有 UC-04-02 | upgrade 已有 IF-XX-YY}
- Persona: {角色}
- 场景: {在 XX 场景下}
- 价值: {解决 XX 问题}
- UC 拆分: {N 个 UC,概要} (新建) / 改 {已有 UC-X-Y,新行为概要} (升级)
- 优先级: {P0/P1/P2/P3}
```

#### 方案维度(必谈,1-2 轮)

提问清单:

1. **架构影响** — "涉及架构变更吗?新组件?新存储?新接口?"
2. **决策点** — "需要新决策吗?有没有 ADR 要写?"
3. **视图 / 模块影响** — "哪些 view 要更新?哪些模块要改?"
4. **IF 拆分** — "系统内部要拆几个 IF?配套 UC?"

每轮后形成 **方案摘要**:

```
方案摘要:
- 架构影响: {new component / storage / interface}
- 决策: {ADR 编号或"无"}
- 视图影响: {哪些 view}
- IF 拆分: {M 个 IF,概要}
```

#### 任务维度(必谈,1 轮)

提问清单:

1. **排期意向** — "打算排到哪个版本?还是先入 Backlog 等排期?"
2. **依赖** — "依赖其他 UC/IF 吗?还是独立可做?"
3. **粒度** — "每个 UC/IF 大概要多少时间?半天?1 天?1 周?"

每轮后形成 **任务摘要**:

```
任务摘要:
- 排期意向: {v0.X 或"先入 Backlog"}
- 依赖: {UC-XX-YY 等 或"无"}
- 粒度: {估算}
```

#### 结束条件

- 3 维度都至少谈了 1 轮
- 用户说"够了 / 行了 / 落地吧 / 改吧"
- 或超过 6 轮后用户仍未明确 → 提示用户简化想法后重试

### Step 3:提议联动改动(3 文档整体预览)

把 3 维度摘要翻译成 3 文档的具体修改:

```
提议(3 维度头脑风暴 → 联动落地):

[需求摘要]
- Persona: 知识库管理员
- 场景: 在管理界面需要批量导入
- 价值: 提升 30s+ 效率
- UC 拆分: 1 个 UC(UC-05-01)
- 优先级: P3

[方案摘要]
- 架构影响: 无(复用现有 CSV 解析)
- 决策: 无
- 视图影响: §1 View 1 增加批量导入按钮
- IF 拆分: 1 个 IF(IF-05-01 CSV 解析批处理)

[任务摘要]
- 排期意向: 先入 Backlog
- 依赖: 无
- 粒度: 半天

[文档具体改动]

docs/prd.md:
- §2 目标加 8. 批量导入 ≥ 10 个 repo < 30s
- §4 加场景:管理员上传 CSV 含 URL 列表

docs/add.md:
- §1 View 1 增加"批量导入"操作说明

docs/tasks.md:
- `tasks.md User Case` 加 **UC-05-01** [P3] 批量导入 repo(CSV → URL 列表)
  - **作为** 知识库管理员
  - **我希望** 上传一份 CSV 文件一次性导入多个 repo
  - **以便** 不用逐个粘贴 URL
  - **实现细节**:
    - 解析 CSV 第一列为 GitHub URL
    - 跳过格式不合法的行并记 warn 日志
- `tasks.md Inner Feature` 加 **IF-05-01** [P3] CSV 解析批处理
  - **批量解析 CSV 中的 GitHub URL 列表,支持错误容忍**
  - **实现细节**:
    - 文件路径: src/importer/csv.ts
    - 复用现有单条 URL 解析逻辑
- Backlog 抠出 raw → User Case / Inner Feature 段文落定义 + 从 Backlog 移除对应行(flesh 闭环):
  - [ ] UC-05-01 批量导入 repo
  - [ ] IF-05-01 CSV 解析批处理

联动一致性预检:
- UC-05-01 与现有最大 UC ID UC-04-09 连续 ✓
- UC-05-01 同时出现在 tasks.md User Case(完整定义 + 子任务列表)+ Backlog 行已被移除(flesh 闭环) ✓

OK 就改?如要调整文案请说。
```

**编号冲突检测**:

```bash
grep -oE "UC-[0-9]+-[0-9]+" docs/tasks.md | sort -u > /tmp/existing_uc.txt
LAST_UC=$(grep -oE "UC-[0-9]+-[0-9]+" docs/tasks.md | sort -V | tail -1)
NEXT_UC="$LAST_UC"
while grep -q "^$NEXT_UC$" /tmp/existing_uc.txt; do
  NEXT_UC=$(echo "$NEXT_UC" | awk -F'-' '{printf "UC-%s-%d", $2, $3+1}')
done
echo "$NEXT_UC"
```

### Step 4:联动编辑(**3 文档独立按需**,没有"必动")

**核心**: 把 3-dim 头脑风暴的结论逐条对照顶部那张"4 文档触发原则"表,各文档独立判断"改 / 不动":

| 形态                                 | 改动集(独立判断)                                                                                                 |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **纯产品定位调整**(无 UC/IF)         | prd.md §1 愿景 / §2 目标。其余 3 文档**不动**                                                                    |
| **纯架构决策**(如 GraphQL over REST) | add.md §7 Decision (+ tasks.md 已有 IF 的实现细节里备注变更)。其余 2 文档**不动**                                |
| **新功能**(纯新增 ID)                | tasks.md Backlog 抠出 raw → User Case / Inner Feature 段 **新段**(完整定义 + 子任务列表 [ ])+ Backlog 删除对应行。prd/add 各按自身原则判断 |
| **迭代升级**(改已有 UC/IF)           | tasks.md User Case / Inner Feature 既有段**改文**(保留 ID)+ 加新 `[ ]` 子任务。prd/add 各按自身原则判断平级影响(多数情况不动)         |
| **纯实现 / 状态调整**                | **不属 flesh**,属于 wk-task-dev(`/wk-task-dev UC-XX-YY` 入口直接读段文 + 翻 `[ ]` → `[x]`)                                                    |
| **极小 polish**(纯 doc-typo / 措辞)  | 甚至可能**4 文档全不动**——直接 do nothing;flesh 链路就跑了 3-dim 讨论但没产生文档产物                            |

按"先 User Case / Inner Feature 段文(若有)→ Backlog 移除(若有)→ §2 PRD 触发 → ADD §7/视图(若有)"的依赖顺序编辑。每个文档**先判断**:本想法有没有触发它的原则?**没有就跳**——`/wk-idea-flesh "X"` 跑完 3 文档可能有 0/1/2/3 改动,**没有最小限制**。

**灵魂**: 改动集是 3-dim 头脑风暴的**结论**决定的,不是惯例决定的。polish 不动 prd/add。迭代升级不开新 ID。**纯 PR 讨论不动代码文档(也不动 tasks/sprint)** —— 例如"我们 5 年后要做的事",flesh 改 /okrs /prd §1 即可,tasks/sprint 都跳过。

### Step 5:联动校验(**按形态选检查项**,没有"必跑"清单)

校验是**形态驱动的**,不是默认全跑。

#### 新建 ID 路径(产生新 UC/IF)

```bash
# a. 新 UC/IF ID 唯一?
NEW_UC="UC-05-01"
grep -cE "^\- \[[x—~!0-9/]+\] \*\*$NEW_UC" docs/tasks.md   # User Case / Inner Feature 完整定义 1 次
grep -cE "^[ \t]*- \[ \] " docs/tasks.md                       # 子任务列表 ≥ 1
# (完整定义 + 子任务列表加起来,需目视确认)

# b. 跨文件一致性:tasks.md Backlog 引用的 UC/IF 都在 User Case / Inner Feature 定义?(flesh 闭环)
ALL_DEFINED=$(grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/tasks.md | sort -u)
# Backlog 内被引用的 UC/IF(raw 行 / polish ID) - Backlog 桶 1 raw 不应有 ID,Backlog 桶 3 polish 应有 ID
ALL_REFERRED=$(awk '/^## Backlog/{flag=1; next} /^## /{flag=0} flag' docs/tasks.md | grep -oE "(UC|IF)-[0-9]+-[0-9]+" | sort -u)
comm -23 <(echo "$ALL_REFERRED") <(echo "$ALL_DEFINED")
# 应为空(无 dangling UC/IF 引用,即 Backlog 桶 3 polish ID 全在 User Case / Inner Feature 段 已定义)
```

#### 迭代升级路径(改已有 UC/IF 段文)

```bash
# a. 改文是否真的落在 target 段里?
TARGET="UC-04-02"
grep -A 8 "^\- \*\*$TARGET" docs/tasks.md | head -9
# 视觉确认:旧文 / 新文都在 User Case / Inner Feature 段 该 UC 段里
```

#### 通用(无论何形态,各文档触发原则命中时才跑)

```bash
# ADD §7 决策 ↔ Tasks UC/IF 引用一致(若动了 add.md)
grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/add.md | sort -u

# PRD §4 场景锚 → Tasks UC/IF 引用一致(若动了 prd.md)
# (略,人工目视就行)

# 跨文件:tasks.md Backlog 引用的 UC/IF(已塑形 polish 桶)是否都仍在 User Case / Inner Feature 段 定义?(新建路径关键校验)
```

输出校验报告(按形态选):

```
新建 ID 路径:
- UC-05-01 在 tasks.md User Case 完整定义:是 ✓
- UC-05-01 在 tasks.md User Case / Inner Feature 完整定义(含子任务列表):是 ✓
- IF-05-01 在 tasks.md User Case / Inner Feature 完整定义(含子任务列表):是 ✓
- Backlog raw 行已移除(flesh 闭环):是 ✓
- ADD §7 / PRD §4 引用一致(若改了相关文档):一致 ✓

迭代升级路径:
- UC-04-02 User Case 段文已包含新行为:目视确认 ✓
- 其他 UC/IF ID 未变化(没新增 ID):一致 ✓
- tasks.md User Case / Inner Feature 父 bullet 状态前置(若写 `[x]`):目视确认 ✓

零改动路径:
- 产物为空,无 commit;flesh 跑完即结束(可以加 wip 备忘但不入 commit)
```

### Step 6:提议 commit(**按需 stage**,不是默认 4-doc)

```bash
# 只 stage 真正改了的文档(由 Step 3 提议的改动集决定)
# 例如新功能+有需求/架构变更的 path:
git add docs/prd.md docs/add.md docs/tasks.md

# 例如纯迭代升级(只动 tasks.md 一段文):
git add docs/tasks.md

# 例如纯 PRD 改 §1 愿景(其他 3 文档不动):
git add docs/prd.md

# 例如极小 polish / 4 文档全不动:
# (flesh 跑完不产生任何 commit)
```

commit message 按 **3 段式**结构(subject + 3 段 body):

```
idea: <一句话描述 (UC/IF id 或升级范围)>

>> original idea:

<用户原始输入的完整原文,多个段落/条目都保留,不要总结/重写。引用必须 verbatim>

>> 头脑风暴:

需求: <需求维度的产出 — 形态 / persona / 场景 / 价值 / UC 拆分 / 优先级>
方案: <方案维度的产出 — 架构影响 / 决策点 / 视图 / IF 拆分>
任务: <任务维度的产出 — 排期 / 依赖 / 粒度>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**WHY 3 段式**:

- `>> original idea` 段保留用户**完整原文**作为可追溯原始诉求(后续 git blame 时能立刻看到当时诉求,不被脑暴过程覆盖)
- `>> 头脑风暴` 段固化 3 维度结论,让 commit reader 不必读对话历史就能理解决策理由
- `>> 文档改动` 段是 doc-only commit 的核心交付清单,精准到 § 坐标 + 简述

**变体**:

- 纯迭代升级(只动 tasks.md 一段文):3 段都精简,`>> 文档改动` 只 1-2 行
- 极小 polish(4 文档全不动):不 commit
- 已 commit 的历史 commit 用此格式后,`git log --format=%B` 全文检索 "original idea" 即可追溯全部用户原始诉求

### Step 7:后续动作提示(可选)

commit 后提示用户:

```
已落地: <改动集摘要,只列实际改的文档>
位置: <具体 § 坐标>

后续可选:
- 继续 /wk-idea-flesh 加新想法
- 用 /wk-doc-align 评估文档质量(4 文件;只检改了的那几个)
- 用 /wk-task-dev 实现 tasks.md User Case / Inner Feature 子任务 `[ ]`(仅在新加 User Case / Inner Feature 段文时;`wk-sprint-shape` 已废弃)
- 用 /wk-task-dev 实现 §1 Sprint 段的 [ ] 项(仅在加了新 ID 时)
```

---

## 硬约束(含 WHY + 反例)

1. **不修改代码** — WHY: 本 skill 只管文档;代码实应用 `dev:end-to-end` / `ultracode` 模式。
   反例: 联动改完文档顺手改 `src/`。
2. **每个 UC 至少 2-3 个子项(或 UC + IF 配套)** — WHY: 来自 tasks-checklist 实现细节嵌套规范;UC 没实现细节 = 占位。
   反例: UC 写 "I want to" 没翻译成 "我希望" 三段式;UC 段无实现细节嵌套。
3. **UC / IF 编号避免冲突** — WHY: 编号冲突会让 git log 和检索定位失效。
4. **不修改 task 状态 `[ ]` → `[x]`** — WHY: 那是 task-dev 完成实现的工作流;本 skill 只管"加想法"。
   反例: UC 段带 `[x]` —— 翻状态归 wk-task-dev(不在 flesh)。
5. **commit message subject ≤ 60 字 + 3 段式 body** — WHY: git log 可读性 + Conventional Commits 规范;3 段式结构(`>> original idea` / `>> 头脑风暴` / `>> 文档改动`)让后续 reader 不必读对话历史就能理解决策理由 + 追溯用户原始诉求(详见 Step 6 commit 模板)。
6. **PRD 瘦身** — WHY: 已迁到 ADD 的内容(数据模型 / 技术栈等)写回 PRD 会双源失同步。
   反例: 把数据模型 / 技术栈重新写回 PRD(doc-align 视为已迁出章节)。
7. **联动改动不拆 commit**(默认) — WHY: 单 commit 保证原子性,避免中间状态文档失同步。
   反例: prd/add/tasks/sprint 拆多个 commit 但中间没推,别人 pull 时中间状态文档失同步。
8. **不创建独立 `decisions/000N-xxx.md` 文件** — WHY: doc-align 不评估该路径;ADD §7 Decision View 才是 ADR 内容的归宿。
9. **不创建 `design.md` / `roadmap.md` / `idea.md` / `research.md` 文件** — WHY: doc-align 不评估这些文件;design / roadmap 请改用 add.md / tasks.md,idea / research 是旧版幽灵文件。
10. **3 维度必谈** — WHY: 头脑风暴的核心是 3 维度各自清晰化,跳过任一维度会导致产物不完整,后续补全成本高。
    反例: 只谈需求不谈方案/任务。
11. **直接联动改 3 文档** — WHY: 头脑风暴的产物就是 3 文档的完整改动,不是只写 Backlog 一行。
    反例: 只在 tasks.md Backlog 写一行 raw,prd/add/User Case / Inner Feature 段 不动(只写了"待办池",没闭环"完整定义")。
12. **新 UC/IF 进 tasks.md User Case / Inner Feature(完整定义 + 子任务列表 [ ])+ 从 Backlog 移除对应 raw 行** — WHY:`tasks.md Backlog` 是"待办池"角色,任何地方出现新待办工作(新 UC/IF / 已有 IF 段文扩展 / 已有 UC 行为升级)都必须回流,且 flesh 写入 User Case / Inner Feature 段 时从 Backlog 抠出对应 raw(闭环),否则后续 task-dev 会疏漏。
    反例: 加了新 UC/IF 但 Backlog raw 漏删(闭环断)。
13. **不接"开新版本 / 做 v0.X / 从 backlog 抽"等已规划操作** — WHY: 这些是 wk-task-dev 的 `/wk-task-dev v0.X` 入口 + Version 表更新,不属于"新想法"。`wk-sprint-shape` 已废弃(2026-07-17)。
14. **3 文档独立按需,无必动** — WHY: 改动集由 3-dim 头脑风暴结论决定,不是惯例。polish 想法可能只动 1 个或不动,甚至 4 文档全不动。
    反例: 默认 tasks + sprint 必动 + 有动作就改 prd/add; —— 每个文档触发原则是独立判断。
15. **跨文档联动需完整** — WHY: 联动不完整会留下半成品:改了 PRD §2 目标但 Tasks 没拆 UC = 提了目标但没拆任务;改了 ADD §7 Decision 但 Tasks 没拆 UC/IF = 决策失追溯;改了 Tasks UC 但 PRD §4 没加场景 = 实现细节有了但产品向入口没同步。
16. **迭代升级优先:改原条目不开新 ID** — WHY: 新 UC/IF 与已有 ID 在行为上重复会导致历史重叠,git blame 失追溯。升级走 User Case / Inner Feature 段 改段文路径,**禁止开新 ID 复制行为**。
    反例: 想法是"已有 UC-XY 的 behavior 升级",却开 UC-X+1-Y 而不改 UC-XY。
17. **active Sprint ≤ 1** — WHY: 多 active Sprint 会让 commit 节奏混乱;一次性堆十几个 Sprint 应合并为代号化 Sprint。
18. **不改 `docs/` 之外的任何文件** — WHY: README.md 等需同步的应单独指示;`design.md` / `roadmap.md` / `decisions/` 等 doc-align 不评估的文件不在本 skill 范围。

## 模板

> 写入 doc 时 verbatim 复用,见 [references/templates.md](./references/templates.md)。
>
> | 产物           | 模板                        |
> | -------------- | --------------------------- |
> | 新 UC          | Tasks UC 三段式             |
> | 新 IF          | Tasks IF 特性描述           |
> | Backlog 条目   | Tasks Backlog               |
> | 新 PRD §2 目标 | PRD §2 新增目标             |
> | 新 PRD §4 场景 | PRD §4 新增场景             |
> | 新 ADR         | ADD §7 Decision View 新决策 |

## 不做的事(边界声明)

> 上文 §硬约束 已覆盖主要反例。本节为对外明示的边界声明,仅 1 条:
>
> - **不直接 commit** —— 必须用户确认 message 后再 commit(本 skill 提议 commit,用户拍板)

## 回滚

如果用户写完后说「这条不要了」或「改错了」:

```bash
# 软回滚:撤销最后一次 docs 改动
git checkout HEAD~1 -- docs/

# 或生成 revert commit(更安全,保留历史)
git revert <commit-hash>
```

回滚后建议跑一次 `wk-doc-align` 确认没破坏文档质量基线。

## 关联

- **上游**:`wk-doc-align` — 评估本 skill 写入的 PRD/ADD/Tasks/Backlog 是否合规
- **下游**:
  - `wk-task-dev` — 实现本 skill 写入的 `tasks.md User Case / Inner Feature` UC/IF 段文内 **子任务列表** 的 `[ ]` 项;**前提**:本 skill 段文已就位(子任务列表已存在)。`wk-sprint-shape` 已废弃(2026-07-17,功能并入 wk-task-dev)。
- **配套**:写完后若改动显著(新增大模块 / 改 API),建议同步 `README.md` 的索引
- **同族塑形链**:
  - `wk-idea-flesh`(本 skill):深度想法落地 —— 3 维度头脑风暴 → 联动改 3 文档 → UC/IF 进 Backlog
  - ~~`wk-sprint-shape`~~:已废弃(2026-07-17,功能并入 `wk-task-dev` + `tasks.md Backlog`)
  - `wk-task-dev`:批量实现 —— Sprint 段内 [ ] → [x]
