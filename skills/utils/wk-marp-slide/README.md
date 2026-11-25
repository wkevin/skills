# wk-marp-slide

> 用 **Markdown + Marp** 生成**指定品牌版式**的幻灯片。输出 HTML / PDF / PNG。

品牌是**通用的、数据驱动**的：本 skill 的 `assets/images/motherboard/` 下有几个
目录，就有几个可用品牌（每个目录一套背景图）。新增品牌 = 加一个目录，无需改脚本
或文档。

## 怎么用

直接说需求即可，例如：

> 帮我做一份「Git Workflow」的汇报 PPT，用 zte 品牌。

agent 会自动：列出可用品牌 → 建 deck → 读排版手册和样张 → 写 `index.md` →
构建 HTML/PDF/PNG → 静态排版检查 → **（模型支持视觉时）自己看一遍渲染结果再修**
→ 展示给你。**你不需要手动运行任何脚本。**

模型没有视觉能力时会跳过"看渲染结果"这一步（静态检查照跑），并在交付时
明确说明无法自查渲染效果 —— 不会假装看过。

## 目录结构

```
wk-marp-slide/
├── SKILL.md                    ← 给 agent 看的操作说明
├── README.md                   ← 本文件（给人看）
├── references/
│   └── layout-guide.md         ← 排版与内容手册（版式决策表 / 密度 / 反模式）
├── template/
│   ├── index.md                ← deck 骨架（9 种版式，占位用【】标出）
│   ├── style-sample.md         ← 版式样张（真实密度与文风的范例，可直接渲染看）
│   ├── img/                    ← 样张用的示例图
│   ├── vscode.code-snippets
│   └── vscode-settings.json
├── scripts/
│   ├── new_deck.sh             ← 建新 deck（复制全部品牌）
│   ├── build.sh                ← 构建 HTML / PDF / PNG（可切品牌，自动跑排版检查）
│   └── check_layout.py         ← 静态排版检查器（16 条规则）
└── assets/
    ├── main.css                ← 主题（版式 + Heti 中文排版）
    ├── mermaid.min.js          ← Mermaid 运行时
    └── images/motherboard/
        ├── zte/                ← 内部版母版（logo + 内部使用标记）
        └── pub/                ← 对外版母版
        └── <你的新品牌>/       ← 想加品牌就加目录（slide-face/content/bottom.png）
```

## 页面版式

骨架在 `template/index.md`（`【】` = 待替换），样张在 `template/style-sample.md`。

| 版式   | 何时用                     | 骨架                                       |
| ------ | -------------------------- | ------------------------------------------ |
| 封面   | 整份 deck 的第一页         | `## 标题` + `_class: face` + `![bg]`       |
| 目录   | 封面之后、第一章之前       | `## 目录` + `![bg left:30%]` + 真链接      |
| 章节页 | 每 5-8 页一次             | `# 标题` + `_class: chapter`               |
| 内容页 | 默认                       | `## 标题` + 正文                           |
| 双栏   | 两个对等维度               | `.container` + `.col` × 2                  |
| 三栏+分隔线 | 一页承载两组信息      | 两段 `.container`，中间 `<hr>`             |
| 四栏图卡 | 四张图并排比较            | `.col` × 4 + `![h:250px]` + 短注          |
| 宽表   | 字段对照                   | `.centerblock` + `table`，结论写在表下     |
| 分屏   | 一张大图 + 短文            | `![bg fit left:30%]` + 正文                |
| 尾页   | 结束                       | `![bg](…slide-bottom.png)`                 |

详见 [SKILL.md](./SKILL.md) 和 [references/layout-guide.md](./references/layout-guide.md)。

## 排版检查

`build.sh` 构建前会自动跑 `check_layout.py`（默认只报告不阻断，`--strict` 可中断）：

```bash
python3 scripts/check_layout.py <deck_dir> [--strict] [--json]
```

规则覆盖 **E1–E6**（空页、div 内标题、div 不配对、mermaid 运行时缺失、
script 指向的文件不存在、占位符未替换）与 **W1–W9**（文字墙、超长条目、
图没定尺、一级标题非章节页、缺目录页、页面过空、分栏数异常、误用分隔线、
骨架占位符残留）。

## 品牌（brand）

| 品牌 | 用途     | 特征                         |
| ---- | -------- | ---------------------------- |
| `zte`| 内部汇报 | 中兴 logo + "内部使用▲" 标记 |
| `pub`| 对外分享 | 无内部标记，蓝色科技风封面   |

上表只是当前示例，以 `assets/images/motherboard/` 实际目录为准。

**切品牌不用改源文件**：告诉 agent 要哪个品牌，构建时它会临时替换背景图路径，
产物写到独立目录，`index.md` 保持不变。

## 依赖

- `marp`（`npm install -g @marp-team/marp-cli`）—— 必装
- Chrome / Chromium —— PDF、PNG 渲染
- `python3` —— 排版检查
- `gs`（ghostscript）、`convert`（ImageMagick）—— 可选，压缩 PDF / 拼长图
