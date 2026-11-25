---
marp: true
theme: main
headingDivider: 2
paginate: true
header: 幻灯片的排版语汇
footer: wk-marp-slide · 版式样张
math: mathjax
---

<!--
本文件是 wk-marp-slide 的「版式样张」——一份可以直接渲染浏览的排版范例。

  1. 题材是中性技术话题，**不针对任何具体业务**；照抄的是**形状与句式**，不是题材。
  2. 每页上方一条 HTML 注释，说明这一页在演示什么排版决策。
  3. 母版固定用 pub；实际 deck 换成自己品牌的 images/motherboard/<brand>/ 路径。
-->

<!-- 全局内容页背景（封面用 ![bg] 覆盖本页） -->
<!-- backgroundImage: url("../assets/images/motherboard/pub/slide-content.png") -->

## 幻灯片的排版语汇

### 一份用来照抄的样张

wk-marp-slide
2026.11.24

<!-- _class: face -->
<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](../assets/images/motherboard/pub/slide-face.png)

## 目录

- [一、页面怎么排](#一页面怎么排)
- [二、内容怎么写](#二内容怎么写)
- [三、收尾](#三收尾)

![bg left:30%](../assets/images/motherboard/pub/slide-face.png)

# 一、页面怎么排

<!-- _class: chapter -->

## 页面解剖：三层，各司其职

<!-- 版式：双栏 ｜ 演示：左右两块对等的结构说明 -->

<div class="container"><div class="col">

### 固定层：整份 deck 不变

- **页眉** `header:` —— 写 deck 主题，小号灰字
- **页脚** `footer:` —— 写副标题或落款，落左下角
- **页码** `paginate: true` —— 主题生成的 `section::after`，落右下角

</div><div class="col">

### 变动层：每页自己决定

- **`##` 页标题** —— 一页只有一个，左对齐，字号最大
- **`###` 栏标题** —— 只在 `.col` 里用，主题自动居中
- **正文** —— 22px 基准，行距由主题给定

</div></div>

## 一页承载两组信息

<!-- 版式：三栏 + 同页分隔线 ｜ 演示：上下两组信息用一条满宽细线分开 -->

<div class="container smallfont"><div class="col">

### 版式 A · 双栏

- 两个对等维度并排
- 骨架 `.container` + `.col` × 2

</div><div class="col">

### 版式 B · 三栏

- 三个对等维度并排
- 骨架 `.container` + `.col` × 3

</div><div class="col">

### 版式 C · 非对称

- 主次不均时用 `.col2` + `.col`
- `.col2` 占两倍宽，主栏放主线

</div></div>

<hr>

<div class="container smallfont"><div class="col">

- 同一页放**两组**信息时，用 `<hr>` 拉一条满宽细线
- 细线两端对齐版心，把上下两段视觉上分成两块

</div><div class="col">

- `<hr>` 是裸 HTML，**不分页**
- 顶格 `---` 与 `***` 都会分页，别拿来当分隔线

</div><div class="col">

- 分隔线是**结构**不是装饰
- 一页最多一条，再多就该拆页

</div></div>

## 图文混排：四栏图卡

<!-- 版式：四栏图卡 ｜ 演示：等宽等高的图 + 短注，视觉自动对齐 -->

<div class="container"><div class="col">

![h:250px](img/sample-1.png)

- **单栏图卡**
- 图定尺 + 两行短注

</div><div class="col">

![h:250px](img/sample-2.png)

- **并排比较**
- 高度一致，视觉才对齐

</div><div class="col">

![h:250px](img/sample-3.png)

- **留白节奏**
- 图占六成，注占四成

</div><div class="col">

![h:250px](img/sample-4.png)

- **短注优先**
- 一句话说清，不用整段

</div></div>

## 图文混排：大图压一侧

<!-- 版式：图文分屏 ｜ 演示：左图右文，图只负责"长什么样" -->

![bg fit left:30%](img/sample-wide.png)

- **图负责"长什么样"**，正文负责"为什么这样用"
- 分屏时正文控制在 **8 条以内**，超了就得换页
- 正文与图之间留出版心宽的空白，不要贴边
- 一条硬信息 + 一条判断，就够撑起一屏
- 分屏页不要放表格 —— 表格需要整块宽度

## 版式清单：一页一表，表下列点

<!-- 版式：宽表 + 脚注 ｜ 演示：表只放对照关系，结论落在表下 -->

<div class="centerblock">

| 版式 | 何时用 | 骨架 |
| --- | --- | --- |
| 双栏 | 两个对等维度 | `.container` + `.col` × 2 |
| 三栏 | 三个对等维度 | `.container` + `.col` × 3 |
| 非对称 | 主次不均 | `.col2` + `.col` |
| 四栏图卡 | 四张图并列 | `![h:250px]` × 4 |
| 分屏 | 一张大图 + 短文 | `![bg fit left:30%]` |
| 宽表 | 字段对照 | `.centerblock` + `table` |

</div>

- **表只放对照关系**，判断和结论写在表下面
- 表头加粗居中，长表格用 `.centerblock` 居中
- 一页最多一张表 —— 两张表就该拆成两页

<div class="rightBottomInPage smallestfont">
版式清单：wk-marp-slide / references/layout-guide.md
</div>

# 二、内容怎么写

<!-- _class: chapter -->

## 从名词短语到完整短句

<!-- 版式：双栏对照 ｜ 演示：左栏不合格、右栏合格，一一对应 -->

<div class="container"><div class="col">

### 不合格：只有名词

- 标准、规范
- 支持多种格式
- 性能优化
- 与其它工具兼容
- 丰富的扩展点

</div><div class="col">

### 合格：一句完整的话

- **ISO/IEC 30173:2023** 规定了数字孪生的三层参考架构
- 支持 **21** 项 SISO 标准，覆盖制造过程数据交换
- 采样率提升到 **48 kHz**，端到端延迟降到 **120 ms**
- 与 **LangChain / LlamaIndex** 共用同一套 Tool 接口
- 插件点 **17** 个，覆盖鉴权、限流、审计三类

</div></div>

## 密度：一页能装多少

<!-- 版式：三栏 + 同页分隔线 ｜ 演示：量化规则，配一条底线与一条上限 -->

<div class="container smallfont"><div class="col">

### 上限

- 加权密度 = 内容行 + 3 × 图片行
- 超过 **32** 就有溢出风险
- 溢出是**静默**的 —— 内容被裁掉，页面看着还正常

</div><div class="col">

### 区间

- 正文页中位 **17**，典型区间 **8 – 32**
- 低于 **8** 页面发空
- 连续两页低于 **6** 就该并页

</div><div class="col">

### 下限

- 一页只承载**一个论点**
- 第二个论点用 `<hr>` 分段，不是再堆 bullet
- 单栏 **4 – 6** 条 bullet，单条不超过 **60 字**

</div></div>

<hr>

<div class="container smallfont"><div class="col">

- 章节页、封面、尾页不参与密度统计 —— 它们天然只有一行
- 密度不够时的首选动作是**合并**，不是加图

</div><div class="col">

- 合并两页前先看它们是不是同一个论点
- 合并后仍要保住每栏的标题，否则读者失去坐标

</div><div class="col">

- 每 **5 – 8** 页插一个章节页，作为节奏锚点
- 章节页不承载信息，只承载"我们讲到哪了"

</div></div>

# 三、收尾

<!-- _class: chapter -->

## 小结：六条，够用了

<!-- 版式：三栏 ｜ 演示：收尾页把方法压成可执行的清单 -->

<div class="container"><div class="col">

### 结构

- 封面 → 目录 → 章节页 → 内容页 → 小结 → 尾页
- 一页一个 `##` 标题，页标题左对齐

</div><div class="col">

### 版式

- 内容类型决定版式，查清单不凭感觉
- 同页分段用 `<hr>`，分页用 `---`，两者不可混

</div><div class="col">

### 内容

- 每条 bullet 是一个完整短句
- 每页至少一条带数字 / 机构 / 年份的硬信息

</div></div>

---

<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](../assets/images/motherboard/pub/slide-bottom.png)
