---
name: wk-marp-slide
description: >
  Create branded slide decks from Markdown using Marp (Marpit). The brand
  (theme background art) is generic and data-driven: every directory under
  this skill's assets/images/motherboard/ is one selectable brand. Ships a
  cover / TOC / chapter-divider / content / closing page system, multi-column
  layouts, Mermaid diagrams, and Chinese classical typography (Heti). Builds
  to HTML, PDF, and PNG. Use when the user asks to make a slide deck /
  presentation / PPT / 幻灯片 / 汇报材料, to edit or rebuild an existing Marp
  deck, or to add a Mermaid diagram or multi-column layout. Triggers on
  "做 PPT" / "生成 slide" / "建个讲稿" / "slide deck" / "marp" / "汇报材料".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
user-invocable: true
---

# /wk-marp-slide

用 **Markdown + Marp** 生成**指定品牌版式**的幻灯片。源文件是 `index.md`，构建
产物是 HTML / PDF / PNG。

**品牌是通用的、由数据驱动的**：本 skill 的 `assets/images/motherboard/` 下
有几个目录，就有几个可用品牌（每个目录一套背景图，含 `slide-face.png` /
`slide-content.png` / `slide-bottom.png`）。想新增品牌，往 `assets/images/
motherboard/` 里加一个目录即可，不需要改任何脚本或文档。

> 主题 CSS、各品牌背景图、Mermaid 运行时都随 skill 自带（`assets/`），
> 一个 deck 目录是**自包含**的 —— 可以整体拷走、单独构建。

---

## 工作流（agent 驱动，用户不碰脚本）

用户只提需求；**由你（agent）执行脚本**，不要要求用户运行任何 `bash ...`。

### 1. 列出可用品牌

```bash
ls "$SKILL_DIR/assets/images/motherboard/"
```

每个子目录名 = 一个品牌。用户没指定时，默认取**按字母序第一个**。

### 2. 建新 deck

```bash
bash "$SKILL_DIR/scripts/new_deck.sh" <deck_dir> \
     -t "标题" -s "副标题" -a "姓名.工号" -d "2026.11.20" \
     [-b <brand>]
```

`new_deck.sh` 会把**所有**可用品牌都复制进 deck（`images/motherboard/<brand>/`），
并用 `-b`（默认字母序第一个）把其中一个烘焙进 `index.md` 作默认版式。
不加 `-b` 就用默认。

deck 目录放哪由你定 —— 默认建在用户当前工作目录下，或问一下用户想放哪。

### 3. 用户编辑 `index.md`（或你来改）

源文件是 `index.md`，用户在里面填内容。你可以按下面「页面版式」直接帮用户搭
好结构，也可以让用户自己改。

### 4. 构建

```bash
bash "$SKILL_DIR/scripts/build.sh" -d <deck_dir> -f html,pdf,png [-b <brand>] [-s]
```

默认 `-b` 用 `index.md` 里烘焙的品牌；要切到别的品牌就 `-b <brand>`。产物：

| 路径                       | 内容                           |
| -------------------------- | ------------------------------ |
| `dist/html/index.html`     | 浏览器直接看（可翻页、可演讲） |
| `dist/pdf/index.pdf`       | 交付用                         |
| `dist/png/index.001.png …` | 逐页图片                       |
| `dist/sheet-<brand>.png`   | 逐页拼一张长图（需加 `-s`）    |

构建是 visual 的：**构建后把 PNG 或 contact sheet `Read` 进来给用户看**，
别只丢一个路径。PDF 用 `Read` 也能预览。

**切品牌不用改源文件**：`build.sh -b <brand>` 构建时临时把 `index.md` 里的
品牌路径换掉，产物写到独立目录（用 `-o <dir>`），源文件保持不变。

---

## 品牌（brand）：由 assets/motherboard/ 决定

| 品牌目录 | 用途 | 特征 |
| -------- | ---- | ---- |
| `zte`    | 内部汇报 | 中兴 logo + "内部使用▲" 标记 |
| `pub`    | 对外分享 | 无内部标记，蓝色科技风封面 |

> 这张表是**示例**，不是写死的 —— 实际以 `assets/images/motherboard/` 下
> 的目录为准。新增品牌 = 加一个目录，本文档无需改动。

**给一个品牌加说明**：在 `assets/images/motherboard/<brand>/README.md` 里写
一句用途/特征，agent 建 deck 时可读给你看。没有就只列目录名。

---

## deck 目录结构

```
my-talk/
├── index.md            ← 源文件（唯一需要编辑的）
├── main.css            ← 主题（版式 + 中文排版）
├── mermaid.min.js      ← Mermaid 运行时
├── images/motherboard/ ← 所有可用品牌的背景图 <brand>/
├── img/                ← 放你自己的图片
├── .vscode/            ← Marp 预览配置 + 代码片段
└── dist/               ← 构建产物（已在 .gitignore 里）
```

`index.md` 里的图片路径**相对 deck 目录**写，例如 `img/foo.png`、
`images/motherboard/<brand>/slide-face.png`。

### VSCode 预览（可选）

用 VSCode 的 **Marp** 扩展打开 deck 目录即可实时预览。`.vscode/` 里已配好：

- `settings.json` —— 指定 `./main.css` 主题、开启 HTML、限制 TOC 层级
- `marp.code-snippets` —— 代码片段：`insert-2-column`、`insert-3-column`、
  `insert-mermaid-block`、`insert-font-block`、`insert-div-block`

命令面板里 `Marp: Export slide deck...` 可导出 PDF / HTML / PNG；
`Markdown: open preview to the side` 是分页预览。

---

## 页面版式（6 种）

模板 `template/index.md` 演示了全部（以 `<brand>` 指代所选品牌）。关键在于
**Marp 指令 + CSS class**：

### 1. 封面（face）

```markdown
## 标题

### 副标题

姓名.工号
2026.11.20

<!-- _class: face -->
<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](images/motherboard/<brand>/slide-face.png)
```

`_class: face` → 白字大标题；`_paginate: skip` → 不计页码；
`_header/_footer: ''` → 隐藏页眉页脚。

### 2. 目录（TOC）

```markdown
## 目录

- [一级目录](#一级目录)
- [二级目录](#二级目录)

![bg left:30%](images/motherboard/<brand>/slide-face.png)
```

`![bg left:30%]` → 封面图占左侧 30%，正文在右侧。

### 3. 章节页（chapter）

```markdown
# 一级目录

<!-- _class: chapter -->
```

`#` 标题 + `_class: chapter` → 整页变成蓝底白字的大标题条。

### 4. 内容页

```markdown
## 二级目录

正文内容。
```

### 5. 尾页（结束）

```markdown
---

<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](images/motherboard/<brand>/slide-bottom.png)
```

### 6. 分栏

```markdown
<div class="container">
<div class="col">

### 第一列

- 条目

</div>
<div class="col">

### 第二列

- 条目

</div>
</div>
```

`.col` 等分，`.col2` 两倍宽，`.colv` 纵向居中。

### 全局背景

`index.md` 开头（front matter 之后）放一次即可，作用于**之后所有页**：

```markdown
<!-- backgroundImage: url("images/motherboard/<brand>/slide-content.png") -->
```

封面的 `![bg]` 会在该页**覆盖**这个全局背景。

---

## Mermaid 图表

```markdown
<div class="mermaid">
%%{init: {'theme':'base'}}%%
graph LR;
    A-->B;
    B-->C;
</div>
```

**必须**在文件**末尾**（最后一个 `---` 之后）加：

```markdown
<!-- mermaid.js -->
<script src="./mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true});</script>
```

`mermaid.min.js` 必须在**与 md 同目录**（路径 `./mermaid.min.js` 是相对 md 解析的）。

---

## 中文古典排版（Heti）

`main.css` 内置了 Heti（[sivan/heti](https://github.com/sivan/heti)），
用于古诗文、竖排等场景。

**用显式 HTML 标签写标题**（`<h1>` / `<p>`），不要用 Markdown 的 `#`：

```markdown
<div class="heti heti--ancient">

<h1>出师表</h1>

<p>作者：諸葛亮</p>

<p>先帝创业未半而中道崩殂，今天下三分。</p>

</div>
```

原因：`headingDivider: 2` 让 `#` / `##` 成为**分页符**，写在 `<div>` 里会把
这个块从中间劈成两页（实测：标题跑到前一页、正文留在后一页，版式全乱）。
`<h1>` 是普通 HTML，不触发分页。

`heti--ancient` 下的一级标题会变成**居中、加粗、楷体**；正文段落自动首行缩进 2 字符。

诗词用显式 HTML 标签控制得更细：

```markdown
<div class="heti heti--poetry">
  <h2>九月九日忆山东兄弟</h2>
  <p class="heti-x-large">
    独在异乡为异客，<br>
    每逢佳节倍思亲。
  </p>
</div>
```

可用变体：`heti--ancient`（古文）、`heti--poetry`（诗词）、`heti--columns-2`（分栏）、
`heti--vertical`（竖排）、`heti--annotation`（夹注）、`heti--song`/`heti--hei`/`heti--kai`（字体）。

---

## 构建脚本参数

```bash
build.sh [选项] [deck_dir]

-d, --deck DIR       deck 目录（默认当前目录）
-o, --out DIR        输出目录（默认 <deck>/dist）
-f, --format LIST    html,pdf,png（默认 html,pdf）
-b, --brand NAME     背景母版（默认 index.md 里烘焙的）
-c, --compress       用 ghostscript 压缩 PDF
-s, --sheet          额外拼一张 contact sheet 长图
```

`-b` 会校验品牌存在：deck 里 `images/motherboard/` 下没有的，直接报错并列可用列表。

---

## 坑（都已实测，务必遵守）

1. **PDF/PNG 必须加 `--html`**。Marp 默认把 raw HTML 转义成文本 ——
   Mermaid 图变成 `%%{init...}` 源码、`<div class="container">` 分栏塌成一坨、
   Heti 完全失效。脚本已默认带上；手工调 marp 时**别漏**。
   （HTML 输出不受影响，输出 HTML 时可省略。）

2. **单文件模式的 `--images png` 不带扩展名** —— 产物是 `index.001` 而不是
   `index.001.png`。脚本构建后统一改名。手工调时注意。

3. **`-o <dir>` 只在 `-I <dir>`（输入目录）模式下可用**；给多个文件传 `-o <dir>`
   会报 _"Output path cannot specify with processing multiple files"_。

4. **`mermaid.min.js` 必须与 md 同目录**，且用 `./mermaid.min.js` 相对路径引用。

5. **PNG/PDF 里的相对图片路径按 md 所在目录解析**；HTML 里的相对路径按
   **输出 html 所在目录**解析 —— 所以脚本在 `dist/html/` 里软链了
   `images/`、`img/`、`mermaid.min.js`。

6. **章节锚点**：中文标题的 id 是 URL 编码的（`#一级目录` → `#%E4%B8%80...`）。
   Marp 会自动把正文里的中文锚点链接编码成匹配的形式，直接写 `#一级目录` 即可。

7. **`headingDivider: 2`** 让 `#` 和 `##` 都成为分页符 —— 想让某页不换页，
   用 `---` 显式控制。**副作用**：写在 `<div>` 里的 `#` / `##` 也会分页，
   把块劈成两页（Heti 古诗文块尤其容易踩 —— 用 `<h1>` 代替 `#`，见上文）。

8. **临时母版文件**：`build.sh -b <brand>` 会在 deck 目录生成 `build-<brand>.md`，
   构建结束自动删除。**不要**把它提交进 git（`.gitignore` 已含 `build-*.md`）。

---

## 依赖

| 工具                           | 用途          | 缺失时                                     |
| ------------------------------ | ------------- | ------------------------------------------ |
| `marp` (`@marp-team/marp-cli`) | 核心          | 必装：`npm install -g @marp-team/marp-cli` |
| Chrome / Chromium              | PDF、PNG 渲染 | 装 Chrome，或 `CHROME_PATH` 指定           |
| `gs` (ghostscript)             | `-c` 压缩 PDF | 可选                                       |
| `convert` (ImageMagick)        | `-s` 拼长图   | 可选                                       |

---

## 编辑已有 deck

1. 找到 `index.md`；
2. 改内容（保持 `<!-- _class: ... -->`、`<div class="container">` 等结构）；
3. 重新 `build.sh -d <deck_dir>`（默认沿用烘焙品牌，或 `-b` 切品牌）。

**不要**改 `main.css` 里的 `.container` / `.col` / `.chapter` / `.face` 等类名 ——
模板和文档都依赖它们。
