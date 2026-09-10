---
name: wk-paper-triage
description: 对一篇论文做 5–10 分钟速读判断：值不值得精读。回答 7 个固定问题并给出 30 秒结论。面向有软件工程经验但未必熟悉该论文领域的读者。Use when the user asks whether a paper is worth reading, wants a quick screen / triage / skim of a paper, or asks "值不值得读 / 速读 / 快速判断".
---

# Paper Triage

快速判断一篇论文值不值得精读。不做完整摘要，不逐段复述，不写精读报告。

## 触发条件

- 用户说"这篇论文值不值得读"、"速读 / 快速判断 / triage / skim"
- 用户给一篇论文（PDF / arXiv / DOI / 标题）并明确只要"快速判断"
- 用户在做阅读清单筛选

## 不做

- 不写完整阅读报告（→ 用 `paper-reading-card` 或 `paper-reading-sodalone`）
- 不做逐段总结
- 不复述 Abstract
- 不堆术语
- 不强行展开公式推导

## 输入

- 论文 markdown / PDF / arXiv 链接 / DOI / 标题（必填其一）
- 用户当前关心的问题（可选，例如"是否值得借鉴到我的项目"）

## 工作流

b

1. **确定来源**。先拿到 abstract + introduction + conclusion + 主图主表。如果只有 abstract，明确告诉用户"信息不足，结论置信度低"。
2. **抓七个问题的答案**。每条都从原文找证据，找不到就写"原文未提及"，不要从记忆里补。
3. **30 秒总结**用单行链路：Problem → Idea → Innovation → Evidence → Limitation。
4. **给 Verdict**。三选一：
   - **值得精读** — 创新强、证据扎实、对你可能有用
   - **值得浏览** — 看看方法/实验即可，不必逐行读
   - **暂不建议读** — 创新一般 / 证据弱 / 与你方向无关
5. 提示用户是否输出为 triage.md 文件（与用户输入文件相同路径）。

不要四象限打分、不要小数评分。

## 输出模板

```markdown
# Paper Triage: <title>

- Authors:
- Venue / year:
- Source: <arXiv / DOI / PDF>
- Read confidence: <high / medium / low —— 取决于拿到的原文深度>

## Problem

它究竟要解决什么问题？（一句话，不复述 abstract）

### Motivation

为什么这个问题值得解决？解决了能怎样，不解决会怎样？

### Prior Work

以前通常怎么解决？最主流的路线是什么？有什么明显不足？

## Key Idea、Core Work

作者最核心的新想法是什么？（一句话讲"做了什么不一样的事"）

### Novelty

真正的创新在哪里？哪些只是已有技术的组合？夸大之处请直接指出。

### Evidence

实验是否真的证明了这个 idea 有效？数据集合理吗？baseline 够强吗？有 ablation 吗？是否只在 toy 上验证？

## Verdict

值不值得精读？为什么？给出三选一判断 + 一句话理由。

## Paper in 30 seconds

**Problem → Idea → Innovation → Evidence → Limitation**

（每段不超过一行，按这个链路串起来）

## Notes for your project

（如果用户给出了项目背景，写一段"如果你关心 X，这篇的 Y 可能有用 / 无用"；无背景则省略此段）
```

## 写作规则

- **面向有软件工程经验但未必熟悉该子方向的读者**。第一次出现的术语必须用一句话解释，之后才能直接用缩写。
- **优先讲"为什么"**，其次才是"怎么实现"。
- **不要堆术语**。术语只用于指代概念，不是炫技。
- **不要逐段总结**。跳过例子、跳过 related work 的罗列、跳过 implementation detail。
- **不要复述 Abstract**。摘掉 abstract 的修辞外壳，只留骨架。
- **如果作者 claim 夸大，明确指出**："作者声称 X，但实验只在 Y 上验证，差距明显"。
- **如果创新性一般，直接说**："这是 A+B 的组合，没有新东西"或"贡献是工程性的，方法上无新意"。
- **如果论文真正重要，明确告诉我"为什么重要"**：是开辟了新方向、解决了长期 open problem、还是提供了关键实证基准。
- **找不到证据就写"原文未提及"或"证据不足"**，不要从通用知识里补。

## 验证

- 问题都有回答（即便答案是"原文未提及"）。
- Verdict 是三选一并给出一句话理由。
- 30 秒总结是单行链路，不是五段重写。
- 没有出现"我们提出"、"显著优于"这类未消化的宣传语。
- 没有逐段复述论文结构。

## 完成

完成 = 所有问题 + Verdict + 30 秒总结全部填好，且 Verdict 明确。
