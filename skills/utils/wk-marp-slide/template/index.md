---
marp: true
theme: main
headingDivider: 2
paginate: true
header: 改为 Slide 标题
footer: 姓名.工号
math: mathjax
---

<!--
这是新 deck 的**骨架**。每一页只有一种版式，用【】标出待替换的内容。
写之前先读 references/layout-guide.md 和 template/style-sample.md。
【…】 = 待替换的内容，必须全部换掉（check_layout.py 会报 ERROR）
img/… = 放进 deck 的 img/ 目录，路径相对本文件
每页上方的「版式」注释说明这一页在演示什么，替换内容后可以删掉
-->

<!-- 全局内容页背景：封面用 ![bg] 覆盖本页 -->
<!-- backgroundImage: url("images/motherboard/__BRAND__/slide-content.png") -->

## 改为 Slide 标题

### 改为 Slide 副标题

姓名.工号
202x.yy.zz

<!-- _class: face -->
<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](images/motherboard/__BRAND__/slide-face.png)

## 目录

<!-- 版式：目录 ｜ 何时用：整份 deck 的第一页之后 ｜ 注意：条目要与下面的一级标题一一对应，链接要能点 -->
- [【一级目录】](#一级目录)
- [【二级目录】](#二级目录)

![bg left:30%](images/motherboard/__BRAND__/slide-face.png)

# 【一级目录】

<!-- _class: chapter -->

## 【二级目录】

<!-- 版式：双栏正文 ｜ 何时用：两个对等维度 ｜ 密度：每栏 4-6 条短句 -->
<div class="container"><div class="col">

### 【维度 A】

- 【要点一：一句完整的话，加粗关键词】
- 【要点二：带一个具体的数字、版本或机构名】
- 【要点三：先给判断，再给依据】
- 【要点四：术语第一次出现时给一句话定义】

</div><div class="col">

### 【维度 B】

- 【要点一】
- 【要点二】
- 【要点三】
- 【要点四】

</div></div>

## 【二级目录】

<!-- 版式：三栏 + 同页分隔线 ｜ 何时用：一页承载两组信息 ｜ 密度：上下各 3 栏，<hr> 是满宽细线不分页 -->
<div class="container smallfont"><div class="col">

### 【维度 A】

- 【上半部分第一条】
- 【上半部分第二条】

</div><div class="col">

### 【维度 B】

- 【上半部分第一条】
- 【上半部分第二条】

</div><div class="col">

### 【维度 C】

- 【上半部分第一条】
- 【上半部分第二条】

</div></div>

<hr>

<div class="container smallfont"><div class="col">

- 【下半部分第一条】
- 【下半部分第二条】

</div><div class="col">

- 【下半部分第一条】
- 【下半部分第二条】

</div><div class="col">

- 【下半部分第一条】
- 【下半部分第二条】

</div></div>

## 【二级目录】

<!-- 版式：四栏图卡 ｜ 何时用：四张图并排比较 ｜ 密度：每张图同高 h:250px，图下 1 条标题 + 1-2 条短注 -->
<div class="container"><div class="col">

![h:250px](img/figure-1.png)

- 【图 1 的标题】
- 【一句话说明】

</div><div class="col">

![h:250px](img/figure-2.png)

- 【图 2 的标题】
- 【一句话说明】

</div><div class="col">

![h:250px](img/figure-3.png)

- 【图 3 的标题】
- 【一句话说明】

</div><div class="col">

![h:250px](img/figure-4.png)

- 【图 4 的标题】
- 【一句话说明】

</div></div>

## 【二级目录】

<!-- 版式：宽表 + 脚注 ｜ 何时用：字段对照 ｜ 密度：表只放对照关系，结论写在表下面；一页最多一张表 -->
<div class="centerblock">

| 【列一】 | 【列二】 | 【列三】 |
| -------- | -------- | -------- |
| 【值】 | 【值】 | 【值】 |
| 【值】 | 【值】 | 【值】 |

</div>

- 【结论写在表下面，不要塞进表里】
- 【首列加粗，表头居中】

<div class="rightBottomInPage smallestfont">
【出处 / 参考 / 脚注】
</div>

## 【二级目录】

<!-- 版式：Mermaid 图 ｜ 何时用：流程、依赖、状态机 ｜ 注意：文末必须有 mermaid.js 脚本块，否则只显示源码 -->
<div class="mermaid">
%%{init: {'theme':'base'}}%%
graph LR;
    A[【输入】] --> B[【处理】];
    B --> C[【输出】];
</div>

---

<!-- _paginate: skip -->
<!-- _header: '' -->
<!-- _footer: '' -->

![bg](images/motherboard/__BRAND__/slide-bottom.png)

<!-- mermaid.js -->
<script src="./mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true});</script>
