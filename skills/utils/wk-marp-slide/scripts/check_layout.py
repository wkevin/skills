#!/usr/bin/env python3
"""
check_layout.py - wk-marp-slide 静态排版检查器

检查一个 deck 的 index.md，把排版层面的毛病挑出来：空页、div 里写标题、
文字墙、图没定尺、占位符没换、mermaid 运行时缺失……

用法:
  python3 check_layout.py <deck_dir>            # 自动找 index.md / README.md
  python3 check_layout.py <deck_dir> --strict   # 有 ERROR 时 exit 1
  python3 check_layout.py <deck_dir> --json     # 机器可读输出
  python3 check_layout.py <deck_dir> --no-info  # 不打印 INFO 级统计

规则:
  E1  空页            分出来的某页没有任何内容（只有 `---` 切出来的）
  E2  div 内标题      <div> 内部出现 # / ## —— 会分页并把块劈成两半
  E3  div 不配对      <div 与 </div 数量不等
  E4  mermaid 运行时  有 .mermaid 块但文件里没有 mermaid.initialize(
  E5  mermaid.min.js  script src 指到的文件在 md 同目录找不到
  E6  占位符未替换    改了 Slide 标题 / 姓名.工号 / 202x.yy.zz / __BRAND__ 等
  W1  文字墙          单栏 bullet > 6 条，或整页正文 > 900 字
  W2  超长条目        单条 bullet > 60 字
  W3  图未定尺        栏内的图没有 h: / w: 尺寸
  W4  一级标题非章节页 # 标题没有配 <!-- _class: chapter -->
  W5  缺目录页        有 >=2 个一级标题但没有目录页
  W6  页面过空        正文页加权密度 < 6，且连续两页都低
  W7  分栏数异常      .container 的直接子列数不在 {1,2,3,4}
  W8  误用分隔线      顶格 *** / ___ —— Marpit 也当分页符
  W9  骨架占位符残留  文本里还有 【...】
  I1  密度统计        总页数 / 加权密度中位均值 / 最空页
  I2  front matter    缺 paginate / header / footer

页号是**估算**（静态解析，与 marp 实际分页可能有 ±1 的偏差）。
"""

import argparse
import json
import os
import re
import statistics
import sys

# ---------------------------------------------------------------- 常量

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
LEVEL_ORDER = {ERROR: 0, WARN: 1, INFO: 2}

# 骨架占位符（new_deck.sh 负责替换的 5 个）
SCAFFOLD_PLACEHOLDERS = [
    "改为 Slide 标题",
    "改为 Slide 副标题",
    "姓名.工号",
    "202x.yy.zz",
    "__BRAND__",
]

# 加权密度：一行图约等于三行正文
IMG_WEIGHT = 3
DENSITY_LOW = 6  # 低于这个值算"发空"
DENSITY_IDEAL_LOW = 8  # 手册给出的目标下限

RE_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
RE_BREAK = re.compile(r"^-{3,}\s*$|^\*{3,}\s*$|^_{3,}\s*$")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
RE_SPLIT_HEADING = re.compile(r"^#{1,2}\s")
RE_BULLET = re.compile(r"^(\s*)[-*+]\s+(.*)$")
RE_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")
RE_DIV_TOKEN = re.compile(r"<div\b([^>]*)>|</div\s*>", re.I)
RE_CLASS = re.compile(r"""class\s*=\s*["']([^"']*)["']""", re.I)
RE_SCRIPT_SRC = re.compile(r"""<script[^>]*\bsrc\s*=\s*["']([^"']+)["']""", re.I)
RE_LOCAL_CLASS = re.compile(r"_class\s*:\s*([^\s>]+)")

COLUMN_CLASSES = ("col", "col2", "colv")
IMAGE_SIZE = re.compile(r"^\s*(h|w)\s*:")


# ---------------------------------------------------------------- 数据结构


class Finding:
    def __init__(self, line, level, rule, message, fix=None):
        self.line = line
        self.level = level
        self.rule = rule
        self.message = message
        self.fix = fix

    def as_dict(self, path):
        return {
            "file": path,
            "line": self.line,
            "level": self.level,
            "rule": self.rule,
            "message": self.message,
            "fix": self.fix,
        }


class Div:
    def __init__(self, classes, line):
        self.classes = classes
        self.line = line

    @property
    def is_container(self):
        return "container" in self.classes

    @property
    def is_column(self):
        return any(c in COLUMN_CLASSES for c in self.classes)


class Page:
    def __init__(self, start_line):
        self.start_line = start_line
        self.lines = []  # [(lineno, raw_text, is_comment)]
        self.heading = None  # (level, text)
        self.classes = set()

    def add(self, lineno, text, is_comment=False):
        self.lines.append((lineno, text, is_comment))

    def content_lines(self):
        """去掉空行、HTML 注释、HTML 指令后的实质内容行。"""
        out = []
        for lineno, text, is_comment in self.lines:
            s = text.strip()
            if not s or is_comment or s.startswith("<!--"):
                continue
            out.append((lineno, s))
        return out

    def comment_lines(self):
        return [ln for ln, _, is_comment in self.lines if is_comment]

    def has_class(self, name):
        return name in self.classes


# ---------------------------------------------------------------- 解析


def split_front_matter(text):
    """拆掉 front matter，返回 (front_matter_text, body_text, body_offset_line)。"""
    if not text.startswith("---"):
        return "", text, 0
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :]), i + 1
    return "", text, 0


def parse_pages(body, offset=0):
    """把 markdown 正文切成页。Marpit 的分页点：顶格 thematic break、顶格 #/## 标题。"""
    pages = []
    page = Page(offset + 1)
    stack = []  # 打开中的 div
    breaks = []  # [(lineno, kind)] kind in {'---', '***', '___'}
    in_fence = False
    fence_marker = ""
    in_comment = False

    for idx, raw in enumerate(body.split("\n")):
        lineno = offset + idx + 1
        line = raw.rstrip()

        # _class: 指令要在任何分支之前抓（它是 HTML 注释）
        cm = RE_LOCAL_CLASS.search(line)
        if cm:
            page.classes.add(cm.group(1).strip("'\""))

        # --- HTML 注释块（可跨行；Marpit 不在注释里分页） ---
        if in_comment:
            page.add(lineno, line, is_comment=True)
            if "-->" in line:
                in_comment = False
            continue
        if line.strip().startswith("<!--"):
            page.add(lineno, line, is_comment=True)
            if "-->" not in line.strip()[4:]:
                in_comment = True
            continue

        # --- 代码围栏 ---
        if in_fence:
            page.add(lineno, line)
            m = RE_FENCE.match(line)
            if m and line.strip().startswith(fence_marker):
                in_fence = False
            continue
        m = RE_FENCE.match(line)
        if m:
            in_fence = True
            fence_marker = m.group(1)[0] * 3
            page.add(lineno, line)
            continue

        # --- 分页判定：只在 div 深度为 0 时成立 ---
        if not stack:
            if RE_BREAK.match(line):
                s = line.strip()
                kind = "---" if s.startswith("-") else ("***" if s.startswith("*") else "___")
                breaks.append((lineno, kind))
                pages.append(page)
                page = Page(lineno + 1)
                continue
            hm = RE_HEADING.match(line)
            if hm and len(hm.group(1)) <= 2:
                pages.append(page)
                page = Page(lineno)
                page.heading = (len(hm.group(1)), hm.group(2).strip())
                page.add(lineno, line)
                continue

        page.add(lineno, line)

        for m2 in RE_DIV_TOKEN.finditer(line):
            if m2.group(0).startswith("</"):
                if stack:
                    stack.pop()
            else:
                attr = m2.group(1) or ""
                cls = RE_CLASS.search(attr)
                classes = cls.group(1).split() if cls else []
                stack.append(Div(classes, lineno))

    pages.append(page)
    return pages, stack, breaks


def column_spans(page):
    """把一页的 bullet / 图片按所属栏目归组，并统计每个 .container 的直接子列数。

    返回 (columns, page_bullets, containers)：
      columns    = [{bullets: [(lineno, text)], images: [(lineno, alt, url)], line}]
      containers = [{cols: n, line}]
    """
    stack = []  # ('container', idx) / ('col', idx) / ('other',)
    columns = []
    containers = []
    page_bullets = []

    for lineno, raw, is_comment in page.lines:
        s = raw.strip()
        if not s or is_comment or s.startswith("<!--"):
            continue

        for m in RE_DIV_TOKEN.finditer(raw):
            if m.group(0).startswith("</"):
                if stack:
                    stack.pop()
                continue
            attr = m.group(1) or ""
            cls = RE_CLASS.search(attr)
            classes = cls.group(1).split() if cls else []
            if "container" in classes:
                containers.append({"cols": 0, "line": lineno})
                stack.append(("container", len(containers) - 1))
            elif any(c in COLUMN_CLASSES for c in classes):
                idx = len(columns)
                columns.append({"bullets": [], "images": [], "line": lineno})
                stack.append(("col", idx))
                ci = next(
                    (
                        stack[i][1]
                        for i in range(len(stack) - 1, -1, -1)
                        if stack[i][0] == "container"
                    ),
                    None,
                )
                if ci is not None:
                    containers[ci]["cols"] += 1
            else:
                stack.append(("other", -1))

        bm = RE_BULLET.match(raw)
        if bm:
            ci = next((f for f in reversed(stack) if f[0] == "col"), None)
            if ci is not None:
                columns[ci[1]]["bullets"].append((lineno, bm.group(2)))
            else:
                page_bullets.append((lineno, bm.group(2)))

        for alt, url in RE_IMAGE.findall(raw):
            ci = next((f for f in reversed(stack) if f[0] == "col"), None)
            if ci is not None:
                columns[ci[1]]["images"].append((lineno, alt, url))

    return columns, page_bullets, containers


def weighted_density(page):
    """加权密度 = 内容行数 + 3 * 图片行数。"""
    n = 0
    for _, s in page.content_lines():
        n += 1 + IMG_WEIGHT * len(RE_IMAGE.findall(s))
    return n


def plain_len(text):
    """去掉 markdown 标记后的长度。"""
    t = re.sub(r"\*\*|__|`|\*", "", text)
    t = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "图", t)
    return len(t.strip())


# ---------------------------------------------------------------- 规则


def check(md_path, md_text):
    findings = []
    fm, body, offset = split_front_matter(md_text)
    pages, leftover_stack, breaks = parse_pages(body, offset)

    # Marpit 不渲染"没有可见内容"的首屏（实测：文件开头的注释块 / 空行都不会多出一页），
    # 这里同样不算一页。
    if pages and not pages[0].content_lines():
        pages = pages[1:]

    def add(line, level, rule, message, fix=None):
        findings.append(Finding(line, level, rule, message, fix))

    # ---- E3 div 不配对 ----
    opens = len([m for m in RE_DIV_TOKEN.finditer(body) if not m.group(0).startswith("</")])
    closes = len([m for m in RE_DIV_TOKEN.finditer(body) if m.group(0).startswith("</")])
    if opens != closes:
        where = f"，最后一行未闭合的 <div> 在第 {leftover_stack[-1].line} 行" if leftover_stack else ""
        add(
            leftover_stack[-1].line if leftover_stack else 1,
            ERROR,
            "E3",
            f"div 不配对：<div> {opens} 个，</div> {closes} 个{where}",
            "补齐闭合标签",
        )

    # ---- E2 div 内标题 ----
    stack = []
    in_fence = False
    fence_marker = ""
    in_comment = False
    for idx, raw in enumerate(body.split("\n")):
        lineno = offset + idx + 1
        line = raw.rstrip()
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if line.strip().startswith("<!--"):
            if "-->" not in line.strip()[4:]:
                in_comment = True
            continue
        if in_fence:
            m = RE_FENCE.match(line)
            if m and line.strip().startswith(fence_marker):
                in_fence = False
            continue
        m = RE_FENCE.match(line)
        if m:
            in_fence = True
            fence_marker = m.group(1)[0] * 3
            continue
        if stack and RE_SPLIT_HEADING.match(line):
            add(
                lineno,
                ERROR,
                "E2",
                f"<div> 内部出现 {line.split()[0]} 标题 —— Marpit 会在这里分页，把块劈成两半",
                "换成 <h1>/<h2> 显式 HTML 标签，或把标题移到 div 外面",
            )
        for m2 in RE_DIV_TOKEN.finditer(line):
            if m2.group(0).startswith("</"):
                if stack:
                    stack.pop()
            else:
                stack.append(1)

    # ---- E6 占位符未替换（扫全文，含 front matter）----
    for lineno, raw in enumerate(md_text.split("\n"), start=1):
        for ph in SCAFFOLD_PLACEHOLDERS:
            if ph in raw:
                add(
                    lineno,
                    ERROR,
                    "E6",
                    f"占位符未替换：{ph}",
                    "用真实标题 / 作者 / 日期 / 品牌路径替换",
                )

    # ---- W8 误用分隔线 ----
    for lineno, kind in breaks:
        if kind in ("***", "___"):
            add(
                lineno,
                WARN,
                "W8",
                f"顶格 {kind} 会被 Marpit 当成分页符",
                "同页分段请用 <hr>；确实要分页请用 ---",
            )

    # ---- W9 骨架占位符残留（按页聚合，避免刷屏）----
    for idx, page in enumerate(pages, start=1):
        hits = [
            (lineno, s)
            for lineno, s in page.content_lines()
            if "【" in s
        ]
        if hits:
            add(
                hits[0][0],
                WARN,
                "W9",
                f"第 {idx} 页还有 {len(hits)} 处骨架占位符 【…】 没换掉",
                "把 【…】 替换成真实内容",
            )

    # ---- E4 / E5 mermaid 运行时 ----
    has_mermaid = "mermaid" in body and "class=" in body and "mermaid" in body
    if has_mermaid and "mermaid.initialize(" not in md_text:
        add(
            1,
            ERROR,
            "E4",
            "有 mermaid 图，但文件里没有 mermaid.initialize( —— 图不会渲染成 SVG，只会显示源码",
            '在文件末尾补 <!-- mermaid.js --> 与 <script src="./mermaid.min.js"></script>',
        )
    for m in RE_SCRIPT_SRC.finditer(md_text):
        src = m.group(1)
        if src.startswith(("http://", "https://", "//", "data:")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(md_path), src))
        if not os.path.exists(target):
            lineno = md_text[: m.start()].count("\n") + 1
            add(
                lineno,
                ERROR,
                "E5",
                f"script 引用的 {src} 在 md 同目录找不到",
                "把 mermaid.min.js 放在 md 同目录，路径写成 ./mermaid.min.js",
            )

    # ---- 逐页规则 ----
    body_pages = []
    h1_count = 0
    has_toc = False

    for idx, page in enumerate(pages, start=1):
        content = page.content_lines()
        is_chapter = page.has_class("chapter")
        is_face = page.has_class("face")

        if page.heading and page.heading[0] == 1:
            h1_count += 1
            if not is_chapter:
                add(
                    page.start_line,
                    WARN,
                    "W4",
                    f"一级标题「{page.heading[1]}」没有配 <!-- _class: chapter -->",
                    "补 <!-- _class: chapter --> 让它变成蓝底章节页",
                )
        if page.heading and page.heading[0] == 2:
            if any(k in page.heading[1] for k in ("目录", "目次", "TOC", "Contents")):
                has_toc = True

        # E1 空页
        if not content:
            add(
                page.start_line,
                ERROR,
                "E1",
                f"第 {idx} 页是空页（只有 `---` 切出来的）",
                "删掉多余的 `---`，或给这一页补内容",
            )
            continue

        # W8 在 breaks 那里统一报了

        columns, page_bullets, containers = column_spans(page)

        # W1 文字墙
        for c in columns:
            if len(c["bullets"]) > 6:
                add(
                    c["line"],
                    WARN,
                    "W1",
                    f"第 {idx} 页有一栏 {len(c['bullets'])} 条 bullet（建议 ≤ 6）",
                    "拆成两栏，或用 <hr> 分段",
                )
        if len(page_bullets) > 6:
            add(
                page.start_line,
                WARN,
                "W1",
                f"第 {idx} 页有 {len(page_bullets)} 条 bullet（建议 ≤ 6）",
                "分栏，或用 <hr> 分段",
            )

        body_chars = sum(plain_len(s) for _, s in content)
        if body_chars > 900:
            add(
                page.start_line,
                WARN,
                "W1",
                f"第 {idx} 页正文约 {body_chars} 字（建议 ≤ 900）",
                "拆页，或分栏 + smallfont",
            )

        # W2 超长条目
        all_bullets = list(page_bullets)
        for c in columns:
            all_bullets.extend(c["bullets"])
        for lineno, text in all_bullets:
            n = plain_len(text)
            if n > 60:
                add(lineno, WARN, "W2", f"一条 bullet {n} 字（建议 ≤ 60）", "拆成两条，或压成短句")

        # W3 图未定尺
        for c in columns:
            for lineno, alt, url in c["images"]:
                if not IMAGE_SIZE.match(alt):
                    add(
                        lineno,
                        WARN,
                        "W3",
                        f"栏内的图没有定尺：![{alt}]({url})",
                        "写成 ![h:250px](...) 或 ![w:300px](...)",
                    )

        # W7 分栏数异常
        for cont in containers:
            if cont["cols"] not in (1, 2, 3, 4):
                add(
                    cont["line"],
                    WARN,
                    "W7",
                    f"第 {idx} 页有个 .container 里有 {cont['cols']} 个直接子列（建议 1-4）",
                    "补齐或删掉多余的列",
                )

        # 密度
        density = weighted_density(page)
        is_cover_or_tail = is_face or is_chapter or (
            len(content) <= 2 and any(RE_IMAGE.search(s) for _, s in content)
        )
        if not is_cover_or_tail:
            body_pages.append((idx, density, page))

    # W5 缺目录页
    if h1_count >= 2 and not has_toc:
        add(
            1,
            WARN,
            "W5",
            f"有 {h1_count} 个一级标题，但没有目录页",
            "加一页 `## 目录`，条目写成 - [章节名](#章节名)",
        )

    # W6 页面过空（连续两页）
    low = [i for i, (idx, d, _) in enumerate(body_pages) if d < DENSITY_LOW]
    for k in range(len(low) - 1):
        if low[k + 1] == low[k] + 1:
            idx, density, _ = body_pages[low[k]]
            add(
                pages[idx - 1].start_line,
                WARN,
                "W6",
                f"第 {idx} 页加权密度 {density}（< {DENSITY_LOW}），连续两页都发空",
                "与相邻页合并（合并前先确认是不是同一个论点）",
            )

    # I1 密度统计
    densities = [d for _, d, _ in body_pages]
    if densities:
        median = statistics.median(densities)
        mean = sum(densities) / len(densities)
        emptiest = min(body_pages, key=lambda x: x[1])
        findings.append(
            Finding(
                1,
                INFO,
                "I1",
                f"共 {len(pages)} 页（正文页 {len(body_pages)}）；加权密度中位 {median:.0f}、"
                f"均值 {mean:.1f}（手册目标 ≥ {DENSITY_IDEAL_LOW}）；最空的是第 {emptiest[0]} 页，"
                f"密度 {emptiest[1]}",
            )
        )

    # I2 front matter
    missing = []
    if not re.search(r"^paginate\s*:\s*true", fm, re.M):
        missing.append("paginate: true")
    if not re.search(r"^header\s*:", fm, re.M):
        missing.append("header:")
    if not re.search(r"^footer\s*:", fm, re.M):
        missing.append("footer:")
    if missing:
        findings.append(Finding(1, INFO, "I2", "front matter 缺少：" + "、".join(missing)))

    return findings, len(pages)


# ---------------------------------------------------------------- 输出


def render(md_path, findings, show_info=True):
    rel = os.path.basename(md_path)
    shown = [f for f in findings if show_info or f.level != INFO]
    shown.sort(key=lambda f: (LEVEL_ORDER[f.level], f.line))
    for f in shown:
        print(f"{rel}:{f.line}  [{f.level:<5}] {f.rule}  {f.message}")
        if f.fix:
            print(f"{' ' * (len(rel) + 1)}          → {f.fix}")
    errors = sum(1 for f in findings if f.level == ERROR)
    warns = sum(1 for f in findings if f.level == WARN)
    infos = len(findings) - errors - warns
    tail = f"{errors} error, {warns} warn"
    if show_info:
        tail += f", {infos} info"
    print(f"\n{rel}: {tail}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="wk-marp-slide 静态排版检查器")
    ap.add_argument("deck", help="deck 目录（含 index.md），也可直接给 .md 文件")
    ap.add_argument("--strict", action="store_true", help="有 ERROR 时 exit 1")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--no-info", action="store_true", help="不打印 INFO 级统计")
    args = ap.parse_args(argv)

    target = os.path.abspath(args.deck)
    md_path = ""
    if os.path.isfile(target) and target.lower().endswith(".md"):
        md_path = target
    else:
        for cand in ("index.md", "README.md"):
            p = os.path.join(target, cand)
            if os.path.isfile(p):
                md_path = p
                break
    if not md_path:
        print(f"错误: {target} 下找不到 index.md", file=sys.stderr)
        return 2

    with open(md_path, encoding="utf-8") as fh:
        md_text = fh.read()

    findings, n_pages = check(md_path, md_text)

    if args.json:
        print(
            json.dumps(
                {
                    "file": md_path,
                    "pages": n_pages,
                    "findings": [f.as_dict(md_path) for f in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        render(md_path, findings, show_info=not args.no_info)

    if args.strict and any(f.level == ERROR for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
