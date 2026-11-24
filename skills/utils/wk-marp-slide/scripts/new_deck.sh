#!/usr/bin/env bash
# new_deck.sh - 从 skill 模板创建一个新的 Marp slide deck 目录。
#
# 母版（brand）是通用的：本 skill 的 assets/images/motherboard/ 下有几个目录，
# 就有几个可用母版。新 deck 会把它们全部复制进来，index.md 默认烘焙其中一个
# （-b 指定的，默认按字母序第一个）。
#
# 用法:
#   new_deck.sh <deck_dir> [选项]
#
# 选项:
#   -t, --title TITLE   封面主标题（默认 "改为 Slide 标题"）
#   -s, --subtitle S    封面副标题（默认 "Slide 副标题"）
#   -a, --author A      作者行，显示为 "A.工号"（默认 "姓名.工号"）
#   -d, --date D        日期行（默认 "202x.yy.zz"）
#   -b, --brand NAME    烘焙进 index.md 的默认母版（默认: 按字母序第一个）
#   -h, --help          显示本帮助
#
# 生成的结构:
#   <deck_dir>/
#   ├── index.md            ← deck 源文件（改这个）
#   ├── main.css            ← Marp 主题（版式 + 中文排版）
#   ├── mermaid.min.js      ← Mermaid 运行时（图表用）
#   ├── images/motherboard/ ← 全部可用母版（每个子目录一套背景图）
#   └── img/                ← 放你自己的图片
#
# 例:
#   new_deck.sh ~/slides/my-talk -t "Git Workflow" -a "王俊建.10036143"

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HERE/.." && pwd)"
MB_ROOT="$SKILL_DIR/assets/images/motherboard"

TITLE="改为 Slide 标题"
SUBTITLE="Slide 副标题"
AUTHOR="姓名.工号"
DATE="202x.yy.zz"
BRAND=""

usage() {
    awk 'NR>1 && /^[a-zA-Z]/{exit} NR>1{print}' "$0"
}

# 按字母序列出可用母版
list_brands() {
    find "$MB_ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
}

if [ ! -d "$MB_ROOT" ] || [ -z "$(list_brands)" ]; then
    echo "错误: $MB_ROOT 下没有任何母版目录。请先在 skill 里加一个。" >&2
    exit 1
fi

DECK=""
while [ $# -gt 0 ]; do
    case "$1" in
        -t|--title)    TITLE="$2"; shift 2 ;;
        -s|--subtitle) SUBTITLE="$2"; shift 2 ;;
        -a|--author)   AUTHOR="$2"; shift 2 ;;
        -d|--date)     DATE="$2"; shift 2 ;;
        -b|--brand)    BRAND="$2"; shift 2 ;;
        -h|--help)     usage; exit 0 ;;
        -*)            echo "未知选项: $1"; usage; exit 1 ;;
        *)             DECK="$1"; shift ;;
    esac
done

# 解析默认母版
if [ -z "$BRAND" ]; then
    BRAND="$(list_brands | head -n1)"
fi
if [ ! -d "$MB_ROOT/$BRAND" ]; then
    echo "错误: 未知母版 '$BRAND'。可用: $(list_brands | tr '\n' ' ')" >&2
    exit 1
fi

if [ -z "$DECK" ]; then
    echo "错误: 必须指定 deck 目录。" >&2
    usage >&2
    exit 1
fi

if [ -e "$DECK" ] && [ -n "$(ls -A "$DECK" 2>/dev/null)" ]; then
    echo "错误: $DECK 已存在且非空，拒绝覆盖。" >&2
    exit 1
fi

mkdir -p "$DECK/img"
mkdir -p "$DECK/images/motherboard"
mkdir -p "$DECK/.vscode"

# 模板 → index.md：替换占位符，并把 __BRAND__ 烘焙成默认母版。
sed -e "s|改为 Slide 标题|${TITLE}|g" \
    -e "s|改为 Slide 副标题|${SUBTITLE}|g" \
    -e "s|姓名\.工号|${AUTHOR}|g" \
    -e "s|202x\.yy\.zz|${DATE}|g" \
    -e "s|__BRAND__|${BRAND}|g" \
    "$SKILL_DIR/template/index.md" > "$DECK/index.md"

# 主题与运行时
cp "$SKILL_DIR/assets/main.css" "$DECK/main.css"
cp "$SKILL_DIR/assets/mermaid.min.js" "$DECK/mermaid.min.js"

# 全部母版背景图
while read -r b; do
    mkdir -p "$DECK/images/motherboard/$b"
    cp "$MB_ROOT/$b/"*.png "$DECK/images/motherboard/$b/"
done < <(list_brands)

# VSCode: Marp 预览配置 + 代码片段（分栏 / mermaid / 字体块）
cp "$SKILL_DIR/template/vscode-settings.json" "$DECK/.vscode/settings.json"
cp "$SKILL_DIR/template/vscode.code-snippets" "$DECK/.vscode/marp.code-snippets"

# 构建产物不进 git
cat > "$DECK/.gitignore" <<'EOF'
dist/
build-*.md
EOF

echo "已创建 deck: $DECK (默认母版: $BRAND)"
echo "  可用母版: $(list_brands | tr '\n' ' ')"
echo "  编辑源文件: $DECK/index.md"
echo "  构建命令:   bash $HERE/build.sh -d $DECK"
