---
name: wk-marp-slide
description: >
  Create branded slide decks from Markdown using Marp (Marpit). The brand
  (theme background art) is generic and data-driven: every directory under
  this skill's assets/images/motherboard/ is one selectable brand. Ships a
  cover / TOC / chapter-divider / content / closing page system, multi-column
  layouts, Mermaid diagrams, and Chinese classical typography (Heti). Includes
  a layout guide and a static layout linter that catch empty pages, wall-of-
  text pages and unsized images. Builds to HTML, PDF, and PNG. Use when the
  user asks to make a slide deck / presentation / PPT / 幻灯片 / 汇报材料, to
  edit or rebuild an existing Marp deck, to add a Mermaid diagram or
  multi-column layout, or to improve slide 排版 / 版式 / 密度 / 多栏 /
  图文混排. Triggers on "做 PPT" / "生成 slide" / "建个讲稿" / "slide deck" /
  "marp" / "汇报材料" / "排版" / "版式".
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

### 3. 写内容（**这一步决定了 deck 好不好看**）

新 deck 的 `index.md` 是一个**骨架**：9 页，每页一种版式，占位文字用 `【】` 标出。
你要做的是**逐页替换成真实内容**，而不是照着骨架再填一遍占位符。

写之前先读这两份东西：

| 读什么 | 得到什么 |
|---|---|
| `$SKILL_DIR/references/layout-guide.md` | 页面解剖、版式决策表、密度规则、内容深度规则、叙事结构、反模式 |
| `$SKILL_DIR/template/style-sample.md` | 一份**真实排版的样张** —— 照它的密度、句式、分栏方式写 |

三条硬规则（违反即返工）：

1. **一页一个论点**；正文页加权密度 ≥ 8（内容行 + 3×图片行）；单栏 ≤ 6 条 bullet。
2. **每页至少 1 条带具体信息的条目**（数字 / 版本 / 年份 / 机构名 / 判定）。
3. **同页分段用 `<hr>`，分页用 `---`**，两者不可混。

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

### 5. 视觉自检（**模型支持视觉时才做**）

构建后要**自己先看**渲染结果 —— 但**前提是你能看懂图片**。

**先判断自己有没有视觉能力**：把 PNG `Read` 进来。

- **能读出画面内容** → 有视觉能力，按下面的清单逐页自检。
- **读不出**（工具报无法解析 / 你描述不出画面） → **没有视觉能力，直接跳过本步**。
  **不要假装看过。** 改为：
  - 只依赖 `check_layout.py` 的静态结果（它能查空页、文字墙、图没定尺、密度等）；
  - 交付时**明确告诉用户**："我没有视觉能力，无法自查渲染效果，麻烦你过一眼"，
    并把 `dist/sheet-<brand>.png` 或 PDF 的路径一起给出。

有视觉能力时：

```bash
bash "$SKILL_DIR/scripts/build.sh" -d <deck_dir> -f html,png -s
# 然后 Read dist/sheet-<brand>.png（逐页长图），逐页过一遍：
```

- 有没有**空白页**（内容被 `---` 切空）？
- 有没有**溢出**（底部被裁掉、字压到页脚）？
- 有没有**塌陷**（分栏挤成一条、图撑破栏）？
- 有没有**连续 2 页太空**（加权密度 < 6）→ 并页？
- 有没有**孤儿标题**（页面只有标题没内容）？
- 分隔线是不是画成了**满宽细线**（`<hr>`），而不是被当成新的一页？

发现问题 → 改 `index.md` → 重新构建 → 再看。**修完再交付给用户。**

静态检查（空页 / div 内标题 / 文字墙 / 图没定尺 / 占位符残留 / mermaid 运行时
缺失）由 `build.sh` 自动跑 `scripts/check_layout.py`；**它不依赖视觉能力，两种模型
都要跑**。也可以单独跑：

```bash
python3 "$SKILL_DIR/scripts/check_layout.py" <deck_dir> [--strict] [--json]
```

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

## 内容编排

细则在 `$SKILL_DIR/references/layout-guide.md`，这里只放最常用的决策。

### 页面解剖

| 层 | 谁控制 | 长什么样 |
|---|---|---|
| 固定层 | front matter | 页眉 `header:`、页脚 `footer:`、页码（`paginate: true`） |
| 页标题 | `##` | **一页只有一个**，左对齐，字号最大 |
| 栏标题 | `###` | 只在 `.col` 里用，被主题**自动居中** |
| 正文 | markdown | 22px 基准 |

### 版式决策表

| 内容类型 | 版式 | 骨架 |
| --- | --- | --- |
| 两个对等维度 | 双栏 | `.container` + `.col` × 2 |
| 三个对等维度 | 三栏 | `.container` + `.col` × 3 |
| 主次不均 | 非对称 | `.col2` + `.col` |
| 一组对比 + 另一组对比 | 三栏 ×2 + 分隔线 | 两段 `.container`，中间 `<hr>` |
| 四张图 + 短注 | 四栏图卡 | `.col` × 4，每栏 `![h:250px]` + 短注 |
| 一张大图 + 短文 | 图文分屏 | `![bg fit left:30%](...)` + 正文 |
| 字段对照 | 宽表 | `.centerblock` + `table`，结论写在表下 |
| 流程 / 依赖 | 图或 mermaid | `<div class="mermaid">` 或一张 SVG |
| 出处 / 脚注 | 页角 | `.rightBottomInPage smallestfont` |

### 密度

**加权密度 = 内容行数 + 3 × 图片行数。** 真实 deck 的中位是 **17**，典型区间
**8 – 32**。低于 8 页面发空（连续两页低于 6 就并页），高于 32 有溢出风险。

**溢出是静默的** —— 内容被裁掉，页面看起来还正常。所以必须渲染出来看（步骤 5）。

### 内容深度

一条 bullet 要是一个**完整短句**，不是一个名词短语；每页至少一条带具体信息的
条目。

```
❌ - 标准、规范
✅ - **ISO/IEC 30173:2023** 规定了数字孪生的三层参考架构
```

完整清单（成对 before/after）见 `$SKILL_DIR/references/layout-guide.md` §8。

### 叙事结构

```
封面 → 目录 → 章节页 → 内容页 ×(3-8) → 章节页 → … → 小结页 → 尾页
```

章节页每 **5–8 页**出现一次；收尾要有**小结页**，不要直接跳到尾页。

---

## 页面骨架速查

模板 `template/index.md` 演示了全部骨架（以 `<brand>` 指代所选品牌）。

### 1. 封面（face）—— 何时用：整份 deck 的第一页

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

### 2. 目录（TOC）—— 何时用：封面之后第一章之前

```markdown
## 目录

- [一级目录](#一级目录)
- [二级目录](#二级目录)

![bg left:30%](images/motherboard/<brand>/slide-face.png)
```

`![bg left:30%]` → 封面图占左侧 30%，正文在右侧。条目要写真链接。

### 3. 章节页（chapter）—— 何时用：每 5-8 页一次，切换大章节

```markdown
# 一级目录

<!-- _class: chapter -->
```

`#` 标题 + `_class: chapter` → 整页变成蓝底白字的大标题条。

### 4. 内容页 —— 何时用：默认

```markdown
## 二级目录

正文内容。
```

**一页一个 `##` 标题。** 下面 5 种版式都是内容页的内部结构。

### 5. 双栏 —— 何时用：两个对等维度

```markdown
<div class="container"><div class="col">

### 第一列

- 条目

</div><div class="col">

### 第二列

- 条目

</div></div>
```

`.col` 等分，`.col2` 两倍宽，`.colv` 纵向居中。

### 6. 三栏 + 同页分隔线 —— 何时用：一页承载两组信息

```markdown
<div class="container smallfont"><div class="col">
### 维度 A
- …
</div><div class="col">
### 维度 B
- …
</div><div class="col">
### 维度 C
- …
</div></div>

<hr>

<div class="container smallfont"><div class="col">
- …
</div><div class="col">
- …
</div><div class="col">
- …
</div></div>
```

`<hr>` 是**满宽细线、不分页**；顶格 `---` 和 `***` 都会分页，别拿来当分隔线。

### 7. 四栏图卡 —— 何时用：四张图并排比较

```markdown
<div class="container"><div class="col">
![h:250px](img/1.png)
- 一句话说明
</div><div class="col">
![h:250px](img/2.png)
- 一句话说明
</div>…</div>
```

所有图**同一个 `h:` 值**，视觉才对齐。

### 8. 宽表 —— 何时用：字段对照

```markdown
<div class="centerblock">

| 列一 | 列二 |
| --- | --- |
| 值 | 值 |

</div>

- 结论写在表下面
```

### 9. 图文分屏 —— 何时用：一张大图 + 短文

```markdown
![bg fit left:30%](img/poster.png)

- 一条硬信息
- 一条判断
```

分屏页正文 ≤ 8 条，不放表格。

### 10. 尾页（结束）

```markdown
---

<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](images/motherboard/<brand>/slide-bottom.png)
```

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
少了这段，图不会渲染成 SVG，只会显示源码。

---

## 中文古典排版（Heti）

`main.css` 内置了 Heti（[sivan/heti](https://github.com/sivan/heti)），用于古诗文、
竖排等场景。**标题要用显式 HTML 标签（`<h1>` / `<p>`），不要用 Markdown 的 `#`** ——
`headingDivider: 2` 会让 `#` / `##` 变成分页符，把 `<div>` 里的块劈成两页。

```markdown
<div class="heti heti--ancient">

<h1>出师表</h1>

<p>先帝创业未半而中道崩殂，今天下三分。</p>

</div>
```

变体：`heti--ancient`（古文）、`heti--poetry`（诗词）、`heti--columns-2`（分栏）、
`heti--vertical`（竖排）、`heti--annotation`（夹注）、`heti--song`/`heti--hei`/
`heti--kai`（字体）。细节见 `$SKILL_DIR/references/layout-guide.md` §11。

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
    --no-lint        跳过排版检查（默认会跑）
    --strict         排版检查有 ERROR 时中断构建
```

`-b` 会校验品牌存在：deck 里 `images/motherboard/` 下没有的，直接报错并列可用列表。

`check_layout.py` 的规则（E1–E6 / W1–W9 / I1–I2）见文件头 docstring。

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

9. **`<hr>` / `> ---` 是同页横线，不是分页符**；顶格 `---` 和 `***` 才是分页符。
   （`***` / `___` 也分页，很多人以为只有 `---` 会。）

10. **`---` 紧跟标题会产生一张空页** —— `---` 开一页、标题再开一页。

11. **文件开头的 HTML 注释块不会多出一页**，但**注释里不能嵌套 `<!-- -->`** ——
    外层注释会在第一个 `-->` 处提前结束，后面的文字会漏到页面上。

---

## 依赖

| 工具                           | 用途          | 缺失时                                     |
| ------------------------------ | ------------- | ------------------------------------------ |
| `marp` (`@marp-team/marp-cli`) | 核心          | 必装：`npm install -g @marp-team/marp-cli` |
| Chrome / Chromium              | PDF、PNG 渲染 | 装 Chrome，或 `CHROME_PATH` 指定           |
| `gs` (ghostscript)             | `-c` 压缩 PDF | 可选                                       |
| `convert` (ImageMagick)        | `-s` 拼长图   | 可选                                       |
| `python3`                      | 排版检查      | 必装（`check_layout.py`）                  |

---

## 编辑已有 deck

1. 找到 `index.md`；
2. 改内容（保持 `<!-- _class: ... -->`、`<div class="container">` 等结构）；
3. 重新 `build.sh -d <deck_dir>`（默认沿用烘焙品牌，或 `-b` 切品牌）。

**不要**改 `main.css` 里的 `.container` / `.col` / `.chapter` / `.face` 等类名 ——
模板和文档都依赖它们。
