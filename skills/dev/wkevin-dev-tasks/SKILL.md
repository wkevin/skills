---
name: wkevin-dev-tasks
description: 用户批量开发 task 的 skill，启动 docs/tasks.md 中的 tasks 集合（可以是 task 的 id，或 version id，不能指定 milestone id）， 依次开发，每个 task 完成一次 git commit, 过程中无需确认，尽最大努力完成长时间、无人工干预的批量 task 开发。所以启动前由用户掌握 tasks 的实现集、优先级、实现顺序等关键要素。
---

## 用法

**允许：**

```
/wkevin-dev-tasks UC-03-02         # 实现 id 为 UC-03-02 的 User Case
/wkevin-dev-tasks IF-04-01         # 实现 id 为 IF-04-01 的 Inner Feature
/wkevin-dev-tasks v0.5             # 实现 v0.5 version 的所有 tasks（含 UC、IF）
/wkevin-dev-tasks status           # 仅打印当前进度（不开发）
```

**禁止：**

```
/wkevin-dev-tasks M2               # 实现 id 为 M2 的 MileStone -- 危险、禁止操作
/wkevin-dev-tasks all              # 实现 所有 [ ] 项（按 Milestone + Version 顺序）-- 危险、禁止操作
```

`version` 必须能精确匹配 §2 中某个 Milestone 下的 Version 字符串（`v0.1` / `v0.5` / `v0.9` / `v1.0-rc` 等），否则输出 `VERSION_NOT_FOUND: <arg>` 并停止。

## 工作流程

1. 首先提取用户指定的待实现版本（$2），如果没有指定，则停下来询问用户。
2. 针对 `docs/tasks.md` §2 中某个 Milestone 下的指定 Version，**按顺序**逐个实现 task
   - 执行 task 的开发之前，评估 task 的复杂度，如果较高，则启用以下 claude code 功能的一个或多个：
     - workflow（使用 ultracode 关键字）
     - /goal
     - /debug
   - 包括但不限于：UC-XX-YY / IF-XX-YY，有可能有其他编号，以 tasks.md 文件中的实际为准
   - 完成开发后修改 tasks.md 中相应 task 的完成状态 （`[] -> [x]`）
   - 每完成一个 task 就做一次 git commit。**不做** commit 之外的事（不 push / 不 squash / 不 rebase / 不 amend 既有 commit）。
3. 全部完成后，给出一个过程摘要。

## git 提交规范

`<type>(<scope>): <subject>` 格式（来自 CONTRIBUTING.md §5）：

| Type       | 何时用                                      |
| ---------- | ------------------------------------------- |
| `feat`     | 新功能 / 新 UC / 新 IF                      |
| `fix`      | 修 bug（通常对应 §2 "优化与 bug fix" 子节） |
| `refactor` | 重构（无新功能无 bug 修复）                 |
| `docs`     | 纯文档变更                                  |
| `test`     | 加 / 改测试                                 |
| `chore`    | 配置 / 依赖 / 杂事                          |

scope 强制用 `UC-XX-YY` 或 `IF-XX-YY`（不写 `M*-T*`）。Claude 生成的 commit **必须**带 `-m "Co-Authored-By: Claude <noreply@anthropic.com>"`。
