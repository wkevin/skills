# wk-marp-slide

> 用 **Markdown + Marp** 生成**指定品牌版式**的幻灯片。输出 HTML / PDF / PNG。

品牌是**通用的、数据驱动**的：本 skill 的 `assets/images/motherboard/` 下有几个
目录，就有几个可用品牌（每个目录一套背景图）。新增品牌 = 加一个目录，无需改脚本
或文档。

## 怎么用

直接说需求即可，例如：

> 帮我做一份「Git Workflow」的汇报 PPT，用 zte 品牌。

agent 会自动：列出可用品牌 → 建 deck → 引导编辑 `index.md` → 构建 HTML/PDF/PNG
并把结果展示给你。**你不需要手动运行任何脚本。**

## 目录结构

```
wk-marp-slide/
├── SKILL.md                    ← 给 agent 看的操作说明
├── README.md                   ← 本文件（给人看）
├── template/index.md           ← deck 模板（6 种页面版式）
├── scripts/
│   ├── new_deck.sh             ← 建新 deck（复制全部品牌）
│   └── build.sh                ← 构建 HTML / PDF / PNG（可切品牌）
└── assets/
    ├── main.css                ← 主题（版式 + Heti 中文排版）
    ├── mermaid.min.js          ← Mermaid 运行时
    └── images/motherboard/
        ├── zte/                ← 内部版母版（logo + 内部使用标记）
        └── pub/                ← 对外版母版
        └── <你的新品牌>/       ← 想加品牌就加目录（slide-face/content/bottom.png）
```

## 页面版式

| 版式   | 写法                                                           | 效果                 |
| ------ | -------------------------------------------------------------- | -------------------- |
| 封面   | `## 标题` + `<!-- _class: face -->` + `![bg](…slide-face.png)` | 蓝底白字大标题       |
| 目录   | `## 目录` + `![bg left:30%](…slide-face.png)`                  | 左侧封面图，右侧条目 |
| 章节页 | `# 一级目录` + `<!-- _class: chapter -->`                      | 蓝底白字标题条       |
| 内容页 | `## 二级目录`                                                  | 正文                 |
| 分栏   | `<div class="container"><div class="col">…`                    | 多列并排             |
| 尾页   | `![bg](…slide-bottom.png)`                                     | 结束页               |

详见 [SKILL.md](./SKILL.md)。

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
- `gs`（ghostscript）、`convert`（ImageMagick）—— 可选，压缩 PDF / 拼长图
