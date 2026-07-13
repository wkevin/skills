#!/bin/bash
# link-dev.sh - 把本地 plugin 的 skills / commands 链接到 Claude Code 或/和 OpenClaw
#
# 用法:
#   ./link-dev.sh [选项]
#
# 目标选择:
#   -c, --claude    链接到 Claude Code（skills + commands）
#   -o, --openclaw  链接到 OpenClaw（仅 skills，写入 ~/.openclaw/skills/）
#   可同时使用 -c -o 链接到两者；不带任一参数时会交互式询问目标，
#   非交互场景默认 Claude Code。
#
# 作用域（仅对 Claude Code 生效，OpenClaw 始终为全局 ~/.openclaw/）:
#   -g, --global    CC 全局链接到 ~/.claude/
#                    默认 CC 项目级链接到当前目录的 ./.claude/
#
# 其它:
#   -d, --delete    删除由本脚本创建的链接（不影响其它文件）
#   -y, --yes       跳过交互式询问（非 TTY 时自动启用）
#   -h, --help      显示本帮助
#
# 链接完成后请重启对应客户端使 skills 和 commands 生效。
#
# 示例:
#   ./link-dev.sh                       # 交互式选择目标（默认项目级 CC）
#   ./link-dev.sh -c                    # 仅 CC，项目级
#   ./link-dev.sh -o                    # 仅 OC（写入 ~/.openclaw/skills/）
#   ./link-dev.sh -c -o                 # 同时链接两者
#   ./link-dev.sh -c -g                 # CC 全局
#   ./link-dev.sh -d                    # 交互式选择目标（删除）
#   ./link-dev.sh -d -c -o              # 删除两者的链接
#   ./link-dev.sh -d -c -g              # 删除 CC 全局链接

set -e

show_help() {
    # 输出文件顶部、首个非注释行为止的帮助段
    awk 'NR>1 && /^[a-zA-Z_]/{exit} NR>1{print}' "$0"
}

# ===== 相对路径计算 =====
# relpath <from_dir> <to_path>
# 返回从 from_dir 到 to_path 的相对路径；失败则回退到原值
# 注意：必须 --no-symlinks，否则 .claude/skills/<x> 这种"已是软链"的目标
# 会被解析到源，导致相对路径计算错乱
relpath() {
    local from="$1"
    local to="$2"
    local result
    if result=$(realpath --no-symlinks --relative-to="$from" "$to" 2>/dev/null) && [ -n "$result" ]; then
        echo "$result"
        return
    fi
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$to" "$from" 2>/dev/null
        return
    fi
    echo "$to"
}

AGENT_CRAFT_DIR=$(pwd)

# ===== 解析参数 =====
DO_CLAUDE=false
DO_OPENCLAW=false
IS_GLOBAL=false
MODE="link"
SKIP_PROMPT=false

while [ $# -gt 0 ]; do
    case "$1" in
        --claude|-c)
            DO_CLAUDE=true
            ;;
        --openclaw|-o)
            DO_OPENCLAW=true
            ;;
        --global|-g)
            IS_GLOBAL=true
            ;;
        --delete|-d)
            MODE="delete"
            ;;
        --yes|-y)
            SKIP_PROMPT=true
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            echo "使用 --help 查看帮助。"
            exit 1
            ;;
    esac
    shift
done

# ===== 交互式选择目标 =====
if ! $DO_CLAUDE && ! $DO_OPENCLAW; then
    if $SKIP_PROMPT || ! [ -t 0 ]; then
        # 非交互场景：默认 CC
        DO_CLAUDE=true
    else
        if [ "$MODE" = "delete" ]; then
            echo "请选择要删除链接的目标:"
        else
            echo "请选择链接目标:"
        fi
        echo "  1) Claude Code (CC)"
        echo "  2) OpenClaw (OC)"
        echo "  3) 两者都选"
        printf "选择 [1-3]（默认 1）: "
        read -r choice
        case "$choice" in
            ""|1|c|C) DO_CLAUDE=true ;;
            2|o|O) DO_OPENCLAW=true ;;
            3|b|B) DO_CLAUDE=true; DO_OPENCLAW=true ;;
            *)
                echo "无效选择 '$choice'，使用默认值 Claude Code。"
                DO_CLAUDE=true
                ;;
        esac
    fi
fi

if ! $DO_CLAUDE && ! $DO_OPENCLAW; then
    echo "错误：至少选择一个目标（-c / -o / -b）。"
    exit 1
fi

# ===== 计算目标路径 =====
if $DO_CLAUDE; then
    if $IS_GLOBAL; then
        CC_TARGET_DIR="$HOME/.claude"
        CC_TARGET_DESC="全局 ($HOME/.claude)"
    else
        CC_TARGET_DIR="$AGENT_CRAFT_DIR/.claude"
        CC_TARGET_DESC="项目级 (.claude)"
    fi
fi

if $DO_OPENCLAW; then
    OC_TARGET_DIR="$HOME/.openclaw/skills"
    OC_TARGET_DESC="全局 ($OC_TARGET_DIR)"
    if $IS_GLOBAL; then
        :  # OC 始终是全局，忽略 -g
    fi
fi

# ===== 技能发现 =====
# 本仓库不使用 plugins/ 布局，技能直接位于 skills/<分类>/<技能>/SKILL.md。
# 动态发现所有包含 SKILL.md 的目录（去重、排序）。
SKILL_DIRS=()
if [ -d "$AGENT_CRAFT_DIR/skills" ]; then
    while IFS= read -r skill_md; do
        SKILL_DIRS+=("$(dirname "$skill_md")")
    done < <(find "$AGENT_CRAFT_DIR/skills" -name SKILL.md | sort)
fi

# ===== 是否使用相对路径（仅在 CC 项目级链接时启用）=====
IS_LOCAL=false
if $DO_CLAUDE && ! $IS_GLOBAL; then
    IS_LOCAL=true
fi

# ===== 准备目录 =====
if [ "$MODE" != "delete" ]; then
    $DO_CLAUDE && mkdir -p "$CC_TARGET_DIR/skills"
    $DO_OPENCLAW && mkdir -p "$OC_TARGET_DIR"
fi

# ===== 通用链接/删除函数 =====
# 把所有已发现的 skills 链接到 <target_skills_dir>
# use_relative=true 时，symlink 源使用相对路径（基于目标所在目录），
# 打印信息也使用相对路径（基于 CWD）
link_skills_to() {
    local target_skills_dir=$1
    local use_relative=$2
    local skill name dest src_disp dest_disp
    for skill in "${SKILL_DIRS[@]}"; do
        [ -d "$skill" ] || continue
        name=$(basename "$skill")
        dest="$target_skills_dir/$name"
        if $use_relative; then
            src_disp=$(relpath "$target_skills_dir" "$skill")
            dest_disp=$(relpath "$PWD" "$dest")
        else
            src_disp="$skill"
            dest_disp="$dest"
        fi
        rm -f "$dest"
        echo "  ln -sf '$src_disp' '$dest_disp'"
        ln -sf "$src_disp" "$dest"
    done
}

# 删除已发现 skills 在 <target_skills_dir> 中的链接
delete_skills_from() {
    local target_skills_dir=$1
    local use_relative=$2
    local skill name target disp
    for skill in "${SKILL_DIRS[@]}"; do
        name=$(basename "$skill")
        target="$target_skills_dir/$name"
        if [ -L "$target" ]; then
            if $use_relative; then
                disp=$(relpath "$PWD" "$target")
            else
                disp="$target"
            fi
            echo "  rm '$disp'"
            rm "$target"
        fi
    done
}

# ===== 执行 =====
if [ ${#SKILL_DIRS[@]} -eq 0 ]; then
    echo "警告：在 $AGENT_CRAFT_DIR/skills 下未发现任何包含 SKILL.md 的技能。"
fi

if [ "$MODE" = "delete" ]; then
    if $DO_CLAUDE; then
        echo "==> 删除 Claude Code 链接（$CC_TARGET_DESC）"
        delete_skills_from "$CC_TARGET_DIR/skills" "$IS_LOCAL"
    fi
    if $DO_OPENCLAW; then
        echo "==> 删除 OpenClaw 链接（$OC_TARGET_DESC）"
        delete_skills_from "$OC_TARGET_DIR" "false"
    fi
    echo "Done. 链接已删除。"
else
    if $DO_CLAUDE; then
        echo "==> 链接 Claude Code 到 $CC_TARGET_DESC"
        link_skills_to "$CC_TARGET_DIR/skills" "$IS_LOCAL"
    fi
    if $DO_OPENCLAW; then
        echo "==> 链接 OpenClaw 到 $OC_TARGET_DESC"
        link_skills_to "$OC_TARGET_DIR" "false"
    fi
    echo "Done. Restart clients to use skills and commands."
fi