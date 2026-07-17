# 模板参考 — wk-idea-flesh 写入 doc 的标准格式

> 本文件是 SKILL.md §模板 段的外移版。模板只在实际写入文档时被引用,不在 skill 决策主链路上 —— 移出后保持 SKILL.md 顶部清爽。
>
> **使用方式**:根据触发的文档(prd / add / tasks / sprint)与产物形态(UC / IF / Backlog / 目标 / 场景 / ADR)选对应模板,verbatim 复制后填字段。

---

## Tasks UC 三段式(agile,中文标签)

```markdown
- **UC-{xx}-{yy}** [{P0|P1|P2|P3}]
  - **作为** {具体角色 / 场景,不是 "user" 这种空泛词}
  - **我希望** {动作 + 对象}
  - **以便** {价值 / 动机}
  - **实现细节**:
    - {文件路径 / 函数名 / 配置值}
```

## Tasks IF 特性描述

```markdown
- **IF-{mm}-{nn}** [{P0|P1|P2|P3}]
  - **{特性一句话描述}**
  - **实现细节**:
    - {技术点 / 路径}
```

## Tasks Backlog

```markdown
- [ ] UC-{xx}-{yy} {一句话描述}
- [ ] IF-{mm}-{nn} {一句话描述}
```

## PRD §2 新增目标

```markdown
8. **{动词}** — {一句话描述}
```

## PRD §4 新增场景(联动 UC)

```markdown
- **{角色}** {动作}
  - {价值描述}
```

## ADD §7 Decision View 新决策

```markdown
### 7.{N} {新决策标题}

**Status**: Accepted
**Context**: 当时面对什么问题、考虑了哪些备选方案
**Decision**: 最终选了什么 + 为什么
**Consequences**: 选了之后带来的正向 / 负向影响
```