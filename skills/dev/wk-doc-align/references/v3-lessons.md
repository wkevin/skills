# v3 实战复盘 — transform 模式的 lean 教训

> 本文件是 SKILL.md §轻量化原则 的扩展参考,记录 v3 实施后用户手工瘦身的具体清单。
>
> **触发**:transform 模式输出后,如果用户手工大段删改,回来对照本清单,反思是否又犯了同样的"过度生成"毛病。

## 复盘来源

commit `ca3cb2` 的 transform 实施复盘。

## 用户删除 vs 用户保留

| 文件 | 用户删除的 | 用户保留的 |
| --- | --- | --- |
| `prd.md` | §0 文档定位 / 配套 / 最后更新前言 4 行;§6 范围外 8 行(合到 §6 roadmap 表格) | §1-§8 内容,重新编号 1-8 |
| `add.md` | "## 最后更新 + 配套" 4 行 | 视图导航 + 全部 §1-§10 |
| `tasks.md` | "## 最后更新 + 配套 + 文档范式" 多行 blockquote;§3 决策依赖整段;§4 M*-T* 映射附录整段 | §1 UC/IF catalog 主体(扁平化) |
| `sprint.md` | §1-§4 标题结构;§4 Commit Reference Appendix 整段;最后更新 1 行 | MileStone 01/02 扁平结构 |
| `docs/README.md` | — | **新增** "## 文档定位" 段(把 4 个文件头部都重复的内容集中到这里) |

## WHY 用户会手工调整

v3 实施的输出虽然"全面"但"繁杂",每个文件都堆了前言 + 跨文档索引 + 额外章节。**信息密度高 ≠ 可读**。transform 模式应输出"够用即可",多余内容交给用户按需添加。

## 模式抽取(给后续 transform 实施参考)

被反复删除的"过度生成"模式:

1. **每文件头部加 "## 配套 / 最后更新 / 文档定位" blockquote** → 应集中在 `docs/README.md`,主文档不重复
2. **tasks.md 加 §3 决策依赖 / §4 M*-T* 映射附录** → tasks.md 应只含 UC/IF catalog,这些是 nice-to-have
3. **sprint.md 加 §4 Commit Reference Appendix** → commit 历史在 git log,文档不必复述
4. **严格 §1-§N 编号** → 编号是建议,项目可自由合并 / 重排,不留空号
5. **tasks.md 用 4 级嵌套 (`## §1 > ### §1.1 > #### UC-XX`)** → 扁平化为 `## User Case / ### UC-01`
6. **每个主文档头部加 "## 文档定位" 段** → 集中在 `docs/README.md`
7. **过度长的 ADR `**Consequences**:` 后不空行** → CommonMark 列表紧贴段落会渲染成同一段,必须空行