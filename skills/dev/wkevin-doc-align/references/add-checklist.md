# ADD（Architecture Design Document）评估清单

对 `docs/add.md` / `docs/design.md` 逐节评估。

## 0. 文件级检查

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 0.1 | 文件存在且 ≥ 300 行（太短说明架构还没成型） | | critical |
| 0.2 | 顶部有"最后更新"日期 | | nice-to-have |
| 0.3 | 有清晰的视图导航（5+1 view + Decision + Behavior + Synthesis + Critical Lens） | | critical |

**警告信号**：

- ❌ < 200 行 — 大概率是占位或堆术语
- ❌ > 1500 行 — 架构可能还在剧烈变化，文档追不上

---

## 1. §0 Context & Mental Model

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 1.1 | **0.1 根本痛点** 一句话能讲清（不是"提升效率"空话） | | important |
| 1.2 | **0.2 核心信念** 列 3-5 条带出处（commit / doc / issue） | | important |
| 1.3 | **0.4 一句话核心抽象** 通过 30 秒理解测试 | | important |
| 1.4 | **0.5 项目类型识别** + checklist（AI / Web / CLI / 框架） | | nice-to-have |

**30 秒理解测试**：拿掉 §0，让一个没看过代码的人复述——他能说出"这个项目 = X + Y + Z"吗？

---

## 2. §1-§5 五视图

每个视图都强制检查 **WHY 列 + 图后解读**。

### §1 Logical View

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 1.1 | 模块职责表带 **WHY** 列（不能只写"职责"） | | critical |
| 1.2 | 含**逻辑分层图**（mermaid 或 ASCII） | | important |
| 1.3 | ≥ 2 条核心业务链路（带时序图） | | important |
| 1.4 | 每个时序图后有 **≥ 2 段解读**（事实层 + 判断层） | | critical |

### §2 Data View

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 2.1 | 含 **ER 图** 或实体关系描述 | | important |
| 2.2 | 存储选型表带 WHY 列 | | critical |
| 2.3 | **字段归属契约**（哪些字段归用户 / 哪些归 GitHub / 哪些归 LLM） | | critical |
| 2.4 | 数据一致性章节（事务 / 锁 / 冲突） | | important |

### §3 Development View

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 3.1 | 技术栈矩阵带 WHY 列（含版本） | | critical |
| 3.2 | 模块依赖图（mermaid graph TB） | | important |
| 3.3 | 目录结构（实际代码长什么样） | | nice-to-have |
| 3.4 | **"刻意没引入的依赖"清单**（至少 3 条同类项目常用但本项目没用 + WHY） | | important |

### §4 Runtime View

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 4.1 | 关键链路时序图（≥ 1 条） | | critical |
| 4.2 | 并发 / 一致性机制表带 **失败模式**列 | | critical |
| 4.3 | 每个机制后写"如果失效会怎样" | | critical |

### §5 Physical View

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 5.1 | 部署拓扑图（mermaid） | | important |
| 5.2 | 环境变量表（必需 / 可选 / 用途） | | important |
| 5.3 | **水平扩展瓶颈** 即使不扩也写 | | nice-to-have |

---

## 3. §6 Scenarios（+1 视图）

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 6.1 | ≥ 3 条核心用户路径 | | important |
| 6.2 | 每条用流程图 / 序列图 / ASCII 表达 | | nice-to-have |
| 6.3 | 不与 §4 时序图重复 | | nice-to-have |

---

## 4. §7 Decision View ⚠️ v2 核心创新

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 7.1 | **7.1 ADR 摘要表** 存在 | | important |
| 7.2 | 关键 ADR 用 Context / Decision / Consequences 格式 | | important |
| 7.3 | **7.3 显式取舍** 列了"放弃什么换来什么" | | important |
| 7.4 | **7.4 未走的路（Roads Not Taken）≥ 3 条** | | critical |
| 7.5 | 每条 Roads Not Taken 都说明"为什么不做" | | critical |
| 7.6 | **7.5 失败模式** 列出具体崩溃场景 | | critical |
| 7.7 | **7.6 适用边界（When NOT to use this architecture）** 诚实写 | | important |

**Roads Not Taken 是关键信号**：缺失 = 作者没思考过"为什么不选 X"——架构决策往往是惯性。

---

## 5. §8 Behavior View（AI 项目专属）

⚠️ 仅当 §0.5 checklist 标记 AI / Agent 时执行。

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 8.1 | **8.1 LLM 决策触发链**（hook / 自助 / 何时） | | critical（如果项目有 LLM） |
| 8.2 | **8.2 提示工程位置图**——列出所有 prompt 字面值散布位置 | | critical（如果项目有 LLM） |
| 8.3 | **8.3 Token 经济**——省 token 的具体设计 + 数量级 | | important |
| 8.4 | **8.4 自主性 vs 确定性**——哪些字段用 enum / schema 锁死 | | critical |
| 8.5 | **8.5 多 Agent 协作模式**（N/A 时也要写"N/A 因为..."） | | nice-to-have |

**非 AI 项目**：可以省略整个 §8，但要在 §0.5 显式说明"非 AI 项目，无 Behavior View"。

---

## 6. §9 Synthesis

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 9.1 | **9.1 一句话核心抽象** 通过 30 秒测试 | | important |
| 9.2 | **9.2 三个骨架决策**——"如果只能保留 3 个，会是哪 3 个" | | important |
| 9.3 | **9.3 项目灵魂**——"作者最不希望被改坏的部分" | | nice-to-have |
| 9.4 | **9.4 mental model 对照** §9.1 vs §0.4 是否一致 | | nice-to-have |

---

## 7. §10 Critical Lens ⚠️ 强制 3 个毛病

| # | 检查项 | 是/否/部分 | 严重度 |
|---|---|---|---|
| 10.1 | **存在** §10 批判性视角章节 | | critical |
| 10.2 | **≥ 3 个具体毛病**——不能写"这个项目很完美" | | critical |
| 10.3 | 每个毛病含**影响范围** + **修复成本** | | important |
| 10.4 | **10.2 hype 风险**——"作者可能过度推销了什么" | | nice-to-have |
| 10.5 | **10.3 二次开发陷阱**——"新人最容易踩的坑" | | nice-to-have |

**§10 是 skill-judge 必检项**：缺失或敷衍（"还需优化"）= critical。真正挑 3 个毛病需要作者诚实面对自己的代码。

---

## 8. WHY 列质量测试

逐个扫描 §1-§5 每个表格的 WHY 列。

| WHY 内容 | 评级 |
|---|---|
| "为了简单" | ❌ critical（空话） |
| "为了性能" | ❌ critical（没说对比什么快多少） |
| "为了扩展性" | ❌ critical（没说扩展哪方面） |
| "不上 ORM 是因为：① 单用户场景无并发 ② 增加部署依赖 ③ 数据量 < 1k" | ✅ good |
| "用 SQLite WAL 而非 PostgreSQL 是因为：① 单用户无并发写 ② 零运维 ③ 文本 diff 友好" | ✅ good |

**判定规则**：每个 WHY 列必须给具体替代方案 + 该替代方案的失败原因。

---

## 9. mermaid 图解读质量

每张 mermaid 后必须有 ≥ 2 段文字解读。

| 解读内容 | 评级 |
|---|---|
| 无解读（光图） | ❌ critical |
| 1 段"这段流程调用了 X 函数"描述 | ❌ important（只说事实无判断） |
| 1 段事实 + 1 段"为什么这么设计"判断 | ✅ good |
| 事实 + 判断 + **失败场景** | ✅✅ best |

**反模式**：mermaid 后只跟一句"如图所示"——直接砍图。

---

## ADD 综合判定

| critical 数 | important 数 | verdict |
|---|---|---|
| 0 | ≤ 3 | **PASS** |
| 0 | ≥ 4 | **FIX** |
| ≥ 1 | 任意 | **REWRITE** |

**最常见的 3 个 ADD 问题**：

1. **WHY 列是空话**——"为了性能 / 简单" 等不可验证的词
2. **Critical Lens < 3 毛病**或写"这个项目很优秀"——失分关键
3. **mermaid 图光秃秃无解读**——图本身不能传达设计意图

---

## 10. 跨文档引用一致性(cross-doc)

| # | 检查项 | 命令 / 方法 | 严重度 |
|---|---|---|---|
| 10.1 | **add §7 ADR 引用的 commit hash 必须能 `git show <hash>` 验证存在** | 对 N 条 ADR 的 commit 逐一 `git show` | critical |
| 10.2 | **tasks §1.2 IF 引用的 ADR 编号在 add §7 存在** | `grep 'ADR-[0-9]' docs/tasks.md` 验证每个引用 | critical |
| 10.3 | **PRD §1 引用 ADR 编号在 add §7 存在** | `grep 'ADR-[0-9]' docs/prd.md` 验证每个引用 | important |
| 10.4 | **squash commit(如 `4ef9c68`)在 ADR 表格里明确标 "(squash)"** — 否则读者 git log 查不到 | 人工抽检 | important |
| 10.5 | **add §10 Critical Lens 编号(如 `CL-1`)在 PRD §9 风险表或 tasks §1.2 IF 实现细节有引用** — cross-doc 一致 | `grep 'CL-[0-9]' docs/prd.md docs/tasks.md` | nice-to-have |

---

## 11. 内容质量加严(基于实际改造经验)

> 这些是 v1 没强调但实际改造时反复出现的质量问题。

### §7 ADR 数量与详略

| # | 检查项 | 严重度 |
|---|---|---|
| 11.1 | **ADR 数量在 8-20 条之间** — < 8 = 没筛选;> 20 = 退化成 changelog | nice-to-have |
| 11.2 | **ADR 必有"完整三段式"** — Status + Commit + Context + Decision + Consequences(正/负/缓解) | critical |
| 11.3 | **ADR Consequences 必须诚实列 ≥ 2 条负面** — 不能只写正面 | important |
| 11.4 | **Top N(N ≤ 10)详解 + 其余索引** — 详解三段式,索引一行 + 一句 rationale | nice-to-have |
| 11.5 | **Roads Not Taken ≥ 3 条且每条"放弃什么换来什么 + 何时重评估"** | critical |

### §8 Behavior View(AI 项目)

| # | 检查项 | 严重度 |
|---|---|---|
| 11.6 | **列出所有 SKILL.md 文件路径** — 不能只写"读 prompt 找" | important |
| 11.7 | **Token 计量链路明确** — per-job → DB → quota 守卫 → kill switch | important |
| 11.8 | **失败模式列出具体崩溃场景** — 不是"可能失败" | critical |
| 11.9 | **工具调用规约** — 工具名 + 入参 + 出参 + 副作用 | important |

### §10 Critical Lens 严格度

| # | 检查项 | 严重度 |
|---|---|---|
| 11.10 | **§10 严格 3 个真毛病** — 多了变列举失去锐度,降级到 §1 Known Production Gaps | important |
| 11.11 | **每个毛病含"症状 / 根因 / 修复路径 / 不做会怎样"4 段** | important |
| 11.12 | **至少 1 个毛病提到具体 prod 事故场景** — 不是"用户体验差" | critical |
| 11.13 | **§10 不许写"未来可以优化"等套话** | critical |
| 11.14 | **§10 "根因"段必须诚实** — "有意识地没做"或"决策不连贯",不是"忘了" | important |

### §9 Synthesis

| # | 检查项 | 严重度 |
|---|---|---|
| 11.15 | **"三个骨架决策"明确** — 如果只能留 3 个,会留哪 3 个 | important |
| 11.16 | **"项目灵魂"段** — 作者最不希望被改坏的部分 | nice-to-have |
| 11.17 | **§9.1 vs §0.4 一句话抽象对照** — 必须一致 | nice-to-have |

---

## 加载指引

本文件仅在评估 ADD / design.md 时加载。如果用户问"评估 prd.md"——不要读此文件，跳到 [prd-checklist.md](prd-checklist.md)。

本 skill 触发名：`/doc-align`。