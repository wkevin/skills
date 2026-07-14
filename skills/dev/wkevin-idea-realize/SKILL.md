---
name: wkevin-idea-realize
description: 把新想法通过 3 维度头脑风暴(需求 / 方案 / 任务)落到文档系统,直接联动修改 docs/prd.md + docs/add.md + docs/tasks.md + docs/sprint.md 四个文档,新产生的 UC/IF 自动进入 tasks.md §1.1/§1.2(完整定义)+ sprint.md §2 Product Backlog(等待排期)。所有产物严格对齐 wkevin-doc-align 评估基线。触发词:"/idea-realize"、用户说"加需求 / 加个 task / 加个 UC / 加个 IF / 加个决策 / btw, ..."、或任何模糊想法描述。
---

# /idea-realize — 3 维度头脑风暴驱动的想法落地

把当前轮用户描述的想法,通过 **3 维度头脑风暴** 落到文档系统 —— 跟用户多轮交互把需求、方案、任务各自清晰化,然后**直接联动修改 prd.md / add.md / tasks.md / sprint.md 四个文档**。新产生的 UC/IF 进入 `tasks.md §1.1/§1.2`(完整定义)+ `sprint.md §2 Product Backlog`(等待排期)。

> **核心理念**:头脑风暴 + 直接联动
>
> | ❌ 单向写入                 | ✅ 3 维度头脑风暴 + 直接落地              |
> | --------------------------- | ----------------------------------------- |
> | 用户给一句话,AI 直接拆 UC   | 用户给模糊想法,AI 多轮反问把 3 维度清晰化 |
> | 改完 PRD 但 Tasks 没拆 task | 3 维度讨论完,prd/add/tasks 一次性联动改   |

## 接口

```sh
/wkevin-idea-realize <任意模糊想法>
```

**例**:

```sh
/wkevin-idea-realize 我要赚到一个小目标
/wkevin-idea-realize btw 能不能批量导入 repo
/wkevin-idea-realize 加个暗色主题
```

skill 内部自动决定 3 维度的讨论深度(简单想法 3 轮,复杂想法 6 轮)。

## 3 维度头脑风暴

| 维度     | 讨论什么                                 | 落到哪个文档                                                     |
| -------- | ---------------------------------------- | ---------------------------------------------------------------- |
| **需求** | persona / 场景 / 价值 / 优先级 / UC 拆分 | `docs/prd.md`(§2 目标 / §4 场景)+ `docs/tasks.md §1.1 UC`        |
| **方案** | 架构影响 / 决策点 / IF 拆分 / 视图更新   | `docs/add.md`(§1-§5 视图 / §7 Decision)+ `docs/tasks.md §1.2 IF` |
| **任务** | 排期意向 / 依赖 / 粒度                   | `docs/sprint.md §2 Product Backlog`(暂存)                        |

**核心规则**:

- **3 个维度必谈**(每维度至少 1 轮澄清,共 3-6 轮)
- **讨论完才动手** —— 不要边聊边写,避免来回返工
- **直接联动改 4 个文档** —— prd + add + tasks + sprint 一次性落地
- **新 UC/IF 进 tasks.md §1.1/§1.2 + sprint.md §2 Product Backlog** —— 没排进 Sprint 前都是 Backlog 状态

## 文档系统(4 文件,产品 catalog + Sprint 排期分离)

| 文档                                | 职责                                                                         | 何时写入              |
| ----------------------------------- | ---------------------------------------------------------------------------- | --------------------- |
| `docs/prd.md`                       | 产品需求文档(PRD)— 产品向:愿景 / 目标 / 非目标 / 场景 / 范围外 / 风险        | 头脑风暴需求维度      |
| `docs/add.md`                       | 架构设计文档(ADD)— 技术向:Context + 5+1 view + Decision View + Critical Lens | 头脑风暴方案维度      |
| `docs/tasks.md §1.1/§1.2`           | UC/IF 定义(骨架)— 用户向 UC + 系统向 IF                                      | 头脑风暴需求/方案维度 |
| `docs/sprint.md §2 Product Backlog` | **暂存区** — 已头脑风暴但未排进 Sprint 的 UC/IF                              | **本 skill 自动写入** |

**关键**: 新产生的 UC/IF **同时**进 `tasks.md §1.1/§1.2`(完整定义,给未来实现用)+ `sprint.md §2 Product Backlog`(暂存状态)。

> **作用域**:本 skill **只**处理 `docs/prd.md` / `docs/add.md` / `docs/tasks.md` / `docs/sprint.md` 四个文件 —— 这是 wkevin-doc-align 评估基线。任何其他文件(如独立的 `design.md` / `decisions/000N-xxx.md` / `roadmap.md`)**不在本 skill 范围**。

## 何时使用

- 用户描述新想法 / 新需求 / 新决策 / 新技术债
- 任何模糊想法 → 头脑风暴 → 落地

## 何时不要使用

- ❌ 项目没有 `docs/` 目录(先建文档骨架)
- ❌ 文档结构跟 doc-align 不一致(先跑 `wkevin-doc-align` 评估,按其 verdict 修复后再用)
- ❌ 用户要写代码实现(用 `dev:end-to-end` / `ultracode` / `dev:code` 模式)
- ❌ 改动只是代码(无 PRD/ADD/Tasks 联动需求)—— 本 skill 不动代码
- ❌ 要改 `design.md` / `roadmap.md` / `decisions/` 文件 —— 这些不在本 skill 范围
- ❌ 用户已经规划好要做什么(如"开新版本 / 做 v0.X / 从 backlog 抽") —— 这是 wkevin-task-dev 的事,不是新想法

---

## 流程(7 步)

### Step 1:探测文档存在性

```bash
ls docs/prd.md docs/add.md docs/tasks.md docs/sprint.md 2>&1
```

| 情况     | 处理                                                  |
| -------- | ----------------------------------------------------- |
| 4 个全在 | 进 Step 2                                             |
| 只有部分 | **先停**——告诉用户缺哪个,按 doc-align 规范补建空模板 |
| 全都不在 | **拒绝执行**——本 skill 只增量更新,不从零搭文档        |

### Step 2:3 维度头脑风暴(多轮澄清)

**澄清流程**:按 **需求维度 → 方案维度 → 任务维度** 顺序,每维度 1-2 轮澄清,共 3-6 轮。每轮用 `AskUserQuestion` 提问,根据回答更新维度结论。

#### 需求维度(必谈,1-2 轮)

提问清单:

1. **Persona / 场景** — "谁会用这个功能?在什么场景?"(必问)
2. **价值 / 动机** — "解决了什么问题?不做会怎样?"(必问)
3. **优先级** — P0(必须)/P1(重要)/P2(可选)/P3(远期)
4. **UC 拆分** — "拆成 1 个 UC 还是多个?是否需要配套 IF?"

每轮后形成 **需求摘要**(只在对话里,不写入文件):

```
需求摘要:
- Persona: {角色}
- 场景: {在 XX 场景下}
- 价值: {解决 XX 问题}
- UC 拆分: {N 个 UC,概要}
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
- §1.1 加 **UC-05-01** [P3] 批量导入 repo(CSV → URL 列表)
  - **作为** 知识库管理员
  - **我希望** 上传一份 CSV 文件一次性导入多个 repo
  - **以便** 不用逐个粘贴 URL
  - **实现细节**:
    - 解析 CSV 第一列为 GitHub URL
    - 跳过格式不合法的行并记 warn 日志
- §1.2 加 **IF-05-01** [P3] CSV 解析批处理
  - **批量解析 CSV 中的 GitHub URL 列表,支持错误容忍**
  - **实现细节**:
    - 文件路径: src/importer/csv.ts
    - 复用现有单条 URL 解析逻辑
- §2 Product Backlog 加(在 sprint.md):
  - [ ] UC-05-01 批量导入 repo
  - [ ] IF-05-01 CSV 解析批处理

联动一致性预检:
- UC-05-01 与现有最大 UC ID UC-04-09 连续 ✓
- UC-05-01 同时出现在 tasks.md §1.1 和 sprint.md §2(完整定义 + Backlog 暂存) ✓

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

### Step 4:联动编辑(按依赖序)

按 **PRD → ADD → Tasks §1.1/§1.2 → Sprint §2 Product Backlog** 顺序编辑:

| 顺序 | 文档                      | 编辑要点                                    |
| ---- | ------------------------- | ------------------------------------------- |
| 1    | PRD                       | §2/§4 按需                                  |
| 2    | ADD                       | §1-§5 视图按需;§7 Decision 按需             |
| 3    | Tasks §1.1                | UC agile 三段式(作为/我希望/以便)+ 实现细节 |
| 4    | Tasks §1.2                | IF 特性描述 + 实现细节                      |
| 5    | Sprint §2 Product Backlog | **同时**加入新 UC/IF(等待排期)              |

### Step 5:联动校验

```bash
# 1. 新 UC/IF ID 唯一?
NEW_UC="UC-05-01"
NEW_IF="IF-05-01"
grep -c "^\- \*\*$NEW_UC" docs/tasks.md    # §1.1 完整定义 1 次
grep -c "^\- \[ \] $NEW_UC" docs/sprint.md # §2 Product Backlog 1 次
# §1.1 + sprint.md §2 加起来 = 2 才算正确(完整定义 + Backlog 暂存)

# 2. UC 同时出现在 tasks.md §1.1(完整定义)和 sprint.md §2(Backlog)?
awk '/^## §1\.1/,/^## §[12]\./' docs/tasks.md | grep -c "$NEW_UC"  # §1.1 应 = 1
grep "^\- \[ \] $NEW_UC" docs/sprint.md | wc -l                      # §2 应 = 1

# 3. ADD §7 Decision ↔ Tasks UC/IF 引用一致?(如果有 §7 决策)
grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/add.md | sort -u

# 4. 跨文件一致性:sprint.md 引用的 UC/IF 都在 tasks.md 定义?
ALL_DEFINED=$(grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/tasks.md | sort -u)
ALL_REFERRED=$(grep -oE "UC-[0-9]+-[0-9]+|IF-[0-9]+-[0-9]+" docs/sprint.md | sort -u)
comm -23 <(echo "$ALL_REFERRED") <(echo "$ALL_DEFINED")
# 应为空(无 dangling UC/IF 引用)
```

输出校验报告:

```
联动校验结果:
- UC-05-01 唯一(tasks.md §1.1 完整定义):是 ✓
- UC-05-01 在 sprint.md §2 Product Backlog 暂存:是 ✓
- IF-05-01 唯一(tasks.md §1.2 完整定义):是 ✓
- IF-05-01 在 sprint.md §2 Product Backlog 暂存:是 ✓
- ADD §7 决策数 ↔ Tasks UC/IF 引用:一致 ✓
- sprint.md 引用的 UC/IF 都在 tasks.md 定义:一致 ✓

OK 提交?
```

### Step 6:提议 commit(联动版)

```bash
# 单 commit(默认 — 4 文档联动必须原子)
git add docs/prd.md docs/add.md docs/tasks.md docs/sprint.md
git commit -m "idea(3d-brainstorm): 加 UC-05-01 批量导入 repo + IF-05-01 CSV 解析 (3 维度, 联动 prd+add+tasks+sprint)"
```

### Step 7:后续动作提示(可选)

commit 后提示用户:

```
已落地:UC-05-01 批量导入 repo + IF-05-01 CSV 解析
位置:tasks.md §1.1/§1.2 完整定义 + sprint.md §2 Product Backlog 暂存

后续可选:
- 继续 /wkevin-idea-realize 加新想法
- 用 /wkevin-doc-align 评估文档质量(4 文件)
- 用 /wkevin-task-dev 实现 Backlog 条目(先把条目从 sprint.md §2 移到 §1 Sprint 段)
```

---

## 硬约束(含 WHY)

1. **不修改代码** — WHY: 本 skill 只管文档;代码实应用 `dev:end-to-end` / `ultracode` 模式。
2. **每个 UC 至少 2-3 个子项(或 UC + IF 配套)** — WHY: 来自 tasks-checklist §1.1.3 实现细节嵌套规范;UC 没实现细节 = 占位。
3. **UC / IF 编号避免冲突** — WHY: 编号冲突会让 git log 和检索定位失效。
4. **不修改 task 状态 `[ ]` → `[x]`** — WHY: 那是 task-dev 完成实现的工作流;本 skill 只管"加想法"。
5. **commit message subject ≤ 60 字** — WHY: git log 可读性 + Conventional Commits 规范。
6. **PRD 瘦身** — WHY: 已迁到 ADD 的内容(数据模型 / 技术栈等)写回 PRD 会双源失同步。
7. **联动改动不拆 commit**(默认) — WHY: 单 commit 保证原子性,避免中间状态文档失同步。
8. **不创建独立 `decisions/000N-xxx.md` 文件** — WHY: doc-align 不评估该路径;ADD §7 Decision View 才是 ADR 内容的归宿。
9. **不创建 `design.md` / `roadmap.md` 文件** — WHY: doc-align 不评估这两个文件;请改用 add.md / tasks.md。
10. **3 维度必谈** — WHY: 头脑风暴的核心是 3 维度各自清晰化,跳过任一维度会导致产物不完整。
11. **直接联动改 3 文档** — WHY: 头脑风暴的产物就是 3 文档的完整改动,不是只写 Backlog 一行。
12. **新 UC/IF 同时进 tasks.md §1.1/§1.2 + sprint.md §2 Product Backlog** — WHY: §1.1/§1.2 是完整定义(给 task-dev 实现用),§2 是暂存状态(等 Sprint 排期)。
13. **不接"开新版本 / 做 v0.X / 从 backlog 抽"等已规划操作** — WHY: 这些是 wkevin-task-dev 或后续版本规划的事,不属于"新想法"。

## 模板

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

### Tasks Backlog

```markdown
- [ ] UC-{xx}-{yy} {一句话描述}
- [ ] IF-{mm}-{nn} {一句话描述}
```

### PRD §2 新增目标

```markdown
8. **{动词}** — {一句话描述}
```

### PRD §4 新增场景(联动 UC)

```markdown
- **{角色}** {动作}
  - {价值描述}
```

### ADD §7 Decision View 新决策

```markdown
### 7.{N} {新决策标题}

**Status**: Accepted
**Context**: 当时面对什么问题、考虑了哪些备选方案
**Decision**: 最终选了什么 + 为什么
**Consequences**: 选了之后带来的正向 / 负向影响
```

## 联动反模式

- ❌ **跳过任一维度**(只谈需求不谈方案/任务)— 产物不完整,后续补全成本高
- ❌ **只写 Backlog 一行**(不联动改 3 文档)— 失去头脑风暴价值
- ❌ **新 UC/IF 没同时进 Backlog** — 失去 Backlog 暂存意义
- ❌ **改了 PRD §2 目标但 Tasks 没拆 UC** — 提了目标但没拆任务
- ❌ **改了 ADD §7 Decision 但 Tasks 没拆 UC/IF** — 决策失追溯
- ❌ **改了 Tasks UC 但 PRD §4 没加场景** — 实现细节有了,但产品向入口没同步
- ❌ **联动改动拆多个 commit 但中间没推** — 别人 pull 时中间状态文档失同步
- ❌ **UC 不是 agile 三段式**(写了 "I want to" 没翻译成 "我希望")— tasks-checklist §1.1.2 critical
- ❌ **UC 带 `[x]` 状态** — 状态归 `sprint.md §1` Sprint 段,不是 UC 本身;tasks-checklist §1.1.1 critical
- ❌ **Sprint 数量膨胀** — 一次性堆十几个 Sprint;合并为代号化 Sprint,active Sprint ≤ 1
- ❌ **试图把"开新版本 / 做 v0.X / 从 backlog 抽"接进本 skill** — 这些是版本规划,不属于"新想法"

## Worked Example

**用户**:`/wkevin-idea-realize btw 能不能批量导入 repo,现在只能一个个粘贴 URL`

**Step 2 3 维度头脑风暴**:

需求维度:

- Q: 谁能用? → A: 知识库管理员
- Q: 价值? → A: 一次导 10+ 个,效率提升 30s+
- Q: 优先级? → A: P3 远期
- Q: UC 拆分? → A: 1 个 UC

方案维度:

- Q: 架构影响? → A: 无,只是 UI 增强
- Q: 决策? → A: 无
- Q: 视图影响? → A: §1 View 1 加按钮
- Q: IF 拆分? → A: 1 个 IF(CSV 解析批处理)

任务维度:

- Q: 排期? → A: 先入 Backlog
- Q: 依赖? → A: 无
- Q: 粒度? → A: 半天

**Step 3 提议**:

```
提议(3 维度头脑风暴 → 联动落地):

[需求摘要] 知识库管理员批量导入 repo,提升效率,1 个 UC, P3
[方案摘要] 无架构影响,§1 View 1 加按钮,1 个 IF
[任务摘要] 先入 Backlog,无依赖,半天

[文档具体改动]

docs/prd.md:
- §2 目标加 8. 批量导入 ≥ 10 个 repo < 30s
- §4 加场景:管理员上传 CSV 含 URL 列表

docs/add.md:
- §1 View 1 增加"批量导入"操作说明

docs/tasks.md:
- §1.1 加 **UC-05-01** [P3] 批量导入 repo
  - **作为** 知识库管理员
  - **我希望** 上传一份 CSV 文件一次性导入多个 repo
  - **以便** 不用逐个粘贴 URL
  - **实现细节**:
    - 解析 CSV 第一列为 GitHub URL
    - 跳过格式不合法的行并记 warn 日志
- §1.2 加 **IF-05-01** [P3] CSV 解析批处理
  - **批量解析 CSV 中的 GitHub URL 列表,支持错误容忍**
  - **实现细节**:
    - 文件路径: src/importer/csv.ts
    - 复用现有单条 URL 解析逻辑
- §2 Product Backlog 加(在 sprint.md):
  - [ ] UC-05-01 批量导入 repo
  - [ ] IF-05-01 CSV 解析批处理

OK 就改?
```

**Step 6 commit**:

```bash
git add docs/prd.md docs/add.md docs/tasks.md
git commit -m "idea(3d-brainstorm): 加 UC-05-01 批量导入 + IF-05-01 CSV 解析 (3 维度)"
```

---

## 不做的事

- ❌ 不写代码实现
- ❌ 不改 `docs/` 之外的任何文件(README.md 等需同步的单独指示)
- ❌ **不创建 / 修改 `design.md`、`roadmap.md`、`decisions/` 等 doc-align 不评估的文件** —— 这些是历史遗留,本 skill 强制 4 文件(prd + add + tasks + sprint)+ Product Backlog 模型
- ❌ 不直接 commit(必须用户确认 message 后再 commit)
- ❌ 不创建 `idea.md` / `research.md`(旧版幽灵文件)
- ❌ 不重新创建 doc-align 视为已迁出的 PRD 章节(数据模型 / 技术栈等应写 ADD)
- ❌ **不接"开新版本 / 做 v0.X / 从 backlog 抽"等已规划操作** —— 这些是版本规划,不属于"新想法"

## 回滚

如果用户写完后说「这条不要了」或「改错了」:

```bash
# 软回滚:撤销最后一次 docs 改动
git checkout HEAD~1 -- docs/

# 或生成 revert commit(更安全,保留历史)
git revert <commit-hash>
```

回滚后建议跑一次 `wkevin-doc-align` 确认没破坏文档质量基线。

## 关联

- **上游**:`wkevin-doc-align` — 评估本 skill 写入的 PRD/ADD/Tasks/Backlog 是否合规
- **下游**:`wkevin-task-dev` — 实现 `sprint.md §1` Sprint 段的 [ ] 项;**注意**:Product Backlog 条目要先做 Sprint 排期移到 §1 才能被 task-dev 实现
- **配套**:写完后若改动显著(新增大模块 / 改 API),建议同步 `README.md` 的索引
- **同族**:
  - **wkevin-add-idea**:另一种轻量想法入库模型 —— 只写 Backlog 一行(无 UC/IF 完整定义),适合快速随手记下想法
  - **wkevin-idea-realize**(本 skill):深度想法落地模型 —— 3 维度头脑风暴 + 直接联动改 3 文档 + UC/IF 进 Backlog 暂存
  - 两个 skill 的 Backlog 互通:wkevin-add-idea 写的"一行 idea"在需要展开时,可由 wkevin-idea-realize 做 3 维度头脑风暴补全
