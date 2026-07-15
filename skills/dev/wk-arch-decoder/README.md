# wkevin-arch-decoder (架构解码器)

> 代码仓库架构深度分析 skill —— 从代码反推设计哲学与决策取舍

把"看代码"变成"**理解代码为什么这么写**"。区别于传统的"事实清点表",本 skill 强调**判断、取舍、批判**。

## 文件结构

| 文件                   | 角色                                    | 何时被读                             |
| ---------------------- | --------------------------------------- | ------------------------------------ |
| `SKILL.md`             | skill 入口,操作规范(被 Claude 加载执行) | skill 激活时                         |
| `example.md`           | 输出模板,7 视图 + 批判的完整示例        | 写报告时参考                         |
| `reference-5-views.md` | v1.0 沉淀的五视图法方法论               | Phase 1 视图定义参考(不直接对外触发) |

## 7 阶段工作流(快览)

```
Phase 0  上下文摸底 (40% 时间)        ← v2.0 新增,强制前置
Phase 1  五视图清点 (每个表带 WHY)    ← 经典方法论 (Phase 1 的 1/7)
Phase 2  决策视图 (Roads Not Taken)   ← v2.0 新增
Phase 3  行为视图 (AI 项目专属)       ← v2.0 新增
Phase 4  凝结 (反向 mental model)     ← v2.0 新增
Phase 5  批判性视角 (强制 3 个毛病)    ← v2.0 新增
Phase 6  完整性校验
```

## 触发关键词

`架构解码`、`架构理解`、`分析代码仓库`、`分析 repo`、`分析项目架构`、`架构分析`、`代码架构`、`系统架构`、`五视图`、`为什么这么设计`、`设计哲学`、`架构取舍`、`harness`、`agent 项目分析`、`MCP 项目分析`

## 用户输入要求

- **必填**:GitHub/GitLab URL 或本地路径
- **可选**:**读者意图**(影响详略)
  - 新人入职 → 完整 5-view + 简化版 Decision/Behavior
  - 决策评估 → 重 Decision View + Synthesis + Critical Lens
  - 学习偷师 → 重 Behavior View + Synthesis + 设计哲学
  - 故障排查 → 重 Runtime View + Failure Modes
  - 二次开发 → 重 Development + Behavior + Critical
- **可选**:分析重点、输出格式(Markdown / JSON)

---

## 改动说明 (Changelog)

### v1.0 (基线) — 2026-06-04

- 五视图清点(逻辑/数据/开发/运行/物理)
- 每视图必绘图清单
- 章节归属原则

### v2.0 (重构) — 2026-06-08

> v1.0 只产出"事实清点",在 AI/Agent 类项目上会**只见树木不见森林**(描述了 SQLite、MCP、FTS5,但没解释作者为什么这么选,也没看 prompt 层)。v2.0 加入**前置上下文视图、决策视图、行为视图(AI 专属)、凝结步骤、批判视角**,强制每个事实都配 WHY 和判断,把分析从"清点表"升级为"架构理解"。

- ⭐ 新增 Phase 0: 上下文与心智模型 (强制前置)
- ⭐ 新增 Phase 2: 决策视图 (含 Roads Not Taken)
- ⭐ 新增 Phase 3: 行为视图 (AI 项目专属 -- Prompt 位置图 / Token 经济 / 触发链)
- ⭐ 新增 Phase 4: Synthesis 凝结
- ⭐ 新增 Phase 5: Critical Lens 批判
- ⭐ 强制每张表加 WHY 列,禁止空话
- ⭐ 强制每张 mermaid 配 ≥ 2 段文字解读
- ⭐ 加入事实/判断分层标注 (📋/💭/❓/⚠️)
- ⭐ 加入项目类型识别 + 领域适配 checklist
- ⭐ 加入读者意图前置

### v2.1 (改名) — 2026-06-08

⭐ **改名**:`wkevin-5-views` → `wkevin-arch-decoder`(架构解码器)

**原因**:v2.0 升级后,五视图只占工作流 1/7(Phase 1),"5-views" 已不能代表 skill 全貌。"decoder"(解码)对应新加的"理解/解码设计哲学"定位。核心任务不是"看清代码有什么",而是"**理解作者为什么这么写**"。

**改动**:
- 目录:`skills/dev/wkevin-5-views/` → `skills/dev/wkevin-arch-decoder/`
- `5-views-method.md` 保留为内部参考,改名为 `reference-5-views.md`,头部加 v1.0 定位说明
- `SKILL.md` frontmatter `name` 同步、`description` 增加"架构解码"触发词
- `SKILL.md` 标题改为"架构解码器 - 从代码反推设计哲学"
- `example.md` 头部增加"读者导览",说明 7 视图结构
- 改动说明/changelog 从 `SKILL.md` 移到此 README.md(让 SKILL.md 保持纯操作规范)

**破坏性变更**:无对外接口破坏,文件路径变了而已。
