# Sprint 状态推进 — 为什么 sprint-shape 不做

> 本文件记录"为什么 `wk-sprint-shape` skill 不处理 Sprint 状态机推进(Planning → Active → Done)"以及"实际该怎么做"。

## 不处理的原因

1. **状态是业务承诺**,不是算法产物。"激活 Sprint 1"意味着团队承诺在接下来 2 周集中做这些 task,这需要真人拍板。
2. **激活/收尾的副作用**(通知相关人、调整日历、是否开 retrospective)超出 skill 边界。
3. **状态推进在本 skill 范围内 = no-op** —— 识别意图但不动文件,价值密度低。

## 实际怎么做

| 状态变化 | 触发时机 | 操作 |
| --- | --- | --- |
| Planning → Active | Sprint 段已塑形,准备启动 | 在 Sprint 段标题后加 `Active` 关键词:`### Sprint 3 — Bulk-Onboard (v0.5) [Active]` |
| Active → Done | 所有 [ ] → [x] 都已实现 | 在 Sprint 段标题后加 `Done` 关键词:`### Sprint 3 — Bulk-Onboard (v0.5) [Done 2026-07-31]` |
| 任意 → 取消 | Sprint 决定不再做 | 在段头加 `[Cancelled YYYY-MM-DD: <reason>]`,保留历史 |

## Active 校验

```bash
# 校验 doc-align §1.4.1:Active Sprint ≤ 1
ACTIVE_COUNT=$(awk '/^### Sprint/{flag=1} flag && /Active/{count++; flag=0} END{print count}' docs/sprint.md)
[ "$ACTIVE_COUNT" -le 1 ] || echo "WARN: Active Sprint > 1"
```

## 与 task-dev 的关系

- Sprint 处于 Active 时,`wk-task-dev` 实现 Sprint 段内 [ ] task。
- Sprint 处于 Done 时,`wk-task-dev` 不再处理该 Sprint 内的 task(应建新 Sprint)。
- Sprint 处于 Planning(刚塑形未激活)时,可以增量修改 task 列表,不影响状态。