#!/usr/bin/env bash
# build.sh - 把一个 Marp deck 编译成 HTML / PDF / PNG。
#
# 母版（brand）是通用的：deck 里 images/motherboard/ 下有哪些目录，就能切到哪个。
# index.md 默认烘焙了其中一个母版；-b 指定其它母版时，构建脚本临时把它换成目标
# 母版的路径（源文件不动）。
#
# 用法:
#   build.sh [选项] [deck_dir]
#
# 选项:
#   -d, --deck DIR     deck 目录（默认: 当前目录）
#   -o, --out DIR      输出目录（默认: <deck>/dist）
#   -f, --format LIST  输出格式，逗号分隔: html,pdf,png（默认: html,pdf）
#   -b, --brand NAME   背景母版（默认: index.md 里烘焙的那个）
#   -m, --motherboard  同 --brand，母版名直接替换 images/motherboard/<name>
#   -c, --compress     额外用 ghostscript 压缩 PDF
#   -s, --sheet        把 PNG 逐页拼成一张长图 (contact sheet)
#   -h, --help         显示本帮助
#
# deck 目录结构（用 new_deck.sh 生成）:
#   index.md  main.css  mermaid.min.js  images/motherboard/<brand>/  img/
#
# 输出:
#   <out>/html/index.html
#   <out>/pdf/index.pdf
#   <out>/png/index.001.png ...
#
# 例:
#   build.sh -d ~/slides/my-talk -f html,pdf,png
#   build.sh -d ~/slides/my-talk -b <brand> -f pdf

set -euo pipefail

DECK=""
OUT=""
FORMATS="html,pdf"
BRAND=""
COMPRESS=false
SHEET=false

usage() {
    awk 'NR>1 && /^[a-zA-Z]/{exit} NR>1{print}' "$0"
}

# 列出 deck 里可用的母版
list_brands() {
    find "$1/images/motherboard" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
}

# 从 index.md 里探测烘焙的母版（第一个出现 images/motherboard/<name>/ 的名字）
detect_brand() {
    local md="$1"
    grep -oE 'images/motherboard/[^/]+/' "$md" 2>/dev/null \
        | head -n1 | cut -d/ -f3
}

while [ $# -gt 0 ]; do
    case "$1" in
        -d|--deck)       DECK="$2"; shift 2 ;;
        -o|--out)        OUT="$2"; shift 2 ;;
        -f|--format)     FORMATS="$2"; shift 2 ;;
        -b|--brand)      BRAND="$2"; shift 2 ;;
        -m|--motherboard) BRAND="$2"; shift 2 ;;
        -c|--compress)   COMPRESS=true; shift ;;
        -s|--sheet)      SHEET=true; shift ;;
        -h|--help)       usage; exit 0 ;;
        -*)              echo "未知选项: $1" >&2; usage >&2; exit 1 ;;
        *)               DECK="$1"; shift ;;
    esac
done

[ -z "$DECK" ] && DECK="$PWD"
[ -d "$DECK" ] || { echo "错误: deck 目录不存在: $DECK" >&2; exit 1; }
DECK="$(cd "$DECK" && pwd)"
[ -z "$OUT" ] && OUT="$DECK/dist"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"

command -v marp >/dev/null 2>&1 || {
    echo "错误: 找不到 marp 命令。安装: npm install -g @marp-team/marp-cli" >&2
    exit 1
}

# 找到 deck 的主 markdown
MD=""
for cand in "$DECK/index.md" "$DECK/README.md"; do
    [ -f "$cand" ] && { MD="$cand"; break; }
done
[ -n "$MD" ] || { echo "错误: $DECK 下找不到 index.md" >&2; exit 1; }
MD_NAME="$(basename "$MD" .md)"

THEME="$DECK/main.css"
[ -f "$THEME" ] || { echo "错误: 找不到主题 $THEME（用 new_deck.sh 生成 deck）" >&2; exit 1; }

# --- 母版（brand）解析 ----------------------------------------------------------
# 可用母版 = deck 里 images/motherboard/ 下的目录
AVAILABLE="$(list_brands "$DECK")"
if [ -z "$AVAILABLE" ]; then
    echo "错误: $DECK/images/motherboard/ 下没有任何母版目录" >&2
    exit 1
fi

# 默认母版 = index.md 里烘焙的那个；探测不到则取第一个
if [ -z "$BRAND" ]; then
    BRAND="$(detect_brand "$MD")"
    [ -n "$BRAND" ] || BRAND="$(echo "$AVAILABLE" | head -n1)"
fi

# 校验目标母版存在
if ! echo "$AVAILABLE" | grep -qx "$BRAND"; then
    echo "错误: 未知母版 '$BRAND'。可用: $(echo "$AVAILABLE" | tr '\n' ' ')" >&2
    exit 1
fi

# --- 母版切换：把 md 里烘焙的母版路径换成目标母版 --------------------------------
# 源文件里写死 images/motherboard/<baked>/...；当目标母版 ≠ 烘焙母版时用 sed 换掉，
# 写到临时文件，源文件不动。
# 临时文件放在 deck 目录内（这样相对路径 images/... 仍然解析得到），
# 但不能以 "." 开头 —— marp 会把点开头的文件名当隐藏文件，产物也带点，
# 后面 glob 就匹配不到。
BAKED="$(detect_brand "$MD")"
TMP_MD=""
cleanup() { [ -n "$TMP_MD" ] && rm -f "$TMP_MD" || true; }
trap cleanup EXIT

if [ -n "$BAKED" ] && [ "$BRAND" != "$BAKED" ]; then
    TMP_MD="$DECK/build-$BRAND.md"
    sed "s#images/motherboard/$BAKED/#images/motherboard/$BRAND/#g" "$MD" > "$TMP_MD"
    MD="$TMP_MD"
    # 产物名仍用原 deck 名（index），不要带 build-<brand> 前缀
    MD_NAME="index"
fi

mkdir -p "$OUT"

# --- HTML ---------------------------------------------------------------------
if [[ ",$FORMATS," == *",html,"* ]]; then
    echo "==> HTML"
    mkdir -p "$OUT/html"
    # html 输出里的相对路径按输出文件位置解析，所以把资源软链过去
    for res in images img mermaid.min.js; do
        [ -e "$DECK/$res" ] && ln -sfn "$DECK/$res" "$OUT/html/$res"
    done
    marp --allow-local-files --html --theme "$THEME" \
        -o "$OUT/html/$MD_NAME.html" "$MD"
fi

# --- PDF ----------------------------------------------------------------------
if [[ ",$FORMATS," == *",pdf,"* ]]; then
    echo "==> PDF"
    mkdir -p "$OUT/pdf"
    # --html 必须开：mermaid / 分栏 / heti 都靠原始 HTML，缺了会被转义成文本
    marp --allow-local-files --html --theme "$THEME" --pdf \
        -o "$OUT/pdf/$MD_NAME.pdf" "$MD"
    if $COMPRESS; then
        command -v gs >/dev/null 2>&1 && {
            gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
               -dNOPAUSE -dBATCH -dQUIET \
               -sOutputFile="$OUT/pdf/$MD_NAME.compressed.pdf" "$OUT/pdf/$MD_NAME.pdf"
            mv "$OUT/pdf/$MD_NAME.compressed.pdf" "$OUT/pdf/$MD_NAME.pdf"
            echo "    (已用 ghostscript 压缩)"
        }
    fi
fi

# --- PNG ----------------------------------------------------------------------
if [[ ",$FORMATS," == *",png,"* ]]; then
    echo "==> PNG"
    mkdir -p "$OUT/png"
    # 单文件模式下 marp 输出 index.001 / index.002（不带 .png 后缀），
    # 这里统一改名成 index.001.png ...
    marp --allow-local-files --html --theme "$THEME" --images png \
        -o "$OUT/png/$MD_NAME" "$MD"
    for f in "$OUT/png/$MD_NAME".[0-9]*; do
        [ -e "$f" ] && mv "$f" "$f.png"
    done
    if $SHEET; then
        # 逐页竖向拼成一张长图，便于一眼看完整个 deck
        if command -v convert >/dev/null 2>&1; then
            ( cd "$OUT/png" && convert -bordercolor black -border 0x5 \
                -append ./"$MD_NAME".*.png "$OUT/sheet-$BRAND.png" )
            echo "    (contact sheet: $OUT/sheet-$BRAND.png)"
        else
            echo "    (跳过 contact sheet: 找不到 ImageMagick convert)" >&2
        fi
    fi
fi

echo "完成 (母版: $BRAND) → $OUT"
